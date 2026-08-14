#!/usr/bin/env python3
"""
Dataset download utilities for Soil & Supper ML pipeline.
Downloads approved datasets to training_data/raw/ directory on D: drive.
"""

import os
import requests
import hashlib
import json
import zipfile
import tarfile
from pathlib import Path
from typing import Dict, List

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"
TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
RAW_DIR = TRAINING_DATA_DIR / "raw"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"

RAW_DIR.mkdir(parents=True, exist_ok=True)
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

DATASET_URLS = {
    "bangladesh_veg": "https://data.mendeley.com/public-files/datasets/rtx9ngb68j/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
    "smartphone_veg": "https://data.mendeley.com/public-files/datasets/gnc4s3z2mf/files/3c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
    "banglaveg": "https://data.mendeley.com/public-files/datasets/6nxnjbn9w6/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
    "plantvillage": "https://data.mendeley.com/public-files/datasets/tywbtsjrjv/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
    "deepweeds": "https://github.com/AlexOlsen/DeepWeeds/archive/refs/heads/master.zip",
    "plant_growth_stage": "https://universe.roboflow.com/ds/plant-growth-stage-detection?download=1",
    "bdflower": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/bin/mmc1.zip",
    "sunflower_growth": "https://data.mendeley.com/public-files/datasets/byftmdzg4g/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
    "early_stage_crops": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/bin/mmc1.zip",
    "USDA_ARS": "https://www.ars.usda.gov/oc/images/image-gallery/",
    "uc_ipm_weeds": "https://ipm.ucanr.edu/PMG/WEEDS/",
    "usda_nrcs_plants": "https://plants.usda.gov/",
    "uc_ipm_insects": "https://ipm.ucanr.edu/PMG/INSE/",
    "uc_ipm_beneficials": "https://ipm.ucanr.edu/PMG/BENE/",
    "cornell_disease_herbarium": "https://ppathgbif.cals.cornell.edu/",
    "zenodo_plant_disease": "https://zenodo.org/",
    "mendeley_plant_expanded": "https://data.mendeley.com/",
    "zenodo_insects": "https://zenodo.org/",
}


def download_file(url: str, dest_path: Path, description: str = "") -> bool:
    """Download a file with progress."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if dest_path.exists():
        print(f"[SKIP] {description or dest_path.name} already exists")
        return True
    print(f"[DOWNLOAD] {description or dest_path.name}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=120, stream=True, allow_redirects=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        block_size = 8192
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        pct = (downloaded / total_size) * 100
                        print(f"\r  {pct:.1f}% ({downloaded}/{total_size} bytes)", end="", flush=True)
        print(f"\n[OK] Saved to {dest_path}")
        return True
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False


def extract_archive(archive_path: Path, extract_dir: Path) -> bool:
    """Extract archive based on extension."""
    extract_dir.mkdir(parents=True, exist_ok=True)
    try:
        if archive_path.suffix == ".zip":
            with zipfile.ZipFile(archive_path, "r") as z:
                z.extractall(extract_dir)
        elif archive_path.suffix in [".tar", ".gz", ".bz2"]:
            with tarfile.open(archive_path, "r:*") as t:
                t.extractall(extract_dir)
        else:
            print(f"[SKIP] Unknown archive format: {archive_path.suffix}")
            return False
        print(f"[OK] Extracted to {extract_dir}")
        return True
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        return False


def compute_file_hash(path: Path) -> str:
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def record_download(dataset_id: str, archive_path: Path, success: bool, error: str = ""):
    """Record download metadata."""
    manifest_path = MANIFESTS_DIR / "downloads.jsonl"
    record = {
        "dataset_id": dataset_id,
        "archive_path": str(archive_path),
        "file_size": archive_path.stat().st_size if archive_path.exists() else 0,
        "sha256": compute_file_hash(archive_path) if archive_path.exists() else "",
        "success": success,
        "error": error,
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }
    with open(manifest_path, "a") as f:
        f.write(json.dumps(record) + "\n")


def download_dataset(dataset_id: str, info: Dict) -> bool:
    """Download a specific dataset."""
    if dataset_id not in DATASET_URLS:
        print(f"[SKIP] No download URL configured for {dataset_id}")
        return False
    
    url = DATASET_URLS[dataset_id]
    ext = ".zip" if "zip" in url.lower() or "download=1" in url.lower() else ".tar.gz"
    archive_name = f"{dataset_id}{ext}"
    archive_path = RAW_DIR / archive_name
    extract_dir = RAW_DIR / dataset_id
    
    success = download_file(url, archive_path, info["name"])
    if not success:
        record_download(dataset_id, archive_path, False, "Download failed")
        return False
    
    if extract_dir.exists():
        import shutil
        shutil.rmtree(extract_dir)
    
    extract_success = extract_archive(archive_path, extract_dir)
    record_download(dataset_id, archive_path, extract_success)
    
    if extract_success:
        print(f"[OK] {dataset_id} ready at {extract_dir}")
        return True
    return False


if __name__ == "__main__":
    print("Dataset download utilities loaded.")
    print("Use pipeline.py --step download to download all approved datasets.")
