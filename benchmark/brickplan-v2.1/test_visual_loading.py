"""Pixel-preserving raster optimization and independent preview requests."""
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer
import json
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.request import urlopen

from PIL import Image

from bank import make_mission, task_by_id
from server import Arena, handler_for, run_config
import visual


class VisualLoadingTests(unittest.TestCase):
    def test_fast_raster_matches_frozen_renderer(self):
        for task_id in ("source-10001-03", "source-10220-01"):
            domain = make_mission(task_by_id(task_id)).domain
            selected = sorted(domain.fixed) + domain.mutable[:3]
            labels = {i: f"P{j:03d} S{j+1:03d}" for j, i in enumerate(domain.mutable[:3])}
            for view, explode, single in (("isometric", False, False), ("top", False, False),
                                          ("front", True, False), ("isometric", False, True)):
                with self.subTest(task=task_id, view=view, explode=explode, single=single):
                    parts = selected if not single else [domain.mutable[0]]
                    names = labels if not single else {}
                    expected = visual.core.render(domain, parts, names, view, (640, 480),
                                                  explode, single).resize((320, 240), Image.Resampling.LANCZOS)
                    actual = visual.render(domain, parts, names, view, (320, 240), explode, single)
                    self.assertEqual(actual.tobytes(), expected.tobytes())

    def test_cold_preview_does_not_block_scene_or_tasks(self):
        with tempfile.TemporaryDirectory() as store:
            arena = Arena(store, run_config(), render_images=False)
            server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(arena))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            entered, release = threading.Event(), threading.Event()
            base = f"http://127.0.0.1:{server.server_port}"
            def slow_preview(*args):
                entered.set()
                if not release.wait(5):
                    raise RuntimeError("Preview release timed out")
                return {"ready": True}
            try:
                with patch("catalogue.preview", slow_preview), ThreadPoolExecutor(max_workers=1) as pool:
                    pending = pool.submit(lambda: json.load(urlopen(base + "/api/preview/E001", timeout=8)))
                    try:
                        self.assertTrue(entered.wait(3))
                        # This must finish while the raster request is still waiting.
                        self.assertIn("parts", json.load(urlopen(base + "/api/scene/preview/E001", timeout=2)))
                        self.assertIn("tasks", json.load(urlopen(base + "/api/tasks", timeout=2)))
                    finally:
                        release.set()
                    self.assertEqual(pending.result(), {"ready": True})
            finally:
                release.set()
                server.shutdown()
                server.server_close()
                thread.join()


if __name__ == "__main__":
    unittest.main()
