#!/usr/bin/env python3
"""
Dataset validation utilities for Soil & Supper ML pipeline.
Validates image integrity and detects corrupt files.
"""

from pathlib import Path
from typing import List
from PIL import Image

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_image(image_path: Path) -> bool:
    """Check if image is valid and not corrupt."""
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def find_corrupt_images(directory: Path) -> List[Path]:
    """Find corrupt or invalid images in a directory."""
    corrupt = []
    for img_path in directory.rglob("*"):
        if img_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            if not validate_image(img_path):
                corrupt.append(img_path)
    return corrupt


def remove_corrupt_images(directory: Path) -> int:
    """Remove corrupt images from directory."""
    corrupt = find_corrupt_images(directory)
    removed = 0
    for bad in corrupt:
        try:
            bad.unlink()
            removed += 1
        except Exception:
            pass
    return removed


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1])
    else:
        target_dir = Path(__file__).resolve().parent.parent / "data" / "processed"
    corrupt = find_corrupt_images(target_dir)
    print(f"Found {len(corrupt)} corrupt images.")
