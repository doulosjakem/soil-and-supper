#!/usr/bin/env python3
"""Targeted Phase 20 dataset ingestion into existing pipeline."""

import sys
from pathlib import Path

TRAINING_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TRAINING_DIR))

from class_mapper import initialize_default_mappings
from prepare_dataset import (
    discover_irish_potato_classes,
    discover_common_beans_classes,
    discover_grapevine_classes,
    ingest_images,
    count_images,
    PROCESSED_DIR,
    RAW_DIR,
)

config = {"domains": {"diseases": {"classes": [
    "Healthy", "Powdery_mildew", "Downy_mildew", "Early_blight", "Late_blight",
    "Septoria_leaf_spot", "Bacterial_spot", "Fusarium_wilt", "Verticillium_wilt",
    "Anthracnose", "Rust", "Leaf_spot", "Blossom_end_rot", "Nutrient_deficiency",
    "Sunscald", "Frost_damage", "Hail_damage", "Overwatering_stress",
    "Underwatering_stress", "Insect_damage", "Chewing_damage", "Leaf_miner_damage",
    "Apple_scab", "Cedar_apple_rust", "Grape_black_rot", "Peach_bacterial_spot",
    "Soybean_rust", "Squash_powdery_mildew", "Tomato_mosaic_virus",
    "Tomato_yellow_leaf_curl"
]}}}

mapper = initialize_default_mappings()

# Irish Potato
print("="*60)
print("IRISH POTATO INGESTION")
print("="*60)
irish_potato_dir = RAW_DIR / "irish_potato"
if irish_potato_dir.exists():
    irish_potato_classes = discover_irish_potato_classes(irish_potato_dir)
    print(f"Discovered {len(irish_potato_classes)} classes: {list(irish_potato_classes.keys())}")
    
    total = 0
    for source_label, paths in irish_potato_classes.items():
        mapped_class, _ = mapper.get_target_class("irish_potato", source_label)
        if mapped_class:
            class_dir = PROCESSED_DIR / "diseases" / mapped_class
            existing = count_images(class_dir)
            count = ingest_images(mapped_class, paths, class_dir, "irish_potato")
            if count > 0:
                print(f"  {source_label} -> {mapped_class}: +{count} images (total: {existing + count})")
                total += count
    print(f"Total Irish Potato images ingested: {total}")

# Common Beans
print("\n" + "="*60)
print("COMMON BEANS INGESTION")
print("="*60)
common_beans_dir = RAW_DIR / "common_beans"
if common_beans_dir.exists():
    common_beans_classes = discover_common_beans_classes(common_beans_dir)
    print(f"Discovered {len(common_beans_classes)} classes: {list(common_beans_classes.keys())}")
    
    total = 0
    for source_label, paths in common_beans_classes.items():
        mapped_class, _ = mapper.get_target_class("common_beans", source_label)
        if mapped_class:
            class_dir = PROCESSED_DIR / "diseases" / mapped_class
            existing = count_images(class_dir)
            count = ingest_images(mapped_class, paths, class_dir, "common_beans")
            if count > 0:
                print(f"  {source_label} -> {mapped_class}: +{count} images (total: {existing + count})")
                total += count
    print(f"Total Common Beans images ingested: {total}")

# Grapevine
print("\n" + "="*60)
print("GRAPEVINE INGESTION")
print("="*60)
grapevine_dir = RAW_DIR / "grapevine"
if grapevine_dir.exists():
    grapevine_classes = discover_grapevine_classes(grapevine_dir)
    print(f"Discovered {len(grapevine_classes)} classes: {list(grapevine_classes.keys())}")
    
    total = 0
    for source_label, paths in grapevine_classes.items():
        mapped_class, _ = mapper.get_target_class("grapevine", source_label)
        if mapped_class:
            class_dir = PROCESSED_DIR / "diseases" / mapped_class
            existing = count_images(class_dir)
            count = ingest_images(mapped_class, paths, class_dir, "grapevine")
            if count > 0:
                print(f"  {source_label} -> {mapped_class}: +{count} images (total: {existing + count})")
                total += count
    print(f"Total Grapevine images ingested: {total}")

print("\n" + "="*60)
print("INGESTION COMPLETE")
print("="*60)
