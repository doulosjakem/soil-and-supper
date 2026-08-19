#!/usr/bin/env python3
"""
Generate manifests for the acquired figshare DIsease Dataset.
"""

import os
import json
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

EXTRACT_PATH = Path(__file__).resolve().parent.parent / "training_data" / "raw" / "disease_dataset_figshare" / "extracted"
MANIFESTS_DIR = Path(__file__).resolve().parent.parent / "training_data" / "manifests"
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

# Taxonomy mapping from source classes to Soil & Supper classes
TAXONOMY_MAPPING = {
    "Beans_Angular_LeafSpot": {"class": "Leaf_spot", "confidence": "HIGH", "crop": "Bean"},
    "Beans_Rust": {"class": "Rust", "confidence": "HIGH", "crop": "Bean"},
    "Strawberry_Angular_LeafSpot": {"class": "Leaf_spot", "confidence": "HIGH", "crop": "Strawberry"},
    "Strawberry_Anthracnose_Fruit_Rot": {"class": "Anthracnose", "confidence": "HIGH", "crop": "Strawberry"},
    "Strawberry_Blossom_Blight": {"class": "OUT_OF_TAXONOMY", "confidence": "HIGH", "crop": "Strawberry"},
    "Strawberry_Gray_Mold": {"class": "OUT_OF_TAXONOMY", "confidence": "HIGH", "crop": "Strawberry"},
    "Strawberry_Leaf_Spot": {"class": "Leaf_spot", "confidence": "HIGH", "crop": "Strawberry"},
    "Strawberry_Powdery_Mildew_Fruit": {"class": "Powdery_mildew", "confidence": "HIGH", "crop": "Strawberry"},
    "Strawberry_Powdery_Mildew_Leaf": {"class": "Powdery_mildew", "confidence": "HIGH", "crop": "Strawberry"},
    "Tomato_Early_Blight": {"class": "Early_blight", "confidence": "HIGH", "crop": "Tomato"},
    "Tomato_Leaf_Mold": {"class": "OUT_OF_TAXONOMY", "confidence": "HIGH", "crop": "Tomato"},
    "Tomato_Spider_Mites": {"class": "Spider_mite", "confidence": "HIGH", "crop": "Tomato"},
}

CLASS_NAMES = {
    0: "Beans_Angular_LeafSpot",
    1: "Beans_Rust",
    2: "Strawberry_Angular_LeafSpot",
    3: "Strawberry_Anthracnose_Fruit_Rot",
    4: "Strawberry_Blossom_Blight",
    5: "Strawberry_Gray_Mold",
    6: "Strawberry_Leaf_Spot",
    7: "Strawberry_Powdery_Mildew_Fruit",
    8: "Strawberry_Powdery_Mildew_Leaf",
    9: "Tomato_Early_Blight",
    10: "Tomato_Leaf_Mold",
    11: "Tomato_Spider_Mites",
}

def compute_sha256(image_path):
    h = hashlib.sha256()
    with open(image_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

manifest_entries = []
source_manifest = []
label_distribution = defaultdict(int)
crop_distribution = defaultdict(int)
class_source_counts = defaultdict(lambda: defaultdict(int))

for split in ["train", "valid", "test"]:
    images_dir = EXTRACT_PATH / split / "images"
    labels_dir = EXTRACT_PATH / split / "labels"
    
    if not images_dir.exists():
        continue
    
    image_files = sorted(images_dir.iterdir())
    print(f"Processing {split}: {len(image_files)} images")
    
    for img_path in image_files:
        if not img_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            continue
        
        # Find corresponding label file
        label_path = labels_dir / f"{img_path.stem}.txt"
        
        if label_path.exists():
            with open(label_path, "r") as f:
                lines = f.readlines()
            
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue
                class_id = int(parts[0])
                class_name = CLASS_NAMES.get(class_id, f"Unknown_{class_id}")
                mapping = TAXONOMY_MAPPING.get(class_name, {})
                soil_class = mapping.get("class", "UNKNOWN")
                confidence = mapping.get("confidence", "UNKNOWN")
                crop = mapping.get("crop", "Unknown")
                
                label_distribution[class_name] += 1
                class_source_counts[soil_class]["figshare_disease"] += 1
                crop_distribution[crop] += 1
        else:
            # Image without label
            soil_class = "UNLABELED"
            confidence = "NONE"
            crop = "Unknown"
        
        # Compute hash
        sha256 = compute_sha256(img_path)
        
        entry = {
            "path": str(img_path),
            "filename": img_path.name,
            "split": split,
            "source_dataset": "figshare_disease",
            "source_class": class_name if label_path.exists() else "unlabeled",
            "soil_and_supper_class": soil_class,
            "mapping_confidence": confidence,
            "crop": crop,
            "sha256": sha256,
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "provenance": "figshare DOI 10.17632/9zgkwwv9j8 (Roboflow detecting-diseases v6)",
            "acquired_date": "2026-08-18",
            "resolution": "416x416",
            "annotation_format": "YOLO bounding boxes",
        }
        manifest_entries.append(entry)

# Write manifest
manifest_path = MANIFESTS_DIR / "figshare_disease_manifest.jsonl"
with open(manifest_path, "w", encoding="utf-8") as f:
    for entry in manifest_entries:
        f.write(json.dumps(entry) + "\n")

print(f"\nWrote {len(manifest_entries)} entries to {manifest_path}")

# Write source manifest
source_manifest_path = MANIFESTS_DIR / "figshare_disease_source_manifest.jsonl"
with open(source_manifest_path, "w", encoding="utf-8") as f:
    entry = {
        "dataset_id": "figshare_disease",
        "name": "DIsease Dataset",
        "url": "https://figshare.com/articles/dataset/DIsease_Dataset/28612433",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "commercial_use": True,
        "attribution_required": True,
        "total_images": len(manifest_entries),
        "train_images": len([e for e in manifest_entries if e["split"] == "train"]),
        "val_images": len([e for e in manifest_entries if e["split"] == "valid"]),
        "test_images": len([e for e in manifest_entries if e["split"] == "test"]),
        "annotation_format": "YOLO bounding boxes",
        "resolution": "416x416",
        "actual_source": "Roboflow dataset (detecting-diseases v6)",
        "roboflow_workspace": "artificial-intelligence-82oex",
        "acquired_date": "2026-08-18",
    }
    f.write(json.dumps(entry) + "\n")

print(f"Wrote source manifest to {source_manifest_path}")

# Print summary
print("\n=== Label Distribution ===")
for class_name, count in sorted(label_distribution.items(), key=lambda x: -x[1]):
    print(f"  {class_name}: {count}")

print("\n=== Soil & Supper Class Mapping ===")
for soil_class in sorted(class_source_counts.keys()):
    print(f"  {soil_class}: {sum(class_source_counts[soil_class].values())}")

print("\n=== Crop Distribution ===")
for crop, count in sorted(crop_distribution.items(), key=lambda x: -x[1]):
    print(f"  {crop}: {count}")
