#!/usr/bin/env python3
"""
Dataset manifest generator for Soil & Supper ML pipeline.
Reports class counts, identifies weak classes, and generates metadata.
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"
MANIFESTS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "manifests"
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)


def count_images_per_class(class_dir: Path) -> int:
    """Count images in a class directory."""
    count = 0
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
        count += len(list(class_dir.glob(ext)))
    return count


def generate_class_report(class_dirs: List[Path]) -> Dict:
    """Generate report of class distribution."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "total_classes": len(class_dirs),
        "classes": {},
        "total_images": 0,
    }

    for class_dir in sorted(class_dirs):
        class_name = class_dir.name
        count = count_images_per_class(class_dir)
        report["classes"][class_name] = {
            "count": count,
            "path": str(class_dir),
        }
        report["total_images"] += count

    return report


def find_weak_classes(report: Dict, min_count: int = 20) -> List[str]:
    """Identify classes with insufficient training data."""
    weak = []
    for class_name, info in report["classes"].items():
        if info["count"] < min_count:
            weak.append(class_name)
    return weak


def save_manifest(report: Dict, filename: str = "dataset_manifest.json") -> Path:
    """Save manifest to file."""
    manifest_path = MANIFESTS_DIR / filename
    with open(manifest_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Saved manifest: {manifest_path}")
    return manifest_path


if __name__ == "__main__":
    if not PROCESSED_DIR.exists():
        print(f"Processed directory not found: {PROCESSED_DIR}")
        exit(1)

    class_dirs = [d for d in PROCESSED_DIR.iterdir() if d.is_dir()]
    report = generate_class_report(class_dirs)
    weak_classes = find_weak_classes(report)

    print(f"Total classes: {report['total_classes']}")
    print(f"Total images: {report['total_images']}")
    print(f"Weak classes (< 20 images): {weak_classes}")

    save_manifest(report)
