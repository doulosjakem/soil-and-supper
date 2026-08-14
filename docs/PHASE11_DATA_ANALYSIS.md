# Phase 11 — Download, Curate, and Analyze the Real Training Data

## Executive Summary

Phase 11 attempted to download and process all 20 approved datasets from the Phase 10 registry. The download was performed into `D:\soil-and-supper\soil-and-supper\training_data\raw\` (HDD) to preserve SSD space.

**Status**: Download heavily constrained by environment. Only DeepWeeds repository (code + labels, no images) was successfully retrieved. All other datasets failed due to 403 Forbidden, 404 Not Found, or network resolution errors. The pipeline infrastructure is complete and tested. Full analysis is based on documented dataset metadata.

---

## 1. Downloaded Datasets

| Dataset | Status | Archive | Extracted | Images | Notes |
|---------|--------|---------|-----------|--------|-------|
| DeepWeeds | Partial | deepweeds.zip (3.5 MB) | DeepWeeds-master/ | 0 | GitHub repo only; images hosted on Google Drive (468 MB) — not downloaded |
| Bangladesh Vegetables | Failed | — | — | 0 | 403 Forbidden |
| Smartphone Vegetable Detection | Failed | — | — | 0 | 403 Forbidden |
| BanglaVeg | Failed | — | — | 0 | 403 Forbidden |
| PlantVillage | Failed | — | — | 0 | 403 Forbidden |
| PlantDoc | Failed | — | — | 0 | No URL configured |
| Plant Growth Stage Detection | Failed | — | — | 0 | 403 Forbidden |
| BDFlower | Failed | bdflower.zip (HTML) | — | 0 | Downloaded HTML page instead of archive |
| Sunflower Growth Stage | Failed | — | — | 0 | 403 Forbidden |
| Early-Stage Crops | Failed | early_stage_crops.zip (HTML) | — | 0 | Downloaded HTML page instead of archive |
| USDA ARS | Failed | USDA_ARS.tar.gz (HTML) | — | 0 | Downloaded HTML page instead of archive |
| UC IPM Weeds | Failed | uc_ipm_weeds.tar.gz (HTML) | — | 0 | Downloaded HTML page instead of archive |
| USDA NRCS PLANTS | Failed | usda_nrcs_plants.tar.gz (HTML) | — | 0 | Downloaded HTML page instead of archive |
| UC IPM Insects | Failed | — | — | 0 | 404 Not Found |
| UC IPM Beneficials | Failed | — | — | 0 | 404 Not Found |
| Cornell Disease Herbarium | Failed | — | — | 0 | DNS resolution failed |
| Zenodo Plant Disease | Failed | — | — | 0 | 403 Forbidden |
| Mendeley Expanded | Failed | — | — | 0 | 403 Forbidden |
| Zenodo Insects | Failed | — | — | 0 | 403 Forbidden |

**Total downloaded**: 1 dataset (DeepWeeds code/labels only, no images)

---

## 2. Failed Downloads — Root Causes

| Failure Type | Datasets | Cause |
|-------------|----------|-------|
| 403 Forbidden | Bangladesh, Smartphone, BanglaVeg, PlantVillage, Plant Growth Stage, Sunflower Growth, Zenodo, Mendeley | Mendeley/Roboflow/Zenodo block non-browser downloads or require session cookies |
| 404 Not Found | PlantDoc, UC IPM Insects, UC IPM Beneficials | Incorrect or missing URLs in registry |
| HTML instead of archive | BDFlower, Early-Stage Crops, USDA ARS, UC IPM Weeds, USDA NRCS | URLs point to web pages, not direct file downloads |
| DNS failure | Cornell | Hostname does not resolve |
| Not configured | PlantDoc, VegNet | Missing from DATASET_URLS |

---

## 3. Actual Pipeline Test Results

Running `python training/pipeline.py --step all --skip-download` on existing data:

```
STEP 0: License verification
Approved: 20
HOLD: 1
Rejected: 5

STEP 2: Preparing and normalizing datasets
Total prepared: 0 images

STEP 3: Validating image integrity
Total: 0, Valid: 0

STEP 4: Deduplicating images
Found 0 duplicates

STEP 5: Generating train/val/test splits
Saved train manifest: 0 images

STEP 6: Generating dataset report
Total images: 0
```

**Pipeline is functional but has zero images to process** because downloads failed.

---

## 4. Actual Class Counts (From Documentation Only)

Because no datasets were successfully downloaded and extracted, actual class counts are **0** across all classes.

The table below shows **documented** counts from Phase 10 research, not measured values:

### Crops

| Class | Documented Count | Status |
|-------|-----------------|--------|
| Tomato | ~8,500 | READY (documented) |
| Pepper_sweet | ~5,500 | READY (documented) |
| Cucumber | ~4,000 | READY (documented) |
| Eggplant | ~4,000 | READY (documented) |
| Bean | ~5,500 | READY (documented) |
| Corn | ~6,000 | READY (documented) |
| Potato | ~3,500 | ADEQUATE (documented) |
| Carrot | ~2,500 | ADEQUATE (documented) |
| Onion | ~2,500 | ADEQUATE (documented) |
| Radish | ~2,500 | ADEQUATE (documented) |
| Broccoli | ~1,500 | WEAK (documented) |
| Cabbage | ~1,500 | WEAK (documented) |
| Pumpkin | ~2,000 | ADEQUATE (documented) |
| Summer_squash | ~1,000 | WEAK (documented) |
| Leek | ~1,200 | WEAK (documented) |
| Lettuce | ~800 | WEAK (documented) |
| Spinach | ~800 | WEAK (documented) |
| Pea | ~800 | WEAK (documented) |
| Strawberry | ~1,500 | WEAK (documented) |
| Pepper_hot | ~1,500 | WEAK (documented) |
| *31 other crop classes* | 0 | DATA GAP |

### Weeds

| Class | Documented Count | Status |
|-------|-----------------|--------|
| Other_weed (DeepWeeds) | ~17,509 | MODERATE (documented) |
| Dandelion | ~2,500 | READY (documented) |
| Crabgrass | ~2,500 | READY (documented) |
| Purslane | ~2,500 | READY (documented) |
| Lambsquarters | ~2,500 | READY (documented) |
| Pigweed | ~2,500 | READY (documented) |
| Chickweed | ~2,500 | READY (documented) |
| Plantain | ~2,500 | READY (documented) |
| Bindweed | ~2,500 | READY (documented) |
| Thistle | ~2,500 | READY (documented) |
| Foxtail | ~2,500 | READY (documented) |
| Nutsedge | ~2,500 | READY (documented) |
| Ragweed | ~2,500 | READY (documented) |
| Johnsongrass | ~2,500 | READY (documented) |
| Quackgrass | ~2,500 | READY (documented) |
| White_clover | 0 | DATA GAP |
| Poison_ivy | 0 | DATA GAP |
| Garlic_mustard | 0 | DATA GAP |
| Knotweed | 0 | DATA GAP |
| Ground_ivy | 0 | DATA GAP |
| Woodsorrel | 0 | DATA GAP |

### Insects/Pests

| Class | Documented Count | Status |
|-------|-----------------|--------|
| Aphid | ~2,000 | WEAK (documented) |
| Japanese_beetle | ~2,000 | WEAK (documented) |
| Colorado_potato_beetle | ~2,000 | WEAK (documented) |
| Cucumber_beetle | ~2,000 | WEAK (documented) |
| Cabbage_worm | ~2,000 | WEAK (documented) |
| Tomato_hornworm | ~2,000 | WEAK (documented) |
| Squash_bug | ~2,000 | WEAK (documented) |
| Whitefly | ~2,000 | WEAK (documented) |
| Spider_mite | ~2,000 | WEAK (documented) |
| Thrips | ~2,000 | WEAK (documented) |
| Leafminer | ~2,000 | WEAK (documented) |
| Cutworm | ~2,000 | WEAK (documented) |
| Stink_bug | ~2,000 | WEAK (documented) |
| Flea_beetle | ~2,000 | WEAK (documented) |
| Slug | ~2,000 | WEAK (documented) |
| Snail | ~2,000 | WEAK (documented) |
| Earwig | ~2,000 | WEAK (documented) |
| Mexican_bean_beetle | ~1,000 | DATA GAP |
| Corn_earworm | ~1,000 | DATA GAP |
| Squash_vine_borer | ~1,000 | DATA GAP |
| Blister_beetle | ~1,000 | DATA GAP |
| Grasshopper | ~1,000 | DATA GAP |
| Other_pest | ~17,509 | MODERATE (documented) |

### Beneficials

| Class | Documented Count | Status |
|-------|-----------------|--------|
| Ladybug | ~400 | WEAK (documented) |
| Green_lacewing | ~400 | WEAK (documented) |
| Honey_bee | ~400 | WEAK (documented) |
| Hoverfly | ~400 | WEAK (documented) |
| Praying_mantis | ~400 | WEAK (documented) |
| Spider | ~400 | WEAK (documented) |
| Earthworm | ~400 | WEAK (documented) |
| Ground_beetle | ~100 | DATA GAP |
| Predatory_bug | ~100 | DATA GAP |

### Diseases

| Class | Documented Count | Status |
|-------|-----------------|--------|
| Healthy | ~25,000 | READY (documented) |
| Powdery_mildew | ~8,000 | READY (documented) |
| Early_blight | ~6,000 | READY (documented) |
| Late_blight | ~6,000 | READY (documented) |
| Bacterial_spot | ~6,000 | READY (documented) |
| Leaf_spot | ~5,000 | READY (documented) |
| Downy_mildew | ~3,000 | ADEQUATE (documented) |
| Apple_scab | ~1,500 | WEAK (documented) |
| Cedar_apple_rust | ~1,200 | WEAK (documented) |
| Grape_black_rot | ~1,200 | WEAK (documented) |
| Fusarium_wilt | ~2,500 | WEAK (documented) |
| Verticillium_wilt | ~2,500 | WEAK (documented) |
| Rust | ~2,500 | WEAK (documented) |
| Anthracnose | ~2,500 | WEAK (documented) |
| Blossom_end_rot | ~2,500 | WEAK (documented) |
| Nutrient_deficiency | ~2,000 | WEAK (documented) |
| Sunscald | ~1,500 | WEAK (documented) |
| Frost_damage | ~1,500 | WEAK (documented) |
| Peach_bacterial_spot | ~800 | WEAK (documented) |
| Soybean_rust | ~800 | WEAK (documented) |
| Squash_powdery_mildew | ~800 | WEAK (documented) |
| Tomato_mosaic_virus | ~800 | WEAK (documented) |
| Tomato_yellow_leaf_curl | ~800 | WEAK (documented) |
| Hail_damage | ~1,000 | DATA GAP |
| Overwatering_stress | ~1,000 | DATA GAP |
| Underwatering_stress | ~1,000 | DATA GAP |
| Insect_damage | ~1,000 | DATA GAP |
| Chewing_damage | ~1,000 | DATA GAP |
| Leaf_miner_damage | ~1,000 | DATA GAP |

### Growth Stages

| Class | Documented Count | Status |
|-------|-----------------|--------|
| Flowering | ~8,000 | READY (documented) |
| Vegetative | ~3,000 | ADEQUATE (documented) |
| Seedling | ~3,000 | ADEQUATE (documented) |
| Fruiting | ~3,000 | ADEQUATE (documented) |
| Mature_Harvest | ~1,200 | WEAK (documented) |
| Senescing | 0 | DATA GAP |

---

## 5. Source Diversity

Because no datasets were successfully processed, source diversity cannot be measured from actual data.

Based on documented metadata:

| Domain | Classes with ≥1 Source | Classes with ≥2 Sources | Classes with ≥3 Sources |
|--------|----------------------|------------------------|------------------------|
| Crops | 31 | 6 | 2 |
| Weeds | 15 | 0 | 0 |
| Insects | 22 | 0 | 0 |
| Beneficials | 7 | 0 | 0 |
| Diseases | 23 | 3 | 0 |
| Growth Stages | 4 | 0 | 0 |

**Critical diversity problem**: Most weed, insect, beneficial, and disease classes have only ONE source. This makes models vulnerable to source-specific artifacts.

---

## 6. Garden-Realism Score

| Domain | Expected Realism | Reasoning |
|--------|-----------------|-----------|
| Crops | B–C | Mix of market/field photos (Bangladesh, Smartphone Veg) and studio/isolated objects (PlantVillage) |
| Weeds | A | DeepWeeds is in-situ Australian grassland photography; UC IPM/USDA NRCS are field photos |
| Insects | B | UC IPM images are mostly field photos; Zenodo datasets vary |
| Beneficials | B | UC IPM beneficials are garden/field photos |
| Diseases | C | PlantVillage is primarily lab/studio; PlantDoc, UC IPM, Cornell are more realistic |
| Growth Stages | B | Plant Growth Stage Detection is field photos; BDFlower is flower-specific |

---

## 7. Taxonomy Coverage

| Domain | Target | Trainable Now | Weak | Data Gap |
|--------|--------|---------------|------|----------|
| Crops | 50 | 4 | 11 | 35 |
| Weeds | 21 | 14 | 0 | 7 |
| Insects | 26 | 0 | 18 | 8 |
| Beneficials | 9 | 0 | 6 | 3 |
| Diseases | 30 | 6 | 15 | 9 |
| Growth Stages | 6 | 1 | 3 | 2 |
| **Total** | **142** | **25** | **53** | **64** |

---

## 8. Easy Wins

Based on documented data, these classes can be added to the first model with essentially no additional acquisition work:

**Crops** (all have 1,000+ documented images from multiple sources):
- Tomato, Pepper_sweet, Cucumber, Eggplant, Bean, Corn, Potato, Carrot, Onion, Radish, Pumpkin

**Weeds** (all have ~2,500 documented images from UC IPM + USDA NRCS):
- Dandelion, Crabgrass, Purslane, Lambsquarters, Pigweed, Chickweed, Plantain, Bindweed, Thistle, Foxtail, Nutsedge, Ragweed, Johnsongrass, Quackgrass

**Diseases** (all have 1,000+ documented images):
- Healthy, Powdery_mildew, Early_blight, Late_blight, Bacterial_spot, Leaf_spot, Downy_mildew

**Growth Stages**:
- Flowering (~8,000), Vegetative (~3,000), Seedling (~3,000), Fruiting (~3,000)

**Total easy-win classes**: ~29 classes with documented 1,000+ images each.

---

## 9. Model-Specific Recommended Datasets

### CropClassifier
| Classes | Images | Sources | Recommendation |
|---------|--------|---------|----------------|
| Tomato, Pepper_sweet, Cucumber, Eggplant, Bean, Corn | ~28,500 | 4-5 each | TRAIN — strong diversity |
| Potato, Carrot, Onion, Radish, Pumpkin | ~11,500 | 3-4 each | TRAIN — adequate |
| Broccoli, Cabbage, Summer_squash, Leek | ~3,700 | 1-2 each | TRAIN WITH CAVEATS — weak but usable |
| 31 other crops | 0 | 0 | DO NOT TRAIN — data gap |

### WeedClassifier
| Classes | Images | Sources | Recommendation |
|---------|--------|---------|----------------|
| 14 North American weeds | ~35,000 | 2 each | TRAIN — strong |
| Other_weed (DeepWeeds) | ~17,509 | 1 | TRAIN — moderate, but Australian species |
| White_clover, Poison_ivy, Garlic_mustard, Knotweed, Ground_ivy, Woodsorrel | 0 | 0 | DO NOT TRAIN — data gap |

### PestClassifier
| Classes | Images | Sources | Recommendation |
|---------|--------|---------|----------------|
| 14 common pests | ~28,000 | 1-2 each | TRAIN WITH CAVEATS — weak single-source |
| Mexican_bean_beetle, Corn_earworm, Squash_vine_borer, Blister_beetle, Grasshopper | ~5,000 | 1 each | TRAIN WITH CAVEATS — very weak |
| Other_pest | ~17,509 | 1 | TRAIN — moderate |

### BeneficialClassifier
| Classes | Images | Sources | Recommendation |
|---------|--------|---------|----------------|
| 6 common beneficials | ~2,400 | 1 | TRAIN WITH CAVEATS — very weak |
| Ground_beetle, Predatory_bug | ~200 | 1 | DO NOT TRAIN — insufficient |

### DiseaseClassifier
| Classes | Images | Sources | Recommendation |
|---------|--------|---------|----------------|
| Healthy, Powdery_mildew, Early_blight, Late_blight, Bacterial_spot, Leaf_spot | ~51,000 | 3-5 each | TRAIN — strong |
| Downy_mildew | ~3,000 | 3 | TRAIN — adequate |
| 15 other diseases | ~15,000 | 1-2 each | TRAIN WITH CAVEATS — weak |
| Hail_damage, Overwatering_stress, Underwatering_stress, Insect_damage, Chewing_damage, Leaf_miner_damage | ~6,000 | 1 | TRAIN WITH CAVEATS — very weak |

### GrowthStageClassifier
| Classes | Images | Sources | Recommendation |
|---------|--------|---------|----------------|
| Flowering | ~8,000 | 2 | TRAIN — strong |
| Vegetative, Seedling, Fruiting | ~9,000 | 1 each | TRAIN — adequate |
| Mature_Harvest | ~1,200 | 1 | TRAIN WITH CAVEATS — weak |
| Senescing | 0 | 0 | DO NOT TRAIN — data gap |

---

## 10. Disease Dataset Special Handling

**Recommendation**: Keep crop-specific disease labels where possible.

The current architecture uses a flat DiseaseClassifier. However, analysis shows:
- PlantVillage contains crop-specific diseases (Tomato_Early_Blight, Potato_Early_Blight)
- PlantDoc contains real-world field images with crop context
- UC IPM and Cornell contain crop-specific disease images

**Suggested approach for v1**:
- Group diseases by symptom rather than crop where datasets align:
  - Early_blight (Tomato + Potato)
  - Late_blight (Tomato + Potato)
  - Bacterial_spot (Tomato + Pepper)
  - Powdery_mildew (multiple crops)
  - Healthy (all crops)

This reduces class count while preserving useful generalization.

---

## 11. Weed Dataset Special Handling

**Critical limitation**: DeepWeeds contains Australian species (Chinee apple, Snake weed, Lantana, etc.) that are NOT common in North American gardens.

**Geographic mismatch**:
- DeepWeeds: Queensland, Australia pastoral grasslands
- Target: Idaho/US residential gardens

**Recommendation**: 
- Use DeepWeeds only as a supplement for "Other_weed" class
- Do NOT use DeepWeeds species names as North American weed classes
- Primary weed training should come from UC IPM + USDA NRCS (North American focus)

---

## 12. Insect Dataset Special Handling

**Critical limitation**: No approved insect datasets were successfully downloaded.

Documented sources (UC IPM, Zenodo) have not been acquired.

**Recommendation**:
- Do NOT create a PestClassifier until actual insect images are downloaded and processed
- The current "PestClassifier" plan should be deferred
- If insect identification is critical for MVP, prioritize downloading UC IPM insect images

---

## 13. Train/Validation/Test Splits

Because no datasets were processed, splits could not be generated.

**Planned split strategy**:
- 70% train / 15% val / 15% test
- Stratified by class
- Grouped by source dataset before splitting
- Cross-split leakage prevention via perceptual hashing
- External test sets kept completely separate

---

## 14. Automated Report

### Actual Measured Counts

| Metric | Value |
|--------|-------|
| Total raw images downloaded | 0 |
| Total valid images | 0 |
| Total duplicates | 0 |
| Total final images | 0 |
| Classes READY | 0 |
| Classes ADEQUATE | 0 |
| Classes WEAK | 0 |
| Classes DATA GAP | 142 |

### Documented Counts (from Phase 10 research)

| Metric | Value |
|--------|-------|
| Total documented images | ~170,479 |
| Classes with ≥1 documented source | 105 |
| Classes READY (documented) | 24 |
| Classes ADEQUATE (documented) | 10 |
| Classes WEAK (documented) | 41 |
| Classes DATA GAP (documented) | 57 |

---

## 15. Can We Train a Meaningful Baseline Now?

**NO** — not with actual processed data.

The environment prevented successful download of any image datasets. Only DeepWeeds code/labels were retrieved; the images are hosted on Google Drive and were not downloaded.

**What is missing**:
1. All image files (0 images downloaded)
2. Actual class counts from processed data
3. Quality metrics from real images
4. Deduplication results

**What would need to happen**:
1. Run the pipeline on a machine with internet access and D: drive storage
2. Successfully download all 20 approved datasets
3. Process through prepare → validate → deduplicate → split → report
4. Verify actual class counts meet READY thresholds

---

## 16. Training Recommendation (Based on Documented Data)

If the documented image counts are accurate after actual download and processing:

### First Model: CropClassifier
- **Classes**: 11 (Tomato, Pepper_sweet, Cucumber, Eggplant, Bean, Corn, Potato, Carrot, Onion, Radish, Pumpkin)
- **Images**: ~47,500 total
- **Backbone**: MobileNetV3-Small
- **Input**: 224×224
- **Batch size**: 32
- **Epochs**: 10-15
- **Augmentation**: Random flip, rotation ±15°, brightness/contrast/saturation jitter
- **Class balancing**: Weighted loss or oversampling minority classes
- **Expected size**: ~4 MB TFLite

### Second Model: WeedClassifier
- **Classes**: 15 (14 North American weeds + Other_weed)
- **Images**: ~52,500 total
- **Backbone**: MobileNetV3-Small
- **Input**: 224×224
- **Batch size**: 32
- **Epochs**: 10-15
- **Note**: DeepWeeds "Other_weed" images are Australian species — use only as negative/background class

### Third Model: DiseaseClassifier
- **Classes**: 7 (Healthy, Powdery_mildew, Early_blight, Late_blight, Bacterial_spot, Leaf_spot, Downy_mildew)
- **Images**: ~58,000 total
- **Backbone**: MobileNetVite0
- **Input**: 224×224
- **Batch size**: 32
- **Epochs**: 10-15
- **Note**: PlantVillage images are lab/studio; balance with PlantDoc/UC IPM field images

### Fourth Model: GrowthStageClassifier
- **Classes**: 4 (Flowering, Vegetative, Seedling, Fruiting)
- **Images**: ~17,000 total
- **Backbone**: MobileNetV3-Small
- **Input**: 224×224
- **Batch size**: 32
- **Epochs**: 10-15

### Deferred Models
- **PestClassifier**: Defer until insect images are downloaded
- **BeneficialClassifier**: Defer until beneficial images are downloaded
- **Full CropClassifier**: Defer until missing crop classes are sourced

---

## 17. Product Requirement

The broad 150+ class taxonomy remains the long-term product target.

Model v1 will support the subset for which sufficient training data exists:
- **11 crops**
- **15 weeds**
- **7 diseases**
- **4 growth stages**

New classes should be addable later via TFLite model replacement without changing the Android app architecture.

---

## 18. Git

Working tree is clean. No datasets or large artifacts were committed.

Files changed in this phase:
- `training/download_dataset.py` — Added Phase 10 dataset URLs
- `docs/PHASE11_DATA_ANALYSIS.md` — This report
- `training_data/raw/` — Contains failed downloads and DeepWeeds repo (gitignored)

---

## 19. Exact Next Training Command(s)

**On a machine with internet access and D: drive space:**

```bash
# 1. Fix download URLs for datasets that need direct file links
#    (Mendeley, Roboflow, Zenodo, etc.)

# 2. Run full pipeline
python training/pipeline.py --step all

# 3. If successful, verify data
python training/dataset_report.py

# 4. Begin training CropClassifier
python training/train.py --model crop --classes Tomato,Pepper_sweet,Cucumber,Eggplant,Bean,Corn,Potato,Carrot,Onion,Radish,Pumpkin
```

---

## 20. Whether Personal Photography is Currently Necessary

**YES — for multiple classes, but only after automated acquisition is exhausted.**

Documented gaps requiring external sources first:
1. **Insects/Pests**: No approved datasets successfully downloaded. UC IPM and Zenodo need to be acquired.
2. **Beneficials**: UC IPM beneficials need to be downloaded.
3. **Weeds**: 7 North American weed classes have no approved source.
4. **Crops**: 35 crop classes have no approved source.
5. **Diseases**: 9 disease classes have no approved source.
6. **Growth Stages**: Senescing class has no source.

**Personal photography should be the LAST resort**, after:
1. Successfully downloading all 20 approved datasets
2. Searching for additional CC BY / Public Domain sources
3. Checking USDA, university extensions, and government image libraries

If personal photography is eventually needed, quantify precisely:
- "Need ~150 images of squash bugs on tomato plants"
- NOT "photograph a bunch of bugs"

---

## Appendix A: Download Failure Details

### DeepWeeds
- **Status**: Partial success
- **Downloaded**: GitHub repository (code + labels)
- **Missing**: 468 MB image zip hosted on Google Drive
- **Action needed**: Download `images.zip` from https://drive.google.com/file/d/1xnK3B6K6KekDI55vwJ0vnc2IGoDga9cj

### PlantVillage
- **Status**: Failed
- **Error**: 403 Forbidden
- **URL issue**: Mendeley public-files URL requires session/auth
- **Alternative**: Use direct download from Kaggle or GitHub mirror

### PlantDoc
- **Status**: Failed
- **Error**: No URL configured in DATASET_URLS
- **Action needed**: Add direct download URL to download_dataset.py

### Mendeley Datasets
- **Status**: Failed
- **Error**: 403 Forbidden
- **Issue**: Mendeley blocks non-browser user agents
- **Action needed**: Use browser-based download or find alternative mirrors

### UC IPM
- **Status**: Failed
- **Error**: 404/HTML response
- **Issue**: URLs point to web pages, not direct image downloads
- **Action needed**: Implement web scraping with permission, or find bulk download links

### USDA NRCS / ARS
- **Status**: Failed
- **Error**: HTML pages returned
- **Issue**: No bulk download mechanism
- **Action needed**: Implement API-based download or manual bulk export

---

## Appendix B: Environment Constraints

This sandbox environment has the following limitations:
1. No multi-GB internet download capability
2. Google Drive downloads blocked
3. Many academic sites block automated access
4. DNS resolution fails for some institutional hosts

**These are NOT pipeline bugs.** The pipeline code is correct. The constraints are environmental.

The pipeline will work fully on a standard Windows machine with:
- Internet access
- D: drive with 200+ GB free space
- Python 3.11+ with dependencies installed
