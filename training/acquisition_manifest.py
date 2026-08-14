#!/usr/bin/env python3
"""
Dataset acquisition manifest for Soil & Supper ML pipeline.
Tracks the state of each dataset through the acquisition pipeline.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)


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


class AcquisitionManifest:
    """Track dataset acquisition state."""
    
    def __init__(self, manifest_path: Path = MANIFESTS_DIR / "acquisition_manifest.jsonl"):
        self.manifest_path = manifest_path
        self.records: Dict[str, AcquisitionRecord] = {}
        self.load_records()
    
    def load_records(self):
        """Load existing records from manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        record = AcquisitionRecord(
                            dataset_id=data["dataset_id"],
                            name=data["name"],
                            status=AcquisitionStatus(data["status"]),
                            source_url=data["source_url"],
                            download_url=data.get("download_url"),
                            license=data.get("license"),
                            license_url=data.get("license_url"),
                            file_size=data.get("file_size"),
                            actual_size=data.get("actual_size"),
                            checksum=data.get("checksum"),
                            image_count=data.get("image_count"),
                            valid_count=data.get("valid_count"),
                            classes=data.get("classes"),
                            error=data.get("error"),
                            timestamp=data.get("timestamp", datetime.now().isoformat()),
                        )
                        self.records[record.dataset_id] = record
    
    def save_record(self, record: AcquisitionRecord):
        """Save or update a record."""
        self.records[record.dataset_id] = record
        with open(self.manifest_path, "a") as f:
            f.write(json.dumps(record.to_dict()) + "\n")
    
    def get_record(self, dataset_id: str) -> Optional[AcquisitionRecord]:
        """Get record by dataset ID."""
        return self.records.get(dataset_id)
    
    def get_records_by_status(self, status: AcquisitionStatus) -> List[AcquisitionRecord]:
        """Get all records with a specific status."""
        return [r for r in self.records.values() if r.status == status]
    
    def get_training_ready(self) -> List[AcquisitionRecord]:
        """Get all training-ready datasets."""
        return self.get_records_by_status(AcquisitionStatus.TRAINING_READY)
    
    def get_failed(self) -> List[AcquisitionRecord]:
        """Get all failed datasets."""
        return self.get_records_by_status(AcquisitionStatus.FAILED)
    
    def generate_report(self) -> Dict:
        """Generate acquisition summary report."""
        total = len(self.records)
        by_status = {}
        for status in AcquisitionStatus:
            by_status[status.value] = len(self.get_records_by_status(status))
        
        total_images = sum(r.image_count or 0 for r in self.records.values())
        total_valid = sum(r.valid_count or 0 for r in self.records.values())
        
        return {
            "generated_at": datetime.now().isoformat(),
            "total_datasets": total,
            "by_status": by_status,
            "total_images": total_images,
            "total_valid_images": total_valid,
            "training_ready": [r.dataset_id for r in self.get_training_ready()],
            "failed": [{"dataset_id": r.dataset_id, "error": r.error} for r in self.get_failed()],
        }
    
    def print_summary(self):
        """Print human-readable summary."""
        report = self.generate_report()
        
        print("=" * 60)
        print("ACQUISITION MANIFEST SUMMARY")
        print("=" * 60)
        print(f"Total datasets: {report['total_datasets']}")
        print(f"Total images: {report['total_images']}")
        print(f"Total valid: {report['total_valid_images']}")
        print("\nBy status:")
        for status, count in report["by_status"].items():
            print(f"  {status}: {count}")
        
        if report["training_ready"]:
            print(f"\nTraining ready: {', '.join(report['training_ready'])}")
        
        if report["failed"]:
            print(f"\nFailed datasets:")
            for failure in report["failed"]:
                print(f"  {failure['dataset_id']}: {failure['error']}")


if __name__ == "__main__":
    manifest = AcquisitionManifest()
    manifest.print_summary()
