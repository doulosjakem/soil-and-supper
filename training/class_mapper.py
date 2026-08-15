#!/usr/bin/env python3
"""
Class mapping system for Soil & Supper ML pipeline.

Maps source dataset labels to our standardized taxonomy.
Handles ambiguous mappings by flagging them for human review.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

MANIFESTS_DIR = Path(__file__).resolve().parent.parent / "training_data" / "manifests"
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)


class ClassMapper:
    """Map source labels to standardized taxonomy."""

    def __init__(self):
        self.mappings: Dict[str, Dict] = {}
        self.ambiguous_mappings: List[Dict] = []
        self.load_mappings()

    def load_mappings(self):
        manifest_path = MANIFESTS_DIR / "class_mappings.json"
        if manifest_path.exists():
            with open(manifest_path, "r") as f:
                self.mappings = json.load(f)

    def save_mappings(self):
        manifest_path = MANIFESTS_DIR / "class_mappings.json"
        with open(manifest_path, "w") as f:
            json.dump(self.mappings, f, indent=2)

    def add_mapping(
        self,
        source_dataset: str,
        source_label: str,
        target_class: str,
        domain: str,
        confidence: str = "high",
        notes: str = "",
    ):
        """Add a class mapping."""
        key = f"{source_dataset}::{source_label}"
        mapping = {
            "source_dataset": source_dataset,
            "source_label": source_label,
            "target_class": target_class,
            "domain": domain,
            "confidence": confidence,
            "notes": notes,
        }
        self.mappings[key] = mapping
        self.save_mappings()
        return mapping

    def get_target_class(self, source_dataset: str, source_label: str) -> Tuple[str, str]:
        """Get target class for a source label. Returns (target_class, confidence)."""
        key = f"{source_dataset}::{source_label}"
        if key in self.mappings:
            m = self.mappings[key]
            return m["target_class"], m["confidence"]
        return None, "none"

    def flag_ambiguous(self, source_dataset: str, source_label: str, possible_targets: List[str], notes: str = ""):
        """Flag an ambiguous mapping for human review."""
        entry = {
            "source_dataset": source_dataset,
            "source_label": source_label,
            "possible_targets": possible_targets,
            "notes": notes,
            "status": "HOLD",
        }
        self.ambiguous_mappings.append(entry)
        manifest_path = MANIFESTS_DIR / "ambiguous_mappings.jsonl"
        with open(manifest_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_ambiguous_mappings(self) -> List[Dict]:
        return self.ambiguous_mappings


def initialize_default_mappings():
    """Initialize mappings for approved datasets."""
    mapper = ClassMapper()

    # Bangladesh Vegetables
    bangladesh_mappings = [
        ("Tomato", "Tomato"),
        ("Capsicum", "Pepper_sweet"),
        ("Cucumber", "Cucumber"),
        ("Brinjal", "Eggplant"),
        ("Broccoli", "Broccoli"),
        ("Cabbage", "Cabbage"),
        ("Carrot", "Carrot"),
        ("Onion", "Onion"),
        ("Potato", "Potato"),
        ("Pumpkin", "Pumpkin"),
        ("Radish", "Radish"),
        ("Zucchini", "Summer_squash"),
        ("Flat Bean", "Bean"),
    ]
    for src, tgt in bangladesh_mappings:
        mapper.add_mapping("bangladesh_veg", src, tgt, "crops", confidence="high")

    # Smartphone Vegetable Detection
    smartphone_mappings = [
        ("Tomato", "Tomato"),
        ("Capsicum", "Pepper_sweet"),
        ("Cucumber", "Cucumber"),
        ("Eggplant", "Eggplant"),
        ("Potato", "Potato"),
        ("Pumpkin", "Pumpkin"),
        ("Radish", "Radish"),
        ("Green Bean", "Bean"),
        ("Carrot", "Carrot"),
        ("Onion", "Onion"),
    ]
    for src, tgt in smartphone_mappings:
        mapper.add_mapping("smartphone_veg", src, tgt, "crops", confidence="high")

    # BanglaVeg
    banglaveg_mappings = [
        ("Tomato", "Tomato"),
        ("Capsicum", "Pepper_sweet"),
        ("Cucumber", "Cucumber"),
        ("Eggplant", "Eggplant"),
        ("Potato", "Potato"),
        ("Onion", "Onion"),
        ("Radish", "Radish"),
        ("Bean", "Bean"),
        ("Brinjal", "Eggplant"),
        ("Chilli", "Pepper_hot"),
    ]
    for src, tgt in banglaveg_mappings:
        mapper.add_mapping("banglaveg", src, tgt, "crops", confidence="high")

    # VegNet
    vegnet_mappings = [
        ("Bell Pepper", "Pepper_sweet"),
        ("Tomato", "Tomato"),
        ("Chili Pepper", "Pepper_hot"),
        ("New Mexico Chile", "Pepper_hot"),
    ]
    for src, tgt in vegnet_mappings:
        mapper.add_mapping("vegnet", src, tgt, "crops", confidence="high")

    # Early-Stage Crops
    early_mappings = [
        ("Maize", "Corn"),
        ("Bean", "Bean"),
        ("Leek", "Leek"),
    ]
    for src, tgt in early_mappings:
        mapper.add_mapping("early_stage_crops", src, tgt, "crops", confidence="high")

    # PlantVillage (diseases)
    plantvillage_mappings = [
        ("Apple_scab", "Apple_scab"),
        ("Apple_rust", "Cedar_apple_rust"),
        ("Apple_healthy", "Healthy"),
        ("Blueberry_healthy", "Healthy"),
        ("Cherry_powdery_mildew", "Powdery_mildew"),
        ("Cherry_healthy", "Healthy"),
        ("Corn_rust", "Rust"),
        ("Corn_healthy", "Healthy"),
        ("Grape_black_rot", "Grape_black_rot"),
        ("Grape_healthy", "Healthy"),
        ("Peach_bacterial_spot", "Peach_bacterial_spot"),
        ("Peach_healthy", "Healthy"),
        ("Pepper_bacterial_spot", "Bacterial_spot"),
        ("Pepper_healthy", "Healthy"),
        ("Potato_early_blight", "Early_blight"),
        ("Potato_late_blight", "Late_blight"),
        ("Potato_healthy", "Healthy"),
        ("Raspberry_healthy", "Healthy"),
        ("Soybean_healthy", "Healthy"),
        ("Squash_powdery_mildew", "Squash_powdery_mildew"),
        ("Strawberry_healthy", "Healthy"),
        ("Tomato_bacterial_spot", "Bacterial_spot"),
        ("Tomato_early_blight", "Early_blight"),
        ("Tomato_late_blight", "Late_blight"),
        ("Tomato_leaf_mold", "Leaf_spot"),
        ("Tomato_Septoria_leaf_spot", "Septoria_leaf_spot"),
        ("Tomato_spider_mites", "Spider_mite"),
        ("Tomato_target_spot", "Leaf_spot"),
        ("Tomato_mosaic_virus", "Tomato_mosaic_virus"),
        ("Tomato_yellow_leaf_curl", "Tomato_yellow_leaf_curl"),
        ("Tomato_healthy", "Healthy"),
    ]
    for src, tgt in plantvillage_mappings:
        mapper.add_mapping("plantvillage", src, tgt, "diseases", confidence="high")

    # PlantDoc (diseases)
    plantdoc_mappings = [
        ("Corn_leaf_blight", "Leaf_spot"),
        ("Tomato_Septoria", "Septoria_leaf_spot"),
        ("Squash_powdery_mildew", "Squash_powdery_mildew"),
        ("Potato_leaf_early_blight", "Early_blight"),
        ("Potato_leaf_late_blight", "Late_blight"),
        ("Tomato_early_blight", "Early_blight"),
        ("Tomato_mold", "Leaf_spot"),
        ("Tomato_bacterial_spot", "Bacterial_spot"),
        ("Tomato_yellow_virus", "Tomato_yellow_leaf_curl"),
        ("Tomato_mosaic_virus", "Tomato_mosaic_virus"),
        ("Tomato_two_spotted_spider_mites", "Spider_mite"),
        ("Apple_scab", "Apple_scab"),
        ("Apple_rust", "Cedar_apple_rust"),
        ("Grape_black_rot", "Grape_black_rot"),
        ("Peach_leaf", "Healthy"),
        ("Strawberry_leaf", "Healthy"),
        ("Blueberry_leaf", "Healthy"),
        ("Raspberry_leaf", "Healthy"),
        ("Soybean_leaf", "Healthy"),
        ("Bell_pepper_leaf_spot", "Bacterial_spot"),
        ("Cherry_leaf", "Healthy"),
        ("Tomato_leaf", "Healthy"),
        ("Apple Scab Leaf", "Apple_scab"),
        ("Apple leaf", "Healthy"),
        ("Apple rust leaf", "Cedar_apple_rust"),
        ("Bell_pepper leaf", "Healthy"),
        ("Bell_pepper leaf spot", "Bacterial_spot"),
        ("Blueberry leaf", "Healthy"),
        ("Cherry leaf", "Healthy"),
        ("Corn Gray leaf spot", "Leaf_spot"),
        ("Corn leaf blight", "Leaf_spot"),
        ("Corn rust leaf", "Rust"),
        ("Peach leaf", "Healthy"),
        ("Potato leaf early blight", "Early_blight"),
        ("Potato leaf late blight", "Late_blight"),
        ("Raspberry leaf", "Healthy"),
        ("Soyabean leaf", "Healthy"),
        ("Squash Powdery mildew leaf", "Squash_powdery_mildew"),
        ("Strawberry leaf", "Healthy"),
        ("Tomato Early blight leaf", "Early_blight"),
        ("Tomato Septoria leaf spot", "Septoria_leaf_spot"),
        ("Tomato leaf", "Healthy"),
        ("Tomato leaf bacterial spot", "Bacterial_spot"),
        ("Tomato leaf late blight", "Late_blight"),
        ("Tomato leaf mosaic virus", "Tomato_mosaic_virus"),
        ("Tomato leaf yellow virus", "Tomato_yellow_leaf_curl"),
        ("Tomato mold leaf", "Leaf_spot"),
        ("Tomato two spotted spider mites leaf", "Spider_mite"),
        ("grape leaf", "Healthy"),
        ("grape leaf black rot", "Grape_black_rot"),
    ]
    for src, tgt in plantdoc_mappings:
        mapper.add_mapping("plantdoc", src, tgt, "diseases", confidence="medium", notes="Real-world field images; may have multiple diseases")

    # DeepWeeds (weeds)
    deepweeds_mappings = [
        ("Chinee apple", "Other_weed"),
        ("Snake weed", "Other_weed"),
        ("Lantana", "Other_weed"),
        ("Prickly acacia", "Other_weed"),
        ("Siam weed", "Other_weed"),
        ("Parthenium", "Other_weed"),
        ("Rubber vine", "Other_weed"),
        ("Parkinsonia", "Other_weed"),
        ("Negative", "Other_weed"),
    ]
    for src, tgt in deepweeds_mappings:
        mapper.add_mapping("deepweeds", src, tgt, "weeds", confidence="low", notes="Australian species; not common in North American gardens. Use as supplement only.")

    # Plant Growth Stage Detection
    growth_mappings = [
        ("Flowering", "Flowering"),
        ("Germination", "Seedling"),
        ("Harvesting", "Mature_Harvest"),
        ("Vegetative", "Vegetative"),
    ]
    for src, tgt in growth_mappings:
        mapper.add_mapping("plant_growth_stage", src, tgt, "growth_stages", confidence="high")

    # BDFlower
    bdflower_mappings = [
        ("Early_Stage", "Flowering"),
        ("Mid_Stage", "Flowering"),
        ("Full_Stage", "Flowering"),
    ]
    for src, tgt in bdflower_mappings:
        mapper.add_mapping("bdflower", src, tgt, "growth_stages", confidence="medium", notes="Flower-specific; generalizable to other plants")

    return mapper


if __name__ == "__main__":
    mapper = initialize_default_mappings()
    print(f"Loaded {len(mapper.mappings)} class mappings.")
    print(f"Ambiguous mappings: {len(mapper.get_ambiguous_mappings())}")
