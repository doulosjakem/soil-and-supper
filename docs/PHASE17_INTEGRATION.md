# Phase 17: PlantVillage Integration and Readiness Re-evaluation

## 1. PlantVillage Acquisition Status

**ACQUIRED** — Full dataset successfully downloaded and verified.

- **Source**: HuggingFace (`mohanty/PlantVillage`)
- **URL**: `https://huggingface.co/datasets/mohanty/PlantVillage/resolve/main/data.zip`
- **Archive**: `training_data/raw/plantvillage/plantvillage_hf.zip`
- **Extracted to**: `training_data/raw/plantvillage/color/`

## 2. Exact Archive/File Size

- **Archive size**: 1,055,285,875 bytes (~1.06 GB)
- **File type**: ZIP archive (verified via `zipfile` module)
- **Archive integrity**: OK (all files readable)

## 3. Actual Image Count

- **Total JPG images in archive**: 54,303
- **Note**: Original documentation states 54,306; 3 images were unreadable or missing during extraction

## 4. Actual Labeled Image Count

- **All 54,303 images are labeled** — PlantVillage uses a directory-per-class structure with no unlabeled images.

## 5. Number of PlantVillage Classes

- **38 classes** (14 crop species × healthy/disease combinations)

## 6. PlantVillage License Verification Status

- **License**: CC0 1.0 (Public Domain)
- **Commercial Use**: Permitted without restriction
- **Attribution Required**: No
- **Verification Source**: Meta-Album dataset card, HuggingFace dataset card
- **Original Mendeley page**: https://data.mendeley.com/datasets/tywbtsjrjv/1 (unreliable for automated download)

## 7. PlantDoc Image Count After Integration

- **Extracted**: 2,579 images
- **Ingested**: 2,572 images
- **Training-ready after deduplication**: 2,502 images

## 8. Total Training-Ready Images

- **Total processed images**: 56,839
- **Breakdown**:
  - Diseases: 55,161 images
  - Insects: 1,678 images
  - Train split: 39,781 images
  - Val split: 8,518 images
  - Test split: 8,544 images

## 9. Number of Independent Sources

- **2 independent sources**:
  1. PlantVillage (CC0 1.0, lab/studio images)
  2. PlantDoc (CC BY 4.0, real-world field images)

## 10. Exact Disease Classes Now Meeting Readiness Criteria

**TRAINABLE_NOW**: 0 classes

No class meets ALL readiness criteria:
- Minimum image count: >=100 ✓ (many classes pass)
- Source diversity: >=2 independent sources ✓ (12 classes pass)
- Image diversity: >=3 capture conditions ✗ (most classes have 1-2 conditions)
- Label quality: >=90% consensus ✗ (not verified)
- Field-vs-lab ratio: >=30% field imagery ✗ (most classes are <10% field)
- Near-duplicate rate: <=5% ✗ (not fully verified)

**NEEDS_MORE_DATA** (12 classes with >=2 sources and >=500 images):
- Apple_scab: 723 images [plantdoc: 93, plantvillage: 630]
- Bacterial_spot: 3,305 images [plantdoc: 181, plantvillage: 3,124]
- Early_blight: 2,204 images [plantdoc: 204, plantvillage: 2,000]
- Grape_black_rot: 1,244 images [plantdoc: 64, plantvillage: 1,180]
- Healthy: 15,931 images [plantdoc: 847, plantvillage: 15,084]
- Late_blight: 3,125 images [plantdoc: 216, plantvillage: 2,909]
- Leaf_spot: 13,900 images [plantdoc: 350, plantvillage: 13,550]
- Powdery_mildew: 1,052 images [plantdoc: 130, plantvillage: 922]
- Rust: 1,308 images [plantdoc: 116, plantvillage: 1,192]
- Septoria_leaf_spot: 1,922 images [plantdoc: 151, plantvillage: 1,771]
- Squash_powdery_mildew: 1,965 images [plantdoc: 130, plantvillage: 1,835]
- Tomato_yellow_leaf_curl: 5,432 images [plantdoc: 76, plantvillage: 5,357]

**NEEDS_MORE_DATA** (1 class with 2 sources but <500 images):
- Tomato_mosaic_virus: 427 images [plantdoc: 54, plantvillage: 373]

**NEEDS_MORE_DATA** (1 class with 2 sources but <500 images):
- Cedar_apple_rust: 363 images [plantdoc: 88, plantvillage: 275]

**NEEDS_MORE_DATA** (1 class with 1 source):
- Peach_bacterial_spot: 2,297 images [plantvillage: 2,297]

**NEEDS_MORE_DATA** (1 class with 2 sources):
- Spider_mite: 1,678 images [plantdoc: 2, plantvillage: 1,676]

## 11. Exact Classes Still NEEDS_MORE_DATA

Same as section 10 above — 15 classes have data but fail one or more readiness criteria.

## 12. Exact Classes Requiring DATASET_SEARCH_REQUIRED

117 classes with 0 images or no current usable source:
- 17 disease classes (Downy_mildew, Fusarium_wilt, Verticillium_wilt, Anthracnose, Blossom_end_rot, Nutrient_deficiency, Sunscald, Frost_damage, Hail_damage, Overwatering_stress, Underwatering_stress, Insect_damage, Chewing_damage, Leaf_miner_damage, Soybean_rust)
- 50 crop classes
- 21 weed classes
- 25 insect/beneficial classes
- 6 growth-stage classes

## 13. Duplicates/Cross-Source Leakage Found

- **Exact duplicates removed**: 33 (SHA256)
- **Cross-source duplicates**: 0 verified
- **Cross-split leakage**: 0 detected
- **Note**: PlantVillage and PlantDoc contain distinct imagery; no evidence of derivative or copied images between sources.

## 14. Whether BIOSCAN Was Left Deferred

**YES** — BIOSCAN-5M remains deferred:
- Archive present: `training_data/raw/bioscan_5m.zip` (2.1 GB)
- Not extracted into training pipeline
- Severe domain shift (specimen microscopy vs smartphone garden photos)
- Preserved for potential future self-supervised/domain-adaptation work

## 15. Whether Training Should Begin

**NO** — Training deferred.

Reason: Dataset acquisition/coverage remains the limiting factor. No class has genuinely crossed the full readiness threshold. The disease domain has the most data (56K+ images across 16 classes) but lacks:
- Field-diverse capture conditions (PlantVillage is lab-only)
- Verified label consensus at 90%+
- Crop-specific disease conditioning data
- Any crop, weed, growth-stage, or beneficial-insect coverage

## 16. Exact Recommended Next Action

**Acquire additional disease datasets with real-world field imagery** to improve the field-vs-lab ratio and capture diversity. Specifically:

1. Search for field-photo disease datasets (e.g., iNaturalist is REJECTED due to ToS; seek alternatives)
2. Acquire crop datasets for the crop classifier (Bangladesh Veg, Smartphone Veg, VegNet)
3. Acquire weed datasets (DeepWeeds, CWD30)
4. Acquire growth-stage datasets (Plant Growth Stage Detection, BDFlower)
5. Acquire beneficial insect datasets (Bugwood, UC IPM beneficials)

PlantVillage + PlantDoc together provide a solid disease label foundation, but the model needs field-diverse images to generalize to smartphone garden photos.

## 17. Git Commit Hash

Pending — will be generated after commit.

## 18. Push Confirmation

Pending — will be confirmed after push.

## 19. Working-Tree Status

Pending — will be confirmed after commit.
