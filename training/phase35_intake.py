#!/usr/bin/env python3
"""
Phase 35 — Crop dataset intake and commercial-readiness pipeline.

Processes manually downloaded Priority 1 crop datasets:
  - bangladesh_veg
  - smartphone_veg
  - vegnet
  - banglaveg
  - early_stage_crops

For each dataset:
  1. Verify archive/file is real data (not HTML/login placeholder)
  2. Verify source identity
  3. Verify license/provenance
  4. Extract safely
  5. Inventory every image
  6. Map source labels to Soil & Supper taxonomy
  7. Reject unsupported/ambiguous labels
  8. Detect corrupt/unreadable images
  9. Detect exact duplicates
  10. Identify near-duplicates where practical
  11. Record provenance
  12. Produce per-class counts

Outputs:
  - training_data/manifests/phase35_intake_manifest.jsonl
  - training_data/reports/phase35_intake_report.json
  - training_data/manifests/phase35_commercial_ready.jsonl
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

PRIORITY_1_DATASETS = [
    {
        "dataset_id": "bangladesh_veg",
        "name": "Bangladesh Comprehensive Vegetables",
        "source": "Mendeley Data",
        "url": "https://data.mendeley.com/datasets/rtx9ngb68j",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "class_mappings": {
            "Tomato": "Tomato",
            "Capsicum": "Pepper",
            "Cucumber": "Cucumber",
            "Brinjal": "Eggplant",
            "Broccoli": "Broccoli",
            "Cabbage": "Cabbage",
            "Carrot": "Carrot",
            "Onion": "Onion",
            "Potato": "Potato",
            "Pumpkin": "Winter Squash / Pumpkin",
            "Radish": "Radish",
            "Zucchini": "Summer Squash / Zucchini",
            "Flat Bean": "Bean",
        },
    },
    {
        "dataset_id": "smartphone_veg",
        "name": "Smartphone Vegetable Detection",
        "source": "Mendeley Data",
        "url": "https://data.mendeley.com/datasets/gnc4s3z2mf/3",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "class_mappings": {
            "Tomato": "Tomato",
            "Capsicum": "Pepper",
            "Cucumber": "Cucumber",
            "Eggplant": "Eggplant",
            "Potato": "Potato",
            "Pumpkin": "Winter Squash / Pumpkin",
            "Radish": "Radish",
            "Green Bean": "Bean",
            "Carrot": "Carrot",
            "Onion": "Onion",
        },
    },
    {
        "dataset_id": "vegnet",
        "name": "VegNet Vegetable Quality Dataset",
        "source": "Mendeley Data",
        "url": "https://data.mendeley.com/datasets/6nxnjbn9w6",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "class_mappings": {
            "Bell Pepper": "Pepper",
            "Tomato": "Tomato",
            "Chili Pepper": "Pepper",
            "New Mexico Chile": "Pepper",
        },
    },
    {
        "dataset_id": "banglaveg",
        "name": "BanglaVeg",
        "source": "ScienceDirect / Mendeley",
        "url": "https://www.sciencedirect.com/science/article/pii/S2352340925001738",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "class_mappings": {
            "Tomato": "Tomato",
            "Capsicum": "Pepper",
            "Cucumber": "Cucumber",
            "Eggplant": "Eggplant",
            "Potato": "Potato",
            "Onion": "Onion",
            "Radish": "Radish",
            "Bean": "Bean",
            "Chilli": "Pepper",
        },
    },
    {
        "dataset_id": "early_stage_crops",
        "name": "Early-Stage Vegetable Crops",
        "source": "PMC / PubMed Central",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "class_mappings": {
            "Maize": "Corn",
            "Bean": "Bean",
            "Leek": "Leek",
        },
    },
]


def compute_sha256(file_path: Path, chunk_size: int = 65536) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


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
                info["image_count"] = sum(
                    1 for n in namelist if Path(n).suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
                )
        elif archive_path.suffix.lower() in {".tar.gz", ".tgz", ".tar"}:
            with tarfile.open(archive_path, "r:*") as tf:
                namelist = tf.getnames()
                info["file_count"] = len(namelist)
                info["valid"] = True
                info["sample_files"] = namelist[:10]
                info["image_count"] = sum(
                    1 for n in namelist if Path(n).suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
                )
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


def ingest_dataset(dataset_info: Dict) -> Dict:
    dataset_id = dataset_info["dataset_id"]
    dataset_dir = RAW_DIR / dataset_id

    report = {
        "dataset_id": dataset_id,
        "name": dataset_info["name"],
        "source": dataset_info["source"],
        "url": dataset_info["url"],
        "license": dataset_info["license"],
        "commercial_ok": dataset_info["commercial_ok"],
        "ingest_timestamp": datetime.now().isoformat(),
        "dataset_path": str(dataset_dir),
        "archive": None,
        "total_files": 0,
        "total_images": 0,
        "valid_images": 0,
        "corrupt_images": 0,
        "too_small_images": 0,
        "extreme_aspect_images": 0,
        "blank_images": 0,
        "unreadable_images": 0,
        "classes_discovered": [],
        "class_counts": {},
        "mapped_class_counts": {},
        "unmapped_classes": [],
        "image_records": [],
        "duplicates_vs_core": 0,
        "duplicates_vs_figshare": 0,
        "new_unique_images": 0,
        "resolution_summary": {},
        "errors": [],
        "status": "MISSING",
    }

    if not dataset_dir.exists():
        report["errors"].append(f"Dataset directory does not exist: {dataset_dir}")
        return report

    # Check for archive
    for ext in SUPPORTED_ARCHIVE_EXTENSIONS:
        archive_path = dataset_dir / f"{dataset_id}{ext}"
        if not archive_path.exists():
            for item in dataset_dir.iterdir():
                if item.is_file() and item.suffix.lower() == ext:
                    archive_path = item
                    break
        if archive_path.exists():
            archive_info = verify_archive(archive_path)
            report["archive"] = archive_info
            if archive_info.get("error"):
                report["errors"].append(f"Archive error: {archive_info['error']}")
                report["status"] = "ARCHIVE_INVALID"
            elif archive_info.get("valid"):
                report["status"] = "ARCHIVE_VALID"
            break

    # Discover classes
    class_dirs = []
    for item in dataset_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            class_dirs.append(item.name)
    report["classes_discovered"] = sorted(class_dirs)

    # Map classes
    class_mappings = dataset_info.get("class_mappings", {})
    mapped_counts = defaultdict(int)
    unmapped = []

    for cls in class_dirs:
        if cls in class_mappings:
            mapped_counts[class_mappings[cls]] += 1
        else:
            unmapped.append(cls)

    report["class_counts"] = {cls: 0 for cls in class_dirs}
    report["mapped_class_counts"] = dict(mapped_counts)
    report["unmapped_classes"] = sorted(unmapped)

    # Scan images
    image_files = []
    for ext in SUPPORTED_IMAGE_EXTENSIONS:
        image_files.extend(dataset_dir.rglob(f"*{ext}"))

    report["total_files"] = sum(1 for _ in dataset_dir.rglob("*") if _.is_file())
    report["total_images"] = len(image_files)

    if report["total_images"] > 0:
        report["status"] = "READY"

    core_hashes, figshare_hashes = load_existing_hashes()

    corrupt_count = 0
    too_small_count = 0
    extreme_aspect_count = 0
    blank_count = 0
    valid_count = 0
    dup_core = 0
    dup_figshare = 0
    new_unique = 0

    resolution_buckets = defaultdict(int)

    for img_path in image_files:
        record = {
            "path": str(img_path),
            "filename": img_path.name,
            "dataset_id": dataset_id,
            "source_class": img_path.parent.name,
            "target_class": class_mappings.get(img_path.parent.name, "UNMAPPED"),
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
            "commercial_ready": False,
        }

        # Count by source class
        if img_path.parent.name in report["class_counts"]:
            report["class_counts"][img_path.parent.name] += 1

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

                bucket = f"{width}x{height}"
                resolution_buckets[bucket] += 1

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
                if record["target_class"] != "UNMAPPED":
                    record["commercial_ready"] = True

        except Exception as e:
            record["corrupt"] = True
            record["valid"] = False
            record["error"] = str(e)
            corrupt_count += 1

        report["image_records"].append(record)

    report["valid_images"] = valid_count
    report["corrupt_images"] = corrupt_count
    report["too_small_images"] = too_small_count
    report["extreme_aspect_images"] = extreme_aspect_count
    report["blank_images"] = blank_count
    report["duplicates_vs_core"] = dup_core
    report["duplicates_vs_figshare"] = dup_figshare
    report["new_unique_images"] = new_unique
    report["resolution_summary"] = dict(sorted(resolution_buckets.items(), key=lambda x: -x[1]))

    return report


def print_report(report: Dict):
    print("=" * 80)
    print(f"DATASET INTAKE REPORT: {report['name']}")
    print("=" * 80)
    print(f"Dataset ID:      {report['dataset_id']}")
    print(f"Source:          {report['source']}")
    print(f"URL:             {report['url']}")
    print(f"License:         {report['license']}")
    print(f"Commercial OK:   {report['commercial_ok']}")
    print(f"Status:          {report['status']}")
    print(f"Path:            {report['dataset_path']}")
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
    print(f"  Total images:         {report.get('total_images', 0):,}")
    print(f"  Valid images:         {report.get('valid_images', 0):,}")
    print(f"  Corrupt/unreadable:   {report.get('corrupt_images', 0):,}")
    print(f"  Too small (<64px):    {report.get('too_small_images', 0):,}")
    print(f"  Extreme aspect (>10): {report.get('extreme_aspect_images', 0):,}")
    print(f"  Blank images:         {report.get('blank_images', 0):,}")
    print()

    print("--- Duplicates ---")
    print(f"  vs Commercial core:   {report.get('duplicates_vs_core', 0):,}")
    print(f"  vs Figshare dataset:  {report.get('duplicates_vs_figshare', 0):,}")
    print(f"  New unique images:    {report.get('new_unique_images', 0):,}")
    print()

    if report.get("classes_discovered"):
        print("--- Classes Discovered ---")
        for cls in report["classes_discovered"]:
            count = report.get("class_counts", {}).get(cls, 0)
            mapped = report.get("mapped_class_counts", {})
            target = [k for k, v in mapped.items() if v > 0 and cls in report.get("class_mappings", {}).get(cls, "")]
            print(f"  {cls:<30} {count:>6} images")
        print()

    if report.get("unmapped_classes"):
        print("--- Unmapped Classes (REVIEW) ---")
        for cls in report["unmapped_classes"]:
            print(f"  {cls}")
        print()

    if report.get("mapped_class_counts"):
        print("--- Mapped to Soil & Supper Classes ---")
        for cls, count in sorted(report["mapped_class_counts"].items(), key=lambda x: -x[1]):
            print(f"  {cls:<30} {count:>6} images")
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


def save_report(report: Dict, output_path: Optional[Path] = None) -> Path:
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = REPORTS_DIR / f"phase35_intake_{report['dataset_id']}_{timestamp}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Report saved to: {output_path}")
    return output_path




def generate_gap_report(approved, review, rejected, not_yet):
    class_sources = defaultdict(set)
    for entry in approved:
        for cls in entry.get("mapped_class_counts", {}).keys():
            class_sources[cls].add(entry.get("dataset_id"))

    tier1_gaps = []
    for cls in TIER1_CLASSES:
        if cls not in class_sources or len(class_sources[cls]) == 0:
            tier1_gaps.append(cls)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "approved": len(approved),
            "review": len(review),
            "rejected": len(rejected),
            "not_yet_received": len(not_yet),
            "tier1_classes_with_data": len([cls for cls in TIER1_CLASSES if cls in class_sources and len(class_sources[cls]) > 0]),
            "tier1_classes_without_data": len(tier1_gaps),
        },
        "approved_datasets": [{"dataset_id": e.get("dataset_id"), "status": e.get("status"), "approved_images": e.get("approved_images", 0)} for e in approved],
        "review_datasets": [{"dataset_id": e.get("dataset_id"), "status": "REVIEW", "reason": e.get("notes", "")} for e in review],
        "rejected_datasets": [{"dataset_id": e.get("dataset_id"), "status": "REJECTED", "errors": e.get("errors", [])} for e in rejected],
        "not_yet_received": [{"dataset_id": e.get("dataset_id"), "status": "NOT_YET_RECEIVED"} for e in not_yet],
        "tier1_gaps": tier1_gaps,
    }


def write_acquisition_report(ledger_entries: List[Dict], gap_report: Dict):
    lines = []
    lines.append("# Soil & Supper — Phase 35 Acquisition Report")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"**Phase**: 35 — Incremental Dataset Intake")
    lines.append(f"**Status**: OPEN — acquisition ongoing")
    lines.append("")
    lines.append("## 1. Dataset Status")
    lines.append("")
    lines.append("| Dataset ID | Status | Approved Images | Notes |")
    lines.append("|------------|--------|-----------------|-------|")

    for entry in ledger_entries:
        status = entry.get("status", "UNKNOWN")
        ds_id = entry.get("dataset_id", "unknown")
        approved = entry.get("approved_images", 0)
        notes = entry.get("notes", "")
        if status in ("APPROVED", "APPROVED_WITH_ATTRIBUTION"):
            lines.append(f"| {ds_id} | {status} | {approved:,} | {notes} |")
        elif status == "NOT_YET_RECEIVED":
            lines.append(f"| {ds_id} | {status} | 0 | Awaiting human download |")
        elif status == "REVIEW":
            lines.append(f"| {ds_id} | {status} | 0 | {notes} |")
        elif status == "REJECTED":
            lines.append(f"| {ds_id} | {status} | 0 | {entry.get('errors', [''])[0]} |")
        else:
            lines.append(f"| {ds_id} | {status} | 0 | |")

    lines.append("")
    lines.append("## 2. Tier 1 Class Coverage")
    lines.append("")
    lines.append("| Class | Approved Images | Source Datasets | Status |")
    lines.append("|-------|-----------------|-----------------|--------|")

    coverage = generate_class_coverage(ledger_entries)
    for cls in TIER1_CLASSES:
        info = coverage["classes"].get(cls, {})
        approved = info.get("approved_images", 0)
        sources = info.get("source_dataset_count", 0)
        status = info.get("status", "NO_DATA")
        lines.append(f"| {cls} | {approved:,} | {sources} | {status} |")

    lines.append("")
    lines.append("## 3. Gap Summary")
    lines.append("")
    summary = gap_report.get("summary", {})
    lines.append(f"- **Approved datasets**: {summary.get('approved', 0)}")
    lines.append(f"- **Review datasets**: {summary.get('review', 0)}")
    lines.append(f"- **Rejected datasets**: {summary.get('rejected', 0)}")
    lines.append(f"- **Not yet received**: {summary.get('not_yet_received', 0)}")
    lines.append(f"- **Tier 1 classes with data**: {summary.get('tier1_classes_with_data', 0)} / {len(TIER1_CLASSES)}")
    lines.append(f"- **Tier 1 classes without data**: {summary.get('tier1_classes_without_data', 0)}")
    lines.append("")

    if gap_report.get("tier1_gaps"):
        lines.append("### Classes Without Commercial Data")
        lines.append("")
        for cls in gap_report["tier1_gaps"]:
            lines.append(f"- {cls}")
        lines.append("")

    lines.append("## 4. Next Steps")
    lines.append("")
    lines.append("1. Human downloads datasets listed as NOT_YET_RECEIVED into inputs/")
    lines.append("2. Rerun: `python training/phase35_intake.py --all`")
    links = [
        ("Bangladesh Comprehensive Vegetables", "https://data.mendeley.com/datasets/rtx9ngb68j", "CC BY 4.0"),
        ("Smartphone Vegetable Detection", "https://data.mendeley.com/datasets/gnc4s3z2mf/3", "CC BY 4.0"),
        ("VegNet", "https://data.mendeley.com/datasets/6nxnjbn9w6", "CC BY 4.0"),
        ("BanglaVeg", "https://doi.org/10.1016/j.dcha.2025.100058", "CC BY 4.0"),
        ("Early-Stage Crops", "https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/", "CC BY 4.0"),
        ("Vegetables (images.cv)", "https://images.cv/dataset/vegetables-image-classification-dataset", "CC0 claimed"),
        ("Fruit and Vegetables (Kaggle)", "https://www.kaggle.com/datasets/youssefsalahzakria/fruit-and-vegetables-classification", "CC0 claimed"),
        ("Herbs (images.cv)", "https://images.cv/dataset/herbs-image-classification-dataset", "CC0 claimed"),
    ]
    for name, url, license in links:
        lines.append(f"- [{name}]({url}) — {license}")
    lines.append("")
    lines.append("---")
    lines.append("*Phase 35 remains open until acquisition is complete.*")
    lines.append("*Do not train crop model yet.*")

    ACQUISITION_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Acquisition report written to: {ACQUISITION_REPORT}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Phase 35 incremental dataset intake")
    parser.add_argument("--all", action="store_true", help="Scan inputs/ and process all candidates")
    parser.add_argument("--dataset", type=str, help="Process specific dataset path under inputs/")
    parser.add_argument("--json", action="store_true", help="Emit JSON reports")
    args = parser.parse_args()

    ledger = load_ledger()
    existing_hashes = load_existing_hashes()

    if args.dataset:
        candidate = Path(args.dataset)
        if not candidate.exists():
            print(f"ERROR: {candidate} does not exist")
            sys.exit(1)
        report = ingest_candidate(candidate, existing_hashes, ledger)
        print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else str(report))
        save_ledger_entry(report)
        if report.get("image_records"):
            append_image_manifest(report["image_records"], report.get("license"), report.get("attribution_required", False), report.get("attribution_text", ""))
        return

    if not args.all:
        parser.print_help()
        sys.exit(1)

    all_reports = []
    candidates = []

    if INPUTS_DIR.exists():
        for item in sorted(INPUTS_DIR.iterdir()):
            if item.name.startswith("."):
                continue
            candidates.append(item)

    for ds in PLANNED_DATASETS:
        found = False
        for c in candidates:
            if identify_dataset(c) and identify_dataset(c).get("dataset_id") == ds["dataset_id"]:
                found = True
                break
        if not found:
            not_yet_entry = {
                "dataset_id": ds["dataset_id"],
                "status": "NOT_YET_RECEIVED",
                "discovered_at": datetime.now(timezone.utc).isoformat(),
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "fingerprint": f"planned-{ds['dataset_id']}",
                "source_url": ds.get("url"),
                "license": ds.get("license"),
                "commercial_ok": ds.get("commercial_ok", False),
                "attribution_required": ds.get("attribution_required", False),
                "attribution_text": ds.get("attribution_text", ""),
                "total_images": 0,
                "valid_images": 0,
                "approved_images": 0,
                "rejected_images": 0,
                "classes_discovered": [],
                "class_counts": {},
                "mapped_class_counts": {},
                "unmapped_classes": [],
                "duplicates_vs_corpus": 0,
                "new_unique_images": 0,
                "image_records": [],
                "errors": [],
                "notes": "Planned but not yet present in inputs/",
            }
            if not find_ledger_entry(ledger, not_yet_entry["fingerprint"]):
                all_reports.append(not_yet_entry)
                save_ledger_entry(not_yet_entry)

    for candidate in candidates:
        report = ingest_candidate(candidate, existing_hashes, ledger)
        all_reports.append(report)
        save_ledger_entry(report)
        if report.get("image_records"):
            append_image_manifest(report["image_records"], report.get("license"), report.get("attribution_required", False), report.get("attribution_text", ""))

    gap = generate_gap_report(all_reports)
    with open(GAP_REPORT, "w", encoding="utf-8") as f:
        json.dump(gap, f, indent=2, ensure_ascii=False)

    coverage = generate_class_coverage(all_reports)
    with open(CLASS_COVERAGE, "w", encoding="utf-8") as f:
        json.dump(coverage, f, indent=2, ensure_ascii=False)

    write_acquisition_report(all_reports, gap)

    print("\n" + "=" * 80)
    print("PHASE 35 INTAKE SUMMARY")
    print("=" * 80)
    print(f"Datasets processed: {len(all_reports)}")
    print(f"Total images discovered: {sum(r.get('total_images', 0) for r in all_reports):,}")
    print(f"Total valid images: {sum(r.get('valid_images', 0) for r in all_reports):,}")
    print(f"Total approved images: {sum(r.get('approved_images', 0) for r in all_reports):,}")
    print()
    for r in all_reports:
        print(f"  {r.get('dataset_id', 'unknown'):<30} {r.get('status', 'UNKNOWN'):<25} {r.get('total_images', 0):>8} images  {r.get('approved_images', 0):>8} approved")
    print("=" * 80)


if __name__ == "__main__":
    main()

    rejected = [e for e in ledger_entries if e.get("status") == "REJECTED"]
    not_yet = [e for e in ledger_entries if e.get("status") == "NOT_YET_RECEIVED"]

    class_sources = defaultdict(set)
    for entry in approved:
        for cls in entry.get("mapped_class_counts", {}).keys():
            class_sources[cls].add(entry.get("dataset_id"))

    tier1_gaps = []
    for cls in TIER1_CLASSES:
        if cls not in class_sources or len(class_sources[cls]) == 0:
            tier1_gaps.append(cls)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "approved": len(approved),
            "review": len(review),
            "rejected": len(rejected),
            "not_yet_received": len(not_yet),
            "tier1_classes_with_data": len([cls for cls in TIER1_CLASSES if cls in class_sources and len(class_sources[cls]) > 0]),
            "tier1_classes_without_data": len(tier1_gaps),
        },
        "approved_datasets": [{"dataset_id": e.get("dataset_id"), "status": e.get("status"), "approved_images": e.get("approved_images", 0)} for e in approved],
        "review_datasets": [{"dataset_id": e.get("dataset_id"), "status": "REVIEW", "reason": e.get("notes", "")} for e in review],
        "rejected_datasets": [{"dataset_id": e.get("dataset_id"), "status": "REJECTED", "errors": e.get("errors", [])} for e in rejected],
        "not_yet_received": [{"dataset_id": e.get("dataset_id"), "status": "NOT_YET_RECEIVED"} for e in not_yet],
        "tier1_gaps": tier1_gaps,
    }


def write_acquisition_report(ledger_entries: List[Dict], gap_report: Dict):
    lines = []
    lines.append("# Soil & Supper — Phase 35 Acquisition Report")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"**Phase**: 35 — Incremental Dataset Intake")
    lines.append(f"**Status**: OPEN — acquisition ongoing")
    lines.append("")
    lines.append("## 1. Dataset Status")
    lines.append("")
    lines.append("| Dataset ID | Status | Approved Images | Notes |")
    lines.append("|------------|--------|-----------------|-------|")

    for entry in ledger_entries:
        status = entry.get("status", "UNKNOWN")
        ds_id = entry.get("dataset_id", "unknown")
        approved = entry.get("approved_images", 0)
        notes = entry.get("notes", "")
        if status in ("APPROVED", "APPROVED_WITH_ATTRIBUTION"):
            lines.append(f"| {ds_id} | {status} | {approved:,} | {notes} |")
        elif status == "NOT_YET_RECEIVED":
            lines.append(f"| {ds_id} | {status} | 0 | Awaiting human download |")
        elif status == "REVIEW":
            lines.append(f"| {ds_id} | {status} | 0 | {notes} |")
        elif status == "REJECTED":
            lines.append(f"| {ds_id} | {status} | 0 | {entry.get('errors', [''])[0]} |")
        else:
            lines.append(f"| {ds_id} | {status} | 0 | |")

    lines.append("")
    lines.append("## 2. Tier 1 Class Coverage")
    lines.append("")
    lines.append("| Class | Approved Images | Source Datasets | Status |")
    lines.append("|-------|-----------------|-----------------|--------|")

    coverage = generate_class_coverage(ledger_entries)
    for cls in TIER1_CLASSES:
        info = coverage["classes"].get(cls, {})
        approved = info.get("approved_images", 0)
        sources = info.get("source_dataset_count", 0)
        status = info.get("status", "NO_DATA")
        lines.append(f"| {cls} | {approved:,} | {sources} | {status} |")

    lines.append("")
    lines.append("## 3. Gap Summary")
    lines.append("")
    summary = gap_report.get("summary", {})
    lines.append(f"- **Approved datasets**: {summary.get('approved', 0)}")
    lines.append(f"- **Review datasets**: {summary.get('review', 0)}")
    lines.append(f"- **Rejected datasets**: {summary.get('rejected', 0)}")
    lines.append(f"- **Not yet received**: {summary.get('not_yet_received', 0)}")
    lines.append(f"- **Tier 1 classes with data**: {summary.get('tier1_classes_with_data', 0)} / {len(TIER1_CLASSES)}")
    lines.append(f"- **Tier 1 classes without data**: {summary.get('tier1_classes_without_data', 0)}")
    lines.append("")

    if gap_report.get("tier1_gaps"):
        lines.append("### Classes Without Commercial Data")
        lines.append("")
        for cls in gap_report["tier1_gaps"]:
            lines.append(f"- {cls}")
        lines.append("")

    lines.append("## 4. Next Steps")
    lines.append("")
    lines.append("1. Human downloads datasets listed as NOT_YET_RECEIVED into inputs/")
    lines.append("2. Rerun: `python training/phase35_intake.py --all`")
    lines.append("")
    links = [
        ("Bangladesh Comprehensive Vegetables", "https://data.mendeley.com/datasets/rtx9ngb68j", "CC BY 4.0"),
        ("Smartphone Vegetable Detection", "https://data.mendeley.com/datasets/gnc4s3z2mf/3", "CC BY 4.0"),
        ("VegNet", "https://data.mendeley.com/datasets/6nxnjbn9w6", "CC BY 4.0"),
        ("BanglaVeg", "https://doi.org/10.1016/j.dcha.2025.100058", "CC BY 4.0"),
        ("Early-Stage Crops", "https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/", "CC BY 4.0"),
        ("Vegetables (images.cv)", "https://images.cv/dataset/vegetables-image-classification-dataset", "CC0 claimed"),
        ("Fruit and Vegetables (Kaggle)", "https://www.kaggle.com/datasets/youssefsalahzakria/fruit-and-vegetables-classification", "CC0 claimed"),
        ("Herbs (images.cv)", "https://images.cv/dataset/herbs-image-classification-dataset", "CC0 claimed"),
    ]
    for name, url, license in links:
        lines.append(f"- [{name}]({url}) — {license}")
    lines.append("")
    lines.append("---")
    lines.append("*Phase 35 remains open until acquisition is complete.*")
    lines.append("*Do not train crop model yet.*")

    ACQUISITION_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Acquisition report written to: {ACQUISITION_REPORT}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Phase 35 incremental dataset intake")
    parser.add_argument("--all", action="store_true", help="Scan inputs/ and process all candidates")
    parser.add_argument("--dataset", type=str, help="Process specific dataset path under inputs/")
    parser.add_argument("--json", action="store_true", help="Emit JSON reports")
    args = parser.parse_args()

    ledger = load_ledger()
    existing_hashes = load_existing_hashes()

    if args.dataset:
        candidate = Path(args.dataset)
        if not candidate.exists():
            print(f"ERROR: {candidate} does not exist")
            sys.exit(1)
        report = ingest_candidate(candidate, existing_hashes, ledger)
        print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else str(report))
        save_ledger_entry(report)
        if report.get("image_records"):
            append_image_manifest(report["image_records"], report.get("license"), report.get("attribution_required", False), report.get("attribution_text", ""))
        return

    if not args.all:
        parser.print_help()
        sys.exit(1)

    all_reports = []
    candidates = []

    if INPUTS_DIR.exists():
        for item in sorted(INPUTS_DIR.iterdir()):
            if item.name.startswith("."):
                continue
            candidates.append(item)

    for ds in PLANNED_DATASETS:
        found = False
        for c in candidates:
            if identify_dataset(c) and identify_dataset(c).get("dataset_id") == ds["dataset_id"]:
                found = True
                break
        if not found:
            not_yet_entry = {
                "dataset_id": ds["dataset_id"],
                "status": "NOT_YET_RECEIVED",
                "discovered_at": datetime.now(timezone.utc).isoformat(),
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "fingerprint": f"planned-{ds['dataset_id']}",
                "source_url": ds.get("url"),
                "license": ds.get("license"),
                "commercial_ok": ds.get("commercial_ok", False),
                "attribution_required": ds.get("attribution_required", False),
                "attribution_text": ds.get("attribution_text", ""),
                "total_images": 0,
                "valid_images": 0,
                "approved_images": 0,
                "rejected_images": 0,
                "classes_discovered": [],
                "class_counts": {},
                "mapped_class_counts": {},
                "unmapped_classes": [],
                "duplicates_vs_corpus": 0,
                "new_unique_images": 0,
                "image_records": [],
                "errors": [],
                "notes": "Planned but not yet present in inputs/",
            }
            if not find_ledger_entry(ledger, not_yet_entry["fingerprint"]):
                all_reports.append(not_yet_entry)
                save_ledger_entry(not_yet_entry)

    for candidate in candidates:
        report = ingest_candidate(candidate, existing_hashes, ledger)
        all_reports.append(report)
        save_ledger_entry(report)
        if report.get("image_records"):
            append_image_manifest(report["image_records"], report.get("license"), report.get("attribution_required", False), report.get("attribution_text", ""))

    gap = generate_gap_report(all_reports)
    with open(GAP_REPORT, "w", encoding="utf-8") as f:
        json.dump(gap, f, indent=2, ensure_ascii=False)

    coverage = generate_class_coverage(all_reports)
    with open(CLASS_COVERAGE, "w", encoding="utf-8") as f:
        json.dump(coverage, f, indent=2, ensure_ascii=False)

    write_acquisition_report(all_reports, gap)

    print("\n" + "=" * 80)
    print("PHASE 35 INTAKE SUMMARY")
    print("=" * 80)
    print(f"Datasets processed: {len(all_reports)}")
    print(f"Total images discovered: {sum(r.get('total_images', 0) for r in all_reports):,}")
    print(f"Total valid images: {sum(r.get('valid_images', 0) for r in all_reports):,}")
    print(f"Total approved images: {sum(r.get('approved_images', 0) for r in all_reports):,}")
    print()
    for r in all_reports:
        print(f"  {r.get('dataset_id', 'unknown'):<30} {r.get('status', 'UNKNOWN'):<25} {r.get('total_images', 0):>8} images  {r.get('approved_images', 0):>8} approved")
    print("=" * 80)


if __name__ == "__main__":
    main()

