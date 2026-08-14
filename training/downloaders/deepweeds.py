#!/usr/bin/env python3
"""
DeepWeeds downloader for Soil & Supper ML pipeline.
Downloads images from Zenodo (primary) or Google Drive (fallback).
"""

from pathlib import Path
from typing import Dict, Optional

from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus
from .shared import download_with_resume


class DeepWeedsDownloader(BaseDownloader):
    ZENODO_URL = "https://zenodo.org/records/7939060/files/images.zip?download=1"
    GOOGLE_DRIVE_URL = "https://drive.google.com/uc?export=download&id=1xnK3B6K6KekDI55vwJ0vnc2IGoDga9cj"

    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        import requests
        try:
            response = requests.head(self.ZENODO_URL, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                return self.ZENODO_URL
        except Exception:
            pass
        return self.GOOGLE_DRIVE_URL

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
        record.download_url = url
        dest_path = self.output_dir / f"{dataset_id}_images.zip"
        download_meta = download_with_resume(url, dest_path)
        return self._finalize_download(record, dataset_id, info, dest_path, download_meta)
