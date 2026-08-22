#!/usr/bin/env python3
"""
Phase 35I — Compute exact duplicate hashes for critical dataset pairs.
"""

import hashlib
from pathlib import Path
from collections import defaultdict

RAW_DIR = Path(__file__).resolve().parent.parent / "raw"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("Computing SHA256 hashes for duplicate detection...")
    hashes = defaultdict(list)

    # Focus on datasets most likely to overlap
    priority_datasets = [
        "plants_type_30class",
        "plants_type_30class_alt",
        "hf_100crops",
        "hf_veg_bangladesh",
        "fruits262_101class_subset",
        "hf_food_veg",
    ]

    for dataset_name in priority_datasets:
        dataset_dir = RAW_DIR / dataset_name
        if not dataset_dir.exists():
            continue
        count = 0
        for img_file in dataset_dir.rglob("*"):
            if img_file.is_file() and img_file.suffix.lower() in SUPPORTED_EXTENSIONS:
                try:
                    h = compute_sha256(img_file)
                    hashes[h].append((dataset_name, str(img_file.relative_to(RAW_DIR))))
                    count += 1
                except Exception:
                    pass
        print(f"  {dataset_name}: {count} hashes computed")

    dupes = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    print(f"\nFound {len(dupes)} duplicate hash groups")

    if dupes:
        print("\nDuplicate details:")
        for h, paths in dupes.items():
            print(f"\n  Hash: {h[:32]}...")
            for dataset, path in paths:
                print(f"    - {dataset}: {path}")

    # Save results
    import json
    out_path = RAW_DIR.parent / "training_data" / "manifests" / "phase35i_duplicates.json"
    results = {
        "total_hashes": len(hashes),
        "duplicate_groups": len(dupes),
        "duplicates": [
            {"hash": h, "count": len(paths), "paths": paths}
            for h, paths in dupes.items()
        ],
    }
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {out_path}")


if __name__ == "__main__":
    main()
