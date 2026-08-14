#!/usr/bin/env python3
"""
Dataset preparation utilities for Soil & Supper ML pipeline.
Filters, normalizes, and organizes images for training.
"""

import shutil
import json
from pathlib import Path
from typing import Dict, List
import yaml
from PIL import Image

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"
TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
RAW_DIR = TRAINING_DATA_DIR / "raw"
PROCESSED_DIR = TRAINING_DATA_DIR / "processed"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def normalize_filename(src: Path, class_name: str, index: int) -> str:
    """Generate normalized filename."""
    ext = src.suffix.lower()
    return f"{class_name}_{index:05d}{ext}"


def prepare_class(class_name: str, source_dirs: List[Path], output_dir: Path, dataset_id: str) -> int:
    """Copy and normalize images for a single class."""
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    manifest_entries = []
    
    for src_dir in source_dirs:
        if not src_dir.exists():
            continue
        for img_path in src_dir.rglob("*"):
            if img_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                try:
                    with Image.open(img_path) as img:
                        img.verify()
                    dest_name = normalize_filename(img_path, class_name, count)
                    dest_path = output_dir / dest_name
                    if not dest_path.exists():
                        shutil.copy2(img_path, dest_path)
                        manifest_entries.append({
                            "local_path": str(dest_path.relative_to(TRAINING_DATA_DIR)),
                            "source_path": str(img_path),
                            "source_dataset": dataset_id,
                            "class": class_name,
                        })
                        count += 1
                except Exception:
                    continue
    
    if manifest_entries:
        manifest_path = MANIFESTS_DIR / f"{dataset_id}_{class_name}_manifest.jsonl"
        with open(manifest_path, "a") as f:
            for entry in manifest_entries:
                f.write(json.dumps(entry) + "\n")
    
    return count


def prepare_all(config: Dict):
    """Prepare all approved datasets."""
    from class_mapper import initialize_default_mappings
    mapper = initialize_default_mappings()
    
    domain_map = {
        "crops": config["domains"]["crops"]["classes"],
        "weeds": config["domains"]["weeds"]["classes"],
        "insects": config["domains"]["insects"]["classes"],
        "diseases": config["domains"]["diseases"]["classes"],
        "growth_stages": config["domains"]["growth_stages"]["classes"],
    }
    
    total = 0
    for domain, classes in domain_map.items():
        print(f"\nProcessing domain: {domain}")
        for cls in classes:
            class_dir = PROCESSED_DIR / domain / cls
            if class_dir.exists():
                existing = len(list(class_dir.rglob("*.jpg"))) + len(list(class_dir.rglob("*.jpeg"))) + len(list(class_dir.rglob("*.png"))) + len(list(class_dir.rglob("*.webp")))
                print(f"  {cls}: {existing} images (already prepared)")
                total += existing
                continue
            
            source_dirs = []
            dataset_id = None
            
            if domain == "crops" and cls in ["Tomato", "Pepper_sweet", "Cucumber", "Eggplant"]:
                source_dirs = [
                    RAW_DIR / "bangladesh_veg" / cls,
                    RAW_DIR / "smartphone_veg" / cls,
                ]
                dataset_id = "bangladesh_veg"
            elif domain == "diseases" and cls in ["Apple_scab", "Powdery_mildew", "Bacterial_spot", "Early_blight"]:
                source_dirs = [
                    RAW_DIR / "plantvillage" / cls,
                    RAW_DIR / "plantdoc" / cls,
                ]
                dataset_id = "plantvillage"
            elif domain == "weeds" and cls == "Other_weed":
                source_dirs = [RAW_DIR / "deepweeds" / cls]
                dataset_id = "deepweeds"
            elif domain == "growth_stages" and cls in ["Flowering", "Vegetative", "Seedling", "Fruiting"]:
                source_dirs = [
                    RAW_DIR / "plant_growth_stage" / cls,
                ]
                dataset_id = "plant_growth_stage"
            else:
                source_dirs = [RAW_DIR / domain / cls]
                dataset_id = domain
            
            count = prepare_class(cls, source_dirs, class_dir, dataset_id)
            print(f"  {cls}: {count} images")
            total += count
    
    print(f"\nTotal prepared: {total} images")


if __name__ == "__main__":
    config = load_config()
    prepare_all(config)
