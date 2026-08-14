#!/usr/bin/env python3
"""
Acquisition diagnostic and verification tool for Soil & Supper ML pipeline.

Provides a unified report answering:
  Dataset | Source | License | Download status | Archive valid? | Image count |
  Annotation/label count | Classes discovered | Taxonomy classes matched |
  Unmatched classes | Commercial-use status | Failure reason | Recommended next action

Distinguishes:
  - dataset documented
  - download attempted
  - archive downloaded
  - archive valid
  - images extracted
  - images labeled
  - images mapped to our taxonomy
  - training-ready
"""

import json
import sys
import zipfile
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

TRAINING_DIR = Path(__file__).resolve().parent
if str(TRAINING_DIR) not in sys.path:
    sys.path.insert(0, str(TRAINING_DIR))

from discover_datasets import APPROVED_DATASETS
from downloaders.shared import verify_archive, detect_known_error_page, is_html_or_error

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
RAW_DIR = TRAINING_DATA_DIR / "raw"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SUPPORTED_ARCHIVE_EXTENSIONS = {".zip", ".tar.gz", ".tgz", ".tar", ".gz"}


def load_acquisition_manifest() -> Dict[str, Dict]:
    records = {}
    manifest_path = MANIFESTS_DIR / "acquisition_manifest.jsonl"
    if not manifest_path.exists():
        return records
    with open(manifest_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                dataset_id = data.get("dataset_id")
                if dataset_id:
                    records[dataset_id] = data
            except json.JSONDecodeError:
                continue
    return records


def count_images_in_dir(directory: Path) -> int:
    count = 0
    if not directory.exists():
        return 0
    for ext in SUPPORTED_IMAGE_EXTENSIONS:
        count += len(list(directory.rglob(f"*{ext}")))
    return count


def discover_classes_in_dir(directory: Path) -> List[str]:
    classes = []
    if not directory.exists():
        return classes
    for item in directory.iterdir():
        if item.is_dir():
            classes.append(item.name)
    return sorted(classes)


def scan_archive(archive_path: Path) -> Dict:
    info = {
        "path": str(archive_path.relative_to(RAW_DIR)),
        "size": archive_path.stat().st_size,
        "format": archive_path.suffix.lower(),
        "valid": False,
        "file_count": 0,
        "image_count": 0,
        "sample_files": [],
        "is_html": False,
        "error": None,
    }

    error_type = detect_known_error_page(archive_path)
    if error_type:
        info["is_html"] = True
        info["error"] = error_type
        return info

    try:
        with open(archive_path, "rb") as f:
            header = f.read(200)
        if b"<!doctype html>" in header.lower() or b"<html" in header.lower():
            info["is_html"] = True
            info["error"] = "File is HTML, not an archive"
            return info
    except Exception as e:
        info["error"] = str(e)
        return info

    return verify_archive(archive_path)


def find_archive_for_dataset(dataset_id: str) -> Optional[Path]:
    for ext in [".zip", ".tar.gz", ".tgz", ".tar"]:
        potential = RAW_DIR / f"{dataset_id}{ext}"
        if potential.exists():
            return potential
        for item in RAW_DIR.iterdir():
            if item.is_file() and item.suffix.lower() == ext:
                if dataset_id in item.stem:
                    return item
    return None


def generate_acquisition_status_table() -> str:
    manifest = load_acquisition_manifest()

    lines = []
    lines.append("=" * 130)
    lines.append("ACQUISITION STATUS REPORT")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append("=" * 130)
    lines.append(
        f"{'Dataset':<28} {'Status':<12} {'Archive':<8} {'Valid':<6} {'Images':<8} {'Classes':<8} {'Commercial':<12} {'License'}"
    )
    lines.append("-" * 130)

    auto_count = 0
    manual_count = 0
    blocked_count = 0
    acquired_count = 0

    for dataset_id, info in sorted(APPROVED_DATASETS.items()):
        dataset_dir = RAW_DIR / dataset_id
        archive_path = find_archive_for_dataset(dataset_id)
        archive_valid = False
        image_count = 0
        classes_discovered = []

        if dataset_dir.exists():
            image_count = count_images_in_dir(dataset_dir)
            classes_discovered = discover_classes_in_dir(dataset_dir)

        record = manifest.get(dataset_id)
        if record:
            status = record.get("status", "unknown")
            if status == "downloaded":
                status = "ARCHIVE"
            elif status == "failed":
                status = "FAILED"
            elif status == "extracted":
                status = "EXTRACTED"
            elif status == "validated":
                status = "VALIDATED"
        else:
            if image_count > 0:
                status = "READY"
            elif archive_path:
                scan = scan_archive(archive_path)
                if scan.get("is_html"):
                    status = "HTML"
                elif scan.get("valid"):
                    status = "ARCHIVE"
                else:
                    status = "INVALID"
            elif dataset_dir.exists():
                status = "EMPTY"
            else:
                status = "MISSING"

        archive = "yes" if archive_path else "no"
        if archive_path:
            scan = scan_archive(archive_path)
            archive_valid = scan.get("valid", False)
            archive_error = scan.get("error")

        license_str = info.get("license", "unknown")
        commercial = "Yes" if info.get("commercial_ok") else ("No" if info.get("commercial_ok") is False else "Unknown")

        if info.get("status") == "LICENSE_BLOCKED":
            status = "BLOCKED"
            blocked_count += 1
        elif info.get("status") == "DATASET_SEARCH_REQUIRED":
            status = "SEARCH"
            manual_count += 1
        elif archive_path and archive_valid and image_count == 0:
            status = "NEEDS_EXTRACT"
            manual_count += 1
        elif image_count > 0:
            acquired_count += 1
        elif archive_path and not archive_valid:
            manual_count += 1
        elif status == "MISSING":
            manual_count += 1

        lines.append(
            f"{dataset_id:<28} {status:<12} {archive:<8} {'yes' if archive_valid else 'no':<6} {image_count:<8} {len(classes_discovered):<8} {commercial:<12} {license_str}"
        )

    lines.append("=" * 130)
    lines.append(f"Acquired datasets: {acquired_count}")
    lines.append(f"Manual action required: {manual_count}")
    lines.append(f"License blocked: {blocked_count}")
    lines.append("=" * 130)
    return "\n".join(lines)


def generate_detailed_report() -> Dict:
    manifest = load_acquisition_manifest()
    report = {
        "generated_at": datetime.now().isoformat(),
        "datasets": [],
        "summary": {
            "total_documented": 0,
            "acquired": 0,
            "archive_valid": 0,
            "images_extracted": 0,
            "labels_mapped": 0,
            "training_ready": 0,
            "manual_required": 0,
            "license_blocked": 0,
            "dataset_search_required": 0,
        },
        "recommended_actions": [],
    }

    for dataset_id, info in sorted(APPROVED_DATASETS.items()):
        dataset_dir = RAW_DIR / dataset_id
        archive_path = find_archive_for_dataset(dataset_id)
        image_count = count_images_in_dir(dataset_dir) if dataset_dir.exists() else 0
        classes_discovered = discover_classes_in_dir(dataset_dir) if dataset_dir.exists() else []

        archive_valid = False
        archive_error = None
        if archive_path:
            scan = scan_archive(archive_path)
            archive_valid = scan.get("valid", False)
            archive_error = scan.get("error")

        record = manifest.get(dataset_id)
        download_status = "not_attempted"
        if record:
            download_status = record.get("status", "not_attempted")

        dataset_status = info.get("status", "DOCUMENTED")
        if dataset_status == "LICENSE_BLOCKED":
            actual_status = "LICENSE_BLOCKED"
        elif dataset_status == "DATASET_SEARCH_REQUIRED":
            actual_status = "DATASET_SEARCH_REQUIRED"
        elif image_count > 0:
            actual_status = "READY"
        elif archive_valid:
            actual_status = "ARCHIVE_VALID"
        elif archive_path and archive_error and "HTML" in str(archive_error):
            actual_status = "HTML_ERROR"
        elif archive_path:
            actual_status = "ARCHIVE_INVALID"
        elif dataset_dir.exists():
            actual_status = "EMPTY"
        else:
            actual_status = "MISSING"

        entry = {
            "dataset_id": dataset_id,
            "name": info.get("name"),
            "documented_status": dataset_status,
            "actual_status": actual_status,
            "download_status": download_status,
            "archive_valid": archive_valid,
            "archive_error": archive_error,
            "image_count": image_count,
            "classes_discovered": classes_discovered,
            "taxonomy_classes_matched": [],
            "unmatched_classes": [],
            "commercial_ok": info.get("commercial_ok"),
            "license": info.get("license"),
            "failure_reason": record.get("error") if record else None,
            "notes": info.get("notes", ""),
        }

        if actual_status == "MISSING":
            entry["recommended_action"] = "Automatic download attempted by pipeline"
        elif actual_status == "HTML_ERROR":
            entry["recommended_action"] = "Manual download required (website blocks automated access)"
        elif actual_status == "ARCHIVE_INVALID":
            entry["recommended_action"] = "Manual download required or re-run pipeline"
        elif actual_status == "ARCHIVE_VALID":
            entry["recommended_action"] = "Run: python training/pipeline.py --step prepare"
        elif actual_status == "READY":
            entry["recommended_action"] = "Run pipeline to prepare, validate, and train"
        elif actual_status == "LICENSE_BLOCKED":
            entry["recommended_action"] = "Contact copyright holder or find alternative"
        elif actual_status == "DATASET_SEARCH_REQUIRED":
            entry["recommended_action"] = "Research alternative datasets with compatible licenses"
        else:
            entry["recommended_action"] = "Investigate"

        report["datasets"].append(entry)
        report["summary"]["total_documented"] += 1
        report["summary"][actual_status.lower().replace("-", "_")] = (
            report["summary"].get(actual_status.lower().replace("-", "_"), 0) + 1
        )
        if image_count > 0:
            report["summary"]["images_extracted"] += image_count

        if actual_status in ("MISSING", "HTML_ERROR", "ARCHIVE_INVALID", "DATASET_SEARCH_REQUIRED"):
            report["summary"]["manual_required"] += 1
            report["recommended_actions"].append(
                f"{dataset_id}: {entry['recommended_action']}"
            )
        elif actual_status == "LICENSE_BLOCKED":
            report["summary"]["license_blocked"] += 1
            report["recommended_actions"].append(
                f"{dataset_id}: {entry['recommended_action']}"
            )

    return report


def print_detailed_report():
    report = generate_detailed_report()

    print("=" * 130)
    print("DETAILED ACQUISITION REPORT")
    print("=" * 130)

    for entry in report["datasets"]:
        print(f"\nDataset: {entry['dataset_id']} — {entry['name']}")
        print(f"  Documented status: {entry['documented_status']}")
        print(f"  Actual status:     {entry['actual_status']}")
        print(f"  Download status:   {entry['download_status']}")
        print(f"  Archive valid:     {entry['archive_valid']}")
        if entry.get("archive_error"):
            print(f"  Archive error:     {entry['archive_error']}")
        print(f"  Images extracted:  {entry['image_count']}")
        print(f"  Classes discovered:{entry['classes_discovered']}")
        print(f"  Commercial OK:     {entry['commercial_ok']}")
        print(f"  License:           {entry['license']}")
        if entry.get("failure_reason"):
            print(f"  Failure reason:    {entry['failure_reason']}")
        print(f"  Action:            {entry['recommended_action']}")
        if entry.get("notes"):
            print(f"  Notes:             {entry['notes']}")

    print("\n" + "=" * 130)
    print("SUMMARY")
    print("=" * 130)
    for k, v in report["summary"].items():
        print(f"  {k}: {v}")

    if report["recommended_actions"]:
        print("\nRECOMMENDED ACTIONS:")
        for action in report["recommended_actions"]:
            print(f"  - {action}")

    print("=" * 130)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Acquisition verification tool")
    parser.add_argument("--status", action="store_true", help="Show acquisition status table")
    parser.add_argument("--scan", action="store_true", help="Full scan of raw directory")
    parser.add_argument("--detailed", action="store_true", help="Show detailed per-dataset report")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.detailed:
        report = generate_detailed_report()
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_detailed_report()
    elif args.status:
        print(generate_acquisition_status_table())
    elif args.scan:
        r = scan_raw_directory()
        if args.json:
            print(json.dumps(r, indent=2))
        else:
            print_report(r)
    else:
        print(generate_acquisition_status_table())
