#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Automated Test Suite for jk-agy-mermaid Native Rendering and Aspect Ratio Pipeline.
Validates:
1. pad_diagram.py aspect ratio calibration (H / W <= 1.15).
2. Symmetrical white canvas padding logic on tall vs wide geometries.
3. render_native.js and render_pipeline.py resolution and integration.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "skills" / "mermaid-designer" / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))
from pad_diagram import pad_diagram


class TestPadDiagram(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        for f in os.listdir(self.temp_dir):
            try:
                os.unlink(os.path.join(self.temp_dir, f))
            except Exception:
                pass
        try:
            os.rmdir(self.temp_dir)
        except Exception:
            pass

    def test_pad_tall_image_to_max_ratio(self):
        """A vertical image (ratio 2.0) must be padded horizontally to ratio <= 1.15."""
        src = os.path.join(self.temp_dir, "tall.png")
        # 1000 wide x 2000 tall -> ratio = 2.0
        im = Image.new("RGB", (1000, 2000), color=(66, 133, 244))
        im.save(src)

        out = pad_diagram(src, max_ratio=1.15)
        self.assertTrue(os.path.exists(out))

        with Image.open(out) as result:
            w, h = result.size
            ratio = h / w
            self.assertLessEqual(ratio, 1.151, f"Expected ratio <= 1.15, got {ratio:.3f}")
            # Height should remain 2000, width should expand to at least 1739
            self.assertEqual(h, 2000)
            self.assertGreaterEqual(w, 1739)
            # Corner pixel must be white (#FFFFFF)
            self.assertEqual(result.getpixel((0, 0)), (255, 255, 255))

    def test_pad_wide_image_adds_breathing_margin(self):
        """An already compliant image (ratio 0.8) must receive proportional breathing margin."""
        src = os.path.join(self.temp_dir, "wide.png")
        # 2000 wide x 1000 tall -> ratio = 0.5
        im = Image.new("RGB", (2000, 1000), color=(52, 168, 83))
        im.save(src)

        out = pad_diagram(src, max_ratio=1.15, margin_ratio=0.03)
        self.assertTrue(os.path.exists(out))

        with Image.open(out) as result:
            w, h = result.size
            # 3% of 2000 is 60px on each side -> 2120 wide x 1120 tall
            self.assertEqual(w, 2120)
            self.assertEqual(h, 1120)
            self.assertEqual(result.getpixel((0, 0)), (255, 255, 255))

    def test_file_not_found_raises(self):
        with self.assertRaises(FileNotFoundError):
            pad_diagram("/nonexistent/path/to/image.png")


class TestScriptResolution(unittest.TestCase):
    def test_render_native_script_exists_and_executable(self):
        render_native = SCRIPTS_DIR / "render_native.js"
        self.assertTrue(render_native.exists(), "render_native.js does not exist in skill scripts")
        self.assertTrue(os.access(str(render_native), os.X_OK), "render_native.js is not executable")

    def test_render_pipeline_script_exists_and_executable(self):
        pipeline = SCRIPTS_DIR / "render_pipeline.py"
        self.assertTrue(pipeline.exists(), "render_pipeline.py does not exist in skill scripts")
        self.assertTrue(os.access(str(pipeline), os.X_OK), "render_pipeline.py is not executable")

    def test_plugin_root_symlinks(self):
        root_scripts = REPO_ROOT / "scripts"
        self.assertTrue((root_scripts / "render_pipeline.py").exists())
        self.assertTrue((root_scripts / "render_native.js").exists())
        self.assertTrue((root_scripts / "pad_diagram.py").exists())


if __name__ == "__main__":
    unittest.main()
