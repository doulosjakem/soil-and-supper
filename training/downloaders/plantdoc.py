#!/usr/bin/env python3
"""
PlantDoc downloader for Soil & Supper ML pipeline.
Downloads from GitHub repository.
"""

import requests
import zipfile
import tarfile
from pathlib import Path
from typing import Dict, Optional
from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus


class PlantDocDownloader(BaseDownloader):
    """Download PlantDoc dataset from GitHub."""
    
    GITHUB_URL = "https://github.com/pratikkayal/PlantDoc-Dataset"
    
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """Try to find direct download URL from GitHub."""
        # Try ZIP archive of the repository
        zip_url = f"https://github.com/pratikkayal/PlantDoc-Dataset/archive/refs/heads/main.zip"
        
        try:
            response = requests.head(zip_url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                return zip_url
        except Exception:
            pass
        
        return None
    
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        """Download PlantDoc."""
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
            record = self.update_status(record, AcquisitionStatus.FAILED, "No downloadable URL found")
            return record
        
        record.download_url = url
        dest_path = self.output_dir / f"{dataset_id}.zip"
        
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
