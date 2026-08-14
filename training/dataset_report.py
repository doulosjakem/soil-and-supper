#!/usr/bin/env python3
"""
Dataset report generator for Soil & Supper ML pipeline.
Generates human-readable and machine-readable reports.
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
MANIFESTS_DIR = Path(__file__).resolve().parent.parent / "data" / "manifests"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "data" / "reports"


def load_config() -> Dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def count_images(directory: Path) -> int:
    """Count images in directory."""
    count = 0
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
        count += len(list(directory.rglob(ext)))
    return count


def generate_report() -> Dict:
    """Generate dataset report."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "processed_dir": str(PROCESSED_DIR),
        "manifests_dir": str(MANIFESTS_DIR),
        "classes": {},
        "total_images": 0,
        "splits": {},
    }

    if PROCESSED_DIR.exists():
        class_dirs = [d for d in PROCESSED_DIR.iterdir() if d.is_dir()]
        for class_dir in class_dirs:
            class_name = class_dir.name
            count = count_images(class_dir)
            report["classes"][class_name] = {
                "count": count,
                "path": str(class_dir),
            }
            report["total_images"] += count

    for split in ["train", "val", "test"]:
        manifest_path = MANIFESTS_DIR / f"{split}_manifest.json"
        if manifest_path.exists():
            with open(manifest_path, "r") as f:
                data = json.load(f)
            report["splits"][split] = len(data)

    return report


def save_report(report: Dict, filename: str = "dataset_report.json") -> Path:
    """Save JSON report."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / filename
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Saved report: {report_path}")
    return report_path


def print_summary(report: Dict) -> None:
    """Print human-readable summary."""
    print("=" * 60)
    print("DATASET REPORT")
    print("=" * 60)
    print(f"Generated: {report['generated_at']}")
    print(f"Total images: {report['total_images']}")
    print(f"Total classes: {len(report['classes'])}")
    print("\nClass distribution:")
    for class_name, info in sorted(report["classes"].items()):
        print(f"  {class_name}: {info['count']} images")
    print("\nSplits:")
    for split, count in report["splits"].items():
        print(f"  {split}: {count} images")


if __name__ == "__main__":
    report = generate_report()
    save_report(report)
    print_summary(report)
