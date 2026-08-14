#!/usr/bin/env python3
"""
Deduplication utilities for Soil & Supper ML pipeline.
Detects exact and near-duplicate images using hashing.
"""

import imagehash
from pathlib import Path
from typing import Dict, Set, Tuple
from PIL import Image

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def compute_phash(image_path: Path, hash_size: int = 8) -> imagehash.ImageHash:
    """Compute perceptual hash of an image."""
    with Image.open(image_path) as img:
        return imagehash.phash(img, hash_size=hash_size)


def find_duplicates(
    directory: Path,
    hash_size: int = 8,
    similarity_threshold: int = 5
) -> Tuple[Dict[imagehash.ImageHash, list], Set[Path]]:
    """Find duplicate and near-duplicate images."""
    hashes = {}
    duplicates = set()
    for img_path in directory.rglob("*"):
        if img_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            try:
                img_hash = compute_phash(img_path, hash_size)
                for existing_hash, existing_paths in hashes.items():
                    if img_hash - existing_hash <= similarity_threshold:
                        duplicates.add(img_path)
                        existing_paths.append(img_path)
                        break
                else:
                    hashes[img_hash] = [img_path]
            except Exception:
                pass
    return hashes, duplicates


def remove_duplicates(directory: Path, **kwargs) -> int:
    """Remove duplicate images from directory."""
    _, duplicates = find_duplicates(directory, **kwargs)
    removed = 0
    for dup in duplicates:
        try:
            dup.unlink()
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
    hashes, duplicates = find_duplicates(target_dir)
    print(f"Found {len(duplicates)} duplicate/near-duplicate images.")
