#!/usr/bin/env python3
"""
GitHub release/asset downloader for Soil & Supper ML pipeline.
Used for datasets hosted on GitHub with release assets.
"""

import requests
import json
import zipfile
import tarfile
from pathlib import Path
from typing import Dict, Optional
from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus


class GitHubDownloader(BaseDownloader):
    """Download datasets from GitHub releases/assets."""
    
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """Get download URL from GitHub release assets or repository."""
        # For DeepWeeds, images are on Google Drive, not GitHub
        # But we can try to get them from the repo if they're there
        repo_url = info.get("url", "")
        if "github.com" not in repo_url:
            return None
        
        # Try to find release assets
        api_url = repo_url.replace("github.com", "api.github.com/repos")
        if not api_url.endswith("/"):
            api_url += "/"
        api_url += "releases/latest"
        
        try:
            response = requests.get(api_url, timeout=30)
            if response.status_code == 200:
                release = response.json()
                assets = release.get("assets", [])
                for asset in assets:
                    if asset["name"].endswith((".zip", ".tar.gz", ".tgz")):
                        return asset["browser_download_url"]
        except Exception:
            pass
        
        return None
    
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        """Download from GitHub."""
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
            record = self.update_status(record, AcquisitionStatus.FAILED, "No downloadable asset found")
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
            
            # Verify it's actually a zip/archive
            if dest_path.suffix == ".zip" and zipfile.is_zipfile(dest_path):
                record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
            elif dest_path.suffix in [".tar.gz", ".tgz"] and tarfile.is_tarfile(dest_path):
                record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
            else:
                # Check if it's HTML (failed download)
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
