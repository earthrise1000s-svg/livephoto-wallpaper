"""
LivePhoto-Wallpaper: Open-source Apple Live Photo wallpaper synthesizer.
"""

from .engine import LivePhotoEngine, LivePhotoInputError
from .capsule import unpack_capsule

__version__ = "1.0.0"
__all__ = ["LivePhotoEngine", "LivePhotoInputError", "unpack_capsule"]
