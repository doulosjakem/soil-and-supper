#!/usr/bin/env python3
"""
USDA downloader for Soil & Supper ML pipeline.
Handles USDA NRCS PLANTS Database and USDA ARS Image Gallery.
"""

import requests
import time
from pathlib import Path
from typing import Dict, Optional, List
from bs4 import BeautifulSoup
from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus


class USDADownloader(BaseDownloader):
    """Download images from USDA websites."""
    
    BASE_URL = "https://plants.usda.gov"
    ARS_URL = "https://www.ars.usda.gov"
    
    def find_plant_images(self, scientific_name: str) -> List[str]:
        """Find images for a specific plant in USDA NRCS."""
        image_urls = []
        
        try:
            # Search for plant
            search_url = f"{self.BASE_URL}/api/plants/search"
            params = {"q": scientific_name}
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                # Process results...
                pass
        except Exception:
            pass
        
        return image_urls
    
    def find_ars_images(self, url: str) -> List[str]:
        """Find images from USDA ARS image gallery."""
        image_urls = []
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            for img in soup.find_all("img"):
                src = img.get("src", "")
                if src and (src.endswith(".jpg") or src.endswith(".jpeg") or src.endswith(".png")):
                    if not src.startswith("http"):
                        src = self.ARS_URL + src
                    image_urls.append(src)
        except Exception:
            pass
        
        return image_urls
    
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """USDA doesn't have single archive downloads."""
        return None
    
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        """Download images from USDA."""
        record = AcquisitionRecord(
            dataset_id=dataset_id,
            name=info["name"],
            status=AcquisitionStatus.LICENSE_VERIFIED,
            source_url=info.get("url", ""),
            license=info.get("license"),
            license_url=info.get("license_url"),
        )
        
        source_url = info.get("url", "")
        
        if "ars.usda.gov" in source_url:
            image_urls = self.find_ars_images(source_url)
        else:
            image_urls = []
        
        if not image_urls:
            record = self.update_status(record, AcquisitionStatus.FAILED, "No images found or site blocks automated access")
            return record
        
        dataset_dir = self.output_dir / dataset_id
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded = 0
        for i, img_url in enumerate(image_urls[:100]):  # Limit to first 100
            try:
                ext = ".jpg"
                dest_path = dataset_dir / f"image_{i:04d}{ext}"
                
                if dest_path.exists():
                    downloaded += 1
                    continue
                
                response = requests.get(img_url, timeout=30, allow_redirects=True)
                if response.status_code == 200:
                    with open(dest_path, "wb") as f:
                        f.write(response.content)
                    downloaded += 1
                    time.sleep(0.1)
            except Exception:
                continue
        
        record.actual_size = sum(f.stat().st_size for f in dataset_dir.glob("*") if f.is_file())
        record.image_count = downloaded
        record.valid_count = downloaded
        
        if downloaded > 0:
            record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
        else:
            record = self.update_status(record, AcquisitionStatus.FAILED, "No images downloaded")
        
        return record
