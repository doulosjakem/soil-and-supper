#!/usr/bin/env python3
"""Corrected detailed inventory - counts all splits."""
import json
from pathlib import Path

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

def get_full_inventory(dataset_dir):
    """Get complete image count across all splits and class dirs."""
    total = 0
    classes = {}
    
    # Check for train/test/val splits
    found_splits = False
    for split in ["train", "val", "test", "Train", "Val", "Test", "images", "extracted"]:
        split_dir = dataset_dir / split
        if split_dir.exists() and split_dir.is_dir():
            found_splits = True
            for item in split_dir.iterdir():
                if item.is_dir() and not item.name.startswith("."):
                    cnt = count_images(item)
                    if cnt > 0:
                        classes[item.name] = classes.get(item.name, 0) + cnt
                        total += cnt
    
    if found_splits:
        return total, classes
    
    # Check top-level class dirs
    skip_dirs = {".cache", "extracted", "splits", "images", "leaf_grouping", "data", "train", "val", "test", "valid", "Train", "Val", "Test", "Valid"}
    for item in dataset_dir.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name not in skip_dirs:
            cnt = count_images(item)
            if cnt > 0:
                classes[item.name] = cnt
                total += cnt
    
    if classes:
        return total, classes
    
    # Flat structure
    total = count_images(dataset_dir)
    return total, {}

results = {}
for dataset_dir in sorted(INBOX_EXTRACTED.iterdir()):
    if not dataset_dir.is_dir():
        continue
    
    total, classes = get_full_inventory(dataset_dir)
    results[dataset_dir.name] = {
        "total_images": total,
        "num_classes": len(classes),
        "classes": dict(sorted(classes.items()))
    }

with open(INBOX_EXTRACTED.parent / "reports" / "phase35h_inbox_detailed_inventory_v2.json", "w") as f:
    json.dump(results, f, indent=2)

print("Corrected inventory complete.")
for name, info in results.items():
    print(f"{name}: {info['total_images']} images, {info['num_classes']} classes")
