#!/usr/bin/env python3
"""
Base download adapter interface for Soil & Supper ML pipeline.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime


class AcquisitionStatus(Enum):
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


@dataclass
class AcquisitionRecord:
    dataset_id: str
    name: str
    status: AcquisitionStatus
    source_url: str
    download_url: Optional[str] = None
    license: Optional[str] = None
    license_url: Optional[str] = None
    file_size: Optional[int] = None
    actual_size: Optional[int] = None
    checksum: Optional[str] = None
    image_count: Optional[int] = None
    valid_count: Optional[int] = None
    classes: Optional[List[str]] = None
    error: Optional[str] = None
    timestamp: str = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "dataset_id": self.dataset_id,
            "name": self.name,
            "status": self.status.value,
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
            "timestamp": self.timestamp,
        }


class BaseDownloader(ABC):
    """Base class for dataset download adapters."""
    
    def __init__(self, output_dir: Path, manifest_dir: Path):
        self.output_dir = output_dir
        self.manifest_dir = manifest_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def get_download_url(self, dataset_id: str, info: Dict) -> Optional[str]:
        """Get the actual download URL for a dataset."""
        pass
    
    @abstractmethod
    def download(self, dataset_id: str, info: Dict) -> AcquisitionRecord:
        """Download the dataset and return the record."""
        pass
    
    def save_record(self, record: AcquisitionRecord):
        """Save acquisition record to manifest."""
        manifest_path = self.manifest_dir / "acquisition_manifest.jsonl"
        with open(manifest_path, "a") as f:
            f.write(json.dumps(record.to_dict()) + "\n")
    
    def update_status(self, record: AcquisitionRecord, status: AcquisitionStatus, error: str = None):
        """Update record status and save."""
        record.status = status
        if error:
            record.error = error
        record.timestamp = datetime.now().isoformat()
        self.save_record(record)
        return record
