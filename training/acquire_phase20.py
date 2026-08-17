#!/usr/bin/env python3
"""
Download and extract Phase 20 datasets.
"""

import requests
import zipfile
import io
import os
import sys
from pathlib import Path

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
RAW_DIR = TRAINING_DATA_DIR / "raw"

def download_file(url, dest_path, chunk_size=1024*1024):
    """Download file with resume support."""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if file exists and get size
    existing_size = 0
    if dest_path.exists():
        existing_size = dest_path.stat().st_size
    
    # Get remote file size
    r = requests.head(url, timeout=30, allow_redirects=True)
    remote_size = int(r.headers.get('Content-Length', 0))
    
    if remote_size == 0:
        print(f"ERROR: Could not determine file size for {url}")
        return False
    
    if existing_size == remote_size:
        print(f"File already exists and complete: {dest_path}")
        return True
    
    print(f"Downloading {url}")
    print(f"  Remote size: {remote_size / 1024/1024/1024:.2f} GB")
    print(f"  Existing: {existing_size / 1024/1024:.1f} MB")
    
    # Resume download
    headers = {}
    if existing_size > 0:
        headers['Range'] = f'bytes={existing_size}-'
    
    r = requests.get(url, headers=headers, timeout=120, stream=True)
    
    if r.status_code not in (200, 206):
        print(f"ERROR: Download failed with status {r.status_code}")
        return False
    
    mode = 'ab' if existing_size > 0 else 'wb'
    with open(dest_path, mode) as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                f.flush()
    
    final_size = dest_path.stat().st_size
    print(f"  Downloaded to: {dest_path} ({final_size / 1024/1024/1024:.2f} GB)")
    
    if final_size != remote_size:
        print(f"WARNING: Size mismatch. Expected {remote_size}, got {final_size}")
        return False
    
    return True

def extract_zip(zip_path, extract_to):
    """Extract zip file."""
    zip_path = Path(zip_path)
    extract_to = Path(extract_to)
    extract_to.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting {zip_path} to {extract_to}")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            # Get list of files
            files = z.namelist()
            print(f"  Files in archive: {len(files)}")
            
            # Extract all
            z.extractall(extract_to)
            
            print(f"  Extracted successfully")
            return True
    except Exception as e:
        print(f"ERROR extracting {zip_path}: {e}")
        return False

# Datasets to acquire
DATASETS = [
    {
        'name': 'irish_potato',
        'files': [
            {
                'url': 'https://zenodo.org/api/records/8286529/files/earlyblt.zip/content',
                'dest': RAW_DIR / 'irish_potato' / 'earlyblt.zip',
                'extract_to': RAW_DIR / 'irish_potato' / 'earlyblt',
            },
            {
                'url': 'https://zenodo.org/api/records/8286529/files/lateblt.zip/content',
                'dest': RAW_DIR / 'irish_potato' / 'lateblt.zip',
                'extract_to': RAW_DIR / 'irish_potato' / 'lateblt',
            },
            {
                'url': 'https://zenodo.org/api/records/8286529/files/healthy.zip/content',
                'dest': RAW_DIR / 'irish_potato' / 'healthy.zip',
                'extract_to': RAW_DIR / 'irish_potato' / 'healthy',
            },
        ],
    },
    {
        'name': 'common_beans',
        'files': [
            {
                'url': 'https://zenodo.org/api/records/8286126/files/rust.zip/content',
                'dest': RAW_DIR / 'common_beans' / 'rust.zip',
                'extract_to': RAW_DIR / 'common_beans' / 'rust',
            },
            {
                'url': 'https://zenodo.org/api/records/8286126/files/anthra.zip/content',
                'dest': RAW_DIR / 'common_beans' / 'anthra.zip',
                'extract_to': RAW_DIR / 'common_beans' / 'anthra',
            },
            {
                'url': 'https://zenodo.org/api/records/8286126/files/healthy.zip/content',
                'dest': RAW_DIR / 'common_beans' / 'healthy.zip',
                'extract_to': RAW_DIR / 'common_beans' / 'healthy',
            },
        ],
    },
    {
        'name': 'grapevine',
        'files': [
            {
                'url': 'https://zenodo.org/api/records/17343474/files/Resized%201024%20%C3%97%201024.zip/content',
                'dest': RAW_DIR / 'grapevine' / 'resized_1024.zip',
                'extract_to': RAW_DIR / 'grapevine' / 'resized',
            },
        ],
    },
]

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', choices=['irish_potato', 'common_beans', 'grapevine', 'all'], default='all')
    parser.add_argument('--skip-download', action='store_true')
    parser.add_argument('--skip-extract', action='store_true')
    args = parser.parse_args()
    
    for ds in DATASETS:
        if args.dataset != 'all' and ds['name'] != args.dataset:
            continue
        
        print(f"\n{'='*60}")
        print(f"Dataset: {ds['name']}")
        print('='*60)
        
        for file_info in ds['files']:
            print(f"\nFile: {file_info['dest'].name}")
            
            if not args.skip_download:
                success = download_file(file_info['url'], file_info['dest'])
                if not success:
                    print(f"ERROR: Failed to download {file_info['dest']}")
                    continue
            
            if not args.skip_extract:
                if file_info['dest'].exists():
                    extract_zip(file_info['dest'], file_info['extract_to'])
                else:
                    print(f"ERROR: Archive not found: {file_info['dest']}")
    
    print("\nDone!")
