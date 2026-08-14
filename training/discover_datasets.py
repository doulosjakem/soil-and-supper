#!/usr/bin/env python3
"""
Dataset discovery utilities for Soil & Supper ML pipeline.
Lists approved datasets and their target class overlap.
"""

import yaml
from pathlib import Path
from typing import Dict, List

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


def load_config() -> Dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


APPROVED_DATASETS = {
    "bangladesh_veg": {
        "name": "Bangladesh Comprehensive Vegetables",
        "url": "https://data.mendeley.com/datasets/rtx9ngb68j",
        "license": "CC BY 4.0",
        "classes": [
            "Tomato", "Capsicum", "Cucumber", "Eggplant", "Broccoli",
            "Cabbage", "Carrot", "Onion", "Potato", "Pumpkin",
            "Radish", "Zucchini", "Flat Bean"
        ],
    },
    "smartphone_veg": {
        "name": "Smartphone Vegetable Detection",
        "url": "https://data.mendeley.com/datasets/gnc4s3z2mf/3",
        "license": "CC BY 4.0",
        "classes": [
            "Tomato", "Capsicum", "Cucumber", "Eggplant", "Potato",
            "Pumpkin", "Radish", "Green Bean", "Carrot", "Onion"
        ],
    },
    "early_stage_crops": {
        "name": "Early-Stage Vegetable Crops",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/",
        "license": "CC BY 4.0",
        "classes": ["Maize", "Bean", "Leek"],
    },
    "USDA_ARS": {
        "name": "USDA ARS Image Gallery",
        "url": "https://www.ars.usda.gov/oc/images/image-gallery/",
        "license": "Public Domain",
        "classes": ["Tomato", "Pepper", "Cucumber", "Corn", "Potato", "Onion", "Strawberry"],
    },
    "vegnet": {
        "name": "VegNet Vegetable Quality Dataset",
        "url": "https://data.mendeley.com/datasets/6nxnjbn9w6",
        "license": "CC BY 4.0",
        "classes": ["Bell Pepper", "Tomato", "Chili Pepper", "New Mexico Chile"],
    },
    "banglaveg": {
        "name": "BanglaVeg",
        "url": "https://www.sciencedirect.com/science/article/pii/S2352340925001738",
        "license": "CC BY 4.0",
        "classes": [
            "Tomato", "Capsicum", "Cucumber", "Eggplant", "Potato",
            "Onion", "Radish", "Bean", "Brinjal", "Chilli"
        ],
    },
}


def list_datasets() -> List[str]:
    return list(APPROVED_DATASETS.keys())


def get_dataset_info(dataset_id: str) -> Dict:
    if dataset_id not in APPROVED_DATASETS:
        raise ValueError(f"Unknown dataset: {dataset_id}")
    return APPROVED_DATASETS[dataset_id]


def print_summary():
    config = load_config()
    target_classes = set(config["target_classes"])
    print("Approved Datasets:")
    print("=" * 60)
    for ds_id, info in APPROVED_DATASETS.items():
        overlap = set(info["classes"]) & target_classes
        print(f"\n{ds_id}:")
        print(f"  Name: {info['name']}")
        print(f"  License: {info['license']}")
        print(f"  Classes: {len(info['classes'])}")
        print(f"  Target overlap: {len(overlap)} classes")
        if overlap:
            print(f"    Matching: {sorted(overlap)}")


if __name__ == "__main__":
    print_summary()
