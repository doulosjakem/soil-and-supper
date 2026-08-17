#!/usr/bin/env python3
"""Targeted SegPPD-101 ingestion into existing pipeline."""

import sys
from pathlib import Path

TRAINING_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TRAINING_DIR))

from class_mapper import initialize_default_mappings
from prepare_dataset import (
    discover_segppd101_classes,
    ingest_images,
    count_images,
    PROCESSED_DIR,
    RAW_DIR,
    MANIFESTS_DIR,
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
segppd101_dir = RAW_DIR / "segppd101"

if not segppd101_dir.exists():
    print("ERROR: segppd101 directory not found")
    sys.exit(1)

segppd101_classes = discover_segppd101_classes(segppd101_dir)
print(f"Discovered {len(segppd101_classes)} SegPPD-101 source classes")

total_ingested = 0
for source_label, paths in segppd101_classes.items():
    mapped_class, confidence = mapper.get_target_class("segppd101", source_label)
    if mapped_class:
        class_dir = PROCESSED_DIR / "diseases" / mapped_class
        existing = count_images(class_dir)
        count = ingest_images(mapped_class, paths, class_dir, "segppd101")
        if count > 0:
            print(f"  {source_label} -> {mapped_class}: +{count} images (total: {existing + count})")
            total_ingested += count

print(f"\nTotal SegPPD-101 images ingested: {total_ingested}")
