#!/usr/bin/env python3
"""
Provenance and manifest generation for Soil & Supper ML pipeline.
Records complete metadata for every image.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from PIL import Image

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
REPORTS_DIR = TRAINING_DATA_DIR / "reports"
PROCESSED_DIR = TRAINING_DATA_DIR / "processed"

MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def compute_phash(image_path: Path, hash_size: int = 8) -> str:
    """Compute perceptual hash."""
    try:
        import imagehash
        with Image.open(image_path) as img:
            return str(imagehash.phash(img, hash_size=hash_size))
    except Exception:
        return ""


def compute_sha256(image_path: Path) -> str:
    """Compute SHA256 hash."""
    h = hashlib.sha256()
    with open(image_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def generate_image_manifest(image_path: Path, source_dataset: str, source_image_id: str, 
                           source_url: str, class_name: str, domain: str, 
                           license_type: str, license_url: str, attribution_required: bool,
                           attribution_text: str = "") -> Dict:
    """Generate manifest entry for a single image."""
    rel_path = image_path.relative_to(TRAINING_DATA_DIR)
    
    return {
        "image_id": f"{source_dataset}_{source_image_id}",
        "local_path": str(rel_path),
        "source_dataset": source_dataset,
        "source_image_id": source_image_id,
        "source_url": source_url,
        "class": class_name,
        "domain": domain,
        "license": license_type,
        "license_url": license_url,
        "attribution_required": attribution_required,
        "attribution_text": attribution_text,
        "verification_date": datetime.now().isoformat(),
        "hash": compute_sha256(image_path),
        "phash": compute_phash(image_path),
        "split": "unknown",
    }


def generate_provenance_report() -> Dict:
    """Generate full provenance report."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "total_images": 0,
        "by_domain": {},
        "by_class": {},
        "by_source": {},
        "split_distribution": {"train": 0, "val": 0, "test": 0, "unknown": 0},
    }
    
    if not PROCESSED_DIR.exists():
        return report
    
    for domain_dir in PROCESSED_DIR.iterdir():
        if not domain_dir.is_dir():
            continue
        domain = domain_dir.name
        report["by_domain"][domain] = {"count": 0, "classes": {}}
        
        for class_dir in domain_dir.iterdir():
            if not class_dir.is_dir():
                continue
            class_name = class_dir.name
            images = list(class_dir.rglob("*.jpg")) + list(class_dir.rglob("*.jpeg")) + list(class_dir.rglob("*.png")) + list(class_dir.rglob("*.webp"))
            count = len(images)
            report["by_domain"][domain]["classes"][class_name] = count
            report["by_domain"][domain]["count"] += count
            report["by_class"][class_name] = report["by_class"].get(class_name, 0) + count
            report["total_images"] += count
    
    return report


if __name__ == "__main__":
    report = generate_provenance_report()
    report_path = REPORTS_DIR / "provenance_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Saved provenance report: {report_path}")
    print(f"Total images: {report['total_images']}")
    for domain, data in report["by_domain"].items():
        print(f"  {domain}: {data['count']} images")
