"""Exercise the real HTTP submission path without touching reviewer data."""
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json

from review_server import REVIEWERS, ReviewServer


def get(url):
    try:
        with urlopen(url,timeout=5) as response:
            return response.status,response.read()
    except HTTPError as error:
        return error.code,error.read()


def post(url,value):
    request=Request(url,data=json.dumps(value).encode(),method='POST',
                    headers={'Content-Type':'application/json'})
    try:
        with urlopen(request,timeout=5) as response:
            return response.status,json.loads(response.read())
    except HTTPError as error:
        return error.code,json.loads(error.read())


def main():
    with TemporaryDirectory() as directory:
        root=Path(directory)
        for reviewer in REVIEWERS:
            (root/f'{reviewer}.html').write_text('<html>blind review page</html>')
        codes=[f'T{i:03}' for i in range(1,13)]
        key=root/'answer-key.private.json'
        key.write_text(json.dumps({'rows':[{'code':code} for code in codes]}))
        server=ReviewServer(('127.0.0.1',0),root=root,answer_key=key,secret_path=root/'tokens.json')
        thread=Thread(target=server.serve_forever,daemon=True);thread.start()
        base=f'http://127.0.0.1:{server.server_port}'
        try:
            token=server.tokens['reviewer-A']
            assert get(base+'/health')[0]==200
            assert get(base+'/r/'+token)[0]==200
            assert get(base+'/answer-key.private.json')[0]==404
            assert get(base+'/r/invalid')[0]==404
            answers=[dict(code=code,changed='no') for code in codes]
            payload=dict(reviewer='reviewer-A',answers=answers)
            assert post(base+'/api/submit/invalid',payload)[0]==403
            assert post(base+'/api/submit/'+token,dict(reviewer='reviewer-B',answers=answers))[0]==400
            assert post(base+'/api/submit/'+token,dict(reviewer='reviewer-A',answers=answers[:-1]))[0]==400
            code,response=post(base+'/api/submit/'+token,payload)
            assert code==200 and response['ok'] and response['revision']==1
            assert json.loads((root/'submissions/reviewer-A.json').read_text())['answers']==answers
            assert '已提交' in get(base+'/status/'+server.tokens['admin'])[1].decode()
            answers[0]['changed']='yes'
            code,response=post(base+'/api/submit/'+token,payload)
            assert code==200 and response['revision']==2
            assert (root/'submissions/reviewer-A-revision-001.json').exists()
            assert json.loads((root/'submissions/reviewer-A.json').read_text())['answers'][0]['changed']=='yes'
            print('human review HTTP submission: PASS')
        finally:
            server.shutdown();server.server_close();thread.join(timeout=5)


if __name__=='__main__':main()
