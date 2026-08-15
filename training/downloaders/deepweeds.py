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
        return self.update_status(record, AcquisitionStatus.FAILED, "Google Drive returns virus scan warning; Zenodo returns 403. Manual download required.")
