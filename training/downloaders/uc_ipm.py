#!/usr/bin/env python3
"""
UC IPM downloader for Soil & Supper ML pipeline.
Downloads images from UC Integrated Pest Management website.
"""

import requests
import time
import os
from pathlib import Path
from typing import Dict, Optional, List
from bs4 import BeautifulSoup
from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus


class UCIPMDownloader(BaseDownloader):
    """Download images from UC IPM website."""
    
    BASE_URL = "https://ipm.ucanr.edu"
    
    def find_image_gallery(self, url: str) -> List[str]:
        """Find image URLs from UC IPM gallery pages."""
        image_urls = []
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find all image tags
            for img in soup.find_all("img"):
                src = img.get("src", "")
                if src and (src.endswith(".jpg") or src.endswith(".jpeg") or src.endswith(".png")):
                    if not src.startswith("http"):
                        src = self.BASE_URL + src
                    image_urls.append(src)
            
            # Also look for links to image pages
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/PMG/" in href and href.endswith((".jpg", ".jpeg", ".png")):
                    if not href.startswith("http"):
                        href = self.BASE_URL + href
                    image_urls.append(href)
        except Exception:
            pass
        
        return list(set(image_urls))
    
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """UC IPM doesn't have single archive downloads."""
        return None
    
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        """Download images from UC IPM gallery."""
        record = AcquisitionRecord(
            dataset_id=dataset_id,
            name=info["name"],
            status=AcquisitionStatus.LICENSE_VERIFIED,
            source_url=info.get("url", ""),
            license=info.get("license"),
            license_url=info.get("license_url"),
        )
        
        source_url = info.get("url", "")
        image_urls = self.find_image_gallery(source_url)
        
        if not image_urls:
            record = self.update_status(record, AcquisitionStatus.FAILED, "No images found on gallery page")
            return record
        
        # Create dataset directory
        dataset_dir = self.output_dir / dataset_id
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded = 0
        failed = 0
        
        for i, img_url in enumerate(image_urls):
            try:
                ext = ".jpg" if ".jpg" in img_url.lower() else ".jpeg" if ".jpeg" in img_url.lower() else ".png"
                dest_path = dataset_dir / f"image_{i:04d}{ext}"
                
                if dest_path.exists():
                    downloaded += 1
                    continue
                
                response = requests.get(img_url, timeout=30, allow_redirects=True)
                if response.status_code == 200:
                    with open(dest_path, "wb") as f:
                        f.write(response.content)
                    downloaded += 1
                    time.sleep(0.1)  # Be polite
            except Exception:
                failed += 1
                continue
        
        record.actual_size = sum(f.stat().st_size for f in dataset_dir.glob("*") if f.is_file())
        record.image_count = downloaded
        record.valid_count = downloaded
        record.classes = info.get("classes", [])
        
        if downloaded > 0:
            record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
        else:
            record = self.update_status(record, AcquisitionStatus.FAILED, f"No images downloaded (failed: {failed})")
        
        return record
