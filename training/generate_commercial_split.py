#!/usr/bin/env python3
"""
Generate deterministic train/validation/test splits for commercial-only images.

Reads:
  - training_data/manifests/commercial_manifest.jsonl

Writes:
  - training_data/manifests/commercial_train_manifest.json
  - training_data/manifests/commercial_val_manifest.json
  - training_data/manifests/commercial_test_manifest.json
  - training_data/processed/commercial_train/{class}/
  - training_data/processed/commercial_val/{class}/
  - training_data/processed/commercial_test/{class}/
  - training_data/reports/commercial_split_report.json
"""

import json
import random
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
PROCESSED_DIR = TRAINING_DATA_DIR / "processed"
REPORTS_DIR = TRAINING_DATA_DIR / "reports"

COMMERCIAL_MANIFEST = MANIFESTS_DIR / "commercial_manifest.jsonl"
SPLIT_CONFIG = {
    "train_ratio": 0.70,
    "val_ratio": 0.15,
    "test_ratio": 0.15,
    "seed": 42,
}


def load_commercial_manifest() -> list:
    """Load commercial manifest, skipping metadata header."""
    entries = []
    with open(COMMERCIAL_MANIFEST, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if "image_id" in data:
                entries.append(data)
    return entries


def generate_stratified_split(entries: list, config: dict) -> dict:
    """Generate stratified split, grouped by class."""
    random.seed(config["seed"])
    by_class = defaultdict(list)
    for entry in entries:
        by_class[entry["class"]].append(entry)

    splits = {"train": [], "val": [], "test": []}
    for cls, class_entries in sorted(by_class.items()):
        random.shuffle(class_entries)
        n = len(class_entries)
        n_train = int(n * config["train_ratio"])
        n_val = int(n * config["val_ratio"])
        splits["train"].extend(class_entries[:n_train])
        splits["val"].extend(class_entries[n_train:n_train + n_val])
        splits["test"].extend(class_entries[n_train + n_val:])

    return splits


def save_split_manifests(splits: dict):
    """Write split manifest files."""
    for split_name, entries in splits.items():
        manifest_path = MANIFESTS_DIR / f"commercial_{split_name}_manifest.json"
        data = [
            {
                "image_id": e["image_id"],
                "path": e["local_path"],
                "class": e["class"],
                "source_dataset": e["source_dataset"],
                "sha256": e["sha256"],
            }
            for e in entries
        ]
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"  {split_name}: {len(entries)} images -> {manifest_path}")


def copy_to_split_dirs(splits: dict):
    """Copy images into commercial_train/val/test directories."""
    for split_name, entries in splits.items():
        split_dir = PROCESSED_DIR / f"commercial_{split_name}"
        split_dir.mkdir(parents=True, exist_ok=True)
        for entry in entries:
            src = Path(entry["local_path"])
            if not src.exists():
                continue
            cls = entry["class"]
            class_dir = split_dir / cls
            class_dir.mkdir(parents=True, exist_ok=True)
            dest = class_dir / src.name
            if not dest.exists():
                shutil.copy2(src, dest)


def generate_split_report(splits: dict, entries: list) -> dict:
    """Generate report for commercial split."""
    by_class = defaultdict(lambda: {"train": 0, "val": 0, "test": 0})
    by_source = defaultdict(lambda: {"train": 0, "val": 0, "test": 0})
    for split_name, split_entries in splits.items():
        for e in split_entries:
            by_class[e["class"]][split_name] += 1
            by_source[e["source_dataset"]][split_name] += 1

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "config": SPLIT_CONFIG,
        "totals": {
            split: len(entries)
            for split, entries in splits.items()
        },
        "by_class": dict(sorted(by_class.items())),
        "by_source": dict(sorted(by_source.items())),
    }


def main():
    print("Loading commercial manifest...")
    entries = load_commercial_manifest()
    print(f"  Loaded {len(entries)} commercial images")

    print("Generating stratified split...")
    splits = generate_stratified_split(entries, SPLIT_CONFIG)
    for split_name, split_entries in splits.items():
        print(f"  {split_name}: {len(split_entries)} images")

    print("Saving split manifests...")
    save_split_manifests(splits)

    print("Copying images to split directories...")
    copy_to_split_dirs(splits)

    print("Generating split report...")
    report = generate_split_report(splits, entries)
    report_path = REPORTS_DIR / "commercial_split_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"  Written to {report_path}")

    print("\nSplit generation complete.")


if __name__ == "__main__":
    main()
