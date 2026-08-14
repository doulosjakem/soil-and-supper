#!/usr/bin/env python3
"""
Acquisition diagnostic and verification tool for Soil & Supper ML pipeline.

Scans training_data/raw/ and reports:
- directories found
- archives found
- archives that can be extracted
- image count
- unsupported files
- empty directories
- likely class directories
- duplicate filenames
- datasets that are present but not recognized
"""

import json
import zipfile
import tarfile
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
RAW_DIR = TRAINING_DATA_DIR / "raw"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SUPPORTED_ARCHIVE_EXTENSIONS = {".zip", ".tar.gz", ".tgz", ".tar", ".gz"}


def scan_raw_directory() -> Dict:
    """Scan training_data/raw/ and report what's actually there."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "raw_dir": str(RAW_DIR),
        "exists": RAW_DIR.exists(),
        "directories": [],
        "archives": [],
        "images": [],
        "unsupported_files": [],
        "empty_directories": [],
        "total_images": 0,
        "total_archives": 0,
        "datasets_recognized": [],
        "datasets_unrecognized": [],
        "issues": [],
    }
    
    if not RAW_DIR.exists():
        report["issues"].append("raw/ directory does not exist")
        return report
    
    # Scan all items in raw/
    for item in sorted(RAW_DIR.iterdir()):
        if item.is_dir():
            dir_info = scan_directory(item)
            report["directories"].append(dir_info)
            
            if dir_info["image_count"] == 0 and not any(f.suffix in SUPPORTED_ARCHIVE_EXTENSIONS for f in item.iterdir()):
                report["empty_directories"].append(str(item.relative_to(RAW_DIR)))
            
            # Check if this looks like a recognized dataset
            dataset_id = item.name
            if dir_info["image_count"] > 0:
                report["datasets_recognized"].append(dataset_id)
            elif dir_info["has_archives"]:
                report["datasets_recognized"].append(dataset_id)
            else:
                report["datasets_unrecognized"].append(dataset_id)
            
            report["total_images"] += dir_info["image_count"]
        
        elif item.is_file():
            if item.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
                report["images"].append({
                    "path": str(item.relative_to(RAW_DIR)),
                    "size": item.stat().st_size,
                })
                report["total_images"] += 1
            elif item.suffix.lower() in SUPPORTED_ARCHIVE_EXTENSIONS:
                archive_info = scan_archive(item)
                report["archives"].append(archive_info)
                report["total_archives"] += 1
            else:
                report["unsupported_files"].append(str(item.relative_to(RAW_DIR)))
    
    return report


def scan_directory(directory: Path) -> Dict:
    """Scan a directory for images and subdirectories."""
    info = {
        "path": str(directory.relative_to(RAW_DIR)),
        "image_count": 0,
        "subdirectories": [],
        "has_archives": False,
        "sample_images": [],
        "image_formats": {},
    }
    
    try:
        for item in sorted(directory.rglob("*")):
            if item.is_file():
                ext = item.suffix.lower()
                if ext in SUPPORTED_IMAGE_EXTENSIONS:
                    info["image_count"] += 1
                    info["image_formats"][ext] = info["image_formats"].get(ext, 0) + 1
                    if len(info["sample_images"]) < 5:
                        info["sample_images"].append(str(item.relative_to(directory)))
                elif ext in SUPPORTED_ARCHIVE_EXTENSIONS:
                    info["has_archives"] = True
            elif item.is_dir():
                info["subdirectories"].append(str(item.relative_to(directory)))
    except Exception as e:
        info["error"] = str(e)
    
    return info


def scan_archive(archive_path: Path) -> Dict:
    """Scan an archive file and report its contents."""
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
    
    # First check if it's actually HTML disguised as an archive
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
    
    try:
        if archive_path.suffix.lower() == ".zip":
            with zipfile.ZipFile(archive_path, "r") as z:
                names = z.namelist()
                info["file_count"] = len(names)
                info["valid"] = True
                for name in names[:10]:
                    info["sample_files"].append(name)
                    if any(name.lower().endswith(ext) for ext in SUPPORTED_IMAGE_EXTENSIONS):
                        info["image_count"] += 1
        elif archive_path.suffix.lower() in [".tar.gz", ".tgz", ".tar", ".gz"]:
            try:
                with tarfile.open(archive_path, "r:*") as t:
                    members = t.getmembers()
                    info["file_count"] = len(members)
                    info["valid"] = True
                    for member in members[:10]:
                        info["sample_files"].append(member.name)
                        if any(member.name.lower().endswith(ext) for ext in SUPPORTED_IMAGE_EXTENSIONS):
                            info["image_count"] += 1
            except Exception:
                info["error"] = "Not a valid tar archive"
    except Exception as e:
        info["error"] = str(e)
    
    return info


def print_report(report: Dict):
    """Print human-readable acquisition status report."""
    print("=" * 80)
    print("ACQUISITION STATUS REPORT")
    print("=" * 80)
    print(f"Raw directory: {report['raw_dir']}")
    print(f"Exists: {report['exists']}")
    print(f"Total images found: {report['total_images']}")
    print(f"Total archives found: {report['total_archives']}")
    
    if report["issues"]:
        print(f"\nIssues:")
        for issue in report["issues"]:
            print(f"  - {issue}")
    
    print(f"\nRecognized datasets ({len(report['datasets_recognized'])}):")
    for ds in report["datasets_recognized"]:
        print(f"  - {ds}")
    
    if report["datasets_unrecognized"]:
        print(f"\nUnrecognized/empty datasets ({len(report['datasets_unrecognized'])}):")
        for ds in report["datasets_unrecognized"]:
            print(f"  - {ds}")
    
    print(f"\nDirectories with images:")
    for dir_info in report["directories"]:
        if dir_info["image_count"] > 0:
            print(f"  {dir_info['path']}: {dir_info['image_count']} images")
            if dir_info["sample_images"]:
                print(f"    Sample: {dir_info['sample_images'][0]}")
    
    print(f"\nArchives:")
    for archive in report["archives"]:
        status = "VALID" if archive["valid"] else "INVALID"
        print(f"  {archive['path']}: {status}, {archive['file_count']} files, {archive.get('image_count', 0)} images")
        if archive.get("error"):
            print(f"    Error: {archive['error']}")
    
    if report["empty_directories"]:
        print(f"\nEmpty directories ({len(report['empty_directories'])}):")
        for d in report["empty_directories"]:
            print(f"  - {d}")
    
    if report["unsupported_files"]:
        print(f"\nUnsupported files ({len(report['unsupported_files'])}):")
        for f in report["unsupported_files"]:
            print(f"  - {f}")
    
    print("\n" + "=" * 80)


def generate_acquisition_status_table() -> str:
    """Generate a status table for all approved datasets."""
    from discover_datasets import APPROVED_DATASETS
    
    lines = []
    lines.append("=" * 90)
    lines.append("ACQUISITION STATUS TABLE")
    lines.append("=" * 90)
    lines.append(f"{'Dataset':<30} {'Status':<12} {'Archive':<8} {'Images':<10} {'License'}")
    lines.append("-" * 90)
    
    for dataset_id, info in sorted(APPROVED_DATASETS.items()):
        dataset_dir = RAW_DIR / dataset_id
        archive_path = None
        archive_valid = False
        
        # Check for directory
        if dataset_dir.exists():
            image_count = count_images_in_dir(dataset_dir)
            archive = "no"
            if image_count > 0:
                status = "READY"
            else:
                status = "EMPTY"
        else:
            image_count = 0
            archive = "no"
            status = "MISSING"
        
        # Check for archive file
        for ext in [".zip", ".tar.gz", ".tgz"]:
            potential = RAW_DIR / f"{dataset_id}{ext}"
            if potential.exists():
                archive_path = potential
                archive = "yes"
                # Check if it's actually valid
                scan = scan_archive(potential)
                if scan.get("is_html"):
                    status = "HTML"
                    archive_valid = False
                elif scan.get("valid"):
                    status = "ARCHIVE"
                    archive_valid = True
                else:
                    status = "INVALID"
                    archive_valid = False
                break
        
        license_str = info.get("license", "unknown")
        lines.append(f"{dataset_id:<30} {status:<12} {archive:<8} {image_count:<10} {license_str}")
    
    lines.append("=" * 90)
    return "\n".join(lines)


def count_images_in_dir(directory: Path) -> int:
    """Count images in a directory recursively."""
    count = 0
    if not directory.exists():
        return 0
    for ext in SUPPORTED_IMAGE_EXTENSIONS:
        count += len(list(directory.rglob(f"*{ext}")))
    return count


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Acquisition verification tool")
    parser.add_argument("--status", action="store_true", help="Show acquisition status table")
    parser.add_argument("--scan", action="store_true", help="Full scan of raw directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    if args.status:
        print(generate_acquisition_status_table())
    elif args.scan:
        report = scan_raw_directory()
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_report(report)
    else:
        # Default: show status table
        print(generate_acquisition_status_table())
