#!/usr/bin/env python3
"""
Roboflow downloader for Soil & Supper ML pipeline.
Downloads datasets from Roboflow Universe.
"""

import requests
import zipfile
import tarfile
from pathlib import Path
from typing import Dict, Optional
from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus


class RoboflowDownloader(BaseDownloader):
    """Download datasets from Roboflow Universe."""
    
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """Get Roboflow export download URL."""
        # Roboflow Universe datasets can be downloaded via export URL
        # Format: https://universe.roboflow.com/ds/<dataset>?download=1
        source_url = info.get("url", "")
        if "roboflow.com" in source_url:
            # Add download parameter
            if "?" in source_url:
                return f"{source_url}&download=1"
            else:
                return f"{source_url}?download=1"
        return None
    
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        """Download from Roboflow."""
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
            record = self.update_status(record, AcquisitionStatus.FAILED, "No Roboflow download URL")
            return record
        
        record.download_url = url
        ext = ".zip"
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
