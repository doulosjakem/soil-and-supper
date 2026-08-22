#!/usr/bin/env python3
"""Detailed inventory of inbox_extracted datasets."""
import json
from pathlib import Path
from collections import defaultdict

INBOX_EXTRACTED = Path("D:/soil-and-supper/soil-and-supper/training_data/inbox_extracted")
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def count_images(d):
    count = 0
    try:
        for item in d.iterdir():
            if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
                count += 1
            elif item.is_dir():
                count += count_images(item)
    except PermissionError:
        pass
    return count

def get_class_structure(dataset_dir):
    """Get class directories and their image counts."""
    classes = {}
    
    # Check for train/test/val splits
    for split in ["train", "val", "test", "Train", "Val", "Test", "images", "extracted"]:
        split_dir = dataset_dir / split
        if split_dir.exists() and split_dir.is_dir():
            for item in split_dir.iterdir():
                if item.is_dir() and not item.name.startswith("."):
                    cnt = count_images(item)
                    if cnt > 0:
                        classes[item.name] = cnt
            if classes:
                return classes
    
    # Check top-level class dirs
    skip_dirs = {".cache", "extracted", "splits", "images", "leaf_grouping", "data", "train", "val", "test", "valid", "Train", "Val", "Test", "Valid"}
    for item in dataset_dir.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name not in skip_dirs:
            cnt = count_images(item)
            if cnt > 0:
                classes[item.name] = cnt
    
    return classes

results = {}
for dataset_dir in sorted(INBOX_EXTRACTED.iterdir()):
    if not dataset_dir.is_dir():
        continue
    
    classes = get_class_structure(dataset_dir)
    if classes:
        results[dataset_dir.name] = {
            "total_images": sum(classes.values()),
            "num_classes": len(classes),
            "classes": dict(sorted(classes.items()))
        }
    else:
        # Flat structure
        total = count_images(dataset_dir)
        results[dataset_dir.name] = {
            "total_images": total,
            "num_classes": 0,
            "classes": {}
        }

with open(INBOX_EXTRACTED.parent / "reports" / "phase35h_inbox_detailed_inventory.json", "w") as f:
    json.dump(results, f, indent=2)

print("Detailed inventory complete.")
for name, info in results.items():
    print(f"\n{name}: {info['total_images']} images, {info['num_classes']} classes")
    if info['classes']:
        for cls, cnt in list(info['classes'].items())[:10]:
            print(f"  {cls}: {cnt}")
        if len(info['classes']) > 10:
            print(f"  ... and {len(info['classes'])-10} more")
