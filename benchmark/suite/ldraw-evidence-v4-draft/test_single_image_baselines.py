"""Synthetic images only. Run and freeze the contract before evaluating the corpus."""
import base64
from copy import deepcopy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw

from single_image_baselines import predict


def wire(color=None, mixed=False):
    image = Image.new("RGB", (192, 128), "white")
    draw = ImageDraw.Draw(image)
    if color:
        draw.rectangle((40, 30, 139, 89), fill=color)
    if mixed:
        draw.rectangle((90, 30, 139, 89), fill="blue")
    # Annotation-like small marks must not dominate a large body.
    draw.rectangle((10, 10, 12, 12), fill="blue")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    payload = {"identity_contract": "Use this image.", "question": "What color is the marked object?",
               "format": "single-choice", "options": [
                   {"id": "A", "label": "Yellow"}, {"id": "B", "label": "Black"},
                   {"id": "C", "label": "Red"}, {"id": "D", "label": "Blue"}]}
    return {"messages": [{"role": "system", "content": "Return one choice."},
                         {"role": "user", "content": [
                             {"type": "text", "text": json.dumps(payload)},
                             {"type": "image_url", "image_url": {
                                 "url": "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode(),
                                 "detail": "high"}}]}]}


class ColorBoundaryTests(unittest.TestCase):
    def test_four_colors_without_files_or_gold(self):
        for color, choice in [("red", "C"), ("blue", "D"), ("yellow", "A"), ("black", "B")]:
            with self.subTest(color=color), patch("builtins.open", side_effect=AssertionError("file access")):
                self.assertEqual(predict(wire(color))["choiceId"], choice)

    def test_abstentions_are_not_guessed(self):
        self.assertEqual(predict(wire())["reason"], "no-color-region")
        self.assertEqual(predict(wire("red", mixed=True))["reason"], "mixed-colors")

    def test_option_permutation_changes_id_only(self):
        original = wire("red")
        changed = deepcopy(original)
        payload = json.loads(changed["messages"][1]["content"][0]["text"])
        payload["options"][0]["id"], payload["options"][2]["id"] = "C", "A"
        changed["messages"][1]["content"][0]["text"] = json.dumps(payload)
        self.assertEqual(predict(original)["choiceId"], "C")
        self.assertEqual(predict(changed)["choiceId"], "A")

    def test_rejects_extra_private_inputs_or_other_images(self):
        for key in ["render_spec", "gold", "body_mask", "pair_id", "source_id", "target_id"]:
            modified = wire("red")
            modified[key] = {"secret": "unused"}
            self.assertEqual(predict(modified)["reason"], "invalid-input")
            modified = wire("red")
            payload = json.loads(modified["messages"][1]["content"][0]["text"])
            payload[key] = "private"
            modified["messages"][1]["content"][0]["text"] = json.dumps(payload)
            self.assertEqual(predict(modified)["reason"], "invalid-input")
        modified = wire("red")
        modified["messages"][1]["content"].append(deepcopy(modified["messages"][1]["content"][1]))
        self.assertEqual(predict(modified)["reason"], "invalid-input")
        modified = wire("red")
        modified["messages"][1]["content"][1]["image_url"]["url"] = "file:///private.png"
        self.assertEqual(predict(modified)["reason"], "invalid-input")

    def test_cli_in_empty_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, "-I", str(Path(__file__).with_name("single_image_baselines.py"))],
                                    input=json.dumps(wire("yellow")), capture_output=True,
                                    text=True, cwd=directory, check=True)
            self.assertEqual(json.loads(result.stdout)["choiceId"], "A")
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
