#!/usr/bin/env python3
"""
Processing template for Plant Pathology Challenge 2020.

Expected directory structure when manually placed:
    training_data/raw/plant_pathology_2020/
        train.csv
        images/
            Train_0.jpg
            Train_1.jpg
            ...

This template activates when training_data/raw/plant_pathology_2020/ exists
and contains train.csv + images directory.

License gate: CC BY 4.0 (claimed). Verify from primary Cornell source before
marking commercially usable. If license cannot be verified, set status = REVIEW.
"""

import csv
import json
import hashlib
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict

from PIL import Image

TRAINING_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TRAINING_DIR.parent
TRAINING_DATA_DIR = PROJECT_ROOT / "training_data"
RAW_DIR = TRAINING_DATA_DIR / "raw"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

DATASET_ID = "plant_pathology_2020"
DATASET_DIR = RAW_DIR / DATASET_ID

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Plant Pathology 2020 source classes mapped to Soil & Supper classes
TAXONOMY_MAPPING = {
    "healthy": {"class": "Healthy", "confidence": "HIGH"},
    "rust": {"class": "Rust", "confidence": "HIGH"},
    "scab": {"class": "Apple_scab", "confidence": "HIGH"},
    "multiple_diseases": {"class": "OUT_OF_TAXONOMY", "confidence": "HIGH"},
    "frog_eye_leaf_spot": {"class": "Leaf_spot", "confidence": "MEDIUM"},
}

# Kaggle columns: image_id, healthy, rust, scab, frog_eye_leaf_spot, powdery_mildew, complex
# Note: complex = multiple diseases


def compute_sha256(file_path: Path, chunk_size: int = 65536) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def load_existing_hashes() -> Tuple[set, set]:
    core_hashes = set()
    figshare_hashes = set()

    exact_dedup = MANIFESTS_DIR / "exact_dedup_manifest.jsonl"
    if exact_dedup.exists():
        with open(exact_dedup, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    h = entry.get("hash")
                    if h:
                        core_hashes.add(h)
                except json.JSONDecodeError:
                    continue

    figshare = MANIFESTS_DIR / "figshare_disease_manifest.jsonl"
    if figshare.exists():
        with open(figshare, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    h = entry.get("sha256")
                    if h:
                        figshare_hashes.add(h)
                except json.JSONDecodeError:
                    continue

    return core_hashes, figshare_hashes


def discover_structure(dataset_dir: Path) -> Optional[Dict]:
    """Discover Plant Pathology 2020 structure."""
    train_csv = dataset_dir / "train.csv"
    images_dir = dataset_dir / "images"

    if not train_csv.exists():
        # Sometimes images are in a subdirectory
        for subdir in dataset_dir.iterdir():
            if subdir.is_dir():
                candidate = subdir / "train.csv"
                if candidate.exists():
                    train_csv = candidate
                    images_dir = subdir / "images"
                    break

    if not train_csv.exists() or not images_dir.exists():
        return None

    return {"train_csv": train_csv, "images_dir": images_dir}


def parse_train_csv(csv_path: Path, images_dir: Path) -> Dict[str, List[Path]]:
    """Parse train.csv and map images to classes."""
    classes: Dict[str, List[Path]] = defaultdict(list)

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_id = row.get("image_id", "").strip()
            if not image_id:
                continue

            # Find image file (may be .jpg or .png)
            img_path = None
            for ext in SUPPORTED_EXTENSIONS:
                candidate = images_dir / f"{image_id}{ext}"
                if candidate.exists():
                    img_path = candidate
                    break

            if not img_path:
                continue

            # Determine primary label from binary columns
            # Columns: healthy, rust, scab, frog_eye_leaf_spot, powdery_mildew, complex
            labels = []
            for col in ["healthy", "rust", "scab", "frog_eye_leaf_spot", "powdery_mildew"]:
                if row.get(col, "").strip() == "1":
                    labels.append(col)

            if not labels or row.get("complex", "").strip() == "1":
                labels = ["multiple_diseases"]

            primary_label = labels[0] if labels else "healthy"
            mapping = TAXONOMY_MAPPING.get(primary_label, {"class": primary_label, "confidence": "LOW"})
            soil_class = mapping["class"]
            classes[soil_class].append(img_path)

    return dict(classes)


def generate_intake_report(dataset_dir: Path) -> Dict:
    """Generate intake report for Plant Pathology 2020."""
    report = {
        "dataset_id": DATASET_ID,
        "dataset_path": str(dataset_dir),
        "intake_timestamp": datetime.now().isoformat(),
        "structure": None,
        "total_images": 0,
        "valid_images": 0,
        "class_counts": {},
        "source_label_counts": {},
        "duplicates_vs_core": 0,
        "duplicates_vs_figshare": 0,
        "new_unique_images": 0,
        "corrupt_images": 0,
        "errors": [],
    }

    structure = discover_structure(dataset_dir)
    if not structure:
        report["errors"].append("Could not find train.csv + images/ directory")
        return report

    report["structure"] = {
        "train_csv": str(structure["train_csv"]),
        "images_dir": str(structure["images_dir"]),
    }

    classes = parse_train_csv(structure["train_csv"], structure["images_dir"])
    report["total_images"] = sum(len(v) for v in classes.values())
    report["class_counts"] = {k: len(v) for k, v in classes.items()}

    # Count source labels
    source_labels = defaultdict(int)
    with open(structure["train_csv"], "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for col in ["healthy", "rust", "scab", "frog_eye_leaf_spot", "powdery_mildew"]:
                if row.get(col, "").strip() == "1":
                    source_labels[col] += 1
            if row.get("complex", "").strip() == "1":
                source_labels["complex"] += 1
    report["source_label_counts"] = dict(source_labels)

    # Validate and hash
    core_hashes, figshare_hashes = load_existing_hashes()
    valid = 0
    corrupt = 0
    dup_core = 0
    dup_figshare = 0
    new_unique = 0

    for cls, paths in classes.items():
        for img_path in paths:
            try:
                with Image.open(img_path) as img:
                    img.verify()
                sha256 = compute_sha256(img_path)
                if sha256 in core_hashes:
                    dup_core += 1
                elif sha256 in figshare_hashes:
                    dup_figshare += 1
                else:
                    new_unique += 1
                valid += 1
            except Exception:
                corrupt += 1

    report["valid_images"] = valid
    report["corrupt_images"] = corrupt
    report["duplicates_vs_core"] = dup_core
    report["duplicates_vs_figshare"] = dup_figshare
    report["new_unique_images"] = new_unique

    return report


def print_report(report: Dict):
    print("=" * 80)
    print("PLANT PATHOLOGY 2020 — INTAKE REPORT")
    print("=" * 80)
    print(f"Dataset:      {report['dataset_id']}")
    print(f"Path:         {report['dataset_path']}")
    print(f"Timestamp:    {report['intake_timestamp']}")
    print()

    if report.get("structure"):
        s = report["structure"]
        print("--- Structure ---")
        print(f"  train.csv:  {s['train_csv']}")
        print(f"  images_dir: {s['images_dir']}")
        print()

    print("--- Image Counts ---")
    print(f"  Total images:         {report['total_images']:,}")
    print(f"  Valid images:         {report['valid_images']:,}")
    print(f"  Corrupt images:       {report['corrupt_images']:,}")
    print()

    print("--- Source Label Distribution ---")
    for label, count in sorted(report.get("source_label_counts", {}).items(), key=lambda x: -x[1]):
        print(f"  {label:<25} {count:>6}")
    print()

    print("--- Soil & Supper Class Mapping ---")
    for cls, count in sorted(report.get("class_counts", {}).items(), key=lambda x: -x[1]):
        print(f"  {cls:<30} {count:>6}")
    print()

    print("--- Duplicates ---")
    print(f"  vs Commercial core:   {report['duplicates_vs_core']:,}")
    print(f"  vs Figshare dataset:  {report['duplicates_vs_figshare']:,}")
    print(f"  New unique images:    {report['new_unique_images']:,}")
    print()

    if report.get("errors"):
        print("--- Errors ---")
        for err in report["errors"]:
            print(f"  {err}")
        print()

    print("=" * 80)
    print("NOTE: This is an INTAKE report only. No images were added to training data.")
    print("      License verification and commercial-use approval are separate gates.")
    print("=" * 80)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Plant Pathology 2020 intake template")
    parser.add_argument("--directory", type=str, default=str(DATASET_DIR), help="Dataset directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    dataset_dir = Path(args.directory).resolve()
    if not dataset_dir.exists():
        error_report = {
            "dataset_id": DATASET_ID,
            "dataset_path": str(dataset_dir),
            "intake_timestamp": datetime.now().isoformat(),
            "status": "BLOCKED",
            "error": f"Directory does not exist: {dataset_dir}",
            "message": "Waiting for manual acquisition via Kaggle.",
            "next_command": f"python training/dataset_intake.py {dataset_dir}",
            "total_images": 0,
            "valid_images": 0,
            "class_counts": {},
            "source_label_counts": {},
            "duplicates_vs_core": 0,
            "duplicates_vs_figshare": 0,
            "new_unique_images": 0,
            "corrupt_images": 0,
        }
        if args.json:
            print(json.dumps(error_report, indent=2, ensure_ascii=False))
        else:
            print(f"ERROR: Directory does not exist: {dataset_dir}")
            print("Waiting for manual acquisition via Kaggle.")
            print(f"Next: {error_report['next_command']}")
        sys.exit(1)

    report = generate_intake_report(dataset_dir)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
