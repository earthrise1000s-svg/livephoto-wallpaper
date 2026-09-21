"""
Unit and integration tests for LivePhoto-Wallpaper.
"""

import os
import tempfile
import unittest
from pathlib import Path

from livephoto.engine import LivePhotoEngine, LivePhotoInputError
from livephoto.capsule import unpack_capsule


class TestLivePhotoWallpaper(unittest.TestCase):
    def setUp(self):
        self.engine = LivePhotoEngine()
        self.test_dir = tempfile.mkdtemp(prefix="livephoto_test_")

    def test_image_rejection(self):
        """Verify that JPG / PNG inputs are rejected with LivePhotoInputError."""
        fake_jpg = Path(self.test_dir) / "test.jpg"
        fake_jpg.write_text("fake image content")

        with self.assertRaises(LivePhotoInputError) as ctx:
            self.engine.validate_input(str(fake_jpg))
        self.assertIn("仅支持视频输入", str(ctx.exception))
        self.assertIn("存储为视频", str(ctx.exception))

    def test_capsule_unpacking(self):
        """Verify that pure data capsule unpacks valid mebx and exif files."""
        mov_path, jpg_path = unpack_capsule(self.test_dir)
        self.assertTrue(os.path.exists(mov_path))
        self.assertTrue(os.path.exists(jpg_path))
        self.assertGreater(os.path.getsize(mov_path), 10000)
        self.assertGreater(os.path.getsize(jpg_path), 2000)

    def test_conversion_on_target_video(self):
        """Verify end-to-end conversion on IMG666.MOV if present."""
        sample_video = Path(__file__).resolve().parent.parent.parent / "需要被转换的视频" / "IMG666.MOV"
        if not sample_video.exists():
            self.skipTest(f"Sample video not found at {sample_video}")

        res = self.engine.convert(
            input_video_path=str(sample_video),
            output_dir=self.test_dir,
            output_name="output_live",
            create_zip=True,
            keep_loose=False,
        )

        self.assertIsNone(res["jpg_path"])
        self.assertIsNone(res["mov_path"])
        self.assertTrue(os.path.exists(res["zip_path"]))
        self.assertIsNotNone(res["uuid"])
        self.assertEqual(res["width"], 886)
        self.assertEqual(res["height"], 1920)

        # Test keep_loose=True
        res_loose = self.engine.convert(
            input_video_path=str(sample_video),
            output_dir=self.test_dir,
            output_name="output_loose",
            create_zip=True,
            keep_loose=True,
        )
        self.assertTrue(os.path.exists(res_loose["jpg_path"]))
        self.assertTrue(os.path.exists(res_loose["mov_path"]))
        self.assertTrue(os.path.exists(res_loose["zip_path"]))


if __name__ == "__main__":
    unittest.main()
