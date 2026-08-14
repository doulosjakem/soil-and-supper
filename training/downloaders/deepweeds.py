#!/usr/bin/env python3
"""
DeepWeeds Google Drive downloader for Soil & Supper ML pipeline.
Downloads images.zip from Google Drive using official file ID.
"""

import requests
import zipfile
import re
from pathlib import Path
from typing import Dict, Optional
from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus


class DeepWeedsDownloader(BaseDownloader):
    """Download DeepWeeds images from Google Drive."""
    
    # Official file ID from DeepWeeds README
    IMAGE_FILE_ID = "1xnK3B6K6KekDI55vwJ0vnc2IGoDga9cj"
    GOOGLE_DRIVE_URL = "https://drive.google.com/uc?export=download"
    
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """Get Google Drive download URL."""
        return f"{self.GOOGLE_DRIVE_URL}&id={self.IMAGE_FILE_ID}"
    
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        """Download DeepWeeds images from Google Drive."""
        record = AcquisitionRecord(
            dataset_id=dataset_id,
            name=info["name"],
            status=AcquisitionStatus.LICENSE_VERIFIED,
            source_url=info.get("url", ""),
            license=info.get("license"),
            license_url=info.get("license_url"),
        )
        
        url = self.get_download_url(dataset_id, info)
        record.download_url = url
        dest_path = self.output_dir / f"{dataset_id}_images.zip"
        
        try:
            session = requests.Session()
            response = session.get(url, timeout=120, stream=True)
            
            # Handle Google Drive confirmation for large files
            if "quota exceeded" in response.text.lower() or "virus scan warning" in response.text.lower():
                # Extract confirmation token
                token_match = re.search(r'confirm=([a-zA-Z0-9_-]+)', response.text)
                if token_match:
                    token = token_match.group(1)
                    url = f"{url}&confirm={token}"
                    response = session.get(url, timeout=120, stream=True)
            
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
            
            # Verify it's actually a zip
            if zipfile.is_zipfile(dest_path):
                record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
            else:
                with open(dest_path, "rb") as f:
                    header = f.read(100)
                    if b"<!doctype html>" in header.lower() or b"<html" in header.lower():
                        dest_path.unlink()
                        record = self.update_status(record, AcquisitionStatus.FAILED, "Downloaded HTML instead of zip")
                    else:
                        record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
        except Exception as e:
            record = self.update_status(record, AcquisitionStatus.FAILED, str(e))
        
        return record
