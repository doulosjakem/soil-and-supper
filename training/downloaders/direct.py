#!/usr/bin/env python3
"""
Direct HTTP downloader for Soil & Supper ML pipeline.
Handles datasets with direct download URLs.
"""

from pathlib import Path
from typing import Dict, Optional

from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus
from .shared import download_with_resume, verify_archive


class DirectDownloader(BaseDownloader):
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        return info.get("download_url")

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
            return self.update_status(record, AcquisitionStatus.FAILED, "No download URL provided")

        record.download_url = url
        parsed = Path(url)
        ext = parsed.suffix or ".zip"
        if ext not in {".zip", ".tar.gz", ".tgz", ".tar", ".gz"}:
            ext = ".zip"
        dest_path = self.output_dir / f"{dataset_id}{ext}"

        download_meta = download_with_resume(url, dest_path)
        return self._finalize_download(record, dataset_id, info, dest_path, download_meta)
