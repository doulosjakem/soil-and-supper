#!/usr/bin/env python3
"""
Phase 35I — Final corrected dedup counts with fixed synonyms.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple

MANIFESTS_DIR = Path(__file__).resolve().parent.parent / "training_data" / "manifests"
LEDGER_PATH = MANIFESTS_DIR / "phase35d_dataset_ledger.jsonl"

TIER1_CLASSES = [
    "Tomato", "Pepper", "Eggplant", "Potato", "Cucumber",
    "Summer Squash / Zucchini", "Winter Squash / Pumpkin", "Corn", "Bean", "Pea",
    "Carrot", "Beet", "Radish", "Turnip", "Onion", "Garlic", "Leek",
    "Broccoli", "Cabbage", "Cauliflower", "Brussels Sprouts", "Kale", "Lettuce", "Spinach", "Swiss Chard", "Sweet Potato",
    "Watermelon", "Cantaloupe",
    "Strawberry", "Raspberry / Blackberry", "Blueberry", "Grape",
    "Apple", "Pear", "Peach", "Cherry", "Plum", "Apricot", "Nectarine",
    "Basil", "Cilantro", "Parsley", "Dill", "Chives", "Mint", "Rosemary", "Thyme",
    "Asparagus", "Rhubarb", "Hops", "Sunflower",
]

TIER1_CLASSES_LOWER = {c.lower(): c for c in TIER1_CLASSES}

SYNONYMS = {
    "capsicum": "Pepper", "bell pepper": "Pepper", "chilli pepper": "Pepper", "chili pepper": "Pepper",
    "brinjal": "Eggplant", "aubergine": "Eggplant",
    "flat bean": "Bean", "green bean": "Bean", "french bean": "Bean", "kidney bean": "Bean",
    "soy bean": "Bean", "soybean": "Bean", "mung bean": "Bean", "green gram": "Bean",
    "maize": "Corn", "sweetcorn": "Corn", "sweet corn": "Corn",
    "zucchini": "Summer Squash / Zucchini", "courgette": "Summer Squash / Zucchini",
    "pumpkin": "Winter Squash / Pumpkin",
    "beet": "Beet", "beetroot": "Beet",
    "brussels sprout": "Brussels Sprouts",
    "swiss chard": "Swiss Chard", "silverbeet": "Swiss Chard",
    "sweet potato": "Sweet Potato", "sweet potatoes": "Sweet Potato", "sweetpotatoes": "Sweet Potato",
    "raspberry": "Raspberry / Blackberry", "blackberry": "Raspberry / Blackberry",
    "coriander": "Cilantro",
    "muskmelon": "Cantaloupe",
    "raddish": "Radish", "carrots": "Carrot",
    "tomato": "Tomato", "potato": "Potato", "cucumber": "Cucumber", "carrot": "Carrot",
    "onion": "Onion", "garlic": "Garlic", "pepper": "Pepper", "eggplant": "Eggplant",
    "broccoli": "Broccoli", "cabbage": "Cabbage", "cauliflower": "Cauliflower",
    "corn": "Corn", "lettuce": "Lettuce", "spinach": "Spinach",
    "strawberry": "Strawberry", "blueberry": "Blueberry", "grape": "Grape",
    "apple": "Apple", "pear": "Pear", "peach": "Peach", "cherry": "Cherry",
    "plum": "Plum", "apricot": "Apricot", "nectarine": "Nectarine",
    "basil": "Basil", "mint": "Mint", "rosemary": "Rosemary", "thyme": "Thyme",
    "parsley": "Parsley", "dill": "Dill", "chives": "Chives",
    "asparagus": "Asparagus", "rhubarb": "Rhubarb", "sunflower": "Sunflower",
    "arum lobe": "Arum lobe", "ash gourd": "Ash Gourd", "bitter melon": "Bitter Melon",
    "bottle gourd": "Bottle Gourd", "chili": "Chili",
    "chives onion": "Chives Onion", "coconut": "Coconut", "coriander": "Coriander",
    "elephant foot yam": "Elephant foot yam", "flat bean": "Flat Bean",
    "gooseberry": "Gooseberry", "green papaya": "Green Papaya",
    "green spinach": "Green Spinach", "jicama": "Jicama", "kohlrabi": "Kohlrabi",
    "lime": "Lime", "malabar spinach seed": "Malabar Spinach Seed",
    "okra": "Okra", "plantain": "Plantain", "pointed gourd": "Pointed Gourd",
    "radish leaves": "Radish Leaves", "red amaranth": "Red Amaranth",
    "shaluk": "Shaluk", "snake gourd": "Snake Gourd", "taro": "Taro",
    "yardlong bean": "Yardlong bean", "ladies finger": "Ladies finger",
    "bitter gourd": "Bitter Gourd",
    "long beans": "Bean", "peper chili": "Pepper", "peperchili": "Pepper",
    "bean": "Bean", "green chili": "Pepper",
    "chile pepper": "Pepper", "new mexico green chile": "Pepper",
}


def auto_map_class(source_label: str) -> Tuple[str, str]:
    source_lower = source_label.lower().strip()
    source_lower = re.sub(r'^\d+\.\s*', '', source_lower)
    if source_lower in TIER1_CLASSES_LOWER:
        return TIER1_CLASSES_LOWER[source_lower], "high"
    if source_lower in SYNONYMS:
        return SYNONYMS[source_lower], "high"
    return None, "none"


def extract_class_from_path(img_path: str, dataset_id: str) -> str:
    p = Path(img_path)
    parts = [part.lower() for part in p.parts]

    if dataset_id == "bangladesh_veg_inbox":
        for i, part in enumerate(parts):
            if part == "actual_dataset" and i + 1 < len(parts):
                return parts[i + 1]
        return p.parent.name.lower()

    elif dataset_id == "veg_bangla_inbox":
        for i, part in enumerate(parts):
            if part == "dataset" and i + 1 < len(parts):
                return parts[i + 1]
        return p.parent.name.lower()

    elif dataset_id == "vegnet_inbox":
        for i, part in enumerate(parts):
            if part == "new vegnet" and i + 1 < len(parts):
                return parts[i + 1]
        return p.parent.name.lower()

    elif dataset_id == "veg_object_bangla_inbox":
        return "veg_object_bangla_flat"

    return p.parent.name.lower()


def main():
    print("Loading ledger...")
    ledger = []
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ledger.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    approved_ids = {
        "bangladesh_veg_inbox", "fruits262_101class_subset", "hf_100crops",
        "hf_digigreen", "hf_food_ingredients_v2", "hf_food_veg",
        "hf_veg_bangladesh", "plants_type_30class", "plants_type_30class_alt",
        "veg_bangla_inbox", "veg_object_bangla_inbox", "vegnet_inbox", "zenodo_vegann",
    }

    path_extract_ids = {
        "bangladesh_veg_inbox",
        "veg_bangla_inbox",
        "vegnet_inbox",
        "veg_object_bangla_inbox",
    }

    hash_to_class = {}
    total_records = 0
    valid_records = 0
    conflict_count = 0
    conflicts = []

    for entry in ledger:
        ds_id = entry.get("dataset_id")
        if ds_id not in approved_ids or entry.get("status") != "APPROVED":
            continue

        image_records = entry.get("image_records", [])
        for rec in image_records:
            total_records += 1
            if not rec.get("valid", False):
                continue
            valid_records += 1

            h = rec.get("hash", "")
            if not h or h == "dir":
                continue

            path = rec.get("path", "")
            source_class = rec.get("source_class", "")

            if ds_id in path_extract_ids:
                extracted = extract_class_from_path(path, ds_id)
                target, conf = auto_map_class(extracted)
            else:
                target, conf = auto_map_class(source_class)

            if target:
                if h in hash_to_class:
                    existing_class = hash_to_class[h][0]
                    if existing_class != target:
                        conflict_count += 1
                        if conflict_count <= 50:
                            conflicts.append({
                                "hash": h[:16],
                                "existing": existing_class,
                                "new": target,
                                "dataset": ds_id,
                                "path": path,
                            })
                else:
                    hash_to_class[h] = (target, ds_id, path)

    print(f"Total image records: {total_records}")
    print(f"Valid image records: {valid_records}")
    print(f"Unique valid mapped images: {len(hash_to_class)}")
    print(f"Cross-class conflicts: {conflict_count}")

    class_counts = defaultdict(int)
    class_sources = defaultdict(set)
    for h, (cls, ds_id, path) in hash_to_class.items():
        class_counts[cls] += 1
        class_sources[cls].add(ds_id)

    print("\n" + "=" * 80)
    print("POST-DEDUP CLASS COVERAGE (FINAL)")
    print("=" * 80)

    class_results = {}
    for cls in TIER1_CLASSES:
        count = class_counts.get(cls, 0)
        sources = sorted(list(class_sources.get(cls, set())))
        class_results[cls] = {
            "approved_images": count,
            "source_dataset_count": len(sources),
            "sources": sources,
            "status": "APPROVED" if count > 0 else "NO_DATA",
            "domain": "CROP / PLANT ID",
        }
        if count > 0:
            print(f"  {cls}: {count} images from {len(sources)} sources")

    total_with_data = sum(1 for c in class_results.values() if c["status"] == "APPROVED")
    total_images = sum(c["approved_images"] for c in class_results.values())
    print(f"\nTotal Tier 1 classes with data: {total_with_data}")
    print(f"Total unique mapped images: {total_images}")

    counts = [c["approved_images"] for c in class_results.values() if c["approved_images"] > 0]
    if counts:
        print(f"Min: {min(counts)}, Max: {max(counts)}, Median: {sorted(counts)[len(counts)//2]}, Mean: {sum(counts)/len(counts):.1f}")
        print(f"Imbalance ratio: {max(counts)/max(min(counts),1):.1f}:1")

    # Save conflicts
    conflicts_path = MANIFESTS_DIR / "phase35i_conflicts.json"
    with open(conflicts_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_conflicts": conflict_count,
            "conflicts": conflicts,
        }, f, indent=2, ensure_ascii=False)

    coverage_output = MANIFESTS_DIR / "phase35i_class_coverage_deduped.json"
    with open(coverage_output, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_tier1_classes": len(TIER1_CLASSES),
            "classes_with_data": total_with_data,
            "classes": class_results,
        }, f, indent=2, ensure_ascii=False)
    print(f"\nConflicts saved to: {conflicts_path}")
    print(f"Post-dedup coverage saved to: {coverage_output}")


if __name__ == "__main__":
    main()
