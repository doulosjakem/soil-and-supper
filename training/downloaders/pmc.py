#!/usr/bin/env python3
"""
PMC/BDFlower downloader for Soil & Supper ML pipeline.
Downloads supplementary files from PubMed Central articles.
"""

import re
from pathlib import Path
from typing import Dict, Optional

import requests

from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus
from .shared import download_with_resume


class PMCDownloader(BaseDownloader):
    PMC_BASE = "https://pmc.ncbi.nlm.nih.gov"

    def find_supplementary_url(self, article_url: str) -> Optional[str]:
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
        return self.update_status(record, AcquisitionStatus.FAILED, "PMC supplementary download returns reCAPTCHA. Manual download required from PMC article page.")
