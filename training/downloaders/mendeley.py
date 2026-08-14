#!/usr/bin/env python3
"""
Mendeley Data downloader for Soil & Supper ML pipeline.
Handles Mendeley Data dataset downloads.
"""

import requests
import re
from pathlib import Path
from typing import Dict, Optional
from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus


class MendeleyDownloader(BaseDownloader):
    """Download datasets from Mendeley Data."""
    
    def find_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """Try to find direct download URL from Mendeley page."""
        source_url = info.get("url", "")
        
        # Try to extract file ID from URL or find download link
        try:
            response = requests.get(source_url, timeout=30, allow_redirects=True)
            if response.status_code == 200:
                # Look for download links in the page
                content = response.text
                # Mendeley often has direct download links
                patterns = [
                    r'href="([^"]*download[^"]*)"',
                    r'href="([^"]*\.zip)"',
                    r'href="([^"]*\.tar\.gz)"',
                    r'data-url="([^"]*)"',
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        # Return first matching URL
                        url = matches[0]
                        if not url.startswith("http"):
                            url = "https://data.mendeley.com" + url
                        return url
        except Exception:
            pass
        
        return None
    
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """Get download URL."""
        return self.find_download_url(dataset_id, info)
    
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        """Download from Mendeley."""
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
            record = self.update_status(record, AcquisitionStatus.FAILED, "No downloadable URL found on Mendeley page")
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
            
            # Verify it's actually an archive
            if dest_path.suffix == ".zip":
                import zipfile
                if zipfile.is_zipfile(dest_path):
                    record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
                else:
                    record = self.update_status(record, AcquisitionStatus.FAILED, "Not a valid zip file")
            elif dest_path.suffix in [".tar.gz", ".tgz"]:
                import tarfile
                if tarfile.is_tarfile(dest_path):
                    record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
                else:
                    record = self.update_status(record, AcquisitionStatus.FAILED, "Not a valid tar.gz file")
            else:
                record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
        except Exception as e:
            record = self.update_status(record, AcquisitionStatus.FAILED, str(e))
        
        return record
