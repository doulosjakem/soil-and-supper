#!/usr/bin/env python3
"""
Dataset curation utilities for Soil & Supper ML pipeline.
Filters, deduplicates, and prepares images for training.
"""

import hashlib
from pathlib import Path
from typing import List, Set
from PIL import Image

PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def compute_image_hash(image_path: Path) -> str:
    """Compute MD5 hash of image file for deduplication."""
    hasher = hashlib.md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicates(directory: Path) -> Set[str]:
    """Find duplicate images in a directory by hash."""
    hashes = {}
    duplicates = set()
    for img_path in directory.rglob("*"):
        if img_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            img_hash = compute_image_hash(img_path)
            if img_hash in hashes:
                duplicates.add(img_path)
            else:
                hashes[img_hash] = img_path
    return duplicates


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


if __name__ == "__main__":
    print("Dataset curation utilities loaded.")
