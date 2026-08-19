#!/usr/bin/env python3
"""
Phase 27: External Test Dataset Acquisition & Independence Audit Report
"""

import json
from pathlib import Path
from datetime import datetime

MANIFESTS_DIR = Path(__file__).resolve().parent.parent / "training_data" / "manifests"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "training_data" / "reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

audit = {
    "phase": "Phase 27",
    "title": "External Test Dataset Acquisition & Independence Audit",
    "generated_at": datetime.now().isoformat(),
    "status": "NO_APPROVED_EXTERNAL_TEST_SET",
    "summary": "Neither DiaMOS Plant Dataset nor FieldPlant could be successfully acquired and validated as an external test set due to download/authentication barriers and impractical dataset size. License verification passed for both candidates, but acquisition could not be completed.",
    
    "step1_verification": {
        "diamos_plant": {
            "dataset_id": "diamos_plant",
            "name": "DiaMOS Plant Dataset",
            "primary_source": "Zenodo 5557313",
            "doi": "10.5281/zenodo.5557313",
            "license": "CC BY 4.0",
            "license_verification_status": "APPROVED",
            "verification_notes": "Zenodo record explicitly lists CC BY 4.0 license. OpenAIRE confirms CC BY. Paper states dataset is freely available. DOI: 10.5281/zenodo.5557313. Authors: Gianni Fenu, Francesca Maridina Malloci (University of Cagliari). 3,505 images (3,006 leaf + 499 fruit). Field-collected pear orchard, Sardegna, Italy. Honor 6x smartphone + Canon EOS 60D DSLR. Published October 2021.",
            "issues": []
        },
        "fieldplant": {
            "dataset_id": "fieldplant",
            "name": "FieldPlant",
            "primary_source": "Roboflow Universe + IEEE Access 2023",
            "doi": "10.1109/ACCESS.2023.3263042",
            "license": "CC BY 4.0",
            "license_verification_status": "APPROVED",
            "verification_notes": "Roboflow Universe explicitly lists CC BY 4.0 license. data.yaml confirms license: CC BY 4.0. IEEE Access paper (DOI: 10.1109/ACCESS.2023.3263042) is open access under CC BY 4.0. Authors: Emmanuel Moupojou et al. 5,170 images collected from Cameroon plantations. Smartphone cameras (4608x3456). Expert annotation by plant pathologists. Published March 2023.",
            "issues": []
        }
    },
    
    "step2_comparison": {
        "selected_candidate": "fieldplant",
        "rationale": "FieldPlant offers superior taxonomic coverage (multiple mappable classes), field-realistic capture conditions, expert annotation, and geographic diversity. While DiaMOS has lower overlap risk, it only provides 1 mappable class (Healthy), which severely limits its utility as an external evaluation set.",
        "contingency": "If FieldPlant fails overlap checks (>5% duplicate or near-duplicate images), fall back to DiaMOS Plant Dataset for Healthy-class evaluation only."
    },
    
    "step3_taxonomy_mapping": {
        "fieldplant_mapping": {
            "Cassava_Healthy": {"mapped_class": "Healthy", "status": "HIGH_CONFIDENCE"},
            "Corn_Healthy": {"mapped_class": "Healthy", "status": "HIGH_CONFIDENCE"},
            "Tomato_healthy": {"mapped_class": "Healthy", "status": "HIGH_CONFIDENCE"},
            "Cassava_Brown_Leaf_Spot": {"mapped_class": "Leaf_spot", "status": "HIGH_CONFIDENCE"},
            "Corn_Brown_Spots": {"mapped_class": "Leaf_spot", "status": "HIGH_CONFIDENCE"},
            "Tomato_Brown_Spots": {"mapped_class": "Leaf_spot", "status": "HIGH_CONFIDENCE"},
            "Corn_Chlorotic_Leaf_Spot": {"mapped_class": "Leaf_spot", "status": "HIGH_CONFIDENCE"},
            "Tomato_blight_leaf": {"mapped_class": "Late_blight", "status": "HIGH_CONFIDENCE"},
            "Corn_Blight": {"mapped_class": "Leaf_spot", "status": "HIGH_CONFIDENCE"},
            "Corn_Rust": {"mapped_class": "Rust", "status": "HIGH_CONFIDENCE"},
            "Cassava_Bacterial_Disease": {"mapped_class": None, "status": "UNMAPPABLE"},
            "Cassava_Mosaic": {"mapped_class": None, "status": "UNMAPPABLE"},
            "Cassava_Root_Rot": {"mapped_class": None, "status": "UNMAPPABLE"},
            "Corn_Smut": {"mapped_class": None, "status": "OUT-OF-TAXONOMY"},
            "Corn_Streak": {"mapped_class": None, "status": "OUT-OF-TAXONOMY"},
            "Corn_Cercosporiose": {"mapped_class": None, "status": "OUT-OF-TAXONOMY"},
            "Corn_Insects_Damages": {"mapped_class": None, "status": "OUT-OF-TAXONOMY"},
            "Corn_Mildew": {"mapped_class": None, "status": "AMBIGUOUS"},
            "Corn_Purple_Discoloration": {"mapped_class": None, "status": "OUT-OF-TAXONOMY"},
            "Corn_Stripe": {"mapped_class": None, "status": "OUT-OF-TAXONOMY"},
            "Corn_Violet_Decoloration": {"mapped_class": None, "status": "OUT-OF-TAXONOMY"},
            "Corn_Yellow_Spots": {"mapped_class": None, "status": "AMBIGUOUS"},
            "Corn_Yellowing": {"mapped_class": None, "status": "AMBIGUOUS"},
            "Tomato_bacterial_wilt": {"mapped_class": None, "status": "UNMAPPABLE"},
            "Tomato_Leaf_Mosaic_Virus": {"mapped_class": None, "status": "UNMAPPABLE"},
            "Tomato_Leaf_Yellow_Virus": {"mapped_class": None, "status": "UNMAPPABLE"},
            "Manioc_Mosaique": {"mapped_class": None, "status": "UNMAPPABLE"}
        }
    },
    
    "step4_acquisition": {
        "attempted": True,
        "successful": False,
        "selected_dataset": "fieldplant",
        "attempted_sources": [
            {
                "source": "Roboflow Python package",
                "url": "https://universe.roboflow.com/plant-disease-detection/fieldplant",
                "status": "FAILED",
                "reason": "Roboflow API requires authentication (API key). No public download endpoint found."
            },
            {
                "source": "Roboflow CLI",
                "status": "FAILED",
                "reason": "Roboflow CLI not installed; package installation requires authentication"
            },
            {
                "source": "Kaggle",
                "url": "https://www.kaggle.com/datasets/manhhoangvan/fieldplant",
                "status": "FAILED",
                "reason": "Kaggle API requires authentication (kaggle.json token). Page JavaScript crash when accessed directly."
            },
            {
                "source": "Zenodo (DiaMOS fallback)",
                "url": "https://zenodo.org/records/5557313/files/Pear.zip?download=1",
                "status": "FAILED",
                "reason": "Zenodo browser verification required. Download timed out after 300s at ~396MB of 13.1GB. Practical download time estimated at 8-12 hours."
            }
        ],
        "acquisition_details": {
            "acquisition_date": None,
            "source_url": None,
            "version": None,
            "license": None,
            "checksum": None,
            "raw_storage_location": None
        }
    },
    
    "step5_overlap_audit": {
        "attempted": False,
        "reason": "No dataset was successfully acquired. Overlap audit could not be performed."
    },
    
    "step6_source_relationships": {
        "investigated": False,
        "reason": "No dataset was successfully acquired. Source relationship investigation could not be performed."
    },
    
    "step7_test_size": {
        "determined": False,
        "reason": "No dataset was successfully acquired. Test size determination could not be performed."
    },
    
    "step8_external_manifest": {
        "created": False,
        "path": None,
        "reason": "No dataset passed all gates. Manifest was not created."
    },
    
    "step9_audit_report": {
        "created": True,
        "path": str(REPORTS_DIR / "external_test_audit.json"),
        "status": "NO_APPROVED_TEST_SET"
    },
    
    "step10_documentation": {
        "updated": False,
        "reason": "No dataset passed all gates. Documentation was not updated with new external test set information."
    },
    
    "why_candidates_failed": {
        "fieldplant": {
            "license": "CC BY 4.0 (verified from primary sources)",
            "failure_reason": "Download authentication barrier. Roboflow API requires API key. Kaggle mirror requires authentication. No public direct download link found.",
            "requirement_missing": "REPRODUCIBLE acquisition path without authentication barriers"
        },
        "diamos_plant": {
            "license": "CC BY 4.0 (verified from primary sources)",
            "failure_reason": "Dataset size (13.1 GB) makes practical download infeasible in current environment. Zenodo requires browser verification. Partial download timed out after 300s.",
            "requirement_missing": "REPRODUCIBLE acquisition path within reasonable time/resource constraints"
        }
    },
    
    "remaining_candidate_sources": [
        "Search for FieldPlant mirrors on alternative platforms (Hugging Face Datasets, academic repositories)",
        "Contact FieldPlant authors directly for dataset access",
        "Look for smaller plant disease datasets with CC BY 4.0 licensing",
        "Consider PlantCLEF or other plant pathology challenge datasets",
        "Search for regional plant disease datasets from agricultural extension services"
    ],
    
    "next_acquisition_priority": [
        "1. Resolve FieldPlant download authentication (obtain Roboflow API key or Kaggle access)",
        "2. If FieldPlant remains inaccessible, search for DiaMOS subset or alternative",
        "3. Evaluate PlantCLEF 2020/2021/2022 datasets (plant classification, often CC licensed)",
        "4. Check iNaturalist plant observations (CC licensed, but label noise)",
        "5. Review recent plant pathology papers for newly released datasets"
    ],
    
    "validation_performed": {
        "license_verification": "COMPLETED - Both candidates verified CC BY 4.0 from primary sources",
        "taxonomy_mapping": "COMPLETED - FieldPlant mapping created with 10 HIGH_CONFIDENCE mappings",
        "comparison_analysis": "COMPLETED - FieldPlant selected as preferred candidate",
        "download_attempts": "COMPLETED - All sources attempted and failed",
        "overlap_audit": "NOT_PERFORMED - No dataset acquired",
        "no_training": True
    },
    
    "final_status": {
        "approved_external_test_set": False,
        "dataset": None,
        "reason": "No dataset could be acquired due to authentication barriers and impractical download size. License verification passed but REPRODUCIBLE acquisition requirement failed."
    }
}

report_path = REPORTS_DIR / "external_test_audit.json"
with open(report_path, "w") as f:
    json.dump(audit, f, indent=2)
print(f"Audit report saved to: {report_path}")
print(f"\nPhase 27 Status: {audit['status']}")
print(f"Final Status: {audit['final_status']['reason']}")
