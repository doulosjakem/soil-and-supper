#!/usr/bin/env python3
"""Generate commercial split report from already-created manifests."""
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

MANIFESTS_DIR = Path(__file__).resolve().parent.parent / "training_data" / "manifests"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "training_data" / "reports"

SPLIT_CONFIG = {
    "train_ratio": 0.70,
    "val_ratio": 0.15,
    "test_ratio": 0.15,
    "seed": 42,
}

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    train = load_json(MANIFESTS_DIR / "commercial_train_manifest.json")
    val = load_json(MANIFESTS_DIR / "commercial_val_manifest.json")
    test = load_json(MANIFESTS_DIR / "commercial_test_manifest.json")
    splits = {"train": train, "val": val, "test": test}

    by_class = defaultdict(lambda: {"train": 0, "val": 0, "test": 0})
    by_source = defaultdict(lambda: {"train": 0, "val": 0, "test": 0})
    for split_name, entries in splits.items():
        for e in entries:
            by_class[e["class"]][split_name] += 1
            by_source[e["source_dataset"]][split_name] += 1

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "config": SPLIT_CONFIG,
        "totals": {
            split: len(entries)
            for split, entries in splits.items()
        },
        "by_class": dict(sorted(by_class.items())),
        "by_source": dict(sorted(by_source.items())),
    }

    report_path = REPORTS_DIR / "commercial_split_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Written to {report_path}")
    for split, count in report["totals"].items():
        print(f"  {split}: {count}")

if __name__ == "__main__":
    main()
