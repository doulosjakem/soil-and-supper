#!/usr/bin/env python3
"""
Dataset curation pipeline for Soil & Supper.
Consolidates extracted images from raw/*/images/ into curated/ and splits/.
"""

import os
import json
import csv
import hashlib
import shutil
import random
from pathlib import Path
from datetime import datetime

# Configuration
RAW_DIR = Path("./raw")
CURATED_DIR = Path("./curated")
SPLITS_DIR = Path("./splits")
METADATA_DIR = Path("./metadata")

CURATED_DIR.mkdir(exist_ok=True)
SPLITS_DIR.mkdir(exist_ok=True)
METADATA_DIR.mkdir(exist_ok=True)

TARGET_CLASSES = [
    "Tomato", "Pepper", "Eggplant", "Cucumber", "Zucchini",
    "Green Bean", "Corn", "Broccoli", "Carrot", "Potato",
    "Onion", "Strawberry"
]

# Source dataset configurations
SOURCE_DATASETS = [
    {
        "id": "DS-VEGANN",
        "name": "VegAnn (Zenodo 7636408)",
        "path": RAW_DIR / "zenodo_vegann" / "images",
        "license": "CC-BY-4.0",
        "attribution": "Madec et al., 2023. Zenodo. https://doi.org/10.5281/zenodo.7636408",
        "class_map": {
            "Corn": ["Corn"],
            "Green Bean": ["Green Bean"],
            "Onion": ["Onion"],
            "Pepper": ["Pepper"],
            "Potato": ["Potato"],
            "Strawberry": ["Strawberry"],
            "Broccoli": ["Broccoli"],
        }
    },
    {
        "id": "DS-BD-VEG",
        "name": "Bangladesh Comprehensive Vegetables (Project-AgML)",
        "path": RAW_DIR / "hf_veg_bangladesh" / "images",
        "license": "CC BY 4.0",
        "attribution": "Authors et al., 2025. Mendeley Data / HuggingFace.",
        "class_map": {
            "Tomato": ["Tomato"],
            "Eggplant": ["Eggplant"],
            "Cucumber": ["Cucumber"],
            "Green Bean": ["Green Bean"],
            "Onion": ["Onion"],
            "Pepper": ["Pepper"],
            "Potato": ["Potato"],
        }
    },
    {
        "id": "DS-100CROPS",
        "name": "LeafLogic 100 Crops Object Detection (Roboflow)",
        "path": RAW_DIR / "hf_100crops" / "images",
        "license": "CC BY 4.0",
        "attribution": "LeafLogic / Roboflow. https://universe.roboflow.com/lasso-pacific-qyid3/leaflogic-object-detection-b33dm",
        "class_map": {
            "Broccoli": ["Broccoli"],
            "Carrot": ["Carrot"],
            "Corn": ["Corn"],
            "Cucumber": ["Cucumber"],
            "Eggplant": ["Eggplant"],
            "Green Bean": ["Green Bean"],
            "Onion": ["Onion"],
            "Pepper": ["Pepper"],
            "Potato": ["Potato"],
            "Strawberry": ["Strawberry"],
            "Tomato": ["Tomato"],
        }
    },
    {
        "id": "DS-PLANTVILLAGE",
        "name": "PlantVillage (Mohanty et al., 2016)",
        "path": RAW_DIR / "hf_plantvillage" / "images",
        "license": "CC BY-SA 3.0",
        "attribution": "Mohanty et al., 2016. Frontiers in Plant Science. https://doi.org/10.3389/fpls.2016.01419",
        "class_map": {
            "Pepper": ["Pepper"],
            "Potato": ["Potato"],
            "Strawberry": ["Strawberry"],
            "Tomato": ["Tomato"],
            "Corn": ["Corn"],
        }
    },
    {
        "id": "DS-FRUIT-VEG",
        "name": "Fruit and Vegetable Image Recognition (Nattakarn)",
        "path": RAW_DIR / "hf_fruit_veg" / "images",
        "license": "Unknown (verify on HuggingFace)",
        "attribution": "Nattakarn. HuggingFace: Nattakarn/fruit-and-vegetable-image-recognition",
        "class_map": {
            "Carrot": ["Carrot"],
            "Corn": ["Corn"],
            "Cucumber": ["Cucumber"],
            "Eggplant": ["Eggplant"],
            "Green Bean": ["Green Bean"],
            "Onion": ["Onion"],
            "Pepper": ["Pepper"],
            "Potato": ["Potato"],
            "Tomato": ["Tomato"],
        }
    },
    {
        "id": "DS-FOOD-INGREDIENTS",
        "name": "Food Ingredients Dataset (Scuccorese)",
        "path": RAW_DIR / "hf_food_ingredients" / "images",
        "license": "Unknown (verify on HuggingFace)",
        "attribution": "Scuccorese. HuggingFace: Scuccorese/food-ingredients-dataset",
        "class_map": {
            "Broccoli": ["Broccoli"],
            "Carrot": ["Carrot"],
            "Corn": ["Corn"],
            "Green Bean": ["Green Bean"],
            "Onion": ["Onion"],
            "Potato": ["Potato"],
            "Strawberry": ["Strawberry"],
        }
    },
]

def get_file_hash(filepath):
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()

def consolidate_images():
    print("=" * 60)
    print("CONSOLIDATING IMAGES")
    print("=" * 60)

    stats = {cls: 0 for cls in TARGET_CLASSES}
    file_manifest = []

    for ds in SOURCE_DATASETS:
        ds_path = ds["path"]
        if not ds_path.exists():
            print(f"[SKIP] {ds['name']} - path not found: {ds_path}")
            continue

        print(f"\nProcessing: {ds['name']}")
        for source_cls, target_classes in ds["class_map"].items():
            src_dir = ds_path / source_cls
            if not src_dir.exists():
                continue

            images = [f for f in src_dir.iterdir() if f.is_file()]
            count = 0
            for img_path in images:
                for target_cls in target_classes:
                    if target_cls not in TARGET_CLASSES:
                        continue
                    dest_dir = CURATED_DIR / target_cls
                    dest_dir.mkdir(exist_ok=True)
                    dest_path = dest_dir / f"{ds['id']}_{img_path.name}"
                    if not dest_path.exists():
                        shutil.copy2(img_path, dest_path)
                        stats[target_cls] += 1
                        count += 1
                        file_manifest.append({
                            "filename": dest_path.name,
                            "class": target_cls,
                            "source_dataset": ds["id"],
                            "source_class": source_cls,
                            "license": ds["license"],
                            "attribution": ds["attribution"],
                        })
            if count > 0:
                print(f"  {source_cls} -> {target_classes}: {count} images")

    print("\nConsolidated class distribution:")
    for cls in TARGET_CLASSES:
        print(f"  {cls}: {stats[cls]}")
    print(f"Total: {sum(stats.values())}")

    return stats, file_manifest

def remove_duplicates():
    print("\n" + "=" * 60)
    print("REMOVING DUPLICATES")
    print("=" * 60)

    hashes = {}
    duplicates_removed = 0

    for cls in TARGET_CLASSES:
        class_dir = CURATED_DIR / cls
        if not class_dir.exists():
            continue

        images = list(class_dir.iterdir())
        for img_path in images:
            if not img_path.is_file():
                continue

            file_hash = get_file_hash(img_path)
            if file_hash in hashes:
                img_path.unlink()
                duplicates_removed += 1
                print(f"  Removed duplicate: {img_path.name}")
            else:
                hashes[file_hash] = img_path

    print(f"\nTotal duplicates removed: {duplicates_removed}")
    return duplicates_removed

def filter_by_quality():
    print("\n" + "=" * 60)
    print("FILTERING BY QUALITY")
    print("=" * 60)

    try:
        from PIL import Image
    except ImportError:
        print("[SKIP] Pillow not installed.")
        return 0

    removed = 0

    for cls in TARGET_CLASSES:
        class_dir = CURATED_DIR / cls
        if not class_dir.exists():
            continue

        images = list(class_dir.iterdir())
        for img_path in images:
            if not img_path.is_file():
                continue

            try:
                with Image.open(img_path) as img:
                    width, height = img.size

                    if min(width, height) < 100:
                        img_path.unlink()
                        removed += 1
                        print(f"  Removed (too small): {img_path.name} ({width}x{height})")
                        continue

                    gray = img.convert("L")
                    histogram = gray.histogram()
                    pixels = sum(histogram)
                    if pixels == 0:
                        continue

                    mean_brightness = sum(i * count for i, count in enumerate(histogram)) / pixels

                    if mean_brightness < 10 or mean_brightness > 245:
                        img_path.unlink()
                        removed += 1
                        print(f"  Removed (extreme exposure): {img_path.name} (brightness={mean_brightness:.1f})")

            except Exception as e:
                print(f"  Error processing {img_path.name}: {e}")
                img_path.unlink()
                removed += 1

    print(f"\nTotal removed by quality filter: {removed}")
    return removed

def create_splits(train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    print("\n" + "=" * 60)
    print("CREATING SPLITS")
    print("=" * 60)

    random.seed(seed)

    for cls in TARGET_CLASSES:
        class_dir = CURATED_DIR / cls
        if not class_dir.exists():
            continue

        images = [f for f in class_dir.iterdir() if f.is_file()]
        if not images:
            continue

        random.shuffle(images)

        n = len(images)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)
        n_test = n - n_train - n_val

        train_dir = SPLITS_DIR / "train" / cls
        val_dir = SPLITS_DIR / "val" / cls
        test_dir = SPLITS_DIR / "test" / cls

        train_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True, exist_ok=True)
        test_dir.mkdir(parents=True, exist_ok=True)

        for i, img_path in enumerate(images):
            if i < n_train:
                shutil.copy2(img_path, train_dir / img_path.name)
            elif i < n_train + n_val:
                shutil.copy2(img_path, val_dir / img_path.name)
            else:
                shutil.copy2(img_path, test_dir / img_path.name)

        print(f"  {cls}: train={n_train}, val={n_val}, test={n_test}")

def generate_manifests(file_manifest):
    print("\n" + "=" * 60)
    print("GENERATING MANIFESTS")
    print("=" * 60)

    manifest = []

    for split in ["train", "val", "test"]:
        split_dir = SPLITS_DIR / split
        if not split_dir.exists():
            continue

        for cls in TARGET_CLASSES:
            class_dir = split_dir / cls
            if not class_dir.exists():
                continue

            for img_path in class_dir.iterdir():
                if img_path.is_file():
                    source_info = next((m for m in file_manifest if m["filename"] == img_path.name), {
                        "source_dataset": "unknown",
                        "source_class": "unknown",
                        "license": "unknown",
                        "attribution": ""
                    })
                    manifest.append({
                        "filename": img_path.name,
                        "class": cls,
                        "split": split,
                        "source_dataset": source_info.get("source_dataset", "unknown"),
                        "source_class": source_info.get("source_class", "unknown"),
                        "license": source_info.get("license", "unknown"),
                        "attribution": source_info.get("attribution", ""),
                    })

    manifest_path = METADATA_DIR / "dataset_manifest.jsonl"
    with open(manifest_path, "w") as f:
        for entry in manifest:
            f.write(json.dumps(entry) + "\n")

    print(f"Saved manifest: {manifest_path}")
    print(f"Total images: {len(manifest)}")

    # Generate CSV for easy viewing
    csv_path = METADATA_DIR / "dataset_manifest.csv"
    if manifest:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=manifest[0].keys())
            writer.writeheader()
            writer.writerows(manifest)
        print(f"Saved CSV: {csv_path}")

def main():
    print("=" * 60)
    print("SOIL & SUPPER DATASET CURATION PIPELINE")
    print("=" * 60)
    print(f"Started: {datetime.now().isoformat()}")

    # Step 1: Consolidate images from all sources
    stats, file_manifest = consolidate_images()

    if sum(stats.values()) == 0:
        print("\n[STOP] No images found to curate.")
        return

    # Step 2: Remove duplicates
    remove_duplicates()

    # Step 3: Quality filter
    filter_by_quality()

    # Step 4: Create splits
    create_splits()

    # Step 5: Generate manifests
    generate_manifests(file_manifest)

    print("\n" + "=" * 60)
    print("CURATION COMPLETE")
    print("=" * 60)
    print(f"Finished: {datetime.now().isoformat()}")
    print(f"\nNext steps:")
    print(f"1. Review splits/ directory")
    print(f"2. Run quality_control.py for detailed checks")
    print(f"3. Run audit_licenses.py for attribution")
    print(f"4. Proceed to training when ready")

if __name__ == "__main__":
    main()
