#!/usr/bin/env python3
"""
Base download adapter interface for Soil & Supper ML pipeline.
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from .shared import (
    download_with_resume,
    verify_archive,
    compute_sha256,
    detect_known_error_page,
    is_html_or_error,
)


class AcquisitionStatus:
    DISCOVERED = "discovered"
    LICENSE_VERIFIED = "license_verified"
    DOWNLOADABLE = "downloadable"
    DOWNLOADED = "downloaded"
    EXTRACTED = "extracted"
    VALIDATED = "validated"
    DEDUPLICATED = "deduplicated"
    TRAINING_READY = "training_ready"
    FAILED = "failed"
    HOLD = "hold"


class AcquisitionRecord:
    def __init__(
        self,
        dataset_id: str,
        name: str,
        status: str,
        source_url: str,
        download_url: Optional[str] = None,
        license: Optional[str] = None,
        license_url: Optional[str] = None,
        file_size: Optional[int] = None,
        actual_size: Optional[int] = None,
        checksum: Optional[str] = None,
        image_count: Optional[int] = None,
        valid_count: Optional[int] = None,
        classes: Optional[list] = None,
        error: Optional[str] = None,
        http_status: Optional[int] = None,
        final_url: Optional[str] = None,
        content_type: Optional[str] = None,
        failure_reason: Optional[str] = None,
    ):
        self.dataset_id = dataset_id
        self.name = name
        self.status = status
        self.source_url = source_url
        self.download_url = download_url
        self.license = license
        self.license_url = license_url
        self.file_size = file_size
        self.actual_size = actual_size
        self.checksum = checksum
        self.image_count = image_count
        self.valid_count = valid_count
        self.classes = classes or []
        self.error = error
        self.http_status = http_status
        self.final_url = final_url
        self.content_type = content_type
        self.failure_reason = failure_reason
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "dataset_id": self.dataset_id,
            "name": self.name,
            "status": self.status,
            "source_url": self.source_url,
            "download_url": self.download_url,
            "license": self.license,
            "license_url": self.license_url,
            "file_size": self.file_size,
            "actual_size": self.actual_size,
            "checksum": self.checksum,
            "image_count": self.image_count,
            "valid_count": self.valid_count,
            "classes": self.classes,
            "error": self.error,
            "http_status": self.http_status,
            "final_url": self.final_url,
            "content_type": self.content_type,
            "failure_reason": self.failure_reason,
            "timestamp": self.timestamp,
        }


class BaseDownloader(ABC):
    def __init__(self, output_dir: Path, manifest_dir: Path):
        self.output_dir = Path(output_dir)
        self.manifest_dir = Path(manifest_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        pass

    @abstractmethod
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        pass

    def save_record(self, record: AcquisitionRecord):
        manifest_path = self.manifest_dir / "acquisition_manifest.jsonl"
        with open(manifest_path, "a") as f:
            f.write(json.dumps(record.to_dict()) + "\n")

    def update_status(self, record: AcquisitionRecord, status: str, error: str = None):
        record.status = status
        if error:
            record.error = error
        record.timestamp = datetime.now().isoformat()
        self.save_record(record)
        return record

    def _finalize_download(
        self,
        record: AcquisitionRecord,
        dataset_id: str,
        info: Dict,
        dest_path: Path,
        download_meta: Dict,
    ) -> AcquisitionRecord:
        record.http_status = download_meta.get("http_status")
        record.final_url = download_meta.get("final_url")
        record.content_type = download_meta.get("content_type")
        record.actual_size = download_meta.get("actual_size")
        record.checksum = download_meta.get("checksum")

        if not download_meta.get("success"):
            record = self.update_status(
                record,
                AcquisitionStatus.FAILED,
                download_meta.get("error", "Download failed"),
            )
            record.failure_reason = download_meta.get("error")
            return record

        html_reason = detect_known_error_page(dest_path)
        if html_reason:
            record.failure_reason = html_reason
            failed_path = dest_path.with_suffix(dest_path.suffix + ".failed")
            try:
                dest_path.rename(failed_path)
            except OSError:
                pass
            record = self.update_status(
                record,
                AcquisitionStatus.FAILED,
                f"Downloaded error page: {html_reason}",
            )
            return record

        html, reason = is_html_or_error(dest_path)
        if html:
            failed_path = dest_path.with_suffix(dest_path.suffix + ".failed")
            try:
                dest_path.rename(failed_path)
            except OSError:
                pass
            record.failure_reason = reason
            record = self.update_status(
                record,
                AcquisitionStatus.FAILED,
                f"File is not a valid dataset: {reason}",
            )
            return record

        archive_info = verify_archive(dest_path)
        if not archive_info["valid"]:
            failed_path = dest_path.with_suffix(dest_path.suffix + ".failed")
            try:
                dest_path.rename(failed_path)
            except OSError:
                pass
            record.failure_reason = archive_info.get("error")
            record = self.update_status(
                record,
                AcquisitionStatus.FAILED,
                archive_info.get("error", "Invalid archive"),
            )
            return record

        record.image_count = archive_info.get("image_count", 0)
        record.file_size = download_meta.get("content_length") or download_meta.get("actual_size")
        record = self.update_status(record, AcquisitionStatus.DOWNLOADED)
        return record
