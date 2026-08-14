#!/usr/bin/env python3
"""
Train/validation/test split generator for Soil & Supper ML pipeline.
Creates stratified splits with leakage prevention.
"""

import random
from pathlib import Path
from typing import Dict, List, Tuple
import json
import shutil
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
MANIFESTS_DIR = Path(__file__).resolve().parent.parent / "data" / "manifests"


def load_config() -> Dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def get_class_images(class_dir: Path) -> List[Path]:
    """Get all image paths for a class."""
    images = []
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
        images.extend(class_dir.glob(ext))
    return sorted(images)


def generate_stratified_split(
    class_dirs: List[Path],
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42
) -> Dict[str, List[Tuple[Path, str]]]:
    """Generate stratified train/val/test split."""
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6
    random.seed(seed)
    splits = {"train": [], "val": [], "test": []}
    for class_dir in class_dirs:
        class_name = class_dir.name
        images = get_class_images(class_dir)
        random.shuffle(images)
        n = len(images)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)
        splits["train"].extend([(img, class_name) for img in images[:n_train]])
        splits["val"].extend([(img, class_name) for img in images[n_train:n_train + n_val]])
        splits["test"].extend([(img, class_name) for img in images[n_train + n_val:]])
    return splits


def save_splits(splits: Dict[str, List[Tuple[Path, str]]], output_dir: Path) -> None:
    """Save splits to manifest files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for split_name, items in splits.items():
        manifest_path = output_dir / f"{split_name}_manifest.json"
        data = [
            {"path": str(img_path), "class": class_name}
            for img_path, class_name in items
        ]
        with open(manifest_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {split_name} manifest: {len(items)} images")


def copy_to_split_dirs(splits: Dict[str, List[Tuple[Path, str]]], output_dir: Path) -> None:
    """Copy images into train/val/test directories."""
    for split_name, items in splits.items():
        split_dir = output_dir / split_name
        split_dir.mkdir(parents=True, exist_ok=True)
        for img_path, class_name in items:
            class_dir = split_dir / class_name
            class_dir.mkdir(parents=True, exist_ok=True)
            dest = class_dir / img_path.name
            if not dest.exists():
                shutil.copy2(img_path, dest)


if __name__ == "__main__":
    config = load_config()
    class_dirs = [d for d in PROCESSED_DIR.iterdir() if d.is_dir()]
    splits = generate_stratified_split(
        class_dirs,
        train_ratio=config["split"]["train_ratio"],
        val_ratio=config["split"]["val_ratio"],
        test_ratio=config["split"]["test_ratio"],
        seed=config["split"]["seed"],
    )
    save_splits(splits, MANIFESTS_DIR)
    copy_to_split_dirs(splits, PROCESSED_DIR)
    print("Split generation complete.")
