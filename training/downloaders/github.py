#!/usr/bin/env python3
"""
GitHub release/asset downloader for Soil & Supper ML pipeline.
Used for datasets hosted on GitHub with release assets.
"""

import zipfile
from pathlib import Path
from typing import Dict, Optional

from . import BaseDownloader, AcquisitionRecord, AcquisitionStatus
from .shared import download_with_resume, verify_archive


class GitHubDownloader(BaseDownloader):
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        repo_url = info.get("url", "")
        if "github.com" not in repo_url:
            return None

        api_url = repo_url.replace("github.com", "api.github.com/repos")
        if not api_url.endswith("/"):
            api_url += "/"
        api_url += "releases/latest"

        try:
            import requests
            response = requests.get(api_url, timeout=30)
            if response.status_code == 200:
                release = response.json()
                assets = release.get("assets", [])
                for asset in assets:
                    if asset["name"].endswith((".zip", ".tar.gz", ".tgz")):
                        return asset["browser_download_url"]
        except Exception:
            pass
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
            return self.update_status(record, AcquisitionStatus.FAILED, "No downloadable asset found")

        record.download_url = url
        dest_path = self.output_dir / f"{dataset_id}.zip"
        download_meta = download_with_resume(url, dest_path)
        return self._finalize_download(record, dataset_id, info, dest_path, download_meta)
