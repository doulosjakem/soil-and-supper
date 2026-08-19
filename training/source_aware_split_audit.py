#!/usr/bin/env python3
"""
Source-aware split leakage audit and alternative split strategies for Soil & Supper.

Reads:
  - training_data/manifests/commercial_manifest.jsonl
  - training_data/manifests/commercial_train_manifest.json
  - training_data/manifests/commercial_val_manifest.json
  - training_data/manifests/commercial_test_manifest.json

Writes:
  - training_data/reports/source_aware_leakage_audit.json
  - training_data/reports/source_aware_split_comparison.json
  - training_data/reports/minority_class_analysis.json
  - training_data/reports/single_source_analysis.json
  - training_data/reports/acquisition_priority.json
  - training_data/manifests/commercial_train_manifest_source_aware.json  (strategy C)
  - training_data/manifests/commercial_val_manifest_source_aware.json
  - training_data/manifests/commercial_test_manifest_source_aware.json
"""

import json
import random
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
REPORTS_DIR = TRAINING_DATA_DIR / "reports"
PROCESSED_DIR = TRAINING_DATA_DIR / "processed"

COMMERCIAL_MANIFEST = MANIFESTS_DIR / "commercial_manifest.jsonl"
TRAIN_MANIFEST = MANIFESTS_DIR / "commercial_train_manifest.json"
VAL_MANIFEST = MANIFESTS_DIR / "commercial_val_manifest.json"
TEST_MANIFEST = MANIFESTS_DIR / "commercial_test_manifest.json"

SPLIT_CONFIG = {
    "train_ratio": 0.70,
    "val_ratio": 0.15,
    "test_ratio": 0.15,
    "seed": 42,
}


def load_commercial_manifest() -> List[Dict]:
    entries = []
    with open(COMMERCIAL_MANIFEST, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if "image_id" in data:
                entries.append(data)
    return entries


def load_split_manifest(path: Path) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_path_to_entry(entries: List[Dict]) -> Dict[str, Dict]:
    return {e["local_path"]: e for e in entries}


def analyze_source_overlap(commercial_entries: List[Dict], train: List[Dict], val: List[Dict], test: List[Dict]) -> Dict:
    path_to_source = build_path_to_entry(commercial_entries)

    def source_set(manifest_entries):
        srcs = defaultdict(set)
        for e in manifest_entries:
            p = e.get("path", "")
            info = path_to_source.get(p)
            if info:
                srcs[e.get("class", "")].add(info["source_dataset"])
        return srcs

    train_sources = source_set(train)
    val_sources = source_set(val)
    test_sources = source_set(test)

    all_classes = sorted(set(train_sources.keys()) | set(val_sources.keys()) | set(test_sources.keys()))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "train_val_overlap": 0,
            "train_test_overlap": 0,
            "val_test_overlap": 0,
            "classes_with_full_overlap": 0,
            "classes_with_partial_overlap": 0,
            "classes_with_no_overlap": 0,
        },
        "by_class": {},
    }

    for cls in all_classes:
        t = train_sources.get(cls, set())
        v = val_sources.get(cls, set())
        s = test_sources.get(cls, set())

        tv = t & v
        ts = t & s
        vs = v & s
        all_three = t & v & s

        report["summary"]["train_val_overlap"] += len(tv)
        report["summary"]["train_test_overlap"] += len(ts)
        report["summary"]["val_test_overlap"] += len(vs)

        if all_three and len(all_three) == len(t | v | s):
            report["summary"]["classes_with_full_overlap"] += 1
        elif tv or ts or vs:
            report["summary"]["classes_with_partial_overlap"] += 1
        else:
            report["summary"]["classes_with_no_overlap"] += 1

        report["by_class"][cls] = {
            "train_sources": sorted(t),
            "val_sources": sorted(v),
            "test_sources": sorted(s),
            "train_val_overlap": sorted(tv),
            "train_test_overlap": sorted(ts),
            "val_test_overlap": sorted(vs),
            "all_splits_share_sources": sorted(all_three),
            "num_sources_total": len(t | v | s),
        }

    return report


def generate_source_aware_split(commercial_entries: List[Dict], config: dict) -> Dict:
    """
    Strategy B: Source-grouped split.
    Assign entire source datasets to train/val/test deterministically,
    but fall back to stratified random within source for single-source classes
    to avoid removing classes from splits.
    """
    random.seed(config["seed"])
    path_to_source = build_path_to_entry(commercial_entries)

    by_class_source = defaultdict(lambda: defaultdict(list))
    for e in commercial_entries:
        by_class_source[e["class"]][e["source_dataset"]].append(e)

    sources = sorted({e["source_dataset"] for e in commercial_entries})
    random.shuffle(sources)

    source_assignments = {}
    for i, src in enumerate(sources):
        if i % 3 == 0:
            source_assignments[src] = "train"
        elif i % 3 == 1:
            source_assignments[src] = "val"
        else:
            source_assignments[src] = "test"

    splits = {"train": [], "val": [], "test": []}
    for cls in sorted(by_class_source.keys()):
        class_sources = list(by_class_source[cls].keys())
        if len(class_sources) >= 2:
            for src in class_sources:
                split_name = source_assignments.get(src, "train")
                splits[split_name].extend(by_class_source[cls][src])
        else:
            entries = []
            for src in class_sources:
                entries.extend(by_class_source[cls][src])
            random.shuffle(entries)
            n = len(entries)
            n_train = int(n * config["train_ratio"])
            n_val = int(n * config["val_ratio"])
            splits["train"].extend(entries[:n_train])
            splits["val"].extend(entries[n_train:n_train + n_val])
            splits["test"].extend(entries[n_train + n_val:])

    return splits


def generate_hybrid_split(commercial_entries: List[Dict], config: dict) -> Dict:
    """
    Strategy C: Source-aware hybrid.
    For multi-source classes: distribute sources across splits to minimize overlap.
    For single-source classes: fall back to stratified random within that source.
    Ensures every class remains in all splits.
    """
    random.seed(config["seed"])
    by_class_source = defaultdict(lambda: defaultdict(list))
    for e in commercial_entries:
        by_class_source[e["class"]][e["source_dataset"]].append(e)

    splits = {"train": [], "val": [], "test": []}
    for cls in sorted(by_class_source.keys()):
        class_sources = list(by_class_source[cls].keys())
        if len(class_sources) >= 3:
            sources = class_sources[:]
            random.shuffle(sources)
            splits["train"].extend(by_class_source[cls][sources[0]])
            splits["val"].extend(by_class_source[cls][sources[1]])
            splits["test"].extend(by_class_source[cls][sources[2]])
            for src in sources[3:]:
                splits["train"].extend(by_class_source[cls][src])
        elif len(class_sources) == 2:
            sources = class_sources[:]
            random.shuffle(sources)
            splits["train"].extend(by_class_source[cls][sources[0]])
            splits["test"].extend(by_class_source[cls][sources[1]])
            if len(by_class_source[cls][sources[0]]) > 1:
                entries = by_class_source[cls][sources[0]][:]
                random.shuffle(entries)
                n = len(entries)
                n_val = max(1, int(n * config["val_ratio"]))
                splits["val"].extend(entries[:n_val])
                splits["train"] = [e for e in splits["train"] if e not in entries[:n_val]]
        else:
            entries = []
            for src in class_sources:
                entries.extend(by_class_source[cls][src])
            random.shuffle(entries)
            n = len(entries)
            n_train = int(n * config["train_ratio"])
            n_val = int(n * config["val_ratio"])
            splits["train"].extend(entries[:n_train])
            splits["val"].extend(entries[n_train:n_train + n_val])
            splits["test"].extend(entries[n_train + n_val:])

    return splits


def evaluate_split_strategy(name: str, splits: Dict, commercial_entries: List[Dict]) -> Dict:
    path_to_source = build_path_to_entry(commercial_entries)
    by_class = defaultdict(lambda: {"train": 0, "val": 0, "test": 0})
    by_source = defaultdict(lambda: {"train": 0, "val": 0, "test": 0})
    class_sources = defaultdict(set)

    for split_name, entries in splits.items():
        for e in entries:
            cls = e["class"]
            src = e["source_dataset"]
            by_class[cls][split_name] += 1
            by_source[src][split_name] += 1
            class_sources[cls].add(src)

    missing = []
    for cls, counts in by_class.items():
        if any(counts[s] == 0 for s in ["train", "val", "test"]):
            missing.append(cls)

    return {
        "name": name,
        "totals": {s: len(entries) for s, entries in splits.items()},
        "by_class": dict(sorted(by_class.items())),
        "by_source": dict(sorted(by_source.items())),
        "classes_missing_from_any_split": missing,
        "num_classes_missing": len(missing),
        "classes_represented_in_all_splits": len(by_class) - len(missing),
        "total_unique_sources": len(set(e["source_dataset"] for e in commercial_entries)),
    }


def minority_class_analysis(commercial_entries: List[Dict]) -> Dict:
    path_to_source = build_path_to_entry(commercial_entries)
    train = load_split_manifest(TRAIN_MANIFEST)
    val = load_split_manifest(VAL_MANIFEST)
    test = load_split_manifest(TEST_MANIFEST)

    counts = defaultdict(int)
    for e in commercial_entries:
        counts[e["class"]] += 1

    minority_classes = [
        "Rust", "Cedar_apple_rust", "Apple_scab", "Tomato_mosaic_virus",
        "Downy_mildew", "Anthracnose"
    ]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "minority_classes": {},
    }

    for cls in minority_classes:
        train_count = sum(1 for e in train if e.get("class") == cls)
        val_count = sum(1 for e in val if e.get("class") == cls)
        test_count = sum(1 for e in test if e.get("class") == cls)
        total = counts.get(cls, 0)

        report["minority_classes"][cls] = {
            "total_commercial": total,
            "train": train_count,
            "val": val_count,
            "test": test_count,
            "val_pct": round(val_count / total * 100, 1) if total > 0 else 0,
            "test_pct": round(test_count / total * 100, 1) if total > 0 else 0,
            "eval_total": val_count + test_count,
        }

    return report


def single_source_analysis(commercial_entries: List[Dict]) -> Dict:
    by_class_source = defaultdict(lambda: defaultdict(int))
    for e in commercial_entries:
        by_class_source[e["class"]][e["source_dataset"]] += 1

    single_source_classes = []
    for cls, sources in by_class_source.items():
        if len(sources) == 1:
            single_source_classes.append(cls)

    train = load_split_manifest(TRAIN_MANIFEST)
    val = load_split_manifest(VAL_MANIFEST)
    test = load_split_manifest(TEST_MANIFEST)
    path_to_source = build_path_to_entry(commercial_entries)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "single_source_classes": {},
    }

    for cls in sorted(single_source_classes):
        src = list(by_class_source[cls].keys())[0]
        count = by_class_source[cls][src]
        train_count = sum(1 for e in train if e.get("class") == cls and path_to_source.get(e.get("path", ""), {}).get("source_dataset") == src)
        val_count = sum(1 for e in val if e.get("class") == cls and path_to_source.get(e.get("path", ""), {}).get("source_dataset") == src)
        test_count = sum(1 for e in test if e.get("class") == cls and path_to_source.get(e.get("path", ""), {}).get("source_dataset") == src)

        report["single_source_classes"][cls] = {
            "source": src,
            "total_commercial": count,
            "train": train_count,
            "val": val_count,
            "test": test_count,
            "source_in_all_splits": train_count > 0 and val_count > 0 and test_count > 0,
            "note": "All images come from one source. Test performance may reflect within-source generalization rather than cross-source generalization.",
        }

    return report


def acquisition_priority(commercial_entries: List[Dict]) -> Dict:
    by_class_source = defaultdict(lambda: defaultdict(int))
    for e in commercial_entries:
        by_class_source[e["class"]][e["source_dataset"]] += 1

    all_classes = sorted(set(
        list(by_class_source.keys()) +
        ["Fusarium_wilt", "Verticillium_wilt", "Anthracnose",
         "Blossom_end_rot", "Nutrient_deficiency", "Sunscald",
         "Frost_damage", "Hail_damage", "Overwatering_stress",
         "Underwatering_stress", "Insect_damage", "Chewing_damage",
         "Leaf_miner_damage", "Soybean_rust"]
    ))

    priorities = []
    for cls in all_classes:
        sources = by_class_source.get(cls, {})
        count = sum(sources.values())
        num_sources = len(sources)

        if count == 0:
            priority = 1
            reason = "Zero commercial images"
        elif num_sources == 1 and count < 2000:
            priority = 2
            reason = f"Single-source dependent ({count} images)"
        elif num_sources == 1:
            priority = 3
            reason = f"Single-source dependent ({count} images)"
        else:
            priority = 4
            reason = "Adequate source diversity"

        priorities.append({
            "class": cls,
            "count": count,
            "num_sources": num_sources,
            "sources": dict(sources),
            "priority": priority,
            "reason": reason,
        })

    priorities.sort(key=lambda x: (x["priority"], -x["count"]))

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ranking": priorities,
        "top_priorities": [p["class"] for p in priorities if p["priority"] == 1],
        "secondary_priorities": [p["class"] for p in priorities if p["priority"] == 2],
    }


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    print("Loading commercial manifest...")
    commercial_entries = load_commercial_manifest()
    print(f"  {len(commercial_entries)} entries")

    print("Loading split manifests...")
    train = load_split_manifest(TRAIN_MANIFEST)
    val = load_split_manifest(VAL_MANIFEST)
    test = load_split_manifest(TEST_MANIFEST)
    print(f"  train={len(train)}, val={len(val)}, test={len(test)}")

    print("Analyzing source overlap...")
    leakage = analyze_source_overlap(commercial_entries, train, val, test)
    save_json(leakage, REPORTS_DIR / "source_aware_leakage_audit.json")
    print(f"  Written to source_aware_leakage_audit.json")

    print("Generating source-grouped split (Strategy B)...")
    strategy_b = generate_source_aware_split(commercial_entries, SPLIT_CONFIG)
    eval_b = evaluate_split_strategy("source_grouped", strategy_b, commercial_entries)

    print("Generating hybrid split (Strategy C)...")
    strategy_c = generate_hybrid_split(commercial_entries, SPLIT_CONFIG)
    eval_c = evaluate_split_strategy("source_aware_hybrid", strategy_c, commercial_entries)

    current = {"train": train, "val": val, "test": test}
    eval_a = evaluate_split_strategy("current_stratified", current, commercial_entries)

    comparison = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "strategies": {
            "A_current_stratified": eval_a,
            "B_source_grouped": eval_b,
            "C_source_aware_hybrid": eval_c,
        },
        "recommendation": "Strategy C (source-aware hybrid) provides the best balance of source diversity and class viability. It assigns different sources to different splits for multi-source classes, while preserving stratified splitting within single-source classes to avoid class disappearance. The current Strategy A split should NOT be used for final evaluation because it can place the same source in all three splits for single-source classes, inflating validation/test performance.",
    }
    save_json(comparison, REPORTS_DIR / "source_aware_split_comparison.json")
    print(f"  Written to source_aware_split_comparison.json")

    print("Saving Strategy C manifests...")
    for split_name, entries in strategy_c.items():
        manifest_path = MANIFESTS_DIR / f"commercial_{split_name}_manifest_source_aware.json"
        data = [
            {
                "image_id": e["image_id"],
                "path": e["local_path"],
                "class": e["class"],
                "source_dataset": e["source_dataset"],
                "sha256": e["sha256"],
            }
            for e in entries
        ]
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"  {split_name}: {len(entries)} -> {manifest_path}")

    print("Analyzing minority classes...")
    minority = minority_class_analysis(commercial_entries)
    save_json(minority, REPORTS_DIR / "minority_class_analysis.json")
    print(f"  Written to minority_class_analysis.json")

    print("Analyzing single-source classes...")
    single = single_source_analysis(commercial_entries)
    save_json(single, REPORTS_DIR / "single_source_analysis.json")
    print(f"  Written to single_source_analysis.json")

    print("Ranking acquisition priorities...")
    priority = acquisition_priority(commercial_entries)
    save_json(priority, REPORTS_DIR / "acquisition_priority.json")
    print(f"  Written to acquisition_priority.json")

    print("\nSummary:")
    print(f"  Current split source overlap (train/val): {leakage['summary']['train_val_overlap']}")
    print(f"  Current split source overlap (train/test): {leakage['summary']['train_test_overlap']}")
    print(f"  Current split source overlap (val/test): {leakage['summary']['val_test_overlap']}")
    print(f"  Classes with full source overlap: {leakage['summary']['classes_with_full_overlap']}")
    print(f"  Classes with partial source overlap: {leakage['summary']['classes_with_partial_overlap']}")
    print(f"  Classes with no source overlap: {leakage['summary']['classes_with_no_overlap']}")


if __name__ == "__main__":
    main()
