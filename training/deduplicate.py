#!/usr/bin/env python3
"""
Deduplication utilities for Soil & Supper ML pipeline.
Detects exact and near-duplicate images using hashing.
Prevents leakage between train/val/test splits.
"""

import imagehash
from pathlib import Path
from typing import Dict, Set, Tuple, List
from PIL import Image
import json

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

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


def find_cross_split_duplicates(split_dirs: Dict[str, Path], hash_size: int = 8, similarity_threshold: int = 5) -> Set[Tuple[str, str]]:
    """Find near-duplicates across train/val/test splits."""
    all_hashes = {}
    leakage_pairs = set()
    
    for split_name, split_dir in split_dirs.items():
        if not split_dir.exists():
            continue
        for img_path in split_dir.rglob("*"):
            if img_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                try:
                    img_hash = compute_phash(img_path, hash_size)
                    for existing_split, existing_path, existing_hash in all_hashes.get(str(img_hash), []):
                        if img_hash - existing_hash <= similarity_threshold:
                            leakage_pairs.add((split_name, existing_split, str(img_path), str(existing_path)))
                    all_hashes.setdefault(str(img_hash), []).append((split_name, str(img_path), img_hash))
                except Exception:
                    pass
    
    return leakage_pairs


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


def deduplicate_all(config: Dict):
    """Run deduplication on processed directory."""
    processed_dir = TRAINING_DATA_DIR / "processed"
    if not processed_dir.exists():
        print("No processed directory found.")
        return
    
    dedup_config = config.get("deduplication", {})
    hash_size = dedup_config.get("hash_size", 8)
    threshold = dedup_config.get("similarity_threshold", 5)
    
    print(f"Finding duplicates (hash_size={hash_size}, threshold={threshold})...")
    hashes, duplicates = find_duplicates(processed_dir, hash_size, threshold)
    
    print(f"Found {len(duplicates)} duplicate/near-duplicate images")
    
    if duplicates:
        print("Removing duplicates...")
        removed = remove_duplicates(processed_dir, hash_size=hash_size, similarity_threshold=threshold)
        print(f"Removed {removed} duplicates")
    
    if dedup_config.get("prevent_leakage", True):
        split_dirs = {
            "train": processed_dir / "train",
            "val": processed_dir / "val",
            "test": processed_dir / "test",
        }
        leakage = find_cross_split_duplicates(split_dirs, hash_size, threshold)
        if leakage:
            print(f"WARNING: Found {len(leakage)} cross-split duplicates!")
            for pair in leakage:
                print(f"  {pair[0]} <-> {pair[1]}: {pair[2]} == {pair[3]}")
        else:
            print("No cross-split leakage detected.")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    config = load_config() if len(sys.argv) > 1 else {"deduplication": {"hash_size": 8, "similarity_threshold": 5, "prevent_leakage": True}}
    deduplicate_all(config)
