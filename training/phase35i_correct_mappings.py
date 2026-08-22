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
    "bottle gourd": "Bottle Gourd", "capsicum": "Capsicum", "chili": "Chili",
    "chives onion": "Chives Onion", "coconut": "Coconut", "coriander": "Coriander",
    "elephant foot yam": "Elephant foot yam", "flat bean": "Flat Bean",
    "gooseberry": "Gooseberry", "green papaya": "Green Papaya",
    "green spinach": "Green Spinach", "jicama": "Jicama", "kohlrabi": "Kohlrabi",
    "lime": "Lime", "malabar spinach seed": "Malabar Spinach Seed",
    "okra": "Okra", "plantain": "Plantain", "pointed gourd": "Pointed Gourd",
    "radish leaves": "Radish Leaves", "red amaranth": "Red Amaranth",
    "shaluk": "Shaluk", "snake gourd": "Snake Gourd", "taro": "Taro",
    "yardlong bean": "Yardlong bean", "ladies finger": "Ladies finger",
    "brinjal": "Brinjal", "bitter gourd": "Bitter Gourd",
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

    remap_ids = {
        "bangladesh_veg_inbox",
        "veg_bangla_inbox",
        "vegnet_inbox",
        "veg_object_bangla_inbox",
        "plants_type_30class",
        "plants_type_30class_alt",
    }

    corrected_coverage = defaultdict(lambda: {"approved_images": 0, "sources": set(), "domain": "CROP / PLANT ID"})

    for entry in ledger:
        ds_id = entry.get("dataset_id")
        status = entry.get("status", "UNKNOWN")
        mapped_counts = dict(entry.get("mapped_class_counts", {}))
        unmapped = list(entry.get("unmapped_classes", []))

        if ds_id in remap_ids and status == "APPROVED":
            image_records = entry.get("image_records", [])
            new_mapped = defaultdict(int)
            new_unmapped = []

            for rec in image_records:
                if not rec.get("valid", False):
                    continue
                path = rec.get("path", "")
                extracted = extract_class_from_path(path, ds_id)
                target, conf = auto_map_class(extracted)
                if target:
                    new_mapped[target] += 1
                else:
                    new_unmapped.append(extracted)

            if ds_id in ("plants_type_30class", "plants_type_30class_alt"):
                for cls, count in mapped_counts.items():
                    new_mapped[cls] = new_mapped.get(cls, 0) + count
                mapped_counts = dict(new_mapped)
                unmapped = sorted(set(new_unmapped))
            else:
                mapped_counts = dict(new_mapped)
                unmapped = sorted(set(new_unmapped))

            print(f"\n--- {ds_id} ---")
            print(f"  Mapped: {dict(sorted(mapped_counts.items(), key=lambda x: -x[1])[:10])}")
            print(f"  Unmapped: {unmapped[:15]}")
            print(f"  Total mapped: {sum(mapped_counts.values())}")

            for cls, count in mapped_counts.items():
                corrected_coverage[cls]["approved_images"] += count
                corrected_coverage[cls]["sources"].add(ds_id)
        else:
            for cls, count in mapped_counts.items():
                corrected_coverage[cls]["approved_images"] += count
                corrected_coverage[cls]["sources"].add(ds_id)

    print("\n" + "=" * 80)
    print("CORRECTED TIER 1 CLASS COVERAGE")
    print("=" * 80)

    class_results = {}
    for cls in TIER1_CLASSES:
        info = corrected_coverage.get(cls, {"approved_images": 0, "sources": set(), "domain": "CROP / PLANT ID"})
        class_results[cls] = {
            "approved_images": info["approved_images"],
            "source_dataset_count": len(info["sources"]),
            "sources": sorted(list(info["sources"])),
            "status": "APPROVED" if info["approved_images"] > 0 else "NO_DATA",
            "domain": info["domain"],
        }
        if info["approved_images"] > 0:
            print(f"  {cls}: {info['approved_images']} images from {len(info['sources'])} sources")

    total_with_data = sum(1 for c in class_results.values() if c["status"] == "APPROVED")
    total_images = sum(c["approved_images"] for c in class_results.values())
    print(f"\nTotal Tier 1 classes with data: {total_with_data}")
    print(f"Total mapped images: {total_images}")

    coverage_output = MANIFESTS_DIR / "phase35i_class_coverage_corrected.json"
    with open(coverage_output, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_tier1_classes": len(TIER1_CLASSES),
            "classes_with_data": total_with_data,
            "classes": class_results,
        }, f, indent=2, ensure_ascii=False)
    print(f"\nCorrected coverage saved to: {coverage_output}")


if __name__ == "__main__":
    main()
