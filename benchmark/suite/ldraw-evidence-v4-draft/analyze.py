"""Draft analysis helpers; live model/subset integration belongs to later phases."""
from copy import deepcopy
import json

# When the stripped A/B requests are byte-identical and decoding is deterministic,
# joint Both is mechanically 0 because the two golds differ; symmetric endpoint
# accuracy is at most 1/2. This is an image-content dependency floor, not proof of
# reference selection. Temperature zero alone does not establish determinism.
NO_IMAGE_INTERPRETATION = (
    "For byte-identical stripped A/B requests with different golds, identical "
    "deterministic predictions force Both=0 and symmetric endpoint accuracy<=1/2. "
    "This is an image-content floor, not a reference-selection floor. Stochastic "
    "or provider-variable outputs need not be identical; temperature zero alone "
    "does not establish deterministic decoding."
)


def strip_image(wire):
    result = deepcopy(wire)
    for message in result["messages"]:
        if isinstance(message["content"], list):
            message["content"] = [c for c in message["content"] if c["type"] != "image_url"]
    return result


def prompt_bytes(wire):
    """Complete model-visible system/user text; original text strings are unchanged."""
    return json.dumps(strip_image(wire)["messages"], ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode()
