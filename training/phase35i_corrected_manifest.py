#!/usr/bin/env python3
"""
Phase 35I — Corrected manifest generation and duplicate detection.

Generates corrected manifests based on actual filesystem state.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

TRAINING_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TRAINING_DIR.parent
RAW_DIR = PROJECT_ROOT / "raw"
MANIFESTS_DIR = PROJECT_ROOT / "training_data" / "manifests"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

SYNONYMS = {
    "brinjal": "Eggplant", "aubergine": "Eggplant",
    "capsicum": "Pepper", "bell pepper": "Pepper", "chilli": "Pepper", "chili": "Pepper", "green chili": "Pepper",
    "green bean": "Bean", "flat bean": "Bean", "french bean": "Bean", "yardlong bean": "Bean",
    "soybean": "Bean", "soy beans": "Bean",
    "maize": "Corn", "sweetcorn": "Corn", "corn_kernel": "Corn",
    "zucchini": "Summer Squash / Zucchini", "courgette": "Summer Squash / Zucchini",
    "pumpkin": "Winter Squash / Pumpkin",
    "beetroot": "Beet", "beet": "Beet",
    "coriander": "Cilantro",
    "muskmelon": "Cantaloupe",
    "raddish": "Radish",
    "raspberry": "Raspberry / Blackberry", "blackberry": "Raspberry / Blackberry", "rose_leaf_bramble": "Raspberry / Blackberry",
    "chives onion": "Onion",
    "sweet potatoes": "Sweet Potato",
    "peper chili": "Pepper", "peperchili": "Pepper",
    "longbeans": "Bean",
    "waterapple": "Apple",
    "papaya": "Papaya",
    "green papaya": "Papaya",
    "plantain": "Banana",
    "bitter melon": "Bitter Gourd",
    "bitter gourd": "Bitter Gourd",
    "pointed gourd": "Pointed Gourd",
    "ash gourd": "Ash Gourd",
    "elephant foot yam": "Elephant Foot Yam",
    "snake gourd": "Snake Gourd",
    "kohlrabi": "Kohlrabi",
    "jicama": "Jicama",
    "malabar spinach seed": "Malabar Spinach",
    "red amaranth": "Amaranth",
    "coconut": "Coconut",
    "gooseberry": "Gooseberry",
    "bottle gourd": "Bottle Gourd",
    "arum lobe": "Arum Lobe",
    "shaluk": "Shaluk",
    "taro": "Taro",
    "lime": "Lime",
    "squash": "Summer Squash / Zucchini",
    "1. bell pepper": "Pepper",
    "2. chile pepper": "Pepper",
    "3. new mexico green chile": "Pepper",
    "4. tomato": "Tomato",
    "carrot": "Carrot",
}

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


def map_class(name: str) -> str | None:
    lower = name.lower().strip()
    if lower in SYNONYMS:
        return SYNONYMS[lower]
    for cls in TIER1_CLASSES:
        if cls.lower() == lower:
            return cls
    return None


def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def audit_all():
    results = {}

    # hf_100crops
    base = RAW_DIR / "hf_100crops" / "images"
    counts = defaultdict(int)
    if base.exists():
        for class_dir in base.iterdir():
            if class_dir.is_dir():
                files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                mapped = map_class(class_dir.name)
                key = mapped if mapped else class_dir.name
                counts[key] += len(files)
    results["hf_100crops"] = dict(counts)

    # plants_type_30class
    base = RAW_DIR / "plants_type_30class" / "split_ttv_dataset_type_of_plants"
    counts = defaultdict(int)
    if base.exists():
        for split_folder in base.iterdir():
            if split_folder.is_dir():
                for class_dir in split_folder.iterdir():
                    if class_dir.is_dir():
                        files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                        mapped = map_class(class_dir.name)
                        key = mapped if mapped else class_dir.name
                        counts[key] += len(files)
    results["plants_type_30class"] = dict(counts)

    # plants_type_30class_alt
    base = RAW_DIR / "plants_type_30class_alt"
    for item in base.iterdir():
        if item.is_dir() and item.name != ".cache":
            split_base = item
            counts = defaultdict(int)
            for split_folder in split_base.iterdir():
                if split_folder.is_dir():
                    for class_dir in split_folder.iterdir():
                        if class_dir.is_dir():
                            files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                            mapped = map_class(class_dir.name)
                            key = mapped if mapped else class_dir.name
                            counts[key] += len(files)
            results["plants_type_30class_alt"] = dict(counts)
            break

    # fruits262_101class_subset
    base = RAW_DIR / "fruits262_101class_subset"
    classname_path = base / "classname.txt"
    class_map = {}
    if classname_path.exists():
        with open(classname_path, "r") as f:
            for i, line in enumerate(f, 1):
                class_map[i] = line.strip()

    counts = defaultdict(int)
    for split in ["train", "val"]:
        split_base = base / split
        if split_base.exists():
            for class_dir in split_base.iterdir():
                if class_dir.is_dir() and class_dir.name != "classname.txt":
                    files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                    mapped = map_class(class_dir.name)
                    key = mapped if mapped else class_dir.name
                    counts[key] += len(files)

    test_base = base / "test"
    if test_base.exists():
        for class_dir in test_base.iterdir():
            if class_dir.is_dir():
                files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                class_id = class_dir.name
                if class_id.isdigit():
                    class_name = class_map.get(int(class_id) + 1, f"unknown_{class_id}")
                else:
                    class_name = class_id
                mapped = map_class(class_name)
                key = mapped if mapped else class_name
                counts[key] += len(files)

    results["fruits262_101class_subset"] = dict(counts)

    # hf_food_veg
    base = RAW_DIR / "hf_food_veg" / "train"
    counts = defaultdict(int)
    if base.exists():
        for class_dir in base.iterdir():
            if class_dir.is_dir():
                files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                mapped = map_class(class_dir.name)
                key = mapped if mapped else class_dir.name
                counts[key] += len(files)
    results["hf_food_veg"] = dict(counts)

    # hf_food_ingredients_v2
    base = RAW_DIR / "hf_food_ingredients_v2"
    counts = defaultdict(int)
    for split in ["train", "Train"]:
        split_base = base / split
        if split_base.exists():
            for class_dir in split_base.iterdir():
                if class_dir.is_dir():
                    files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                    mapped = map_class(class_dir.name)
                    key = mapped if mapped else class_dir.name
                    counts[key] += len(files)
    results["hf_food_ingredients_v2"] = dict(counts)

    # hf_veg_bangladesh
    base = RAW_DIR / "hf_veg_bangladesh" / "images"
    counts = defaultdict(int)
    if base.exists():
        for class_dir in base.iterdir():
            if class_dir.is_dir():
                files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                mapped = map_class(class_dir.name)
                key = mapped if mapped else class_dir.name
                counts[key] += len(files)
    results["hf_veg_bangladesh"] = dict(counts)

    # bangladesh_veg_inbox
    base = RAW_DIR / "bangladesh_veg_inbox" / "A Comprehensive Image Dataset of  Vegetables Grown in Bangladesh" / "Vegetable_dataset" / "Actual_dataset"
    counts = defaultdict(int)
    if base.exists():
        for class_dir in base.iterdir():
            if class_dir.is_dir():
                files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                mapped = map_class(class_dir.name)
                key = mapped if mapped else class_dir.name
                counts[key] += len(files)
    results["bangladesh_veg_inbox"] = dict(counts)

    # veg_bangla_inbox
    base = RAW_DIR / "veg_bangla_inbox" / "Vegetable Image Dataset for Classification Models A Bangladeshi Perspective" / "Vegetable_Image" / "Vegetable_Image" / "Dataset"
    counts = defaultdict(int)
    if base.exists():
        for class_dir in base.iterdir():
            if class_dir.is_dir():
                files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                mapped = map_class(class_dir.name)
                key = mapped if mapped else class_dir.name
                counts[key] += len(files)
    results["veg_bangla_inbox"] = dict(counts)

    # vegnet_inbox
    base = RAW_DIR / "vegnet_inbox" / "VegNet Vegetable Dataset with quality (Unripe, Ripe, Old, Dried and Damaged)" / "VegNet (Unripe, Ripe, Old, Dried and Damaged)" / "New VegNet"
    counts = defaultdict(int)
    if base.exists():
        for class_dir in base.iterdir():
            if class_dir.is_dir():
                files = [f for f in class_dir.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
                mapped = map_class(class_dir.name)
                key = mapped if mapped else class_dir.name
                counts[key] += len(files)
    results["vegnet_inbox"] = dict(counts)

    # veg_object_bangla_inbox - NOT USABLE for classification
    results["veg_object_bangla_inbox"] = {"NOTE": "Object detection dataset with XML annotations. Not usable for classification without label extraction."}

    # hf_digigreen - disease dataset
    results["hf_digigreen"] = {"NOTE": "Disease/pest dataset. Images show unhealthy plants. Not suitable for healthy plant recognition."}

    # zenodo_vegann - segmentation dataset
    results["zenodo_vegann"] = {"NOTE": "Vegetation segmentation dataset with binary masks. Not suitable for classification without significant processing."}

    return results


def compute_cross_dataset_duplicates():
    print("Computing SHA256 hashes for duplicate detection...")
    hashes = defaultdict(list)
    for dataset_name in ["hf_100crops", "plants_type_30class", "plants_type_30class_alt", "fruits262_101class_subset", "hf_food_veg", "hf_food_ingredients_v2", "hf_veg_bangladesh", "bangladesh_veg_inbox", "veg_bangla_inbox", "vegnet_inbox"]:
        dataset_dir = RAW_DIR / dataset_name
        if not dataset_dir.exists():
            continue
        for img_file in dataset_dir.rglob("*"):
            if img_file.is_file() and img_file.suffix.lower() in SUPPORTED_EXTENSIONS:
                try:
                    h = compute_sha256(img_file)
                    hashes[h].append((dataset_name, str(img_file.relative_to(RAW_DIR))))
                except Exception as e:
                    pass
    return {h: paths for h, paths in hashes.items() if len(paths) > 1}


def main():
    print("=" * 80)
    print("PHASE 35I — CORRECTED MANIFEST GENERATION")
    print("=" * 80)
    print()

    results = audit_all()

    # Print corrected class coverage
    tier1_totals = defaultdict(int)
    tier1_sources = defaultdict(set)

    for dataset, counts in results.items():
        if isinstance(counts, dict) and "NOTE" in counts:
            continue
        print(f"### {dataset}")
        for cls, count in sorted(counts.items(), key=lambda x: -x[1]):
            mapped = map_class(cls)
            if mapped and mapped in TIER1_CLASSES:
                print(f"  {cls}: {count} -> {mapped}")
                tier1_totals[mapped] += count
                tier1_sources[mapped].add(dataset)
            elif mapped:
                print(f"  {cls}: {count} -> {mapped} (not in Tier-1)")
            else:
                print(f"  {cls}: {count} -> UNMAPPED")
        print()

    print("## CORRECTED TIER-1 CLASS COVERAGE")
    print()
    print(f"{'Class':<30} {'Images':>10} {'Sources':>10}")
    print("-" * 55)
    for cls in TIER1_CLASSES:
        total = tier1_totals.get(cls, 0)
        sources = len(tier1_sources.get(cls, set()))
        if total > 0:
            print(f"{cls:<30} {total:>10,} {sources:>10}")

    total_images = sum(tier1_totals.values())
    classes_with_data = sum(1 for cls in TIER1_CLASSES if tier1_totals.get(cls, 0) > 0)
    print()
    print(f"Total Tier-1 images: {total_images:,}")
    print(f"Classes with data: {classes_with_data} / {len(TIER1_CLASSES)}")
    print()

    # Save corrected coverage
    coverage = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier1_classes": len(TIER1_CLASSES),
        "classes_with_data": classes_with_data,
        "class_coverage": {
            cls: {
                "approved_images": tier1_totals.get(cls, 0),
                "sources": list(tier1_sources.get(cls, set())),
            }
            for cls in TIER1_CLASSES
        },
        "dataset_class_counts": {k: v for k, v in results.items() if isinstance(v, dict) and "NOTE" not in v},
    }

    out_path = MANIFESTS_DIR / "phase35i_corrected_coverage.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(coverage, f, indent=2, ensure_ascii=False)
    print(f"Corrected coverage saved to: {out_path}")

    # Duplicate detection (sample-based for speed)
    print()
    print("## DUPLICATE DETECTION (sample)")
    sample_hashes = defaultdict(list)
    for dataset_name in ["plants_type_30class", "plants_type_30class_alt"]:
        dataset_dir = RAW_DIR / dataset_name
        if not dataset_dir.exists():
            continue
        sampled = 0
        for img_file in dataset_dir.rglob("*"):
            if img_file.is_file() and img_file.suffix.lower() in SUPPORTED_EXTENSIONS:
                try:
                    h = compute_sha256(img_file)
                    sample_hashes[h].append((dataset_name, str(img_file.relative_to(RAW_DIR))))
                    sampled += 1
                    if sampled >= 500:
                        break
                except Exception as e:
                    pass
        print(f"  Sampled {sampled} hashes from {dataset_name}")

    dupes = {h: paths for h, paths in sample_hashes.items() if len(paths) > 1}
    if dupes:
        print(f"  Found {len(dupes)} duplicate hash groups in sample")
        for h, paths in list(dupes.items())[:5]:
            print(f"    {h[:16]}...: {len(paths)} copies")
    else:
        print("  No duplicates found in sample (plants_type_30class vs plants_type_30class_alt)")


if __name__ == "__main__":
    main()
