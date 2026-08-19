#!/usr/bin/env python3
"""
Generic dataset intake script for Soil & Supper ML pipeline.

Inspects a manually supplied dataset directory and produces a comprehensive
intake report WITHOUT adding images to the training corpus or marking the
dataset as commercially usable.

Reports:
  - files discovered
  - image files
  - unreadable/corrupt files
  - image dimensions
  - SHA256 hashes
  - exact duplicates vs commercial core and figshare dataset
  - class directories / labels
  - image counts by class
  - archive validity (if archive present)

License approval remains a separate manual gate.
"""

import json
import sys
import zipfile
import tarfile
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from collections import defaultdict

from PIL import Image

TRAINING_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TRAINING_DIR.parent
TRAINING_DATA_DIR = PROJECT_ROOT / "training_data"
RAW_DIR = TRAINING_DATA_DIR / "raw"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
REPORTS_DIR = TRAINING_DATA_DIR / "reports"

for d in [MANIFESTS_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SUPPORTED_ARCHIVE_EXTENSIONS = {".zip", ".tar.gz", ".tgz", ".tar"}

EXACT_DEDUP_MANIFEST = MANIFESTS_DIR / "exact_dedup_manifest.jsonl"
FIGSHARE_MANIFEST = MANIFESTS_DIR / "figshare_disease_manifest.jsonl"


def compute_sha256(file_path: Path, chunk_size: int = 65536) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def is_archive(archive_path: Path) -> bool:
    return archive_path.suffix.lower() in SUPPORTED_ARCHIVE_EXTENSIONS


def detect_html_error(archive_path: Path) -> Optional[str]:
    try:
        with open(archive_path, "rb") as f:
            header = f.read(4096)
        if b"<!doctype html>" in header.lower() or b"<html" in header.lower():
            return "File is HTML, not an archive"
    except Exception as e:
        return str(e)
    return None


def verify_archive(archive_path: Path) -> Dict:
    info = {
        "path": str(archive_path),
        "size": archive_path.stat().st_size,
        "format": archive_path.suffix.lower(),
        "valid": False,
        "file_count": 0,
        "image_count": 0,
        "sample_files": [],
        "error": None,
    }

    html_error = detect_html_error(archive_path)
    if html_error:
        info["error"] = html_error
        return info

    try:
        if archive_path.suffix.lower() == ".zip":
            with zipfile.ZipFile(archive_path, "r") as zf:
                namelist = zf.namelist()
                info["file_count"] = len(namelist)
                info["valid"] = True
                info["sample_files"] = namelist[:10]
                image_count = sum(
                    1 for n in namelist if Path(n).suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
                )
                info["image_count"] = image_count
        elif archive_path.suffix.lower() in {".tar.gz", ".tgz", ".tar"}:
            with tarfile.open(archive_path, "r:*") as tf:
                namelist = tf.getnames()
                info["file_count"] = len(namelist)
                info["valid"] = True
                info["sample_files"] = namelist[:10]
                image_count = sum(
                    1 for n in namelist if Path(n).suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
                )
                info["image_count"] = image_count
        else:
            info["error"] = f"Unsupported archive format: {archive_path.suffix}"
    except Exception as e:
        info["error"] = str(e)

    return info


def load_existing_hashes() -> Tuple[Set[str], Set[str]]:
    core_hashes: Set[str] = set()
    figshare_hashes: Set[str] = set()

    if EXACT_DEDUP_MANIFEST.exists():
        with open(EXACT_DEDUP_MANIFEST, "r", encoding="utf-8") as f:
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

    if FIGSHARE_MANIFEST.exists():
        with open(FIGSHARE_MANIFEST, "r", encoding="utf-8") as f:
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


def discover_classes(directory: Path) -> List[str]:
    classes = []
    if not directory.exists():
        return classes
    for item in directory.iterdir():
        if item.is_dir():
            classes.append(item.name)
    return sorted(classes)


def count_images_in_dir(directory: Path) -> int:
    count = 0
    if not directory.exists():
        return 0
    for ext in SUPPORTED_IMAGE_EXTENSIONS:
        count += len(list(directory.rglob(f"*{ext}")))
    return count


def ingest_directory(dataset_dir: Path) -> Dict:
    report = {
        "dataset_id": dataset_dir.name,
        "dataset_path": str(dataset_dir),
        "intake_timestamp": datetime.now().isoformat(),
        "archive": None,
        "total_files": 0,
        "total_images": 0,
        "valid_images": 0,
        "corrupt_images": 0,
        "too_small_images": 0,
        "extreme_aspect_images": 0,
        "blank_images": 0,
        "unreadable_images": 0,
        "classes": {},
        "class_counts": {},
        "image_records": [],
        "duplicates_vs_core": 0,
        "duplicates_vs_figshare": 0,
        "new_unique_images": 0,
        "resolution_summary": {},
        "errors": [],
    }

    core_hashes, figshare_hashes = load_existing_hashes()

    # Check for archive
    for ext in SUPPORTED_ARCHIVE_EXTENSIONS:
        archive_path = dataset_dir / f"{dataset_dir.name}{ext}"
        if not archive_path.exists():
            for item in dataset_dir.iterdir():
                if item.is_file() and item.suffix.lower() == ext:
                    archive_path = item
                    break
        if archive_path.exists():
            report["archive"] = verify_archive(archive_path)
            if report["archive"].get("error"):
                report["errors"].append(f"Archive error: {report['archive']['error']}")
            break

    # Scan for images
    image_files = []
    for ext in SUPPORTED_IMAGE_EXTENSIONS:
        image_files.extend(dataset_dir.rglob(f"*{ext}"))

    report["total_files"] = sum(1 for _ in dataset_dir.rglob("*") if _.is_file())
    report["total_images"] = len(image_files)

    class_dirs = discover_classes(dataset_dir)
    class_counts = {cls: 0 for cls in class_dirs}
    class_images = defaultdict(list)

    resolution_buckets = defaultdict(int)
    corrupt_count = 0
    unreadable_count = 0
    too_small_count = 0
    extreme_aspect_count = 0
    blank_count = 0
    valid_count = 0
    dup_core = 0
    dup_figshare = 0
    new_unique = 0

    for img_path in image_files:
        record = {
            "path": str(img_path),
            "filename": img_path.name,
            "valid": True,
            "corrupt": False,
            "too_small": False,
            "extreme_aspect": False,
            "blank": False,
            "width": 0,
            "height": 0,
            "hash": "",
            "duplicate_vs_core": False,
            "duplicate_vs_figshare": False,
        }

        # Determine class from parent directory name
        parent_name = img_path.parent.name
        if parent_name in class_counts:
            class_counts[parent_name] += 1
            class_images[parent_name].append(img_path)

        # Validate image
        try:
            with Image.open(img_path) as img:
                img.verify()
            with Image.open(img_path) as img:
                img.load()
                width, height = img.size
                record["width"] = width
                record["height"] = height

                if width < 64 or height < 64:
                    record["too_small"] = True
                    record["valid"] = False
                    too_small_count += 1

                aspect = max(width, height) / max(min(width, height), 1)
                if aspect > 10:
                    record["extreme_aspect"] = True
                    record["valid"] = False
                    extreme_aspect_count += 1

                extrema = img.getextrema()
                if all(e[1] - e[0] < 10 for e in extrema if len(e) == 2):
                    record["blank"] = True
                    record["valid"] = False
                    blank_count += 1

                # Resolution bucket
                bucket = f"{width}x{height}"
                resolution_buckets[bucket] += 1

            # Compute hash
            sha256 = compute_sha256(img_path)
            record["hash"] = sha256

            if sha256 in core_hashes:
                record["duplicate_vs_core"] = True
                dup_core += 1
            elif sha256 in figshare_hashes:
                record["duplicate_vs_figshare"] = True
                dup_figshare += 1
            else:
                new_unique += 1

            if record["valid"]:
                valid_count += 1

        except Exception as e:
            record["corrupt"] = True
            record["valid"] = False
            record["error"] = str(e)
            corrupt_count += 1
            unreadable_count += 1

        report["image_records"].append(record)

    report["valid_images"] = valid_count
    report["corrupt_images"] = corrupt_count
    report["unreadable_images"] = unreadable_count
    report["too_small_images"] = too_small_count
    report["extreme_aspect_images"] = extreme_aspect_count
    report["blank_images"] = blank_count
    report["class_counts"] = dict(class_counts)
    report["classes"] = sorted(class_dirs)
    report["duplicates_vs_core"] = dup_core
    report["duplicates_vs_figshare"] = dup_figshare
    report["new_unique_images"] = new_unique
    report["resolution_summary"] = dict(sorted(resolution_buckets.items(), key=lambda x: -x[1]))

    return report


def print_report(report: Dict):
    print("=" * 80)
    print("DATASET INTAKE REPORT")
    print("=" * 80)
    print(f"Dataset:      {report['dataset_id']}")
    print(f"Path:         {report['dataset_path']}")
    print(f"Timestamp:    {report['intake_timestamp']}")
    print()

    if report.get("archive"):
        arch = report["archive"]
        print("--- Archive ---")
        print(f"  Path:            {arch.get('path')}")
        print(f"  Size:            {arch.get('size', 0):,} bytes")
        print(f"  Format:          {arch.get('format')}")
        print(f"  Valid:           {arch.get('valid', False)}")
        print(f"  Files in archive:{arch.get('file_count', 0):,}")
        print(f"  Images in archive:{arch.get('image_count', 0):,}")
        if arch.get("sample_files"):
            print(f"  Sample files:    {arch['sample_files'][:5]}")
        if arch.get("error"):
            print(f"  ERROR:           {arch['error']}")
        print()

    print("--- File Counts ---")
    print(f"  Total files:          {report.get('total_files', 0):,}")
    print(f"  Total images:         {report['total_images']:,}")
    print(f"  Valid images:         {report['valid_images']:,}")
    print(f"  Corrupt/unreadable:   {report['corrupt_images']:,}")
    print(f"  Too small (<64px):    {report['too_small_images']:,}")
    print(f"  Extreme aspect (>10): {report['extreme_aspect_images']:,}")
    print(f"  Blank images:         {report['blank_images']:,}")
    print()

    print("--- Duplicates ---")
    print(f"  vs Commercial core:   {report['duplicates_vs_core']:,}")
    print(f"  vs Figshare dataset:  {report['duplicates_vs_figshare']:,}")
    print(f"  New unique images:    {report['new_unique_images']:,}")
    print()

    if report.get("class_counts"):
        print("--- Class Distribution ---")
        for cls, count in sorted(report["class_counts"].items(), key=lambda x: -x[1]):
            print(f"  {cls:<30} {count:>6}")
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


def save_report(report: Dict, output_path: Optional[Path] = None, verbose: bool = True) -> Path:
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = REPORTS_DIR / f"intake_{report['dataset_id']}_{timestamp}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    if verbose:
        print(f"\nReport saved to: {output_path}")
    return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generic dataset intake tool")
    parser.add_argument("directory", type=str, help="Path to raw dataset directory")
    parser.add_argument("--output", "-o", type=str, help="Output JSON report path")
    parser.add_argument("--json", action="store_true", help="Output report as JSON")
    args = parser.parse_args()

    dataset_dir = Path(args.directory).resolve()
    if not dataset_dir.exists():
        print(f"ERROR: Directory does not exist: {dataset_dir}")
        sys.exit(1)

    if not dataset_dir.is_dir():
        print(f"ERROR: Path is not a directory: {dataset_dir}")
        sys.exit(1)

    report = ingest_directory(dataset_dir)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        save_report(report, Path(args.output) if args.output else None, verbose=False)
    else:
        print_report(report)
        save_report(report, Path(args.output) if args.output else None, verbose=True)


if __name__ == "__main__":
    main()
