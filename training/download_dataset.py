#!/usr/bin/env python3
"""
Dataset download utilities for Soil & Supper ML pipeline.
Downloads approved datasets to raw/ directory.
"""

import os
import requests
import hashlib
import json
from pathlib import Path
from typing import Dict, List

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def download_file(url: str, dest_path: Path, description: str = "") -> bool:
    """Download a file with progress."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if dest_path.exists():
        print(f"[SKIP] {description or dest_path.name} already exists")
        return True
    print(f"[DOWNLOAD] {description or dest_path.name}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=60, stream=True)
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
    import zipfile
    import tarfile
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


if __name__ == "__main__":
    print("Dataset download utilities loaded.")
    print("Use download_dataset.py --dataset <id> to download a specific dataset.")
