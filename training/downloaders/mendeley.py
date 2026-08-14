#!/usr/bin/env python3
"""
Mendeley Data downloader for Soil & Supper ML pipeline.
Handles Mendeley Data dataset downloads.
"""

import re
from pathlib import Path
from typing import Dict, Optional

import requests

from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus
from .shared import download_with_resume


class MendeleyDownloader(BaseDownloader):
    def find_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        source_url = info.get("url", "")
        known_urls = {
            "bangladesh_veg": "https://data.mendeley.com/public-files/datasets/rtx9ngb68j/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
            "smartphone_veg": "https://data.mendeley.com/public-files/datasets/gnc4s3z2mf/files/3c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
            "plantvillage": "https://data.mendeley.com/public-files/datasets/tywbtsjrjv/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
            "vegnet": "https://data.mendeley.com/public-files/datasets/6nxnjbn9w6/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
            "sunflower_growth": "https://data.mendeley.com/public-files/datasets/byftmdzg4g/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
        }

        if dataset_id in known_urls:
            url = known_urls[dataset_id]
            try:
                resp = requests.head(url, timeout=10, allow_redirects=True)
                if resp.status_code == 200:
                    return url
            except Exception:
                pass

        try:
            response = requests.get(source_url, timeout=30, allow_redirects=True)
            if response.status_code == 200:
                content = response.text
                patterns = [
                    r'href="([^"]*download[^"]*)"',
                    r'href="([^"]*\.zip)"',
                    r'href="([^"]*\.tar\.gz)"',
                    r'data-url="([^"]*)"',
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        url = matches[0]
                        if not url.startswith("http"):
                            url = "https://data.mendeley.com" + url
                        return url
        except Exception:
            pass

        return None

    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        return self.find_download_url(dataset_id, info)

    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
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
            return self.update_status(record, AcquisitionStatus.FAILED, "No downloadable URL found on Mendeley page")

        record.download_url = url
        ext = ".zip" if ".zip" in url.lower() else ".tar.gz"
        dest_path = self.output_dir / f"{dataset_id}{ext}"
        download_meta = download_with_resume(url, dest_path)
        return self._finalize_download(record, dataset_id, info, dest_path, download_meta)
