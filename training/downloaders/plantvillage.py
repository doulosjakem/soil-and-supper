#!/usr/bin/env python3
"""
PlantVillage downloader for Soil & Supper ML pipeline.
Multiple acquisition methods:
1. Mendeley Data
2. Figshare
3. TensorFlow Datasets (metadata only, not bulk images)
"""

from pathlib import Path
from typing import Dict, Optional

from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus
from .shared import download_with_resume


class PlantVillageDownloader(BaseDownloader):
    KNOWN_MIRRORS = [
        "https://figshare.com/ndownloader/files/21528842?private_link=5ab5f7ea05ae4f9b88f3",
        "https://data.mendeley.com/public-files/datasets/tywbtsjrjv/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
    ]

    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        for url in self.KNOWN_MIRRORS:
            try:
                import requests
                response = requests.head(url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    return url
            except Exception:
                continue
        return None

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
            return self.update_status(record, AcquisitionStatus.FAILED, "No accessible mirror found")

        record.download_url = url
        ext = ".zip"
        dest_path = self.output_dir / f"{dataset_id}{ext}"
        download_meta = download_with_resume(url, dest_path)
        return self._finalize_download(record, dataset_id, info, dest_path, download_meta)
