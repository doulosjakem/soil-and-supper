#!/usr/bin/env python3
"""
Dataset download utilities for Soil & Supper ML pipeline.
Uses modular adapters for different data sources.
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
    # Phase 9 core datasets
    "bangladesh_veg": "https://data.mendeley.com/datasets/rtx9ngb68j",
    "smartphone_veg": "https://data.mendeley.com/datasets/gnc4s3z2mf/3",
    "banglaveg": "https://www.sciencedirect.com/science/article/pii/S2352340925001738",
    "plantvillage": "https://data.mendeley.com/datasets/tywbtsjrjv/1",
    "deepweeds": "https://github.com/AlexOlsen/DeepWeeds",
    "plant_growth_stage": "https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection",
    "bdflower": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/",
    "sunflower_growth": "https://data.mendeley.com/datasets/byftmdzg4g",
    "early_stage_crops": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/",
    "USDA_ARS": "https://www.ars.usda.gov/oc/images/image-gallery/",
    # Phase 10 expansion datasets
    "uc_ipm_weeds": "https://ipm.ucanr.edu/PMG/WEEDS/",
    "usda_nrcs_plants": "https://plants.usda.gov/",
    "uc_ipm_insects": "https://ipm.ucanr.edu/PMG/INSE/",
    "uc_ipm_beneficials": "https://ipm.ucanr.edu/PMG/BENE/",
    "cornell_disease_herbarium": "https://ppathgbif.cals.cornell.edu/",
    "zenodo_plant_disease": "https://zenodo.org/",
    "mendeley_plant_expanded": "https://data.mendeley.com/",
    "zenodo_insects": "https://zenodo.org/",
}


def get_downloader(dataset_id: str, info: Dict):
    """Get appropriate downloader for dataset."""
    url = info.get("url", "")
    download_url = info.get("download_url", "")
    
    if dataset_id == "deepweeds":
        from downloaders.deepweeds import DeepWeedsDownloader
        return DeepWeedsDownloader(RAW_DIR, MANIFESTS_DIR)
    elif dataset_id == "plantvillage":
        from downloaders.plantvillage import PlantVillageDownloader
        return PlantVillageDownloader(RAW_DIR, MANIFESTS_DIR)
    elif dataset_id == "plantdoc":
        from downloaders.plantdoc import PlantDocDownloader
        return PlantDocDownloader(RAW_DIR, MANIFESTS_DIR)
    elif dataset_id == "plant_growth_stage":
        from downloaders.roboflow import RoboflowDownloader
        return RoboflowDownloader(RAW_DIR, MANIFESTS_DIR)
    elif dataset_id in ["bdflower"]:
        from downloaders.pmc import PMCDownloader
        return PMCDownloader(RAW_DIR, MANIFESTS_DIR)
    elif "github.com" in url:
        from downloaders.github import GitHubDownloader
        return GitHubDownloader(RAW_DIR, MANIFESTS_DIR)
    elif "zenodo.org" in url:
        from downloaders.zenodo import ZenodoDownloader
        return ZenodoDownloader(RAW_DIR, MANIFESTS_DIR)
    elif "mendeley.com" in url:
        from downloaders.mendeley import MendeleyDownloader
        return MendeleyDownloader(RAW_DIR, MANIFESTS_DIR)
    elif "ipm.ucanr.edu" in url:
        from downloaders.uc_ipm import UCIPMDownloader
        return UCIPMDownloader(RAW_DIR, MANIFESTS_DIR)
    elif "usda.gov" in url or "plants.usda.gov" in url:
        from downloaders.usda import USDADownloader
        return USDADownloader(RAW_DIR, MANIFESTS_DIR)
    else:
        from downloaders.direct import DirectDownloader
        return DirectDownloader(RAW_DIR, MANIFESTS_DIR)


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
    """Download a specific dataset using appropriate adapter."""
    if not info.get("commercial_ok", False):
        print(f"[SKIP] {dataset_id}: Not commercially approved")
        return False
    
    print(f"\n[DOWNLOAD] {info['name']}")
    downloader = get_downloader(dataset_id, info)
    
    try:
        record = downloader.download(dataset_id, info)
        
        if hasattr(record, 'status') and record.status.value in ["failed", "hold"]:
            print(f"[FAILED] {dataset_id}: {record.error}")
            return False
        
        print(f"[OK] {dataset_id} acquired")
        return True
    except Exception as e:
        print(f"[ERROR] {dataset_id}: {e}")
        return False


if __name__ == "__main__":
    print("Dataset download utilities loaded.")
    print("Use pipeline.py --step download to download all approved datasets.")
