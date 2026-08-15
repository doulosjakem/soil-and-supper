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
        return None

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
        return self.update_status(record, AcquisitionStatus.FAILED, "Mendeley direct download URLs return 403. Manual download required from Mendeley dataset page.")
