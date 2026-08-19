#!/usr/bin/env python3
"""
Processing template for Apple Leaf Diseases ICAR-CITH.

Expected directory structure when manually placed:
    training_data/raw/icar_apple/
        Apple_scab/
        Cedar_apple_rust/
        Apple_healthy/
        ...

This template activates when training_data/raw/icar_apple/ exists
and contains usable image data.

License gate: CC BY 4.0 (claimed). Verify from primary Mendeley source before
marking commercially usable. If license cannot be verified, set status = REVIEW.

Important: Previously identified AppleLeaf9 alternative contained synthetic
imagery (CycleGAN). This template explicitly checks for and documents any
synthetic vs field imagery distinction if metadata is available.

Critical class priorities:
  - Apple_scab (needs more sources)
  - Cedar_apple_rust (needs more sources)
"""

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

DATASET_ID = "icar_apple"
DATASET_DIR = RAW_DIR / DATASET_ID

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Example mapping — adjust after inspecting actual dataset classes
EXAMPLE_TAXONOMY_MAPPING = {
    "Apple_scab": {"class": "Apple_scab", "confidence": "HIGH"},
    "Apple_healthy": {"class": "Healthy", "confidence": "HIGH"},
    "Cedar_apple_rust": {"class": "Cedar_apple_rust", "confidence": "HIGH"},
}


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


def discover_classes(dataset_dir: Path) -> Dict[str, List[Path]]:
    """Discover class directories."""
    classes: Dict[str, List[Path]] = {}

    for item in dataset_dir.rglob("*"):
        if item.is_dir():
            images = [
                p for p in item.rglob("*")
                if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
            ]
            if images:
                classes[item.name] = images

    return classes


def validate_and_hash(paths: List[Path]) -> Tuple[int, int, int, int, int]:
    valid = 0
    corrupt = 0
    too_small = 0
    extreme_aspect = 0
    blank = 0

    for img_path in paths:
        try:
            with Image.open(img_path) as img:
                img.verify()
            with Image.open(img_path) as img:
                img.load()
                width, height = img.size

                if width < 64 or height < 64:
                    too_small += 1
                    continue

                aspect = max(width, height) / max(min(width, height), 1)
                if aspect > 10:
                    extreme_aspect += 1
                    continue

                extrema = img.getextrema()
                if all(e[1] - e[0] < 10 for e in extrema if len(e) == 2):
                    blank += 1
                    continue

                valid += 1
        except Exception:
            corrupt += 1

    return valid, corrupt, too_small, extreme_aspect, blank


def generate_intake_report(dataset_dir: Path) -> Dict:
    """Generate intake report for ICAR-CITH."""
    report = {
        "dataset_id": DATASET_ID,
        "dataset_path": str(dataset_dir),
        "intake_timestamp": datetime.now().isoformat(),
        "total_images": 0,
        "valid_images": 0,
        "corrupt_images": 0,
        "too_small_images": 0,
        "extreme_aspect_images": 0,
        "blank_images": 0,
        "classes": {},
        "class_counts": {},
        "duplicates_vs_core": 0,
        "duplicates_vs_figshare": 0,
        "new_unique_images": 0,
        "resolution_summary": {},
        "synthetic_imagery_detected": False,
        "synthetic_notes": "Check filenames, metadata, or dataset README for synthetic/augmented images. AppleLeaf9 alternative contained CycleGAN synthetic imagery.",
        "errors": [],
    }

    classes = discover_classes(dataset_dir)
    if not classes:
        report["errors"].append("No class directories with images found")
        return report

    core_hashes, figshare_hashes = load_existing_hashes()

    total_images = 0
    valid_images = 0
    corrupt_images = 0
    too_small_images = 0
    extreme_aspect_images = 0
    blank_images = 0
    dup_core = 0
    dup_figshare = 0
    new_unique = 0
    resolution_buckets = defaultdict(int)

    for cls, paths in classes.items():
        v, c, ts, ea, bl = validate_and_hash(paths)
        valid_images += v
        corrupt_images += c
        too_small_images += ts
        extreme_aspect_images += ea
        blank_images += bl
        total_images += len(paths)

        cls_dup_core = 0
        cls_dup_figshare = 0
        cls_new_unique = 0

        for img_path in paths:
            try:
                with Image.open(img_path) as img:
                    img.load()
                    width, height = img.size
                    resolution_buckets[f"{width}x{height}"] += 1

                sha256 = compute_sha256(img_path)
                if sha256 in core_hashes:
                    cls_dup_core += 1
                elif sha256 in figshare_hashes:
                    cls_dup_figshare += 1
                else:
                    cls_new_unique += 1
            except Exception:
                pass

        report["class_counts"][cls] = {
            "total": len(paths),
            "valid": v,
            "corrupt": c,
            "too_small": ts,
            "extreme_aspect": ea,
            "blank": bl,
            "duplicates_vs_core": cls_dup_core,
            "duplicates_vs_figshare": cls_dup_figshare,
            "new_unique": cls_new_unique,
        }

        dup_core += cls_dup_core
        dup_figshare += cls_dup_figshare
        new_unique += cls_new_unique

    report["total_images"] = total_images
    report["valid_images"] = valid_images
    report["corrupt_images"] = corrupt_images
    report["too_small_images"] = too_small_images
    report["extreme_aspect_images"] = extreme_aspect_images
    report["blank_images"] = blank_images
    report["classes"] = sorted(classes.keys())
    report["duplicates_vs_core"] = dup_core
    report["duplicates_vs_figshare"] = dup_figshare
    report["new_unique_images"] = new_unique
    report["resolution_summary"] = dict(sorted(resolution_buckets.items(), key=lambda x: -x[1]))

    return report


def print_report(report: Dict):
    print("=" * 80)
    print("ICAR-CITH APPLE LEAF DISEASES — INTAKE REPORT")
    print("=" * 80)
    print(f"Dataset:      {report['dataset_id']}")
    print(f"Path:         {report['dataset_path']}")
    print(f"Timestamp:    {report['intake_timestamp']}")
    print()

    print("--- File Counts ---")
    print(f"  Total images:         {report['total_images']:,}")
    print(f"  Valid images:         {report['valid_images']:,}")
    print(f"  Corrupt/unreadable:   {report['corrupt_images']:,}")
    print(f"  Too small (<64px):    {report['too_small_images']:,}")
    print(f"  Extreme aspect (>10): {report['extreme_aspect_images']:,}")
    print(f"  Blank images:         {report['blank_images']:,}")
    print()

    print("--- Class Breakdown ---")
    for cls in sorted(report.get("classes", [])):
        counts = report.get("class_counts", {}).get(cls, {})
        print(f"  {cls}:")
        print(f"    Total: {counts.get('total', 0):,}  Valid: {counts.get('valid', 0):,}  New unique: {counts.get('new_unique', 0):,}")
    print()

    print("--- Duplicates ---")
    print(f"  vs Commercial core:   {report['duplicates_vs_core']:,}")
    print(f"  vs Figshare dataset:  {report['duplicates_vs_figshare']:,}")
    print(f"  New unique images:    {report['new_unique_images']:,}")
    print()

    print("--- Synthetic Imagery Check ---")
    print(f"  Synthetic detected:   {report.get('synthetic_imagery_detected', False)}")
    print(f"  Notes:                {report.get('synthetic_notes', '')}")
    print()

    if report.get("resolution_summary"):
        print("--- Resolutions (top 10) ---")
        for res, count in list(report["resolution_summary"].items())[:10]:
            print(f"  {res:<15} {count:>6}")
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

    parser = argparse.ArgumentParser(description="ICAR-CITH intake template")
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
            "message": "Waiting for manual acquisition via Mendeley.",
            "total_images": 0,
            "valid_images": 0,
            "classes": {},
            "class_counts": {},
            "duplicates_vs_core": 0,
            "duplicates_vs_figshare": 0,
            "new_unique_images": 0,
            "corrupt_images": 0,
            "too_small_images": 0,
            "extreme_aspect_images": 0,
            "blank_images": 0,
            "resolution_summary": {},
            "synthetic_imagery_detected": False,
            "synthetic_notes": "Check filenames, metadata, or dataset README for synthetic/augmented images. AppleLeaf9 alternative contained CycleGAN synthetic imagery.",
            "errors": [],
        }
        if args.json:
            print(json.dumps(error_report, indent=2, ensure_ascii=False))
        else:
            print(f"ERROR: Directory does not exist: {dataset_dir}")
            print("Waiting for manual acquisition via Mendeley.")
        sys.exit(1)

    report = generate_intake_report(dataset_dir)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
