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
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
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
        return self.update_status(record, AcquisitionStatus.FAILED, "All automatic download URLs stale (Mendeley 403, Figshare 202/0 bytes). Manual download required.")
