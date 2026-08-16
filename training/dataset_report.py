#!/usr/bin/env python3
"""
Dataset report generator for Soil & Supper ML pipeline.
Generates human-readable and machine-readable reports including data gap analysis.
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import yaml

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
PROCESSED_DIR = TRAINING_DATA_DIR / "processed"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
REPORTS_DIR = TRAINING_DATA_DIR / "reports"
CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def count_images(directory: Path) -> int:
    """Count images in directory."""
    count = 0
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
        count += len(list(directory.rglob(ext)))
    return count


def get_class_sources(class_name: str) -> Dict[str, int]:
    """Get source counts for a class from manifests."""
    sources = {}
    for mf in MANIFESTS_DIR.glob("*.jsonl"):
        if not mf.name.startswith(("download", "acquisition", "license", "quality", "validation")):
            stem = mf.stem
            if stem.endswith(f"_{class_name}_manifest"):
                source = stem.split("_")[0]
                with open(mf, "r") as f:
                    count = sum(1 for line in f if line.strip())
                if count > 0:
                    sources[source] = count
    return sources


def get_domain_stats(domain: str) -> Dict:
    """Get statistics for a domain."""
    domain_dir = PROCESSED_DIR / domain
    if not domain_dir.exists():
        return {"total": 0, "classes": {}}
    
    stats = {"total": 0, "classes": {}}
    for class_dir in domain_dir.iterdir():
        if class_dir.is_dir():
            count = count_images(class_dir)
            sources = get_class_sources(class_dir.name)
            stats["classes"][class_dir.name] = {
                "count": count,
                "sources": sources,
                "num_sources": len(sources),
            }
            stats["total"] += count
    
    return stats


def classify_strength(count: int, num_sources: int) -> str:
    """Classify class strength."""
    if count >= 1000 and num_sources >= 3:
        return "STRONG"
    elif count >= 500 and num_sources >= 2:
        return "MODERATE"
    elif count >= 100:
        return "WEAK"
    else:
        return "INSUFFICIENT"


def generate_gap_report(config: Dict) -> Dict:
    """Generate comprehensive data gap report."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "domains": {},
        "summary": {
            "total_images": 0,
            "total_classes": 0,
            "strong": 0,
            "moderate": 0,
            "weak": 0,
            "insufficient": 0,
        }
    }
    
    for domain, domain_config in config.get("domains", {}).items():
        if not domain_config.get("enabled", False):
            continue
        
        domain_stats = get_domain_stats(domain)
        domain_report = {
            "total": domain_stats["total"],
            "classes": {},
        }
        
        for cls in domain_config.get("classes", []):
            class_info = domain_stats.get("classes", {}).get(cls, {"count": 0, "num_sources": 0})
            count = class_info["count"]
            num_sources = class_info["num_sources"]
            strength = classify_strength(count, num_sources)
            
            domain_report["classes"][cls] = {
                "approved": count,
                "sources": num_sources,
                "source_breakdown": class_info.get("sources", {}),
                "status": strength,
            }
            
            report["summary"]["total_images"] += count
            report["summary"]["total_classes"] += 1
            report["summary"][strength.lower()] += 1
        
        report["domains"][domain] = domain_report
    
    return report


def generate_full_report(config: Dict):
    """Generate and save full dataset report."""
    report = generate_gap_report(config)
    
    report_path = REPORTS_DIR / "data_gap_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Saved gap report: {report_path}")
    
    print("\n" + "=" * 60)
    print("DATA GAP REPORT")
    print("=" * 60)
    
    for domain, domain_data in report["domains"].items():
        print(f"\n{domain.upper()}")
        print("-" * 40)
        for cls, info in sorted(domain_data["classes"].items()):
            status = info["status"]
            count = info["approved"]
            sources = info["sources"]
            source_breakdown = info.get("source_breakdown", {})
            marker = "OK" if status == "STRONG" else "..." if status == "MODERATE" else "!!" if status == "WEAK" else "XX"
            source_str = ", ".join(f"{s}: {c}" for s, c in sorted(source_breakdown.items()))
            print(f"  {marker} {cls}: {count} images, {sources} source(s) [{source_str}] -> {status}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    summary = report["summary"]
    print(f"Total images: {summary['total_images']}")
    print(f"Total classes: {summary['total_classes']}")
    print(f"STRONG: {summary['strong']}")
    print(f"MODERATE: {summary['moderate']}")
    print(f"WEAK: {summary['weak']}")
    print(f"INSUFFICIENT: {summary['insufficient']}")
    
    return report


if __name__ == "__main__":
    config = load_config()
    generate_full_report(config)
