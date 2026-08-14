#!/usr/bin/env python3
"""
Dataset validation utilities for Soil & Supper ML pipeline.
Validates image integrity and detects corrupt, blank, or low-quality images.
"""

import json
from pathlib import Path
from typing import List, Dict
from PIL import Image
import hashlib

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def compute_hash(image_path: Path) -> str:
    """Compute SHA256 hash of image file."""
    h = hashlib.sha256()
    with open(image_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def validate_image(image_path: Path, min_size: int = 64) -> Dict:
    """Validate image and return quality metrics."""
    result = {
        "path": str(image_path),
        "valid": True,
        "corrupt": False,
        "too_small": False,
        "extreme_aspect": False,
        "blank": False,
        "hash": "",
        "width": 0,
        "height": 0,
    }
    
    try:
        with Image.open(image_path) as img:
            img.verify()
        with Image.open(image_path) as img:
            img.load()
            width, height = img.size
            result["width"] = width
            result["height"] = height
            
            if width < min_size or height < min_size:
                result["too_small"] = True
                result["valid"] = False
            
            aspect = max(width, height) / max(min(width, height), 1)
            if aspect > 10:
                result["extreme_aspect"] = True
                result["valid"] = False
            
            extrema = img.getextrema()
            if all(e[1] - e[0] < 10 for e in extrema if len(e) == 2):
                result["blank"] = True
                result["valid"] = False
            
            result["hash"] = compute_hash(image_path)
    except Exception as e:
        result["corrupt"] = True
        result["valid"] = False
        result["error"] = str(e)
    
    return result


def validate_all(config: Dict):
    """Validate all images in processed directory."""
    processed_dir = TRAINING_DATA_DIR / "processed"
    if not processed_dir.exists():
        print("No processed directory found. Run prepare step first.")
        return
    
    stats = {
        "total": 0,
        "valid": 0,
        "corrupt": 0,
        "too_small": 0,
        "extreme_aspect": 0,
        "blank": 0,
    }
    
    invalid_paths = []
    manifest_path = MANIFESTS_DIR / "validation_manifest.jsonl"
    
    with open(manifest_path, "w") as f:
        for img_path in processed_dir.rglob("*"):
            if img_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                stats["total"] += 1
                result = validate_image(img_path, config.get("quality", {}).get("min_image_size", 64))
                
                if result["valid"]:
                    stats["valid"] += 1
                else:
                    invalid_paths.append(img_path)
                    if result["corrupt"]:
                        stats["corrupt"] += 1
                    if result["too_small"]:
                        stats["too_small"] += 1
                    if result["extreme_aspect"]:
                        stats["extreme_aspect"] += 1
                    if result["blank"]:
                        stats["blank"] += 1
                
                f.write(json.dumps(result) + "\n")
    
    print(f"Validation complete:")
    print(f"  Total: {stats['total']}")
    print(f"  Valid: {stats['valid']}")
    print(f"  Corrupt: {stats['corrupt']}")
    print(f"  Too small: {stats['too_small']}")
    print(f"  Extreme aspect: {stats['extreme_aspect']}")
    print(f"  Blank: {stats['blank']}")
    
    if invalid_paths:
        print(f"\nRemoving {len(invalid_paths)} invalid images...")
        for p in invalid_paths:
            try:
                p.unlink()
            except Exception:
                pass
        print("Done.")
    
    return stats


if __name__ == "__main__":
    import sys
    config = load_config() if len(sys.argv) > 1 else {"quality": {"min_image_size": 64}}
    validate_all(config)
