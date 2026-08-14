#!/usr/bin/env python3
"""
Dataset discovery utilities for Soil & Supper ML pipeline.
Lists approved datasets and their target class overlap by domain.
"""

import yaml
from pathlib import Path
from typing import Dict, List

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


def load_config() -> Dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


APPROVED_DATASETS = {
    # Crop datasets
    "bangladesh_veg": {
        "name": "Bangladesh Comprehensive Vegetables",
        "url": "https://data.mendeley.com/datasets/rtx9ngb68j",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "crops",
        "classes": [
            "Tomato", "Capsicum", "Cucumber", "Eggplant", "Broccoli",
            "Cabbage", "Carrot", "Onion", "Potato", "Pumpkin",
            "Radish", "Zucchini", "Flat Bean"
        ],
        "image_count": 4730,
    },
    "smartphone_veg": {
        "name": "Smartphone Vegetable Detection",
        "url": "https://data.mendeley.com/datasets/gnc4s3z2mf/3",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "crops",
        "classes": [
            "Tomato", "Capsicum", "Cucumber", "Eggplant", "Potato",
            "Pumpkin", "Radish", "Green Bean", "Carrot", "Onion"
        ],
        "image_count": 3534,
    },
    "banglaveg": {
        "name": "BanglaVeg",
        "url": "https://www.sciencedirect.com/science/article/pii/S2352340925001738",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "crops",
        "classes": [
            "Tomato", "Capsicum", "Cucumber", "Eggplant", "Potato",
            "Onion", "Radish", "Bean", "Brinjal", "Chilli"
        ],
        "image_count": 4319,
    },
    "vegnet": {
        "name": "VegNet Vegetable Quality Dataset",
        "url": "https://data.mendeley.com/datasets/6nxnjbn9w6",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "crops",
        "classes": ["Bell Pepper", "Tomato", "Chili Pepper", "New Mexico Chile"],
        "image_count": 6850,
    },
    "early_stage_crops": {
        "name": "Early-Stage Vegetable Crops",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "crops",
        "classes": ["Maize", "Bean", "Leek"],
        "image_count": 2801,
    },
    # Disease datasets
    "plantvillage": {
        "name": "PlantVillage Dataset",
        "url": "https://data.mendeley.com/datasets/tywbtsjrjv/1",
        "license": "CC0 1.0",
        "commercial_ok": True,
        "domain": "diseases",
        "classes": [
            "Apple_scab", "Apple_rust", "Apple_healthy",
            "Blueberry_healthy",
            "Cherry_powdery_mildew", "Cherry_healthy",
            "Corn_rust", "Corn_healthy",
            "Grape_black_rot", "Grape_healthy",
            "Peach_bacterial_spot", "Peach_healthy",
            "Pepper_bacterial_spot", "Pepper_healthy",
            "Potato_early_blight", "Potato_late_blight", "Potato_healthy",
            "Raspberry_healthy",
            "Soybean_healthy",
            "Squash_powdery_mildew",
            "Strawberry_healthy",
            "Tomato_bacterial_spot", "Tomato_early_blight", "Tomato_late_blight",
            "Tomato_leaf_mold", "Tomato_Septoria_leaf_spot", "Tomato_spider_mites",
            "Tomato_target_spot", "Tomato_mosaic_virus", "Tomato_yellow_leaf_curl",
            "Tomato_healthy"
        ],
        "image_count": 54306,
    },
    "plantdoc": {
        "name": "PlantDoc Dataset",
        "url": "https://github.com/pratikkayal/PlantDoc-Dataset",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "diseases",
        "classes": [
            "Corn_leaf_blight", "Tomato_Septoria", "Squash_powdery_mildew",
            "Potato_leaf_early_blight", "Potato_leaf_late_blight",
            "Tomato_early_blight", "Tomato_mold", "Tomato_bacterial_spot",
            "Tomato_yellow_virus", "Tomato_mosaic_virus", "Tomato_two_spotted_spider_mites",
            "Apple_scab", "Apple_rust", "Grape_black_rot", "Peach_leaf",
            "Strawberry_leaf", "Blueberry_leaf", "Raspberry_leaf", "Soybean_leaf",
            "Bell_pepper_leaf_spot", "Cherry_leaf", "Tomato_leaf"
        ],
        "image_count": 2569,
    },
    # Weed datasets
    "deepweeds": {
        "name": "DeepWeeds",
        "url": "https://github.com/AlexOlsen/DeepWeeds",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "weeds",
        "classes": [
            "Chinee_apple", "Snake_weed", "Lantana", "Prickly_acacia",
            "Siam_weed", "Parthenium", "Rubber_vine", "Parkinsonia", "Negative"
        ],
        "image_count": 17509,
    },
    "plant_growth_stage": {
        "name": "Plant Growth Stage Detection",
        "url": "https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "growth_stages",
        "classes": ["Flowering", "Germination", "Harvesting", "Vegetative"],
        "image_count": 7306,
    },
    "bdflower": {
        "name": "BDFlower",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "growth_stages",
        "classes": ["Early_Stage", "Mid_Stage", "Full_Stage"],
        "image_count": 23334,
    },
    "sunflower_growth": {
        "name": "Sunflower Growth Stage Dataset",
        "url": "https://data.mendeley.com/datasets/byftmdzg4g",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "growth_stages",
        "classes": ["Stage1", "Stage2", "Stage3", "Stage4", "Stage5"],
        "image_count": 1255,
    },
    # Supplemental
    "USDA_ARS": {
        "name": "USDA ARS Image Gallery",
        "url": "https://www.ars.usda.gov/oc/images/image-gallery/",
        "license": "Public Domain",
        "commercial_ok": True,
        "domain": "crops",
        "classes": ["Tomato", "Pepper", "Cucumber", "Corn", "Potato", "Onion", "Strawberry"],
        "image_count": 6500,
    },
}


def list_datasets() -> List[str]:
    return list(APPROVED_DATASETS.keys())


def get_dataset_info(dataset_id: str) -> Dict:
    if dataset_id not in APPROVED_DATASETS:
        raise ValueError(f"Unknown dataset: {dataset_id}")
    return APPROVED_DATASETS[dataset_id]


def list_datasets_by_domain(domain: str) -> List[str]:
    return [k for k, v in APPROVED_DATASETS.items() if v.get("domain") == domain]


def print_summary():
    config = load_config()
    print("Approved Datasets by Domain:")
    print("=" * 60)
    for domain in config.get("domains", {}).keys():
        ds_list = list_datasets_by_domain(domain)
        print(f"\n{domain.upper()} ({len(ds_list)} datasets):")
        for ds_id in ds_list:
            info = APPROVED_DATASETS[ds_id]
            print(f"  {ds_id}: {info['name']} ({info['image_count']} images, {info['license']})")


if __name__ == "__main__":
    print_summary()
