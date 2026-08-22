#!/usr/bin/env python3
"""Quick inventory script - efficient version."""
import json
from pathlib import Path

TRAINING_DATA_DIR = Path("D:/soil-and-supper/soil-and-supper/training_data")
INBOX_EXTRACTED = TRAINING_DATA_DIR / "inbox_extracted"
RAW = TRAINING_DATA_DIR.parent / "raw"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def count_files_fast(d):
    count = 0
    try:
        for item in d.iterdir():
            if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
                count += 1
            elif item.is_dir():
                count += count_files_fast(item)
    except PermissionError:
        pass
    return count

def get_class_dirs(dataset_dir):
    class_dirs = []
    skip_dirs = {".cache", "extracted", "splits", "images", "leaf_grouping", "data", "train", "val", "test", "valid", "Train", "Val", "Test", "Valid"}
    for item in dataset_dir.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name not in skip_dirs:
            imgs = [f for f in item.iterdir() if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
            if imgs:
                class_dirs.append(item)
            else:
                # Check one level deeper
                for sub in item.iterdir():
                    if sub.is_dir():
                        sub_imgs = [f for f in sub.iterdir() if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                        if sub_imgs:
                            class_dirs.append(item)
                            break
    return class_dirs

results = {}

# Process inbox_extracted - only top-level structure, count first file in each class dir
for dataset_dir in sorted(INBOX_EXTRACTED.iterdir()):
    if not dataset_dir.is_dir():
        continue
    
    # Quick count: just count items at top level
    top_items = list(dataset_dir.iterdir())
    class_dirs = [d for d in top_items if d.is_dir() and not d.name.startswith(".") and d.name not in {".cache", "extracted", "splits", "images", "leaf_grouping", "data", "train", "val", "test", "valid", "Train", "Val", "Test", "Valid"}]
    
    # Check if class dirs have images directly
    real_class_dirs = []
    for cd in class_dirs:
        has_imgs = any(f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS for f in cd.iterdir())
        if has_imgs:
            real_class_dirs.append(cd)
        else:
            # Check subdirs
            for sub in cd.iterdir():
                if sub.is_dir() and any(f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS for f in sub.iterdir()):
                    real_class_dirs.append(cd)
                    break
    
    if real_class_dirs:
        classes = {}
        for cd in real_class_dirs:
            classes[cd.name] = count_files_fast(cd)
        results[dataset_dir.name] = {
            "type": "class_dirs",
            "num_classes": len(classes),
            "classes": dict(sorted(classes.items())),
            "total": sum(classes.values())
        }
    else:
        # Flat structure - count files directly in dataset
        total = count_files_fast(dataset_dir)
        results[dataset_dir.name] = {
            "type": "flat",
            "total": total
        }

with open(TRAINING_DATA_DIR / "reports" / "phase35h_inventory_verification.json", "w") as f:
    json.dump({"inbox_extracted": results}, f, indent=2)

print("Done")
print(f"\ninbox_extracted datasets: {len(results)}")
for name, info in results.items():
    print(f"{name}: {info['total']} images, type={info['type']}")
    if info["type"] == "class_dirs":
        print(f"  classes ({info['num_classes']}): {list(info['classes'].keys())[:8]}")
