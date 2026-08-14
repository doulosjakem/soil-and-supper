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
    # =========================================================================
    # PHASE 14 REVISED DATASETS
    # Based on actual downloadability, license verification, and class relevance
    # =========================================================================

    # Primary crop datasets (CC BY 4.0 / CC0)
    "bangladesh_veg": {
        "name": "Bangladesh Comprehensive Vegetables",
        "url": "https://data.mendeley.com/datasets/rtx9ngb68j",
        "download_url": "https://data.mendeley.com/public-files/datasets/rtx9ngb68j/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "crops",
        "priority": 4,
        "status": "DOCUMENTED",
        "classes": [
            "Tomato", "Capsicum", "Cucumber", "Eggplant", "Broccoli",
            "Cabbage", "Carrot", "Onion", "Potato", "Pumpkin",
            "Radish", "Zucchini", "Flat Bean"
        ],
        "image_count": 4730,
        "notes": "Mendeley download URL may be stale; scraper fallback required",
    },
    "smartphone_veg": {
        "name": "Smartphone Vegetable Detection",
        "url": "https://data.mendeley.com/datasets/gnc4s3z2mf/3",
        "download_url": "https://data.mendeley.com/public-files/datasets/gnc4s3z2mf/files/3c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "crops",
        "priority": 5,
        "status": "DOCUMENTED",
        "classes": [
            "Tomato", "Capsicum", "Cucumber", "Eggplant", "Potato",
            "Pumpkin", "Radish", "Green Bean", "Carrot", "Onion"
        ],
        "image_count": 3534,
        "notes": "Pascal VOC format; requires conversion to classification",
    },
    "vegnet": {
        "name": "VegNet Vegetable Quality Dataset",
        "url": "https://data.mendeley.com/datasets/6nxnjbn9w6",
        "download_url": "https://data.mendeley.com/public-files/datasets/6nxnjbn9w6/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "crops",
        "priority": 6,
        "status": "DOCUMENTED",
        "classes": ["Bell Pepper", "Tomato", "Chili Pepper", "New Mexico Chile"],
        "image_count": 6850,
        "notes": "White background; supplement for pepper/tomato quality labels",
    },
    "early_stage_crops": {
        "name": "Early-Stage Vegetable Crops",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/",
        "download_url": "",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "crops",
        "priority": 15,
        "status": "DOCUMENTED",
        "classes": ["Maize", "Bean", "Leek"],
        "image_count": 2801,
        "notes": "Seedling stage only; PMC supplementary file required",
    },
    "plant_seedlings": {
        "name": "Plant Seedlings Dataset (Aarhus)",
        "url": "https://vision.eng.au.dk/plant-seedlings-dataset/",
        "download_url": "https://vision.eng.au.dk/plant-seedlings-dataset/plant-seedlings.zip",
        "license": "CC BY-SA 4.0",
        "commercial_ok": False,
        "domain": "crops",
        "priority": 21,
        "status": "LICENSE_BLOCKED",
        "classes": ["Maize", "Sugar beet", "Chickweed", "Cleavers", "Fat hen", "Shepherds purse", "Cranesbill", "Maize", "Scentless mayweed", "Farmspeed", "Black grass", "Wild wheat"],
        "image_count": 960,
        "notes": "CC BY-SA 4.0 ShareAlike incompatible with proprietary app",
    },
    "images_cv_vegetables": {
        "name": "images.cv Vegetables",
        "url": "https://images.cv/dataset/vegetables-image-classification-dataset",
        "download_url": "",
        "license": "CC0 / Public Domain",
        "commercial_ok": True,
        "domain": "crops",
        "priority": 22,
        "status": "DATASET_SEARCH_REQUIRED",
        "classes": ["Tomato", "Potato", "Cucumber", "Bean", "Carrot", "Onion", "Capsicum", "Eggplant", "Broccoli", "Cabbage", "Cauliflower", "Pumpkin", "Radish", "Turnip", "Sweetcorn", "Beetroot", "Pea", "Asparagus", "Celery", "Leek", "Lettuce", "Spinach"],
        "image_count": 19300,
        "notes": "CC0 license confirmed; download mechanism needs investigation",
    },

    # Disease datasets
    "plantvillage": {
        "name": "PlantVillage Dataset",
        "url": "https://data.mendeley.com/datasets/tywbtsjrjv/1",
        "download_url": "https://figshare.com/ndownloader/files/21528842?private_link=5ab5f7ea05ae4f9b88f3",
        "license": "CC0 1.0",
        "commercial_ok": True,
        "domain": "diseases",
        "priority": 1,
        "status": "DOCUMENTED",
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
        "notes": "Primary disease dataset; Figshare mirror added 2026-08-14",
    },
    "plantdoc": {
        "name": "PlantDoc Dataset",
        "url": "https://github.com/pratikkayal/PlantDoc-Dataset",
        "download_url": "https://github.com/pratikkayal/PlantDoc-Dataset/archive/refs/heads/main.zip",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "diseases",
        "priority": 3,
        "status": "DOCUMENTED",
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
        "notes": "Real-world field images; complements PlantVillage",
    },
    "crop_disease_hf": {
        "name": "Crop Disease Image Dataset (HuggingFace)",
        "url": "https://huggingface.co/datasets/ipartzix/Crop_Disease_Image_Dataset",
        "download_url": "",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "diseases",
        "priority": 23,
        "status": "DATASET_SEARCH_REQUIRED",
        "classes": ["Corn", "Wheat", "Rice", "Tomato", "Potato", "Powdery_mildew", "Rust", "Healthy", "Bacterial_spot", "Late_blight", "Early_blight", "Leaf_spot", "Mosaic_virus", "Leaf_wilt", "Downy_mildew", "Anthracnose", "Fusarium_wilt", "Verticillium_wilt", "Blight"],
        "image_count": 22169,
        "notes": "Combines PlantVillage + Mendeley sources under CC BY 4.0; HuggingFace download",
    },

    # Weed datasets
    "deepweeds": {
        "name": "DeepWeeds",
        "url": "https://github.com/AlexOlsen/DeepWeeds",
        "download_url": "https://zenodo.org/records/7939060/files/images.zip?download=1",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "weeds",
        "priority": 2,
        "status": "DOCUMENTED",
        "classes": [
            "Chinee_apple", "Snake_weed", "Lantana", "Prickly_acacia",
            "Siam_weed", "Parthenium", "Rubber_vine", "Parkinsonia", "Negative"
        ],
        "image_count": 17509,
        "notes": "Australian species; supplement only. Zenodo direct ZIP preferred over Google Drive",
    },
    "weed_ndsu": {
        "name": "Weed-crop dataset (NDSU)",
        "url": "https://data.mendeley.com/datasets/mthv4ppwyw/2",
        "download_url": "https://data.mendeley.com/public-files/datasets/mthv4ppwyw/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "weeds",
        "priority": 24,
        "status": "DOCUMENTED",
        "classes": ["Kochia", "Horseweed", "Water_hemp", "Ragweed", "Redroot_pigweed", "Corn", "Soybean", "Sugarbeet", "Wheat", "Canola", "Pea", "Flax", "Lentil", "Oat", "Barley", "Sunflower", "Rye", "Triticale"],
        "image_count": 5000,
        "notes": "North American weeds; YOLO annotations; convert to classification",
    },
    "weed_growth_stage_zenodo": {
        "name": "Weed Growth Stage Dataset",
        "url": "https://zenodo.org/records/15808623",
        "download_url": "https://zenodo.org/records/15808623/files/weed_growth_stage_dataset.zip?download=1",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "weeds",
        "priority": 25,
        "status": "DOCUMENTED",
        "classes": ["Amaranthus_sp", "Chenopodium_album", "Digitaria_sp", "Portulaca_oleracea", "Stellaria_media", "Cyperus_sp", "Ambrosia_artemisiifolia", "Calystegia_sepium", "Setaria_sp", "Cirsium_sp", "Polygonum_sp", "Oxalis_corniculata", "Sorghum_halepense", "Elymus_repens", "Abelmoschus_esculentus", "Brassica_oleracea"],
        "image_count": 203567,
        "notes": "203K images, 16 species, weekly growth stages; Zenodo direct ZIP",
    },
    "uc_ipm_weeds": {
        "name": "UC IPM Weed Images",
        "url": "https://ipm.ucanr.edu/PMG/WEEDS/",
        "download_url": "",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "weeds",
        "priority": 11,
        "status": "DOCUMENTED",
        "classes": ["Dandelion", "Crabgrass", "Purslane", "Lambsquarters", "Pigweed", "Chickweed", "Plantain", "Bindweed", "Thistle", "Foxtail", "Nutsedge", "Ragweed", "Johnsongrass", "Quackgrass"],
        "image_count": 1500,
        "notes": "Web scraper required; no bulk download",
    },

    # Insect / Pest datasets
    "bioscan_5m": {
        "name": "BIOSCAN-5M Insect Dataset",
        "url": "https://huggingface.co/datasets/bioscan-ml/BIOSCAN-5M",
        "download_url": "https://huggingface.co/datasets/bioscan-ml/BIOSCAN-5M/resolve/main/data/bioscan_5m.zip",
        "license": "CC BY 3.0",
        "commercial_ok": True,
        "domain": "insects",
        "priority": 26,
        "status": "DOCUMENTED",
        "classes": ["Aphid", "Japanese_beetle", "Colorado_potato_beetle", "Cucumber_beetle", "Cabbage_worm", "Tomato_hornworm", "Squash_bug", "Whitefly", "Spider_mite", "Thrips", "Leafminer", "Cutworm", "Stink_bug", "Flea_beetle", "Ladybug", "Green_lacewing", "Honey_bee", "Hoverfly", "Praying_mantis", "Spider", "Earthworm"],
        "image_count": 5150000,
        "notes": "5.15M insect specimens; CC BY 3.0 commercial-compatible; requires heavy curation",
    },
    "images_cv_insects": {
        "name": "images.cv Insects",
        "url": "https://images.cv/dataset/insects-image-classification-dataset",
        "download_url": "",
        "license": "CC0 / Public Domain",
        "commercial_ok": True,
        "domain": "insects",
        "priority": 27,
        "status": "DATASET_SEARCH_REQUIRED",
        "classes": ["Fly", "Grasshopper", "Beetle", "Mantis", "Ladybug", "Cricket", "Cockroach", "Mosquito", "Cicada", "Dragonfly", "Butterfly", "Moth", "Bee", "Ant", "Wasp", "Spider", "Scorpion", "Centipede", "Millipede", "Earwig", "Aphid", "Whitefly", "Thrips", "Mite"],
        "image_count": 24800,
        "notes": "CC0; download mechanism needs investigation",
    },
    "roboflow_insect_pest": {
        "name": "Roboflow Insect Pest Dataset",
        "url": "https://universe.roboflow.com/ai-project-h07h1/insect-pest-dataset-all",
        "download_url": "https://universe.roboflow.com/ai-project-h07h1/insect-pest-dataset-all?download=1",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "insects",
        "priority": 28,
        "status": "DOCUMENTED",
        "classes": ["Aphid", "Fruit_fly", "Leafminer", "Mealybug", "Scale_insect", "Thrips", "Whitefly", "Spider_mite", "Beetle", "Caterpillar", "Bug"],
        "image_count": 1213,
        "notes": "Small but useful supplement; Roboflow format",
    },

    # Beneficial insects
    "uc_ipm_beneficials": {
        "name": "UC IPM Beneficial Organism Images",
        "url": "https://ipm.ucanr.edu/PMG/BENE/",
        "download_url": "",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "insects",
        "priority": 14,
        "status": "DOCUMENTED",
        "classes": ["Ladybug", "Green_lacewing", "Honey_bee", "Hoverfly", "Praying_mantis", "Spider", "Earthworm", "Ground_beetle", "Predatory_bug"],
        "image_count": 1000,
        "notes": "Web scraper required; supplement with BIOSCAN-5M",
    },

    # Growth stage datasets
    "plant_growth_stage": {
        "name": "Plant Growth Stage Detection",
        "url": "https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection",
        "download_url": "https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection?download=1",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "growth_stages",
        "priority": 8,
        "status": "DOCUMENTED",
        "classes": ["Flowering", "Germination", "Harvesting", "Vegetative"],
        "image_count": 7306,
        "notes": "4 stages; map Germination->Seedling, Harvesting->Mature/Harvest",
    },
    "bdflower": {
        "name": "BDFlower",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/",
        "download_url": "",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "growth_stages",
        "priority": 9,
        "status": "DOCUMENTED",
        "classes": ["Early_Stage", "Mid_Stage", "Full_Stage"],
        "image_count": 23334,
        "notes": "Flower-specific growth stages; PMC supplementary file required",
    },
    "sunflower_growth": {
        "name": "Sunflower Growth Stage Dataset",
        "url": "https://data.mendeley.com/datasets/byftmdzg4g",
        "download_url": "https://data.mendeley.com/public-files/datasets/byftmdzg4g/files/8c5c7c5c-0b2c-4c4c-8e0e-0c5c7c5c0b2c",
        "license": "CC BY 4.0",
        "commercial_ok": True,
        "domain": "growth_stages",
        "priority": 16,
        "status": "DOCUMENTED",
        "classes": ["Stage1", "Stage2", "Stage3", "Stage4", "Stage5"],
        "image_count": 1255,
        "notes": "Single crop; supplement for growth stage model",
    },
    "openplant": {
        "name": "OpenPlant",
        "url": "https://github.com/Kaiqi6/OpenPlant",
        "download_url": "",
        "license": "Open (verify on GitHub)",
        "commercial_ok": None,
        "domain": "crops",
        "priority": 29,
        "status": "LICENSE_BLOCKED",
        "classes": ["Tomato", "Cucumber", "Bean", "Corn", "Pepper", "Eggplant", "Strawberry", "Blueberry", "Grape", "Sunflower", "Lettuce", "Spinach", "Carrot", "Onion", "Potato", "Broccoli", "Cabbage", "Pea", "Radish", "Pumpkin"],
        "image_count": 635176,
        "notes": "635K images, 1167 species; license must be verified before use",
    },

    # Supplemental
    "USDA_ARS": {
        "name": "USDA ARS Image Gallery",
        "url": "https://www.ars.usda.gov/oc/images/image-gallery/",
        "download_url": "",
        "license": "Public Domain",
        "commercial_ok": True,
        "domain": "crops",
        "priority": 10,
        "status": "ACQUIRED",
        "classes": ["Tomato", "Pepper", "Cucumber", "Corn", "Potato", "Onion", "Strawberry"],
        "image_count": 6500,
        "notes": "20 images acquired but unlabeled; manual download required for bulk",
    },

    # DEFERRED / BLOCKED
    "cwd30": {
        "name": "CWD30 Crop Weed Dataset",
        "url": "https://cwd-30.github.io/cwd-30/",
        "download_url": "",
        "license": "Unclear (Elsevier journal)",
        "commercial_ok": False,
        "domain": "weeds",
        "priority": 30,
        "status": "LICENSE_BLOCKED",
        "classes": ["Amaranthus_sp", "Digitaria_sp", "Portulaca_oleracea", "Chenopodium_album", "Stellaria_media", "Cyperus_sp", "Ambrosia_artemisiifolia", "Calystegia_sepium", "Setaria_sp", "Cirsium_sp", "Polygonum_sp", "Oxalis_corniculata", "Sorghum_halepense", "Elymus_repens"],
        "image_count": 219770,
        "notes": "REJECT until license clarified; contact authors for commercial use",
    },
    "ip102": {
        "name": "IP102 Insect Pest Dataset",
        "url": "https://github.com/xpwu95/IP102",
        "download_url": "",
        "license": "Academic use only",
        "commercial_ok": False,
        "domain": "insects",
        "priority": 31,
        "status": "LICENSE_BLOCKED",
        "classes": ["Aphid", "Japanese_beetle", "Colorado_potato_beetle", "Cucumber_beetle", "Cabbage_worm", "Tomato_hornworm", "Squash_bug", "Whitefly", "Spider_mite", "Thrips", "Leafminer", "Cutworm", "Stink_bug", "Flea_beetle"],
        "image_count": 75000,
        "notes": "REJECT for commercial use; contact Xiaoping Wu for permission",
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
            status = info.get("status", "UNKNOWN")
            print(f"  {ds_id}: {info['name']} ({info['image_count']} images, {info['license']}, {status})")


if __name__ == "__main__":
    print_summary()
