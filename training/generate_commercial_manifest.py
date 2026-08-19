#!/usr/bin/env python3
"""
Generate a deterministic commercial training manifest for Soil & Supper.

Reads:
  - training_data/manifests/exact_dedup_manifest.jsonl  (all 136,134 post-dedup images)
  - training_data/manifests/*_manifest.jsonl            (per-dataset provenance, excluding
                                                          exact_dedup, validation, quality,
                                                          train/val/test)

Writes:
  - training_data/manifests/commercial_manifest.jsonl
  - training_data/reports/commercial_class_audit.json
  - training_data/reports/commercial_split_audit.json
  - training_data/reports/commercial_duplicate_audit.json
"""

import json
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
REPORTS_DIR = TRAINING_DATA_DIR / "reports"
PROCESSED_DIR = TRAINING_DATA_DIR / "processed"

MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

EXCLUDE_DATASETS = {"common_beans"}
REVIEW_DATASETS = {"segppd101"}
COMMERCIAL_DATASETS = {
    "plantvillage",
    "irish_potato",
    "plantdoc",
    "grapevine",
}

LICENSE_MAP = {
    "plantvillage": {
        "license": "CC0 1.0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "attribution_required": False,
        "commercial_use": True,
        "verified_from": "Meta-Album dataset page + GitHub mirror",
    },
    "irish_potato": {
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution_required": True,
        "commercial_use": True,
        "verified_from": "Zenodo API record 8286529 + peer-reviewed article (PMC12020891)",
    },
    "plantdoc": {
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution_required": True,
        "commercial_use": True,
        "verified_from": "GitHub repository LICENSE.txt",
    },
    "grapevine": {
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution_required": True,
        "commercial_use": True,
        "verified_from": "Zenodo API record 17343474 + Data in Brief article (2026)",
    },
    "common_beans": {
        "license": "CC BY-NC 4.0",
        "license_url": "https://creativecommons.org/licenses/by-nc/4.0/",
        "attribution_required": True,
        "commercial_use": False,
        "verified_from": "Zenodo API + peer-reviewed article (repository.must.ac.tz)",
    },
    "segppd101": {
        "license": "MIT (claimed)",
        "license_url": "https://opensource.org/licenses/MIT",
        "attribution_required": False,
        "commercial_use": True,
        "verified_from": "GitHub + Kaggle (now inaccessible) — REVIEW",
    },
}

SKIP_MANIFESTS = {
    "exact_dedup_manifest",
    "validation_manifest",
    "quality_manifest",
    "train_manifest",
    "val_manifest",
    "test_manifest",
}


def load_per_dataset_manifests() -> Dict[str, Dict]:
    """Build mapping from absolute path -> source info."""
    path_to_source = {}
    manifest_files = sorted(MANIFESTS_DIR.glob("*_manifest.jsonl"))

    for mf_path in manifest_files:
        stem = mf_path.stem
        # Remove trailing _manifest to get dataset prefix
        dataset_prefix = stem.rsplit("_manifest", 1)[0]
        # Skip non-source manifests
        if dataset_prefix in SKIP_MANIFESTS:
            continue
        # Skip class_mappings
        if dataset_prefix == "class_mappings":
            continue

        with open(mf_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                local_path = entry.get("local_path")
                if not local_path:
                    continue
                # local_path is relative to TRAINING_DATA_DIR
                abs_path = str((TRAINING_DATA_DIR / local_path).resolve())
                path_to_source[abs_path] = {
                    "source_dataset": entry.get("source_dataset", dataset_prefix),
                    "class": entry.get("class", ""),
                    "source_path": entry.get("source_path", ""),
                    "manifest_file": mf_path.name,
                }

    return path_to_source


def load_exact_dedup_manifest() -> List[Dict]:
    """Load all post-dedup images."""
    entries = []
    dedup_path = MANIFESTS_DIR / "exact_dedup_manifest.jsonl"
    if not dedup_path.exists():
        raise FileNotFoundError(f"Missing {dedup_path}")
    with open(dedup_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def build_commercial_manifest(dedup_entries: List[Dict], path_to_source: Dict) -> Tuple[List[Dict], Dict]:
    """Join dedup entries with source info and filter to commercial-only."""
    commercial = []
    stats = {
        "total_dedup_entries": len(dedup_entries),
        "matched_to_source": 0,
        "unmatched": 0,
        "by_source": defaultdict(int),
        "by_class": defaultdict(int),
        "excluded_common_beans": 0,
        "review_segppd101": 0,
        "duplicate_in_dedup": 0,
    }

    for entry in dedup_entries:
        abs_path = entry.get("path", "")
        source_info = path_to_source.get(abs_path)
        if source_info is None:
            stats["unmatched"] += 1
            continue
        stats["matched_to_source"] += 1

        source_dataset = source_info["source_dataset"]
        class_name = source_info["class"]

        if source_dataset in EXCLUDE_DATASETS:
            stats["excluded_common_beans"] += 1
            continue
        if source_dataset in REVIEW_DATASETS:
            stats["review_segppd101"] += 1
            continue

        if entry.get("duplicate", False):
            stats["duplicate_in_dedup"] += 1

        license_info = LICENSE_MAP.get(source_dataset, {})
        filename = abs_path.split("\\")[-1]
        image_id = f"{source_dataset}_{filename}"

        commercial.append({
            "image_id": image_id,
            "local_path": abs_path,
            "source_dataset": source_dataset,
            "source_image_id": abs_path.split("\\")[-1],
            "source_path": source_info.get("source_path", ""),
            "class": class_name,
            "license": license_info.get("license", "Unknown"),
            "license_url": license_info.get("license_url", ""),
            "commercial_use": license_info.get("commercial_use", False),
            "attribution_required": license_info.get("attribution_required", False),
            "verified_from": license_info.get("verified_from", ""),
            "sha256": entry.get("hash", ""),
            "duplicate_in_source_set": entry.get("duplicate", False),
            "inclusion_reason": "Commercially verified source dataset",
            "audit_established_by": "Phase 22 license triage + exact deduplication",
            "audit_date": "2026-08-18",
        })
        stats["by_source"][source_dataset] += 1
        stats["by_class"][class_name] += 1

    # Deterministic ordering: sort by absolute path
    commercial.sort(key=lambda e: e["local_path"])
    return commercial, stats


def write_commercial_manifest(commercial: List[Dict], output_path: Path):
    """Write commercial manifest as JSONL with metadata header."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps({
            "manifest_type": "commercial_training",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generated_by": "generate_commercial_manifest.py",
            "total_images": len(commercial),
            "excluded_sources": {
                "common_beans": "CC BY-NC 4.0 — non-commercial restriction",
                "segppd101": "MIT claimed but primary sources inaccessible — REVIEW",
            },
            "commercial_sources": {
                "plantvillage": "CC0 1.0 — 54,284 images",
                "irish_potato": "CC BY 4.0 — 38,554 images",
                "plantdoc": "CC BY 4.0 — 2,559 images",
                "grapevine": "CC BY 4.0 — 3,245 images",
            },
        }) + "\n")
        for entry in commercial:
            f.write(json.dumps(entry) + "\n")


def generate_class_audit(commercial: List[Dict]) -> Dict:
    """Generate class balance report for commercial images."""
    by_class = defaultdict(int)
    by_class_source = defaultdict(lambda: defaultdict(int))
    for entry in commercial:
        cls = entry["class"]
        src = entry["source_dataset"]
        by_class[cls] += 1
        by_class_source[cls][src] += 1

    total = len(commercial)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_commercial_images": total,
        "classes": {},
    }

    for cls in sorted(by_class.keys()):
        count = by_class[cls]
        pct = round(count / total * 100, 2) if total > 0 else 0.0
        sources = dict(sorted(by_class_source[cls].items()))
        num_sources = len(sources)
        dominant_source = max(sources, key=sources.get) if sources else ""
        dominant_pct = round(sources.get(dominant_source, 0) / count * 100, 2) if count > 0 else 0.0

        report["classes"][cls] = {
            "count": count,
            "percentage": pct,
            "num_sources": num_sources,
            "sources": sources,
            "dominant_source": dominant_source,
            "dominant_source_percentage": dominant_pct,
            "disproportionately_dependent": dominant_pct > 80 and num_sources == 1,
        }

    return report


def load_split_manifest(split_name: str) -> List[Dict]:
    """Load train/val/test manifest which contains canonical paths."""
    manifest_path = MANIFESTS_DIR / f"{split_name}_manifest.json"
    if not manifest_path.exists():
        return []
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_existing_splits(path_to_source: Dict) -> Dict:
    """Check what percentage of current train/val/test splits are commercial."""
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "splits": {},
        "total_commercial_in_splits": 0,
        "total_excluded_in_splits": 0,
        "total_review_in_splits": 0,
        "unknown_in_splits": 0,
    }

    for split_name in ["train", "val", "test"]:
        entries = load_split_manifest(split_name)
        total = 0
        commercial = 0
        excluded = 0
        review = 0
        unknown = 0
        class_counts = defaultdict(int)
        for entry in entries:
            abs_path = entry.get("path", "")
            if not abs_path:
                continue
            total += 1
            source_info = path_to_source.get(abs_path)
            if source_info is None:
                unknown += 1
                continue
            src = source_info["source_dataset"]
            cls = entry.get("class", source_info.get("class", ""))
            class_counts[cls] += 1
            if src in EXCLUDE_DATASETS:
                excluded += 1
            elif src in REVIEW_DATASETS:
                review += 1
            elif src in COMMERCIAL_DATASETS:
                commercial += 1
            else:
                unknown += 1

        report["splits"][split_name] = {
            "total": total,
            "commercial": commercial,
            "excluded": excluded,
            "review": review,
            "unknown": unknown,
            "class_distribution": dict(sorted(class_counts.items())),
        }
        report["total_commercial_in_splits"] += commercial
        report["total_excluded_in_splits"] += excluded
        report["total_review_in_splits"] += review
        report["unknown_in_splits"] += unknown

    return report


def audit_duplicates(commercial: List[Dict]) -> Dict:
    """Lightweight duplicate audit on commercial core."""
    # Check exact duplicates by SHA256
    hash_counts = defaultdict(int)
    for entry in commercial:
        h = entry.get("sha256", "")
        if h:
            hash_counts[h] += 1

    exact_dups = {h: c for h, c in hash_counts.items() if c > 1}
    exact_dup_images = sum(c - 1 for c in exact_dups.values())

    # Check for cross-source duplicates (same SHA256 from different source datasets)
    hash_to_sources = defaultdict(set)
    for entry in commercial:
        h = entry.get("sha256", "")
        if h:
            hash_to_sources[h].add(entry["source_dataset"])

    cross_source = {h: srcs for h, srcs in hash_to_sources.items() if len(srcs) > 1}

    # Phash dedup was already performed in Phase 20 (~22,727 images removed)
    # We report this as historical context.
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commercial_images_audited": len(commercial),
        "exact_duplicate_hashes": len(exact_dups),
        "exact_duplicate_images": exact_dup_images,
        "cross_source_duplicate_hashes": len(cross_source),
        "cross_source_examples": list(cross_source.items())[:20],
        "note": "Phase 20 phash deduplication already removed ~22,727 near-duplicates from the full dataset. Exact deduplication removed 1 duplicate. This audit checks the remaining commercial core.",
    }
    return report


def main():
    print("Loading per-dataset manifests...")
    path_to_source = load_per_dataset_manifests()
    print(f"  Loaded {len(path_to_source)} path->source mappings")

    print("Loading exact dedup manifest...")
    dedup_entries = load_exact_dedup_manifest()
    print(f"  Loaded {len(dedup_entries)} entries")

    print("Building commercial manifest...")
    commercial, stats = build_commercial_manifest(dedup_entries, path_to_source)
    print(f"  Commercial images: {len(commercial)}")
    print(f"  Excluded (common_beans): {stats['excluded_common_beans']}")
    print(f"  Review (segppd101): {stats['review_segppd101']}")
    print(f"  Unmatched paths: {stats['unmatched']}")

    manifest_path = MANIFESTS_DIR / "commercial_manifest.jsonl"
    print(f"Writing commercial manifest to {manifest_path}...")
    write_commercial_manifest(commercial, manifest_path)

    # Class audit
    print("Generating class audit...")
    class_audit = generate_class_audit(commercial)
    audit_path = REPORTS_DIR / "commercial_class_audit.json"
    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(class_audit, f, indent=2)
    print(f"  Written to {audit_path}")

    # Existing split analysis
    print("Analyzing existing splits...")
    split_audit = analyze_existing_splits(path_to_source)
    split_path = REPORTS_DIR / "commercial_split_audit.json"
    with open(split_path, "w", encoding="utf-8") as f:
        json.dump(split_audit, f, indent=2)
    print(f"  Written to {split_path}")

    # Duplicate audit
    print("Auditing duplicates in commercial core...")
    dup_audit = audit_duplicates(commercial)
    dup_path = REPORTS_DIR / "commercial_duplicate_audit.json"
    with open(dup_path, "w", encoding="utf-8") as f:
        json.dump(dup_audit, f, indent=2)
    print(f"  Written to {dup_path}")

    # Summary
    print("\n" + "=" * 60)
    print("COMMERCIAL MANIFEST SUMMARY")
    print("=" * 60)
    print(f"Total commercial images: {len(commercial)}")
    print(f"Excluded (common_beans): {stats['excluded_common_beans']}")
    print(f"Review (segppd101): {stats['review_segppd101']}")
    print(f"Unmatched: {stats['unmatched']}")
    print("\nBy source:")
    for src, count in sorted(stats["by_source"].items()):
        print(f"  {src}: {count}")
    print("\nBy class:")
    for cls, count in sorted(stats["by_class"].items()):
        print(f"  {cls}: {count}")

    print("\nExisting split commercial percentages:")
    for split_name, info in split_audit["splits"].items():
        total = info["total"]
        comm = info["commercial"]
        pct = round(comm / total * 100, 1) if total > 0 else 0
        print(f"  {split_name}: {comm}/{total} = {pct}% commercial")

    print("\nDuplicate audit:")
    print(f"  Exact duplicate hashes: {dup_audit['exact_duplicate_hashes']}")
    print(f"  Exact duplicate images: {dup_audit['exact_duplicate_images']}")
    print(f"  Cross-source duplicates: {dup_audit['cross_source_duplicate_hashes']}")


if __name__ == "__main__":
    main()
