"""
Core LivePhoto Synthesis Engine (Universal Cross-Platform: Linux, macOS, Docker).
Guarantees bypass of iOS 17+ / iOS 27 Lock Screen Live Wallpaper validation.
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
    def __init__(self, exiftool_path: Optional[str] = None, ffmpeg_path: Optional[str] = None):
        self.exiftool_path = exiftool_path or self._find_binary("exiftool")
        if not self.exiftool_path:
            raise RuntimeError(
                "exiftool not found! Please install exiftool:\n"
                "  - Linux: apt-get install -y libimage-exiftool-perl\n"
                "  - macOS: brew install exiftool"
            )
        self.ffmpeg_path = ffmpeg_path or self._find_binary("ffmpeg")
        if not self.ffmpeg_path:
            raise RuntimeError(
                "ffmpeg not found! Please install ffmpeg:\n"
                "  - Linux: apt-get install -y ffmpeg\n"
                "  - macOS: brew install ffmpeg"
            )

    @staticmethod
    def _find_binary(name: str) -> Optional[str]:
        # Check standard PATH
        p = shutil.which(name)
        if p:
            return p
        # Check common Linux and macOS system paths
        user_home = str(Path.home())
        candidates = [
            f"{user_home}/.local/bin/{name}",
            f"/usr/bin/{name}",
            f"/usr/local/bin/{name}",
            f"/opt/homebrew/bin/{name}",
            f"/bin/{name}",
        ]
        for c in candidates:
            if os.path.exists(c) and os.access(c, os.X_OK):
                return c
        return None

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
        custom_gps: Optional[Tuple[float, float]] = None,
        create_zip: bool = True,
        keep_loose: bool = False,
        max_duration: Optional[float] = 3.0,
    ) -> Dict[str, Any]:
        """
        Converts input video into Live Photo wallpaper assets.
        By default, duration is conformed to Apple Live Photo wallpaper baseline (max_duration=3.0s).
        By default (keep_loose=False), intermediate JPG/MOV files are kept in a temp
        directory and ONLY a clean .zip package is placed into output_dir.
        """
        import tempfile

        src_path = self.validate_input(input_video_path)
        out_directory = Path(output_dir).resolve() if output_dir else src_path.parent
        out_directory.mkdir(parents=True, exist_ok=True)

        base_stem = output_name or src_path.stem

        with tempfile.TemporaryDirectory(prefix="livephoto_build_") as tmpdir:
            tmp_path = Path(tmpdir)
            tmp_jpg = tmp_path / f"{base_stem}.JPG"
            tmp_mov = tmp_path / f"{base_stem}.MOV"

            live_uuid = custom_uuid or str(uuid.uuid4()).upper()

            # 1. Unpack pure data capsule
            capsule_mov, capsule_jpg = unpack_capsule()

            # 2. Extract initial frame at t=0 using FFmpeg
            cmd_frame = [
                self.ffmpeg_path,
                "-y",
                "-ss", "0",
                "-i", str(src_path),
                "-frames:v", "1",
                "-q:v", "2",
                str(tmp_jpg)
            ]
            res_frame = subprocess.run(cmd_frame, capture_output=True, text=True)
            if res_frame.returncode != 0:
                raise RuntimeError(f"FFmpeg frame extraction failed:\n{res_frame.stderr}")

            # 3. Mux video with capsule mebx motion tracks via passthrough copy
            # Strictly conform duration to 3.0s (authentic Apple Live Photo wallpaper benchmark)
            cmd_mux = [
                self.ffmpeg_path,
                "-y",
            ]
            if max_duration and max_duration > 0:
                cmd_mux.extend(["-ss", "0", "-t", str(max_duration)])
            cmd_mux.extend([
                "-i", str(src_path),
                "-i", capsule_mov,
                "-map", "0:v",
                "-map", "0:a?",
                "-map", "1:d?",
                "-c", "copy",
                "-movflags", "+faststart",
                str(tmp_mov)
            ])
            res_mux = subprocess.run(cmd_mux, capture_output=True, text=True)
            if res_mux.returncode != 0:
                raise RuntimeError(f"FFmpeg stream mux failed:\n{res_mux.stderr}")

            # 4. Copy authentic Apple QuickTime metadata & motion keys from capsule to MOV
            cmd_mov_keys = [
                self.exiftool_path,
                "-overwrite_original",
                "-TagsFromFile", capsule_mov,
                "-Keys:all",
                str(tmp_mov)
            ]
            subprocess.run(cmd_mov_keys, capture_output=True, text=True)

            # 5. Inject QuickTime ContentIdentifier UUID
            cmd_mov_uuid = [
                self.exiftool_path,
                "-overwrite_original",
                f"-QuickTime:ContentIdentifier={live_uuid}",
                str(tmp_mov)
            ]
            res_uuid = subprocess.run(cmd_mov_uuid, capture_output=True, text=True)
            if res_uuid.returncode != 0:
                raise RuntimeError(f"ExifTool MOV ContentIdentifier injection failed:\n{res_uuid.stderr}")

            # 6. Read exact extracted frame dimensions
            w_cmd = [self.exiftool_path, "-s", "-s", "-s", "-ImageWidth", str(tmp_jpg)]
            h_cmd = [self.exiftool_path, "-s", "-s", "-s", "-ImageHeight", str(tmp_jpg)]
            width = subprocess.check_output(w_cmd, text=True).strip()
            height = subprocess.check_output(h_cmd, text=True).strip()

            # 7. Copy full camera profile from capsule to JPG
            cmd_copy = [
                self.exiftool_path,
                "-overwrite_original",
                "-TagsFromFile", capsule_jpg,
                "-all:all", "-all:all>all:all",
                str(tmp_jpg)
            ]
            res_copy = subprocess.run(cmd_copy, capture_output=True, text=True)
            if res_copy.returncode != 0:
                raise RuntimeError(f"ExifTool JPG copy failed:\n{res_copy.stderr}")

            # 8. Set LivePhoto UUID, orientation, dimensions, clean thumbnails, and GPS on JPG
            cmd_meta = [
                self.exiftool_path,
                "-overwrite_original",
                f"-MakerNotes:ContentIdentifier={live_uuid}",
                f"-ExifImageWidth={width}",
                f"-ExifImageHeight={height}",
                "-Orientation#=1",
                "-ThumbnailImage=", "-PreviewImage=",
            ]

            # GPS Handling (always inject authentic landmark GPS)
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

            cmd_meta.append(str(tmp_jpg))
            res_meta = subprocess.run(cmd_meta, capture_output=True, text=True)
            if res_meta.returncode != 0:
                raise RuntimeError(f"ExifTool JPG injection failed:\n{res_meta.stderr}")

            # 9. Handle GPS on MOV
            cmd_mov_gps = [
                self.exiftool_path,
                "-overwrite_original",
                f"-GPSCoordinates={lat}, {lon}, {DEFAULT_GPS_ALT}",
                str(tmp_mov)
            ]
            subprocess.run(cmd_mov_gps, capture_output=True, text=True)

            zip_file_path = None
            if create_zip:
                zip_file_path = out_directory / f"{base_stem}_livephoto.zip"
                with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    # 1. Native Apple Live Photo bundle structure (.pvt) for Shortcuts recognition
                    zf.write(tmp_jpg, arcname=f"{base_stem}.pvt/{base_stem}.JPG")
                    zf.write(tmp_mov, arcname=f"{base_stem}.pvt/{base_stem}.MOV")
                    # 2. Root files for direct file access
                    zf.write(tmp_jpg, arcname=f"{base_stem}.JPG")
                    zf.write(tmp_mov, arcname=f"{base_stem}.MOV")

            final_jpg = None
            final_mov = None
            if keep_loose:
                final_jpg = out_directory / f"{base_stem}.JPG"
                final_mov = out_directory / f"{base_stem}.MOV"
                shutil.copy2(tmp_jpg, final_jpg)
                shutil.copy2(tmp_mov, final_mov)

            return {
                "uuid": live_uuid,
                "jpg_path": str(final_jpg) if final_jpg else None,
                "mov_path": str(final_mov) if final_mov else None,
                "zip_path": str(zip_file_path) if zip_file_path else None,
                "width": int(width),
                "height": int(height),
                "has_gps": True,
            }
