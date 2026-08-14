#!/usr/bin/env python3
"""
Zenodo downloader for Soil & Supper ML pipeline.
Uses Zenodo API to find and download records.
"""

import requests
from pathlib import Path
from typing import Dict, Optional

from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus
from .shared import download_with_resume, verify_archive


class ZenodoDownloader(BaseDownloader):
    ZENODO_API = "https://zenodo.org/api/records"

    def find_record(self, query: str) -> Optional[Dict]:
        params = {
            "q": query,
            "size": 10,
            "sort": "mostrecent",
        }
        try:
            response = requests.get(self.ZENODO_API, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for hit in data.get("hits", {}).get("hits", []):
                    metadata = hit.get("metadata", {})
                    title = metadata.get("title", "").lower()
                    if any(keyword in title.lower() for keyword in query.lower().split()):
                        return hit
        except Exception:
            pass
        return None

    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        query = info.get("name", dataset_id)
        record = self.find_record(query)
        if not record:
            return None
        files = record.get("files", [])
        for file_info in files:
            filename = file_info.get("key", "")
            if filename.endswith((".zip", ".tar.gz", ".tgz")):
                return file_info.get("links", {}).get("self")
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
            return self.update_status(record, AcquisitionStatus.FAILED, "No Zenodo record found")

        record.download_url = url
        dest_path = self.output_dir / f"{dataset_id}.zip"
        download_meta = download_with_resume(url, dest_path)
        return self._finalize_download(record, dataset_id, info, dest_path, download_meta)
