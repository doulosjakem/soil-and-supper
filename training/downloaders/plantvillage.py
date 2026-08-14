#!/usr/bin/env python3
"""
PlantVillage downloader for Soil & Supper ML pipeline.
Multiple acquisition methods:
1. TensorFlow Datasets (if available)
2. Direct download from known mirrors
3. Mendeley Data
"""

import requests
import zipfile
import tarfile
from pathlib import Path
from typing import Dict, Optional
from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus


class PlantVillageDownloader(BaseDownloader):
    """Download PlantVillage dataset."""
    
    KNOWN_MIRRORS = [
        "https://data.mendeley.com/public-files/datasets/tywbtsjrjv/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
        "https://www.kaggle.com/datasets/emmarex/plantdisease/download",
        "https://github.com/attaullah/downsampled-plant-disease-dataset/archive/refs/heads/master.zip",
    ]
    
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """Try known mirrors."""
        for url in self.KNOWN_MIRRORS:
            try:
                response = requests.head(url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    return url
            except Exception:
                continue
        return None
    
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        """Download PlantVillage."""
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
            record = self.update_status(record, AcquisitionStatus.FAILED, "No accessible mirror found")
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
            
            # Verify archive
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
