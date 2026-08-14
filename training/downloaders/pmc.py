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
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(article_url, headers=headers, timeout=30)
            response.raise_for_status()
            content = response.text

            patterns = [
                r'href="(/articles/PMC\d+/bin/[^"]+\.zip)"',
                r'href="(/articles/PMC\d+/bin/[^"]+\.tar\.gz)"',
                r'data-url="(https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC\d+/bin/[^"]+\.zip)"',
                r'https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC\d+/bin/([^"\']+\.zip)',
            ]

            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    url = matches[0]
                    if not url.startswith("http"):
                        url = self.PMC_BASE + url
                    return url

            pmc_match = re.search(r'PMC(\d+)', article_url)
            if pmc_match:
                pmc_id = pmc_match.group(1)
                for filename in ["mmc1.zip", "mmc1.tar.gz", "supplementary.zip"]:
                    url = f"{self.PMC_BASE}/articles/PMC{pmc_id}/bin/{filename}"
                    try:
                        resp = requests.head(url, timeout=10, allow_redirects=True)
                        if resp.status_code == 200:
                            return url
                    except Exception:
                        continue
        except Exception:
            pass
        return None

    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        source_url = info.get("url", "")
        return self.find_supplementary_url(source_url)

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
            return self.update_status(record, AcquisitionStatus.FAILED, "No supplementary file found")

        record.download_url = url
        ext = ".zip" if ".zip" in url.lower() else ".tar.gz"
        dest_path = self.output_dir / f"{dataset_id}{ext}"
        download_meta = download_with_resume(url, dest_path)
        return self._finalize_download(record, dataset_id, info, dest_path, download_meta)
