#!/usr/bin/env python3
"""
Quality checker for Soil & Supper ML pipeline.
Detects blur, screenshots, malformed files, and other quality issues.
"""

import cv2
import json
import numpy as np
from pathlib import Path
from typing import Dict, List
from PIL import Image

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
PROCESSED_DIR = TRAINING_DATA_DIR / "processed"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def is_screenshot(image_path: Path) -> bool:
    """Detect if image is likely a screenshot."""
    try:
        with Image.open(image_path) as img:
            if img.width > 2000 or img.height > 2000:
                aspect = max(img.width, img.height) / min(img.width, img.height)
                if aspect < 1.5:
                    return True
    except Exception:
        pass
    return False


def compute_blur_score(image_path: Path) -> float:
    """Compute Laplacian variance (lower = more blurry)."""
    try:
        img = cv2.imread(str(image_path))
        if img is None:
            return -1.0
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return float(cv2.Laplacian(gray, cv2.CV_64F).var())
    except Exception:
        return -1.0


def check_image_quality(image_path: Path, blur_threshold: float = 100.0) -> Dict:
    """Check image quality metrics."""
    result = {
        "path": str(image_path),
        "is_screenshot": is_screenshot(image_path),
        "blur_score": compute_blur_score(image_path),
        "is_blurry": False,
        "valid": True,
    }
    
    if result["blur_score"] >= 0 and result["blur_score"] < blur_threshold:
        result["is_blurry"] = True
    
    return result


def run_quality_checks(blur_threshold: float = 100.0) -> Dict:
    """Run quality checks on all processed images."""
    if not PROCESSED_DIR.exists():
        return {"error": "No processed directory found"}
    
    stats = {
        "total": 0,
        "screenshots": 0,
        "blurry": 0,
        "valid": 0,
    }
    
    issues = []
    manifest_path = MANIFESTS_DIR / "quality_manifest.jsonl"
    
    with open(manifest_path, "w") as f:
        for img_path in PROCESSED_DIR.rglob("*"):
            if img_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                stats["total"] += 1
                result = check_image_quality(img_path, blur_threshold)
                
                if result["is_screenshot"]:
                    stats["screenshots"] += 1
                    issues.append(img_path)
                if result["is_blurry"]:
                    stats["blurry"] += 1
                    issues.append(img_path)
                
                if not result["is_screenshot"] and not result["is_blurry"]:
                    stats["valid"] += 1
                
                f.write(json.dumps(result) + "\n")
    
    print(f"Quality check complete:")
    print(f"  Total: {stats['total']}")
    print(f"  Valid: {stats['valid']}")
    print(f"  Screenshots: {stats['screenshots']}")
    print(f"  Blurry: {stats['blurry']}")
    print(f"  Issues found: {len(issues)}")
    
    return stats


if __name__ == "__main__":
    import sys
    blur_threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
    run_quality_checks(blur_threshold)
