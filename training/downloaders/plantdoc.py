#!/usr/bin/env python3
"""
PlantDoc downloader for Soil & Supper ML pipeline.
Downloads from GitHub repository.
"""

from pathlib import Path
from typing import Dict, Optional

from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus
from .shared import download_with_resume


class PlantDocDownloader(BaseDownloader):
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        source_url = info.get("url", "")
        if "github.com" in source_url:
            return f"{source_url}/archive/refs/heads/master.zip"
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
            return self.update_status(record, AcquisitionStatus.FAILED, "No GitHub download URL")

        record.download_url = url
        dest_path = self.output_dir / f"{dataset_id}.zip"
        download_meta = download_with_resume(url, dest_path)
        return self._finalize_download(record, dataset_id, info, dest_path, download_meta)
