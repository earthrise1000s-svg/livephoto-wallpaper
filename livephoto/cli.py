"""
Command Line Interface for LivePhoto-Wallpaper.
"""

import argparse
import os
import sys
from pathlib import Path

from .engine import LivePhotoEngine, LivePhotoInputError


def main():
    parser = argparse.ArgumentParser(
        prog="livephoto",
        description="Convert any video into an authentic iOS 27 Live Wallpaper (.zip package for Shortcuts import)",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Input video file path (.mov, .mp4, .m4v)",
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=None,
        help="Target output directory (default: same as input)",
    )
    parser.add_argument(
        "-n", "--name",
        type=str,
        default=None,
        help="Base name for generated files (e.g. IMG_1234)",
    )
    parser.add_argument(
        "-z", "--zip",
        action="store_true",
        default=True,
        help="Package output into .zip (default: always on)",
    )
    parser.add_argument(
        "--keep-loose",
        action="store_true",
        default=False,
        help="Keep loose .JPG and .MOV files after zip creation (default: auto-clean)",
    )
    parser.add_argument(
        "--no-gps",
        action="store_true",
        help="Strip all GPS coordinates from outputs (privacy protection)",
    )
    parser.add_argument(
        "--gps",
        type=str,
        default=None,
        help="Custom GPS coordinates in format 'lat,lon' (e.g. '24.456,118.172')",
    )

    args = parser.parse_args()

    custom_gps = None
    if args.gps:
        try:
            parts = args.gps.split(",")
            custom_gps = (float(parts[0].strip()), float(parts[1].strip()))
        except Exception:
            print("❌ 错误: --gps 参数格式不正确，应为 '纬度,经度' (例如: 24.456,118.172)")
            sys.exit(1)

    print("\n📸 [LivePhoto-Wallpaper] 苹果原生实况壁纸合成引擎")
    print(f"🎬 输入文件: {args.input}")

    try:
        engine = LivePhotoEngine()
        res = engine.convert(
            input_video_path=args.input,
            output_dir=args.output_dir,
            output_name=args.name,
            no_gps=args.no_gps,
            custom_gps=custom_gps,
            create_zip=True,  # Always generate zip
        )

        # Auto-clean loose JPG and MOV files (only keep zip)
        if not args.keep_loose and res["zip_path"]:
            for loose_file in [res["jpg_path"], res["mov_path"]]:
                try:
                    os.remove(loose_file)
                except OSError:
                    pass

        print("\n✨ 合成成功！")
        print(f"  📦 壁纸包: {res['zip_path']}")
        print(f"  🔑 实况标识: {res['uuid']}")
        print("\n🎉 将壁纸包通过快捷指令一键导入 iPhone 相册即可设为锁屏动态壁纸！\n")

    except LivePhotoInputError as e:
        print(f"\n{e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 转换失败: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
