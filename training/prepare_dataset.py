#!/usr/bin/env python3
"""
Dataset preparation utilities for Soil & Supper ML pipeline.
Filters, normalizes, and organizes images for training.
"""

import shutil
from pathlib import Path
from typing import Dict, List
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def load_config() -> Dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def normalize_filename(src: Path, class_name: str, index: int) -> str:
    """Generate normalized filename."""
    ext = src.suffix.lower()
    return f"{class_name}_{index:05d}{ext}"


def prepare_class(class_name: str, source_dirs: List[Path], output_dir: Path) -> int:
    """Copy and normalize images for a single class."""
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for src_dir in source_dirs:
        if not src_dir.exists():
            continue
        for img_path in src_dir.rglob("*"):
            if img_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                dest_name = normalize_filename(img_path, class_name, count)
                dest_path = output_dir / dest_name
                if not dest_path.exists():
                    shutil.copy2(img_path, dest_path)
                    count += 1
    return count


if __name__ == "__main__":
    config = load_config()
    print("Dataset preparation utilities loaded.")
    print(f"Target classes: {len(config['target_classes'])}")
