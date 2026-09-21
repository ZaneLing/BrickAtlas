"""Strict JSON parsing and single-attempt native-image transport."""
import json
import urllib.error
import urllib.request


def request_bytes(wire, adapter):
    body = {"model":adapter["model"], "messages":wire["messages"], "temperature":0,
            "max_tokens":adapter["max_tokens"], "stream":False}
    return (json.dumps(body,ensure_ascii=True,separators=(",",":"))+"\n").encode()


def parse_receipt(receipt, options, adapter, graph_max=None):
    def failure(reason, output=None):
        return {"answer":None,"valid_format":False,"failure_reason":reason,"output":output}
    if receipt is None:
        return failure("missing-receipt")
    if "transport_error" in receipt:
        assert receipt["raw_response"] is None and receipt["http_status"] is None
        return failure("timeout" if receipt["transport_error"]=="timeout" else "api-error")
    assert type(receipt["http_status"]) is int and isinstance(receipt["raw_response"],str)
    if not 200<=receipt["http_status"]<300:
        return failure("api-error")
    try:
        raw=json.loads(receipt["raw_response"])
    except (ValueError,TypeError):
        return failure("invalid-provider-response")
    if not isinstance(raw,dict):
        return failure("invalid-provider-response")
    assert raw.get("model")==adapter["response_model"], "Served model differs from roster snapshot"
    choices=raw.get("choices")
    message=choices[0].get("message",{}) if isinstance(choices,list) and choices and isinstance(choices[0],dict) else {}
    if not isinstance(message,dict):
        return failure("invalid-provider-response")
    output=message.get("content")
    if message.get("refusal"):
        return failure("refusal",output)
    if not isinstance(output,str):
        return failure("missing-output")
    def pairs(items):
        if len({k for k,_ in items})!=len(items):
            raise ValueError("Duplicate key")
        return dict(items)
    try:
        answer=json.loads(output,object_pairs_hook=pairs,
                          parse_constant=lambda _:(_ for _ in ()).throw(ValueError("nonfinite")))
    except (ValueError,TypeError):
        return failure("invalid-json",output)
    valid=(isinstance(answer,dict) and set(answer)=={"choiceId"} and
           isinstance(answer["choiceId"],str) and answer["choiceId"] in options) if graph_max is None else (
           isinstance(answer,dict) and set(answer)=={"value"} and
           type(answer["value"]) is int and 0<=answer["value"]<=graph_max)
    return {"answer":answer if valid else None,"valid_format":valid,
            "failure_reason":None if valid else "invalid-format","output":output}


def call(adapter, body, api_key):
    request=urllib.request.Request(adapter["endpoint"],data=body,
        headers={"Authorization":"Bearer "+api_key,"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(request,timeout=adapter["timeout_seconds"]) as response:
            return {"http_status":response.status,"raw_response":response.read().decode("utf-8",errors="replace")}
    except urllib.error.HTTPError as error:
        return {"http_status":error.code,"raw_response":error.read().decode("utf-8",errors="replace")}
    except (urllib.error.URLError,TimeoutError,OSError) as error:
        return {"http_status":None,"raw_response":None,
                "transport_error":"timeout" if "timed out" in str(error).lower() else "connection-error"}
