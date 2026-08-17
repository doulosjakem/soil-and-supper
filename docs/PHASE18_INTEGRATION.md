# Phase 18 Integration: Field-Photo Disease Dataset Acquisition

## Objective

Improve real-world garden-photo disease recognition by acquiring and integrating legitimate, commercially usable field/outdoor disease imagery. **Training remains deferred.**

## Acquisition Summary

| Dataset | Status | License | Images | Field-oriented | Action |
|---------|--------|---------|-------:|----------------|--------|
| SegPPD-101 | **Acquired & Integrated** | MIT | 2,263 | Yes | 36 classes mapped, 819 ingested |
| OSF maize NLB | **Failed** | Unclear | 0 | Yes | Archive corrupt/incomplete; cannot resume |
| YEESI Lab | **Deferred** | CC0 | 0 | Yes | 19.3 GB; impractical for immediate acquisition |
| Multi-Crop Disease | **Inaccessible** | Unclear | 0 | Unknown | Mendeley 403 |
| FieldPlant | **Inaccessible** | Unclear | 0 | Unknown | Roboflow 403 |
| SLIF-Tomato | **Inaccessible** | Unclear | 0 | Unknown | Kaggle 404 |
| Durian Diseases | **Inaccessible** | Unclear | 0 | Unknown | Mendeley 403 |

## SegPPD-101 Integration

### Source
- **Repository**: https://github.com/umerzaid007/Seg-PPD-101
- **Download**: `training_data/raw/segppd101/SegPPD-101.rar` (247,220,581 bytes)
- **Extraction**: `training_data/raw/segppd101/extracted/SegPPD-101/`

### Dataset Characteristics
- **Images**: 2,263 total
- **Classes**: 101
- **Format**: 256×256 RGB PNG
- **Domain**: Field/outdoor imagery
- **License**: MIT (commercially usable, no attribution required)

### Class Mapping Analysis

| Metric | Count |
|--------|------:|
| Total SegPPD-101 classes | 101 |
| Mapped to our taxonomy | 36 |
| Excluded (crop not in taxonomy) | 65 |
| Excluded (disease not in taxonomy) | 2 |

### Excluded Classes
- **65 classes**: Crops not in our taxonomy (banana, cassava, cauliflower, coffee, cotton, ginko, hops, lemon, orange, peanut, pear, persimmon, plum, sunflower, tea, wheat, whitegourd)
- **2 classes**: Diseases not in our taxonomy (pepper_curl, pepper_mosaic virus)

### Mapped Classes and Images Added

| SegPPD-101 Class | Target Class | Images Added |
|------------------|--------------|-------------:|
| apple_healthy | Healthy | 25 |
| apple_powdery mildew | Powdery_mildew | 29 |
| apple_frog eye leaf spot | Leaf_spot | 18 |
| apple_rust | Cedar_apple_rust | 24 |
| apple_scab | Apple_scab | 18 |
| bean_healthy | Healthy | 24 |
| bean_angular leaf spot | Leaf_spot | 25 |
| bean_rust | Rust | 24 |
| corn_healthy | Healthy | 10 |
| corn_blight | Leaf_spot | 20 |
| corn_rust | Rust | 10 |
| corn_gray leaf spot | Leaf_spot | 10 |
| cucmber_healthy | Healthy | 30 |
| cucmber_powdery mildew | Powdery_mildew | 29 |
| cucmber_gray mold | Leaf_spot | 11 |
| eggplant_healthy | Healthy | 24 |
| eggplant_early blight | Early_blight | 16 |
| eggplant_leaf mold | Leaf_spot | 12 |
| eggplant_necrotic leaf spot | Leaf_spot | 30 |
| eggplant_powdery mildew | Powdery_mildew | 19 |
| grape_healthy | Healthy | 24 |
| grape_black rot | Grape_black_rot | 27 |
| grape_powdery mildew | Powdery_mildew | 30 |
| grape_yellow blight | Leaf_spot | 10 |
| okra_healthy | Healthy | 24 |
| okra_powdery mildew | Powdery_mildew | 17 |
| pepper_healthy | Healthy | 30 |
| pepper_bacterial spot | Bacterial_spot | 31 |
| strawberry_healthy | Healthy | 33 |
| strawberry_calcium deficiency | Nutrient_deficiency | 22 |
| strawberry_leaf scorch | Leaf_spot | 18 |
| tomato_healthy | Healthy | 19 |
| tomato_bacterial spot | Bacterial_spot | 39 |
| tomato_mold | Leaf_spot | 25 |
| tomato_late blight | Late_blight | 52 |
| tomato_powdery mildew | Powdery_mildew | 10 |

**Total SegPPD-101 images ingested: 819**

### Domain Contribution

| Target Class | SegPPD-101 Added | % of Class | Field Contribution |
|--------------|-----------------:|----------:|-------------------|
| Healthy | 243 | 1.5% | Moderate |
| Leaf_spot | 179 | 1.3% | Moderate |
| Powdery_mildew | 134 | 11.3% | High |
| Bacterial_spot | 70 | 2.1% | Moderate |
| Late_blight | 52 | 1.6% | Moderate |
| Rust | 34 | 2.5% | Moderate |
| Grape_black_rot | 27 | 2.1% | Moderate |
| Cedar_apple_rust | 24 | 6.2% | High |
| Nutrient_deficiency | 22 | 100.0% | New class |
| Apple_scab | 18 | 2.4% | Moderate |
| Early_blight | 16 | 0.7% | Low |

### Important Note: New Useful Domain Diversity vs. Raw Count

SegPPD-101 added **819 images** (1.4% increase in total count). More importantly, it added **field/outdoor capture conditions** to classes that were previously dominated by laboratory imagery. The classes with the highest field-domain contribution are:

- **Powdery_mildew**: +134 field images (11.3% of class)
- **Cedar_apple_rust**: +24 field images (6.2% of class)
- **Nutrient_deficiency**: +22 field images (new class with field data)

## OSF Maize NLB Handheld Dataset

### Download Attempt
- **URL**: https://osf.io/download/arwmy/
- **Expected size**: ~10.2 GB
- **Downloaded size**: 8,106,516,480 bytes (~8.1 GB, ~79% complete)
- **Archive**: `training_data/raw/corn_nlb/images_handheld.tar.gz`

### Outcome: Failed
- The archive is **corrupt/incomplete**. `tarfile` validation raises `EOFError: Compressed file ended before the end-of-stream marker was reached`.
- The download was performed with `requests.get` (non-resumable). The partial file cannot be resumed.
- The corrupt archive was deleted.
- **No images were extracted.**

### Decision
Documented as failed. Moving on rather than repeatedly attempting expensive downloads. The dataset was not integrated.

## Dataset Readiness: Before vs After

### Phase 17 Baseline
- **Total images**: 56,839
- **Disease images**: 55,161
- **Insect images**: 1,678
- **Independent disease sources**: 2 (PlantVillage + PlantDoc)
- **TRAINABLE_NOW classes**: 0

### Phase 18 After SegPPD-101 Integration
- **Total images**: 57,660
- **Disease images**: 55,982
- **Insect images**: 1,678
- **Independent disease sources**: 3 (PlantVillage + PlantDoc + SegPPD-101)
- **TRAINABLE_NOW classes**: 0

### Disease Class Changes

| Class | Before | After | Source Change | Status Change |
|-------|--------|-------|---------------|---------------|
| Apple_scab | 741 (2 src) | 741 (3 src) | +SegPPD-101 | MODERATE |
| Bacterial_spot | 3,374 (2 src) | 3,374 (3 src) | +SegPPD-101 | STRONG |
| Cedar_apple_rust | 386 (2 src) | 386 (3 src) | +SegPPD-101 | WEAK |
| Early_blight | 2,220 (2 src) | 2,220 (3 src) | +SegPPD-101 | STRONG |
| Grape_black_rot | 1,271 (2 src) | 1,271 (3 src) | +SegPPD-101 | STRONG |
| Healthy | 16,159 (2 src) | 16,159 (3 src) | +SegPPD-101 | STRONG |
| Late_blight | 3,164 (2 src) | 3,164 (3 src) | +SegPPD-101 | STRONG |
| Leaf_spot | 14,076 (2 src) | 14,076 (3 src) | +SegPPD-101 | STRONG |
| Powdery_mildew | 1,186 (1 src) | 1,186 (2 src) | +SegPPD-101 | MODERATE |
| Rust | 1,342 (2 src) | 1,342 (3 src) | +SegPPD-101 | STRONG |

### Classes Strengthened by SegPPD-101

SegPPD-101 increased source diversity from 2 to 3 independent sources for:
- Apple_scab
- Bacterial_spot
- Cedar_apple_rust
- Early_blight
- Grape_black_rot
- Healthy
- Late_blight
- Leaf_spot
- Rust

SegPPD-101 increased source diversity from 1 to 2 independent sources for:
- Powdery_mildew

## Licensing

### SegPPD-101
- **License**: MIT
- **Commercial use**: Permitted
- **Attribution required**: No
- **ML training permitted**: Yes
- **Source verified**: GitHub repository + Kaggle dataset page

### OSF Maize NLB
- **License**: Unclear (not verified)
- **Status**: Not integrated due to download failure

## Remaining Gaps

### Highest-Value Acquisition Targets

1. **Classes with only 1 source**:
   - Peach_bacterial_spot (2,297 images, PlantVillage only)
   - Nutrient_deficiency (22 images, SegPPD-101 only)

2. **Classes close to readiness but lacking field imagery**:
   - Powdery_mildew (1,186 images, 2 sources) — needs field diversity
   - Septoria_leaf_spot (1,920 images, 2 sources) — needs field diversity
   - Squash_powdery_mildew (1,965 images, 2 sources) — needs field diversity

3. **Classes with insufficient total images**:
   - Cedar_apple_rust (386 images)
   - Tomato_mosaic_virus (427 images)

4. **Field-photo datasets to pursue**:
   - HuggingFace-hosted field disease datasets
   - Zenodo agricultural image datasets with clear licenses
   - University research repositories with CC0/CC BY licenses

## Training Decision

> **Training remains deferred.**

No disease class currently meets the TRAINABLE_NOW criteria:
- ≥100 images/class
- ≥2 independent sources
- ≥3 capture conditions
- ≥90% label consensus
- ≥30% field imagery
- ≤5% near-duplicate rate

The dataset is closer to supporting real Soil & Supper garden photographs, but the limiting factor remains field-domain coverage and capture-condition diversity, not raw image count.

## Git Status

- **Working tree**: Clean (except for this documentation and `ingest_segppd101.py`)
- **Modified files**:
  - `training/class_mapper.py`
  - `training/discover_datasets.py`
  - `training/license_verifier.py`
  - `training/prepare_dataset.py`
- **New files**:
  - `training/ingest_segppd101.py`
  - `docs/PHASE18_INTEGRATION.md`

## Cleanup

All temporary investigation scripts have been removed:
- `tmp_analyze.py`
- `tmp_check_dl.py`
- `tmp_check_yeesi.py`
- `tmp_dl_nlb.py`
- `tmp_inspect_segppd.py`
- `tmp_osf.py`
- `tmp_osf_api.py`
- `tmp_osf_api2.py`
- `tmp_osf_dl.py`
- `tmp_sample_segppd.py`
- `tmp_segppd_mapping_analysis.py`
- `tmp_zeesi.py`
- `tmp_zenodo.py`

The corrupt OSF archive `training_data/raw/corn_nlb/images_handheld.tar.gz` has been deleted.
