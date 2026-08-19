#!/usr/bin/env python3
"""
Data gap analysis for commercial core.

Reads commercial_class_audit.json and config.yaml-defined classes
to identify classes needing supplemental data.
"""

import json
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

REPORTS_DIR = Path(__file__).resolve().parent.parent / "training_data" / "reports"
AUDIT_PATH = REPORTS_DIR / "commercial_class_audit.json"
CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"
GAP_REPORT_PATH = REPORTS_DIR / "commercial_data_gap_report.json"

# Minimum thresholds from ML_TAXONOMY.md section 2.5
MIN_IMAGES = 100
MIN_SOURCES = 2


def load_config_classes() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("domains", {}).get("diseases", {}).get("classes", [])


def main():
    disease_classes = load_config_classes()
    with open(AUDIT_PATH, "r", encoding="utf-8") as f:
        audit = json.load(f)

    gaps = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_classes": len(disease_classes),
            "zero_images": [],
            "below_threshold": [],
            "single_source": [],
            "adequate": [],
        },
        "by_class": {},
    }

    for cls in disease_classes:
        info = audit.get("classes", {}).get(cls)
        if info is None:
            count = 0
            num_sources = 0
            sources = {}
            dominant_source = ""
            dominant_percentage = 0.0
            disproportionate = False
        else:
            count = info["count"]
            num_sources = info["num_sources"]
            sources = info.get("sources", {})
            dominant_source = info.get("dominant_source", "")
            dominant_percentage = info.get("dominant_source_percentage", 0.0)
            disproportionate = info.get("disproportionately_dependent", False)

        entry = {
            "count": count,
            "num_sources": num_sources,
            "sources": sources,
            "dominant_source": dominant_source,
            "dominant_percentage": dominant_percentage,
            "disproportionate": disproportionate,
        }

        if count == 0:
            entry["status"] = "ZERO_COMMERCIAL"
            entry["recommendation"] = "Find commercially licensed replacement dataset"
            gaps["summary"]["zero_images"].append(cls)
        elif count < MIN_IMAGES:
            entry["status"] = "BELOW_THRESHOLD"
            entry["recommendation"] = "Supplement with commercially licensed images"
            gaps["summary"]["below_threshold"].append(cls)
        elif num_sources < MIN_SOURCES:
            entry["status"] = "SINGLE_SOURCE"
            entry["recommendation"] = "Add second commercially licensed source"
            gaps["summary"]["single_source"].append(cls)
        else:
            entry["status"] = "ADEQUATE"
            gaps["summary"]["adequate"].append(cls)

        gaps["by_class"][cls] = entry

    with open(GAP_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(gaps, f, indent=2)
    print(f"Written to {GAP_REPORT_PATH}")
    print(f"Total classes: {gaps['summary']['total_classes']}")
    print(f"Zero commercial: {gaps['summary']['zero_images']}")
    print(f"Below threshold: {gaps['summary']['below_threshold']}")
    print(f"Single source: {gaps['summary']['single_source']}")
    print(f"Adequate: {gaps['summary']['adequate']}")

if __name__ == "__main__":
    main()
