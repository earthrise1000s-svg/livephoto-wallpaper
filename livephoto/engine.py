"""
Core LivePhoto Synthesis Engine.
Guarantees bypass of iOS 17+ Lock Screen Live Wallpaper validation.
"""

import os
import sys
import uuid
import shutil
import zipfile
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from .capsule import unpack_capsule

# Default landmark GPS: 厦门环岛路“一国两制 统一中国”标语牌
DEFAULT_GPS_LAT = 24.456193
DEFAULT_GPS_LON = 118.171992
DEFAULT_GPS_ALT = 5
DEFAULT_LOCATION_NAME = "一国两制 统一中国 标语牌"
DEFAULT_CITY = "厦门市"
DEFAULT_STATE = "福建省"
DEFAULT_COUNTRY = "中国"

SUPPORTED_VIDEO_EXTS = {".mov", ".mp4", ".m4v"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".bmp"}


class LivePhotoInputError(ValueError):
    """Raised when the input file format is invalid or unsupported."""
    pass


class LivePhotoEngine:
    def __init__(self, exiftool_path: Optional[str] = None):
        self.exiftool_path = exiftool_path or self._find_binary("exiftool")
        if not self.exiftool_path:
            raise RuntimeError("exiftool not found! Please install exiftool or add it to PATH.")
        self.helper_bin = self._ensure_synthesizer_binary()

    @staticmethod
    def _find_binary(name: str) -> Optional[str]:
        # Check standard PATH
        p = shutil.which(name)
        if p:
            return p
        # Check common macOS local paths
        candidates = [
            f"/Users/{os.getenv('USER')}/.local/bin/{name}",
            f"/opt/homebrew/bin/{name}",
            f"/usr/local/bin/{name}",
            f"/usr/bin/{name}",
        ]
        for c in candidates:
            if os.path.exists(c) and os.access(c, os.X_OK):
                return c
        return None

    def _ensure_synthesizer_binary(self) -> str:
        """
        Compiles synthesize.m on macOS if needed, and caches the binary.
        """
        cache_dir = Path.home() / ".cache" / "livephoto"
        cache_dir.mkdir(parents=True, exist_ok=True)
        bin_path = cache_dir / "synthesize_helper"

        source_m = Path(__file__).parent / "synthesize.m"
        if not source_m.exists():
            raise FileNotFoundError(f"Missing synthesizer source: {source_m}")

        # Recompile if binary missing or source is newer
        if not bin_path.exists() or bin_path.stat().st_mtime < source_m.stat().st_mtime:
            clang_bin = shutil.which("clang") or "/usr/bin/clang"
            cmd = [
                clang_bin,
                "-fobjc-arc",
                "-O2",
                "-framework", "Foundation",
                "-framework", "AVFoundation",
                "-framework", "CoreMedia",
                "-framework", "ImageIO",
                "-framework", "CoreGraphics",
                str(source_m),
                "-o", str(bin_path)
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                raise RuntimeError(f"Failed to compile synthesize.m:\n{res.stderr}")

        return str(bin_path)

    def validate_input(self, input_path: str) -> Path:
        p = Path(input_path).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        ext = p.suffix.lower()
        if ext in IMAGE_EXTS:
            raise LivePhotoInputError(
                "⚠️ 仅支持视频输入（.mov / .mp4）。\n"
                "检测到您上传的是图片文件（{ext}）。在 iPhone 端直接发送实况图通常只会被当作普通静态图片发送。\n"
                "如需将 Live Photo 制作成锁屏实况壁纸，请按以下步骤操作：\n"
                "  1. 在 iPhone「照片」中打开该实况图\n"
                "  2. 点击右上角「···」菜单\n"
                "  3. 选择【存储为视频】\n"
                "  4. 将导出的视频发送给我，即可自动合成为完美实况壁纸！".format(ext=ext)
            )

        if ext not in SUPPORTED_VIDEO_EXTS:
            raise LivePhotoInputError(
                f"不支持的文件格式: {ext}。仅支持视频文件: {', '.join(sorted(SUPPORTED_VIDEO_EXTS))}"
            )

        return p

    def convert(
        self,
        input_video_path: str,
        output_dir: Optional[str] = None,
        output_name: Optional[str] = None,
        custom_uuid: Optional[str] = None,
        no_gps: bool = False,
        custom_gps: Optional[Tuple[float, float]] = None,
        create_zip: bool = False,
    ) -> Dict[str, Any]:
        """
        Converts input video into a pair of (.JPG, .MOV) Live Photo wallpaper assets.
        """
        src_path = self.validate_input(input_video_path)
        out_directory = Path(output_dir).resolve() if output_dir else src_path.parent
        out_directory.mkdir(parents=True, exist_ok=True)

        base_stem = output_name or src_path.stem
        out_jpg = out_directory / f"{base_stem}.JPG"
        out_mov = out_directory / f"{base_stem}.MOV"

        live_uuid = custom_uuid or str(uuid.uuid4()).upper()

        # 1. Unpack pure data capsule
        capsule_mov, capsule_jpg = unpack_capsule()

        # 2. Run native AVFoundation synthesizer
        cmd_synth = [
            self.helper_bin,
            str(src_path),
            capsule_mov,
            str(out_mov),
            str(out_jpg),
            live_uuid,
        ]
        res = subprocess.run(cmd_synth, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Synthesizer failed:\n{res.stderr}")

        # 3. Read exact extracted frame dimensions
        w_cmd = [self.exiftool_path, "-s", "-s", "-s", "-ImageWidth", str(out_jpg)]
        h_cmd = [self.exiftool_path, "-s", "-s", "-s", "-ImageHeight", str(out_jpg)]
        width = subprocess.check_output(w_cmd, text=True).strip()
        height = subprocess.check_output(h_cmd, text=True).strip()

        # 4. Step A: Copy full camera profile from capsule
        cmd_copy = [
            self.exiftool_path,
            "-overwrite_original",
            "-TagsFromFile", capsule_jpg,
            "-all:all", "-all:all>all:all",
            str(out_jpg)
        ]
        res_copy = subprocess.run(cmd_copy, capture_output=True, text=True)
        if res_copy.returncode != 0:
            raise RuntimeError(f"ExifTool JPG copy failed:\n{res_copy.stderr}")

        # 4. Step B: Strictly set LivePhoto UUID, orientation, dimensions, clean thumbnails, and GPS
        cmd_meta = [
            self.exiftool_path,
            "-overwrite_original",
            f"-MakerNotes:ContentIdentifier={live_uuid}",
            f"-ExifImageWidth={width}",
            f"-ExifImageHeight={height}",
            "-Orientation#=1",
            "-ThumbnailImage=", "-PreviewImage=",
        ]

        # GPS Handling
        if no_gps:
            cmd_meta.extend(["-GPS*="])
        else:
            lat = custom_gps[0] if custom_gps else DEFAULT_GPS_LAT
            lon = custom_gps[1] if custom_gps else DEFAULT_GPS_LON
            lat_ref = "N" if lat >= 0 else "S"
            lon_ref = "E" if lon >= 0 else "W"
            cmd_meta.extend([
                f"-GPSLatitude={abs(lat)}", f"-GPSLatitudeRef={lat_ref}",
                f"-GPSLongitude={abs(lon)}", f"-GPSLongitudeRef={lon_ref}",
                f"-GPSAltitude={DEFAULT_GPS_ALT}", "-GPSAltitudeRef=0",
            ])
            if not custom_gps:
                cmd_meta.extend([
                    f"-XMP-iptcCore:Location={DEFAULT_LOCATION_NAME}",
                    f"-XMP-photoshop:City={DEFAULT_CITY}",
                    f"-XMP-photoshop:State={DEFAULT_STATE}",
                    f"-XMP-photoshop:Country={DEFAULT_COUNTRY}",
                ])

        cmd_meta.append(str(out_jpg))
        res_meta = subprocess.run(cmd_meta, capture_output=True, text=True)
        if res_meta.returncode != 0:
            raise RuntimeError(f"ExifTool JPG injection failed:\n{res_meta.stderr}")

        # 5. Handle GPS on MOV
        if no_gps:
            cmd_mov_gps = [
                self.exiftool_path,
                "-overwrite_original",
                "-GPSCoordinates=",
                str(out_mov)
            ]
            subprocess.run(cmd_mov_gps, capture_output=True, text=True)
        else:
            lat = custom_gps[0] if custom_gps else DEFAULT_GPS_LAT
            lon = custom_gps[1] if custom_gps else DEFAULT_GPS_LON
            cmd_mov_gps = [
                self.exiftool_path,
                "-overwrite_original",
                f"-GPSCoordinates={lat}, {lon}, {DEFAULT_GPS_ALT}",
                str(out_mov)
            ]
            subprocess.run(cmd_mov_gps, capture_output=True, text=True)

        zip_file_path = None
        if create_zip:
            zip_file_path = out_directory / f"{base_stem}_livephoto.zip"
            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zf:
                # 1. Native Apple Live Photo bundle structure (.pvt) for Shortcuts recognition
                zf.write(out_jpg, arcname=f"{base_stem}.pvt/{base_stem}.JPG")
                zf.write(out_mov, arcname=f"{base_stem}.pvt/{base_stem}.MOV")
                # 2. Root files for direct file access
                zf.write(out_jpg, arcname=f"{base_stem}.JPG")
                zf.write(out_mov, arcname=f"{base_stem}.MOV")

        return {
            "uuid": live_uuid,
            "jpg_path": str(out_jpg),
            "mov_path": str(out_mov),
            "zip_path": str(zip_file_path) if zip_file_path else None,
            "width": int(width),
            "height": int(height),
            "has_gps": not no_gps,
        }
