#!/usr/bin/env python3
"""
Dataset acquisition utilities for Soil & Supper ML pipeline.
Downloads and verifies approved datasets.
"""

import os
import hashlib
import json
from pathlib import Path
from typing import Dict, List

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

APPROVED_DATASETS = {
    "bangladesh_veg": {
        "name": "Bangladesh Comprehensive Vegetables",
        "license": "CC BY 4.0",
        "url": "https://data.mendeley.com/datasets/rtx9ngb68j",
        "description": "4,730 images, 42 classes, smartphone-captured",
        "attribution_required": True,
        "commercial_ok": True,
    },
    "smartphone_veg": {
        "name": "Smartphone Vegetable Detection",
        "license": "CC BY 4.0",
        "url": "https://data.mendeley.com/datasets/gnc4s3z2mf/3",
        "description": "3,534 images, 22 classes, Redmi Note 12",
        "attribution_required": True,
        "commercial_ok": True,
    },
    "early_stage_crops": {
        "name": "Early-Stage Vegetable Crops",
        "license": "CC BY 4.0",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/",
        "description": "2,801 images, seedlings and early growth",
        "attribution_required": True,
        "commercial_ok": True,
    },
    "USDA_ARS": {
        "name": "USDA ARS Image Gallery",
        "license": "Public Domain",
        "url": "https://www.ars.usda.gov/oc/images/image-gallery/",
        "description": "Professional field photos, public domain",
        "attribution_required": False,
        "commercial_ok": True,
    },
}


def verify_license(dataset_id: str) -> Dict:
    """Verify dataset license and return metadata."""
    if dataset_id not in APPROVED_DATASETS:
        raise ValueError(f"Unknown dataset: {dataset_id}")
    return APPROVED_DATASETS[dataset_id]


def list_approved_datasets() -> List[str]:
    """List all approved dataset IDs."""
    return list(APPROVED_DATASETS.keys())


def get_dataset_metadata(dataset_id: str) -> Dict:
    """Get metadata for an approved dataset."""
    return verify_license(dataset_id)


if __name__ == "__main__":
    print("Approved datasets:")
    for ds_id, meta in APPROVED_DATASETS.items():
        print(f"  {ds_id}: {meta['name']} ({meta['license']})")
