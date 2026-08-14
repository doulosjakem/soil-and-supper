#!/usr/bin/env python3
"""
PMC/BDFlower downloader for Soil & Supper ML pipeline.
Downloads supplementary files from PubMed Central articles.
"""

import requests
import zipfile
import tarfile
import re
from pathlib import Path
from typing import Dict, Optional
from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus


class PMCDownloader(BaseDownloader):
    """Download supplementary files from PMC articles."""
    
    PMC_BASE = "https://pmc.ncbi.nlm.nih.gov"
    
    def find_supplementary_url(self, article_url: str) -> Optional[str]:
        """Find supplementary file download URL from PMC article."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(article_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            content = response.text
            
            # Look for supplementary file links
            patterns = [
                r'href="(/articles/PMC\d+/bin/[^"]+\.zip)"',
                r'href="(/articles/PMC\d+/bin/[^"]+\.tar\.gz)"',
                r'data-url="(https://pmc.ncbi.nlm.nih.gov/articles/PMC\d+/bin/[^"]+\.zip)"',
                r'https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC\d+/bin/([^"\']+\.zip)',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    url = matches[0]
                    if not url.startswith("http"):
                        url = self.PMC_BASE + url
                    return url
            
            # Look for PMC ID and construct supplementary URL
            pmc_match = re.search(r'PMC(\d+)', article_url)
            if pmc_match:
                pmc_id = pmc_match.group(1)
                # Try common supplementary file patterns
                for filename in [f"mmc1.zip", f"mmc1.tar.gz", f"supplementary.zip"]:
                    url = f"{self.PMC_BASE}/articles/PMC{pmc_id}/bin/{filename}"
                    try:
                        resp = requests.head(url, timeout=10, allow_redirects=True)
                        if resp.status_code == 200:
                            return url
                    except Exception:
                        continue
        except Exception:
            pass
        
        return None
    
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """Get PMC supplementary download URL."""
        source_url = info.get("url", "")
        return self.find_supplementary_url(source_url)
    
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        """Download from PMC."""
        record = AcquisitionRecord(
            dataset_id=dataset_id,
            name=info["name"],
            status=AcquisitionStatus.LICENSE_VERIFIED,
            source_url=info.get("url", ""),
            license=info.get("license"),
            license_url=info.get("license_url"),
        )
        
        url = self.get_download_url(dataset_id, info)
        if not url:
            record = self.update_status(record, AcquisitionStatus.FAILED, "No supplementary file found")
            return record
        
        record.download_url = url
        ext = ".zip" if ".zip" in url.lower() else ".tar.gz"
        dest_path = self.output_dir / f"{dataset_id}{ext}"
        
        try:
            response = requests.get(url, stream=True, timeout=120, allow_redirects=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0
            
            with open(dest_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            
            record.actual_size = downloaded
            record.file_size = total_size if total_size > 0 else downloaded
            
            if zipfile.is_zipfile(dest_path) or tarfile.is_tarfile(dest_path):
                record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
            else:
                with open(dest_path, "rb") as f:
                    header = f.read(100)
                    if b"<!doctype html>" in header.lower() or b"<html" in header.lower():
                        dest_path.unlink()
                        record = self.update_status(record, AcquisitionStatus.FAILED, "Downloaded HTML instead of archive")
                    else:
                        record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
        except Exception as e:
            record = self.update_status(record, AcquisitionStatus.FAILED, str(e))
        
        return record
