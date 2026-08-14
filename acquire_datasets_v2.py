#!/usr/bin/env python3
"""
Dataset acquisition script - v2
Handles Mendeley, Zenodo, PMC direct downloads
"""

import os
import requests
import json
import time
import zipfile
import io
from pathlib import Path
from urllib.parse import urljoin, urlparse

RAW_DIR = Path("./raw")
RAW_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def download_file(url, dest_path, description="", chunk_size=8192):
    """Download a file with progress."""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    if dest_path.exists() and dest_path.stat().st_size > 0:
        print(f"[SKIP] {description or dest_path.name} already exists ({dest_path.stat().st_size} bytes)")
        return True
    
    print(f"[DOWNLOAD] {description or dest_path.name}")
    print(f"  URL: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=120, stream=True, allow_redirects=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        pct = (downloaded / total_size) * 100
                        print(f"\r  {pct:.1f}% ({downloaded}/{total_size} bytes)", end="", flush=True)
        
        print(f"\n[OK] Saved: {dest_path} ({dest_path.stat().st_size} bytes)")
        return True
    except Exception as e:
        print(f"\n[ERROR] {e}")
        if dest_path.exists():
            dest_path.unlink()
        return False

def download_mendeley_doi(doi, dest_dir, dataset_name):
    """
    Download a Mendeley dataset using the DOI.
    Mendeley datasets are accessible via their DOI redirect.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n=== {dataset_name} ===")
    print(f"DOI: {doi}")
    
    # Mendeley DOI redirects to data.mendeley.com
    doi_url = f"https://doi.org/{doi}"
    
    try:
        # Follow DOI redirect
        response = requests.get(doi_url, headers=HEADERS, timeout=30, allow_redirects=True)
        final_url = response.url
        print(f"Redirected to: {final_url}")
        
        # Look for download API endpoint
        # Mendeley often has /download or similar
        if "data.mendeley.com" in final_url:
            # Try to find the download endpoint
            # Usually it's something like https://data.mendeley.com/public-files/datasets/{id}/file_versions
            # Or direct download via a token
            
            # Parse dataset ID from URL
            parts = final_url.rstrip("/").split("/")
            dataset_id = parts[-1]
            print(f"Dataset ID: {dataset_id}")
            
            # Try direct download endpoint patterns
            possible_urls = [
                f"https://data.mendeley.com/public-files/datasets/{dataset_id}/file_versions",
                f"https://data.mendeley.com/public-files/datasets/{dataset_id}/files",
                f"https://data.mendeley.com/datasets/{dataset_id}/files",
            ]
            
            for url in possible_urls:
                try:
                    r = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
                    print(f"  Trying {url}: {r.status_code}")
                    if r.status_code == 200:
                        print(f"  Content preview: {r.text[:500]}")
                        break
                except Exception as e:
                    print(f"  Failed: {e}")
            
            # Create manifest with manual download instructions
            manifest = {
                "dataset_id": dataset_id,
                "doi": doi,
                "source_url": final_url,
                "license": "CC BY 4.0 (verify on page)",
                "status": "manual_download_required",
                "instructions": f"Visit {final_url} and click Download"
            }
            
            with open(dest_dir / "manifest.json", "w") as f:
                json.dump(manifest, f, indent=2)
            
            return True
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def download_zenodo(record_id, dest_dir, dataset_name):
    """
    Download a Zenodo dataset by record ID.
    Zenodo provides direct download links for files.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n=== {dataset_name} ===")
    print(f"Zenodo Record: {record_id}")
    
    api_url = f"https://zenodo.org/api/records/{record_id}"
    
    try:
        response = requests.get(api_url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        record = response.json()
        
        # Extract metadata
        title = record.get("metadata", {}).get("title", "Unknown")
        license = record.get("metadata", {}).get("license", {}).get("id", "Unknown")
        files = record.get("files", [])
        
        print(f"Title: {title}")
        print(f"License: {license}")
        print(f"Files: {len(files)}")
        
        # Save manifest
        manifest = {
            "dataset_id": f"zenodo-{record_id}",
            "title": title,
            "license": license,
            "zenodo_url": f"https://zenodo.org/record/{record_id}",
            "files": [{"name": f["key"], "size": f["size"], "url": f["links"]["self"]} for f in files],
            "status": "downloading"
        }
        
        with open(dest_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)
        
        # Download each file
        for file_info in files:
            file_name = file_info["key"]
            file_url = file_info["links"]["self"]
            file_size = file_info["size"]
            dest_path = dest_dir / file_name
            
            print(f"\n  File: {file_name} ({file_size} bytes)")
            download_file(file_url, dest_path, file_name)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def download_pmc_supplementary(pmc_id, dest_dir, dataset_name):
    """
    Download supplementary materials from a PMC article.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n=== {dataset_name} ===")
    print(f"PMC ID: {pmc_id}")
    
    pmc_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmc_id}/"
    
    try:
        response = requests.get(pmc_url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "lxml")
        
        # Find supplementary material links
        sup_section = soup.find("div", {"id": "supplementary-material"})
        if not sup_section:
            sup_section = soup.find("section", {"id": "supplementary-material"})
        
        if sup_section:
            links = sup_section.find_all("a", href=True)
            print(f"Found {len(links)} supplementary links")
            for a in links[:10]:
                href = urljoin(pmc_url, a["href"])
                text = a.get_text(strip=True)
                print(f"  - {text}: {href}")
        else:
            print("  No supplementary material section found")
            # Try to find data availability statements
            data_avail = soup.find("div", {"id": "data-availability"})
            if data_avail:
                print("  Data availability section found:")
                print(data_avail.get_text(strip=True)[:500])
        
        # Create manifest
        manifest = {
            "pmc_id": pmc_id,
            "source_url": pmc_url,
            "status": "links_found" if sup_section else "no_supplementary_found",
            "instructions": "Check article supplementary materials or data availability section"
        }
        
        with open(dest_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

# ============================================================
# Main
# ============================================================
def main():
    print("=" * 60)
    print("Soil & Supper Dataset Acquisition - Tier 1 (v2)")
    print("=" * 60)
    
    results = {}
    
    # 1. Zenodo: OLID I (Bangladesh leaf dataset) - CC0
    results["zenodo-8105154"] = download_zenodo(
        record_id="8105154",
        dest_dir=RAW_DIR / "zenodo_olid",
        dataset_name="OLID I - Open Leaf Image Dataset of Bangladesh"
    )
    
    # 2. Mendeley: Bangladesh Comprehensive Vegetables
    results["mendeley-rtx9ngb68j"] = download_mendeley_doi(
        doi="10.17632/rtx9ngb68j",
        dest_dir=RAW_DIR / "bangladesh_veg",
        dataset_name="Bangladesh Comprehensive Vegetables"
    )
    
    # 3. PMC: Smartphone Vegetable Detection
    results["pmc-12686877"] = download_pmc_supplementary(
        pmc_id="PMC12686877",
        dest_dir=RAW_DIR / "smartphone_veg",
        dataset_name="Smartphone Vegetable Detection"
    )
    
    # 4. PMC: Early-Stage Vegetable Crops
    results["pmc-8933512"] = download_pmc_supplementary(
        pmc_id="PMC8933512",
        dest_dir=RAW_DIR / "early_stage_crops",
        dataset_name="Early-Stage Vegetable Crops"
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("ACQUISITION SUMMARY")
    print("=" * 60)
    for ds_id, success in results.items():
        status = "OK" if success else "FAILED"
        print(f"  {ds_id}: {status}")
    
    # Save log
    log = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "results": {k: "success" if v else "failed" for k, v in results.items()},
        "next_steps": [
            "Review manifests in raw/ subdirectories",
            "Manually download datasets where automated download failed",
            "Verify licenses before curation"
        ]
    }
    
    with open(RAW_DIR / "acquisition_log.json", "w") as f:
        json.dump(log, f, indent=2)
    
    print("\nAcquisition log saved to raw/acquisition_log.json")

if __name__ == "__main__":
    main()
