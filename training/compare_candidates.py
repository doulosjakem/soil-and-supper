#!/usr/bin/env python3
"""
Phase 27 Step 2: Candidate comparison report for external test set.
Compares DiaMOS Plant Dataset and FieldPlant.
"""

import json
from pathlib import Path
from datetime import datetime

MANIFESTS_DIR = Path(__file__).resolve().parent.parent / "training_data" / "manifests"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "training_data" / "reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

comparison = {
    "generated_at": datetime.now().isoformat(),
    "phase": "Phase 27",
    "step": "Step 2 — Candidate Comparison",
    "candidates": {
        "diamos_plant": {
            "dataset_name": "DiaMOS Plant Dataset",
            "primary_source": "Zenodo 5557313",
            "doi": "10.5281/zenodo.5557313",
            "license": "CC BY 4.0",
            "license_verification": "PRIMARY_SOURCE — Zenodo record + paper + OpenAIRE",
            "authors": "Gianni Fenu, Francesca Maridina Malloci",
            "institution": "University of Cagliari",
            "publication": "Agronomy 2021, 11, 2107",
            "image_count": 3505,
            "leaf_image_count": 3006,
            "fruit_image_count": 499,
            "classes": [
                "spot_leaf",
                "curl_leaf",
                "slug_leaf",
                "healthy_leaf",
                "fruit_set",
                "nut_fruit",
                "fruit_growth",
                "ripening"
            ],
            "class_counts": {
                "spot_leaf": "unknown (part of 4 leaf diseases)",
                "curl_leaf": "unknown",
                "slug_leaf": "unknown",
                "healthy_leaf": "unknown",
                "fruit_set": "unknown",
                "nut_fruit": "unknown",
                "fruit_growth": "unknown",
                "ripening": "unknown"
            },
            "taxonomy_mapping": {
                "healthy_leaf": "Healthy (HIGH_CONFIDENCE)",
                "spot_leaf": "UNMAPPABLE (too generic — could be Leaf_spot, Bacterial_spot, etc.)",
                "curl_leaf": "UNMAPPABLE (could be viral, bacterial, or physiological)",
                "slug_leaf": "OUT-OF-TAXONOMY (slug damage not in Soil & Supper taxonomy)",
                "fruit_set": "OUT-OF-TAXONOMY (fruit stage, not disease)",
                "nut_fruit": "OUT-OF-TAXONOMY (fruit stage, not disease)",
                "fruit_growth": "OUT-OF-TAXONOMY (fruit stage, not disease)",
                "ripening": "OUT-OF-TAXONOMY (fruit stage, not disease)"
            },
            "mappable_classes": ["Healthy"],
            "mappable_image_count": "unknown — need to download and inspect labels",
            "geography": "Sardegna, Italy",
            "capture_context": "Field-collected pear orchard, real conditions",
            "camera_device": "Honor 6x smartphone + Canon EOS 60D DSLR",
            "time_period": "2021 growing season",
            "annotation_quality": "Expert — plant pathologists annotated bounding boxes",
            "overlap_risk_with_training": "LOW — different geography (Italy), different crop (pear), different device. No relationship to PlantVillage/PlantDoc/Irish_Potato/Grapevine.",
            "known_limitations": [
                "Only 1 mappable class (Healthy) with high confidence",
                "Other leaf classes are too generic or out-of-taxonomy",
                "Fruit stage images are not disease-relevant",
                "No overlap with existing commercial training data expected"
            ]
        },
        "fieldplant": {
            "dataset_name": "FieldPlant",
            "primary_source": "Roboflow Universe + IEEE Access 2023",
            "doi": "10.1109/ACCESS.2023.3263042",
            "license": "CC BY 4.0",
            "license_verification": "PRIMARY_SOURCE — Roboflow data.yaml + paper + Kaggle",
            "authors": "Emmanuel Moupojou, Appolinaire Tagne, Florent Retraint, Anicet Tadonkemwa, Dongmo Wilfried, Hyppolite Tapamo",
            "institution": "Cameroon universities (agro-ecological zones 3 and 5)",
            "publication": "IEEE Access 2023, 11, 35398-35410",
            "image_count": 5170,
            "leaf_image_count": 5170,
            "fruit_image_count": 0,
            "classes": [
                "Cassava_Bacterial_Disease",
                "Cassava_Brown_Leaf_Spot",
                "Cassava_Healthy",
                "Cassava_Mosaic",
                "Cassava_Root_Rot",
                "Corn_Healthy",
                "Corn_Smut",
                "Corn_Streak",
                "Corn_Blight",
                "Corn_Brown_Spots",
                "Corn_Cercosporiose",
                "Corn_Chlorotic_Leaf_Spot",
                "Corn_Insects_Damages",
                "Corn_Mildew",
                "Corn_Purple_Discoloration",
                "Corn_Rust",
                "Corn_Stripe",
                "Corn_Violet_Decoloration",
                "Corn_Yellow_Spots",
                "Corn_Yellowing",
                "Tomato_Brown_Spots",
                "Tomato_bacterial_wilt",
                "Tomato_blight_leaf",
                "Tomato_healthy",
                "Tomato_Leaf_Mosaic_Virus",
                "Tomato_Leaf_Yellow_Virus",
                "Manioc_Mosaique"
            ],
            "class_counts": {
                "Cassava_Bacterial_Disease": "unknown — need to inspect data",
                "Cassava_Brown_Leaf_Spot": "unknown",
                "Cassava_Healthy": "unknown",
                "Cassava_Mosaic": "unknown",
                "Cassava_Root_Rot": "unknown",
                "Corn_Healthy": "unknown",
                "Corn_Smut": "unknown",
                "Corn_Streak": "unknown",
                "Corn_Blight": "unknown",
                "Corn_Brown_Spots": "unknown",
                "Corn_Cercosporiose": "unknown",
                "Corn_Chlorotic_Leaf_Spot": "unknown",
                "Corn_Insects_Damages": "unknown",
                "Corn_Mildew": "unknown",
                "Corn_Purple_Discoloration": "unknown",
                "Corn_Rust": "unknown",
                "Corn_Stripe": "unknown",
                "Corn_Violet_Decoloration": "unknown",
                "Corn_Yellow_Spots": "unknown",
                "Corn_Yellowing": "unknown",
                "Tomato_Brown_Spots": "unknown",
                "Tomato_bacterial_wilt": "unknown",
                "Tomato_blight_leaf": "unknown",
                "Tomato_healthy": "unknown",
                "Tomato_Leaf_Mosaic_Virus": "unknown",
                "Tomato_Leaf_Yellow_Virus": "unknown",
                "Manioc_Mosaique": "unknown"
            },
            "taxonomy_mapping": {
                "Cassava_Healthy": "Healthy (HIGH_CONFIDENCE)",
                "Corn_Healthy": "Healthy (HIGH_CONFIDENCE)",
                "Tomato_healthy": "Healthy (HIGH_CONFIDENCE)",
                "Cassava_Brown_Leaf_Spot": "Leaf_spot (HIGH_CONFIDENCE)",
                "Corn_Brown_Spots": "Leaf_spot (HIGH_CONFIDENCE)",
                "Tomato_Brown_Spots": "Leaf_spot (HIGH_CONFIDENCE)",
                "Corn_Chlorotic_Leaf_Spot": "Leaf_spot (HIGH_CONFIDENCE)",
                "Tomato_blight_leaf": "Late_blight (HIGH_CONFIDENCE — tomato late blight)",
                "Corn_Blight": "Leaf_spot (HIGH_CONFIDENCE — northern corn leaf blight)",
                "Cassava_Bacterial_Disease": "UNMAPPABLE (too generic)",
                "Cassava_Mosaic": "UNMAPPABLE (viral disease not in taxonomy)",
                "Cassava_Root_Rot": "UNMAPPABLE (root disease, not leaf)",
                "Corn_Smut": "OUT-OF-TAXONOMY (corn-specific)",
                "Corn_Streak": "OUT-OF-TAXONOMY (corn-specific viral)",
                "Corn_Cercosporiose": "OUT-OF-TAXONOMY (corn-specific)",
                "Corn_Insects_Damages": "OUT-OF-TAXONOMY (insect damage, not disease)",
                "Corn_Mildew": "AMBIGUOUS (could be Powdery_mildew or Downy_mildew)",
                "Corn_Purple_Discoloration": "OUT-OF-TAXONOMY (nutrient/genetic)",
                "Corn_Rust": "Rust (HIGH_CONFIDENCE — corn rust)",
                "Corn_Stripe": "OUT-OF-TAXONOMY (corn-specific viral)",
                "Corn_Violet_Decoloration": "OUT-OF-TAXONOMY (nutrient/genetic)",
                "Corn_Yellow_Spots": "AMBIGUOUS (could be disease or nutrient)",
                "Corn_Yellowing": "AMBIGUOUS (could be disease or nutrient)",
                "Tomato_bacterial_wilt": "UNMAPPABLE (bacterial wilt not in taxonomy)",
                "Tomato_Leaf_Mosaic_Virus": "UNMAPPABLE (viral disease not in taxonomy)",
                "Tomato_Leaf_Yellow_Virus": "UNMAPPABLE (viral disease not in taxonomy)",
                "Manioc_Mosaique": "UNMAPPABLE (cassava mosaic variant)"
            },
            "mappable_classes": [
                "Cassava_Healthy", "Corn_Healthy", "Tomato_healthy",
                "Cassava_Brown_Leaf_Spot", "Corn_Brown_Spots", "Tomato_Brown_Spots",
                "Corn_Chlorotic_Leaf_Spot", "Corn_Blight",
                "Tomato_blight_leaf",
                "Corn_Rust"
            ],
            "mappable_image_count": "unknown — need to download and inspect labels",
            "geography": "Cameroon plantations (Zones 3 and 5)",
            "capture_context": "Field-collected from plantations, complex backgrounds, multiple leaves per image",
            "camera_device": "Smartphones with 4608×3456 cameras",
            "time_period": "July-December 2022",
            "annotation_quality": "Expert — plant pathologists annotated, two-step validation",
            "overlap_risk_with_training": "MODERATE — images were downloaded from the internet and may overlap with PlantDoc (which is already in training). Some images may be sourced from similar repositories. Requires exact + phash check.",
            "known_limitations": [
                "Some classes are corn/cassava/tomato-specific and not directly mappable",
                "Internet-sourced images may have overlap with PlantDoc training data",
                "Multiple leaves per image make classification more complex",
                "Some disease classes are ambiguous (e.g., Corn_Mildew)"
            ]
        }
    },
    "comparison_matrix": {
        "A_license_certainty": {
            "diamos_plant": "HIGH — Zenodo CC BY 4.0 confirmed from primary source",
            "fieldplant": "HIGH — Roboflow CC BY 4.0 confirmed from data.yaml + paper",
            "winner": "TIE"
        },
        "B_usable_images": {
            "diamos_plant": "3,505 total, ~3,006 leaf images, ~1 mappable class (Healthy) with high confidence",
            "fieldplant": "5,170 total, ~10 mappable classes with high confidence",
            "winner": "fieldplant"
        },
        "C_soil_supper_classes_represented": {
            "diamos_plant": "1 (Healthy only)",
            "fieldplant": "3+ (Healthy, Leaf_spot, Rust, Late_blight potentially)",
            "winner": "fieldplant"
        },
        "D_images_per_mapped_class": {
            "diamos_plant": "Unknown — need to inspect labels, but likely limited Healthy count",
            "fieldplant": "Unknown — need to inspect labels, but likely better distribution",
            "winner": "fieldplant (projected)"
        },
        "E_geographic_diversity": {
            "diamos_plant": "Italy (Sardegna) — European Mediterranean",
            "fieldplant": "Cameroon — West African tropical",
            "winner": "fieldplant (more distinct from US training data)"
        },
        "F_field_vs_laboratory": {
            "diamos_plant": "Field — real pear orchard conditions",
            "fieldplant": "Field — plantation conditions, complex backgrounds",
            "winner": "TIE — both are field images"
        },
        "G_capture_conditions": {
            "diamos_plant": "Variable distances, angles, sunlight; DSLR + smartphone",
            "fieldplant": "Smartphone only, full plantation background, multiple leaves per image",
            "winner": "diamos_plant (more diverse capture conditions)"
        },
        "H_relationship_to_existing_datasets": {
            "diamos_plant": "NONE — independent collection, pear-specific, Italy",
            "fieldplant": "POTENTIAL — images downloaded from internet, compared to PlantDoc in paper",
            "winner": "diamos_plant"
        },
        "I_likelihood_of_overlap": {
            "diamos_plant": "LOW — different crop, geography, device",
            "fieldplant": "MODERATE — internet-sourced, compared to PlantDoc",
            "winner": "diamos_plant"
        },
        "J_suitability_as_external_evaluation_source": {
            "diamos_plant": "MODERATE — excellent independence, but only Healthy class maps directly. Limited taxonomic coverage.",
            "fieldplant": "HIGH — multiple mappable classes, field conditions, expert annotation, geographic diversity. Overlap risk requires verification.",
            "winner": "fieldplant (if overlap checks pass)"
        }
    },
    "recommendation": {
        "selected_candidate": "fieldplant",
        "rationale": "FieldPlant offers superior taxonomic coverage (multiple mappable classes), field-realistic capture conditions, expert annotation, and geographic diversity. While DiaMOS has lower overlap risk, it only provides 1 mappable class (Healthy), which severely limits its utility as an external evaluation set. FieldPlant's overlap risk is moderate and can be mitigated through exact + phash checks. If overlap checks reveal significant duplication with PlantDoc, DiaMOS would be the fallback.",
        "contingency": "If FieldPlant fails overlap checks (>5% duplicate or near-duplicate images), fall back to DiaMOS Plant Dataset for Healthy-class evaluation only."
    }
}

report_path = REPORTS_DIR / "external_test_candidate_comparison.json"
with open(report_path, "w") as f:
    json.dump(comparison, f, indent=2)
print(f"Comparison report saved to: {report_path}")
print(f"\nSelected candidate: {comparison['recommendation']['selected_candidate']}")
print(f"Rationale: {comparison['recommendation']['rationale']}")
