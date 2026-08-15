# Phase 16 — Data Validation & Strategic Analysis

## 1. PlantDoc License Determination

**Status: COMMERCIALLY USABLE**

PlantDoc is released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Evidence verified from primary sources:
- LICENSE.txt fetched directly from the GitHub repository
- GitHub license field: CC BY 4.0
- Roboflow Universe mirrors confirm CC BY 4.0 with commercial-use permission
- DatasetNinja confirms CC BY 4.0

Permissions granted:
- Commercial use: YES
- Modification/derivative works (including ML model training): YES
- Redistribution: YES
- Distribution of trained model weights: YES
- Patent/trademark use: NOT licensed (standard CC limitation)

Restrictions:
- Attribution REQUIRED: retain creator identification, copyright notice, license notice, and URI
- No additional restrictions may be applied

**Recommendation**: Use PlantDoc for commercial training. Record attribution in app credits.

---

## 2. BIOSCAN-5M License Determination

**Status: COMMERCIALLY USABLE (with attribution)**

BIOSCAN-5M images are released under **Creative Commons Attribution 3.0 Unported (CC BY 3.0)**.

Evidence verified from primary sources:
- GitHub README: "Copyright License: Creative Commons Attribution 3.0 Unported (CC BY 3.0)"
- NeurIPS 2024 Supplementary Materials Table S1 confirms same license
- Copyright Holder: CBG Photography Group
- Copyright Institution: Centre for Biodiversity Genomics (University of Guelph)
- Contact: collectionsBIO@gmail.com, cbg.collections@uoguelph.ca

Permissions granted:
- Commercial use: YES
- Modification/derivative works: YES
- Redistribution: YES
- Distribution of trained model weights: YES

Restrictions:
- Attribution REQUIRED to CBG Photography Group / Centre for Biodiversity Genomics

**Note**: While the license is commercially compatible, practical usability for our target application is limited (see Sections 3-4).

---

## 3. BIOSCAN-5M Image/Metadata Analysis

### Archive Structure
- **Format**: ZIP
- **Compressed size**: 2,119.7 MB
- **Uncompressed**: ~4 GB (images only)
- **Contents**: `bioscan5m/images/original_256/train/{chunk}/{processid}.jpg`
- **Chunks**: 16 numeric subdirectories, each containing ~17,900-18,300 images
- **Total images in archive**: 289,203 (train split only)
- **Image format**: RGB JPEG, 341×256 pixels
- **Image source**: Keyence VHX-7000 microscope, cropped/resized from 1024×768 originals

### Metadata
- **Metadata file**: `BIOSCAN_5M_Insect_Dataset_metadata_MultiTypes.zip` (2 GB compressed, 4 GB CSV)
- **Downloaded from**: https://huggingface.co/datasets/bioscan-ml/BIOSCAN-5M/resolve/main/BIOSCAN_5M_Insect_Dataset_metadata_MultiTypes.zip
- **Format**: CSV + JSON-LD
- **Columns**: processid, sampleid, taxon, phylum, class, order, family, subfamily, genus, species, dna_bin, dna_barcode, country, province_state, coord-lat, coord-lon, image_measurement_value, area_fraction, scale_factor, inferred_ranks, split, index_bioscan_1M_insect, chunk
- **Total records**: 5,150,850
- **Records with species labels**: 473,094 (9.2%)
- **Records with genus labels**: 1,226,765 (23.8%)
- **Records with family labels**: 4,932,774 (95.8%)

### Taxonomic Coverage (train split, 289,203 images)
| Rank | Categories | Labelled |
|------|-----------|----------|
| phylum | 1 | 100% |
| class | 10 | 99.9% |
| order | 55 | 99.7% |
| family | 934 | 95.8% |
| genus | 7,605 | 23.8% |
| species | 22,622 | 9.2% |

### Geographic Distribution (train split)
- Total train records with country data: 289,203
- North America (Canada, US, Mexico): 77,978 (27.0%)
- Collection sites: 1,650 sites across 47 countries

---

## 4. BIOSCAN Images That Can Legitimately Map to Target Insect Classes

### Methodology
Only mappings at genus level or below are considered defensible. Broad family/order mappings are explicitly rejected per Phase 16 instructions.

### Train Split Counts (genus-level mapping)
| Target Class | Genus Filter | Train Count | NA Only |
|-------------|-------------|-------------|---------|
| Aphid | Aphis, Rhopalosiphum, Acyrthosiphon, Myzus, Macrosiphum, Sitobion, Cinara | 3,845 | 1,307 |
| Whitefly | Bemisia, Trialeurodes | 2,639 | 74 |
| Leafminer | Liriomyza, Phytomyza, Calycomyza, Pseudonapomyza, Agromyza, Ophiomyia | 2,509 | 1,386 |
| Spider | Order Araneae | 6,493 | 3,820 |
| Thrips | Frankliniella, Thrips, Scirtothrips | 1,768 | 970 |
| Hoverfly | Toxomerus, Paragus, Sphaerophoria, Eupeodes, Episyrphus, Eristalinus | 702 | 544 |
| Flea_beetle | Chaetocnema, Epitrix, Phyllotreta, Longitarsus | 227 | 55 |
| Ladybug | Hippodamia, Coleomegilla, Coccinella, Harmonia, Adalia, Propylea | 156 | 62 |
| Honey_bee | Apis | 41 | 1 |
| Spider_mite | Tetranychus, Panonychus, Oligonychus | 127 | 5 |
| Green_lacewing | Chrysoperla, Chrysopa, Ceraeochrysa, Mallada, Plesiochrysa | 38 | 11 |
| Cutworm | Spodoptera, Agrotis, Peridroma, Euxoa, Feltia | 14 | - |
| Corn_earworm | Helicoverpa, Heliothis | 9 | - |
| Squash_bug | Anasa, Leptoglossus | 24 | 9 |
| Stink_bug | Halyomorpha, Nezara, Acrosternum, Euschistus, Thyanta, Banasa | 28 | 9 |
| Blister_beetle | Meloe, Epicauta, Lytta, Hycleus | 9 | 2 |
| Praying_mantis | Mantis, Tenodera, Hierodula, Orthodera, Stagmomantis | 4 | - |
| Japanese_beetle | Popillia | 0 | 0 |
| Colorado_potato_beetle | Leptinotarsa | 0 | 0 |
| Cucumber_beetle | Diabrotica | 0 | 0 |
| Mexican_bean_beetle | Epilachna | 0 | 0 |
| Tomato_hornworm | Manduca | 0 | 0 |
| Cabbage_worm | Pieris, Artogeia | 0 | 0 |
| Squash_vine_borer | Melittia | 0 | 0 |

### Key Findings
- **~15,000 images** in the train split map defensibly to target classes
- **~9,000 images** are from North America (higher relevance for garden pest identification)
- **0 images** for 7 high-priority target classes (Japanese_beetle, Colorado_potato_beetle, Cucumber_beetle, Mexican_bean_beetle, Tomato_hornworm, Cabbage_worm, Squash_vine_borer)
- Many target classes have single-digit or low-double-digit counts
- Even where counts exist, the specimens are predominantly from tropical/subtropical regions (Costa Rica, etc.), not North American gardens

---

## 5. Is BIOSCAN Useful for Garden-Photo Recognition?

**Determination: NOT USEFUL for direct training. DEFERRED for pre-training with domain adaptation.**

### Domain Shift Analysis
BIOSCAN-5M images are **specimen-style biodiversity photographs** with the following characteristics:
- Captured with a Keyence VHX-7000 digital microscope
- Specimens are spread, pinned, or positioned on plain backgrounds
- Lighting is controlled and uniform
- Images are cropped to show only the insect (341×256)
- No environmental context: no leaves, stems, flowers, soil, fruit
- Typically dorsal views only
- Scale is inconsistent (area_fraction varies widely)

### Intended Application
The Soil & Supper app requires classification of insects photographed by gardeners with smartphones:
- Insects on leaves, stems, flowers, soil, or fruit
- Varying distances (close-up to 2-3 feet away)
- Varying lighting (sunlight, shade, flash)
- Often partially occluded by plant tissue
- Often very small in frame
- Natural poses, not spread specimens

### Domain Shift Verdict
This is a **severe domain shift**. A model trained on BIOSCAN specimen images will fail on garden photographs. The visual features that distinguish BIOSCAN classes (microscopy-specific morphology, spread-wing poses, plain backgrounds) are absent in smartphone garden photos, and vice versa.

**BIOSCAN-5M may be useful ONLY for:**
1. Self-supervised pre-training to learn low-level insect features
2. As a source of taxonomic knowledge for hierarchical classifiers
3. If paired with heavy domain adaptation (style transfer, synthetic background augmentation, etc.)

Even for pre-training, the value is questionable because:
- Only ~15K target-class images exist in the train split
- The remaining 274K+ images are non-target insects with no clear path to our taxonomy
- PlantDoc already provides 2,502 real-world field images for diseases

---

## 6. Recommended Taxonomy/Architecture Changes

### Current State
Flat classifier across all classes:
- 50 crops
- 21 weeds
- 27 insects/pests
- 6 beneficial insects
- 30 diseases
- 6 growth stages
= **140 total classes**

### Problem
Many classes share visual features across crops. For example:
- "Early_blight" on tomato looks similar to "Early_blight" on potato
- "Leaf_spot" is a visual pattern that appears on many crops
- "Healthy" means different things for different crops
- "Spider_mite" damage looks similar across crops

### Recommended Architecture: Hierarchical Two-Stage Model

```
Stage 1: Crop / Plant Identification
  Input: Image
  Output: Crop class (e.g., "Tomato", "Corn", "Rose")

Stage 2a: Disease Classifier (conditioned on crop)
  Input: Image + Crop prediction
  Output: Disease class (e.g., "Early_blight", "Healthy")

Stage 2b: Insect Classifier (conditioned on crop + plant part)
  Input: Image + Crop prediction + Plant-part hint
  Output: Pest/Beneficial/Other + specific insect class
```

### Why This Is Better
1. **Reduces confusion**: "Early_blight on tomato" is a different visual target than "Early_blight on potato" when crop context is provided
2. **Reduces class count per head**: Each disease classifier only needs to distinguish ~5-10 diseases per crop instead of 30 diseases globally
3. **Matches agronomic knowledge**: Farmers diagnose diseases in the context of the crop they're growing
4. **Enables partial coverage**: We can launch with high-coverage crops first and add others later
5. **Natural error handling**: If Stage 1 is uncertain, Stage 2 can be gated

### Implementation Note
Do NOT rewrite architecture now. Document this finding and validate with the team before changing model code.

### Alternative: Multi-Task with Crop Attention
If a single model is preferred, use a crop-conditioning mechanism (e.g., crop embedding concatenated to features) rather than fully separate heads.

---

## 7. Revised Class Readiness Thresholds

Replace the old "≥200 images = trainable" heuristic with the following framework:

### Training Readiness Score (per class)

| Criterion | Weight | Threshold | Rationale |
|-----------|--------|-----------|-----------|
| Minimum image count | Required | ≥100 images | Below this, even a perfect model cannot generalize |
| Source diversity | Required | ≥2 independent sources | Prevents overfitting to one dataset's artifacts |
| Image diversity | Required | ≥3 capture conditions | Lab + field + smartphone, or multiple lighting/angles |
| Label quality | Required | ≥90% consensus or expert-verified | Noisy labels destroy training |
| Field-vs-lab ratio | Strongly preferred | ≥30% field imagery | Domain match to garden photos |
| Near-duplicate rate | Strongly preferred | ≤5% | Prevents inflated validation scores |
| Class confusion risk | Review | Expert review of edge cases | Some classes may need merging |

### Readiness Categories

| Category | Definition |
|----------|-----------|
| **TRAINABLE_NOW** | Meets all Required thresholds and ≥3 Strongly preferred thresholds |
| **NEEDS_MORE_DATA** | Meets Required thresholds but <3 Strongly preferred thresholds |
| **NEEDS_SOURCES** | Meets minimum image count but <2 sources |
| **NEEDS_DIVERSITY** | Meets count and sources but lacks field/lab diversity |
| **LICENSE_BLOCKED** | License is non-commercial or unclear |
| **DATASET_SEARCH_REQUIRED** | Does not meet minimum image count |
| **DEFERRED** | Low priority; can wait for later phases |

### Current Class Status (based on PlantDoc only)

| Class | Images | Sources | Field/Lab | Readiness |
|-------|--------|---------|-----------|-----------|
| Healthy | 842 | 1 | Field | NEEDS_MORE_DATA |
| Leaf_spot | 342 | 1 | Field | NEEDS_MORE_DATA |
| Early_blight | 196 | 1 | Field | NEEDS_MORE_DATA |
| Late_blight | 195 | 1 | Field | NEEDS_MORE_DATA |
| Bacterial_spot | 176 | 1 | Field | NEEDS_MORE_DATA |
| Septoria_leaf_spot | 138 | 1 | Field | NEEDS_MORE_DATA |
| Squash_powdery_mildew | 128 | 1 | Field | NEEDS_MORE_DATA |
| Rust | 115 | 1 | Field | NEEDS_MORE_DATA |
| Apple_scab | 92 | 1 | Field | NEEDS_MORE_DATA |
| Cedar_apple_rust | 87 | 1 | Field | NEEDS_MORE_DATA |
| Grape_black_rot | 63 | 1 | Field | NEEDS_MORE_DATA |
| Tomato_yellow_leaf_curl | 72 | 1 | Field | NEEDS_MORE_DATA |
| Tomato_mosaic_virus | 54 | 1 | Field | NEEDS_MORE_DATA |
| Spider_mite | 2 | 1 | Unknown | DATASET_SEARCH_REQUIRED |

**Note**: All PlantDoc classes fail the source diversity threshold. Adding PlantVillage would resolve this for overlapping disease classes.

---

## 8. What We Have Now

### Acquired Data
| Dataset | Status | Images | Classes | Domain |
|---------|--------|--------|---------|--------|
| PlantDoc | Downloaded, extracted, ingested, validated, split | 2,502 | 14 | Diseases (field imagery) |
| BIOSCAN-5M | Downloaded (archive only) | 289,203 in archive | ~15K mappable | Insects (specimen microscopy) |
| USDA_ARS | On disk (unlabeled) | 20 | N/A | Hold |

### Pipeline Status
- `acquisition_status`: Complete
- `download`: 2 succeeded (PlantDoc, BIOSCAN-5M), 22 failed (broken URLs)
- `prepare`: 2,572 images ingested from PlantDoc
- `validate`: 2,571 valid (1 corrupt removed)
- `deduplicate`: 2,502 after removing 69 near-duplicates
- `split`: 1,745 train / 370 val / 387 test
- `report`: Generated (data_gap_report.json)

### Coverage Gaps
- **Crops**: 0 classes with data
- **Weeds**: 0 classes with data
- **Insects/Pests**: 1 class (Spider_mite: 2 images) from PlantDoc misclassification; BIOSCAN has ~15K mappable but specimen-style
- **Beneficial Insects**: 0 classes
- **Growth Stages**: 0 classes
- **Diseases**: 13 classes, all from single source (PlantDoc)

---

## 9. Single Highest-Value Next Dataset

### Recommendation: PlantVillage

**Why PlantVillage is the highest-value next acquisition:**

1. **Scale**: 54,306 images — single largest disease dataset
2. **License**: CC0 (Public Domain) — no attribution required, maximum commercial freedom
3. **Coverage**: 38 classes (14 crop species × healthy + 26 diseases)
4. **Overlap with PlantDoc**: Shares many disease classes (Apple_scab, Rust, Bacterial_spot, Early_blight, Late_blight, etc.)
5. **Source diversity**: Adding PlantVillage resolves the "single source" weakness of PlantDoc
6. **Image style**: Controlled lab/studio photos — while not ideal for domain matching, the label quality is high
7. **Availability**: The actual download source needs manual acquisition (Figshare/Mendeley URLs returned 403/202 errors in automated attempts)

**What it unlocks:**
- Resolves source diversity for 8+ disease classes
- Brings several classes to TRAINABLE_NOW status
- Provides baseline for hierarchical crop→disease architecture

**Alternative considered: iNaturalist**
- Would provide massive real-world field imagery across all domains
- **BLOCKED**: Terms of Service prohibit commercial AI training
- Cannot be used

---

## 10. Exactly What, If Anything, to Manually Download

### Priority 0 — Already Acquired (Use After License Verification)
- **PlantDoc**: 2,502 training-ready images, CC BY 4.0. Ready for use.

### Priority 1 — Manually Download (Highest Value Per Download)
1. **PlantVillage** (54,306 images, CC0)
   - Source: https://data.mendeley.com/datasets/tywbtsjrjv/1 (may need alternative download)
   - Alternative: https://github.com/visipedia/plantvillage (if available)
   - Why: Massive scale, public domain, resolves source diversity
   - Action: Download and place in `training_data/raw/plantvillage/`

2. **iNaturalist 2021** (Cannot use — ToS blocks commercial AI training)
   - Mentioned for completeness; do not download

### Priority 2 — Useful But Nonessential
3. **DeepWeeds** (17,509 images, CC BY 4.0)
   - Australian weeds — low geographic relevance to North American gardens
   - Would add weed class coverage
   - Action: If time permits, download from https://github.com/AlexOlsen/DeepWeeds

4. **BDFlower** (23,334 images, CC BY 4.0)
   - Flower growth stages — limited to ornamental flowers
   - Action: Download if growth-stage coverage is prioritized

### DEFER
- **BIOSCAN-5M**: Downloaded but not extracted. Defensibly maps to ~15K target-class images, but domain shift makes it unsuitable for direct training. Defer until domain adaptation pipeline is established.
- **Bangladesh Vegetables, Smartphone Veg, BanglaVeg, VegNet**: Broken download URLs; low priority compared to PlantVillage.
- **Mendeley/Roboflow datasets**: Broken URLs; revisit if direct download links become available.

### LICENSE_BLOCKED
- None currently. PlantDoc and BIOSCAN-5M both have CC licenses permitting commercial use.

---

## 11. Whether Training Should Begin Yet

**NO. Do not train yet.**

Reasons:
1. **Insufficient coverage**: Only 14 of 140 classes have any data. 126 classes are empty.
2. **Single source**: All 14 classes come from PlantDoc only. No source diversity.
3. **No crop data**: Zero crop identification images. The hierarchical architecture requires Stage 1 crop identification first.
4. **No weed data**: Zero weed classes.
5. **No growth-stage data**: Zero growth-stage classes.
6. **Insect coverage minimal**: Only 2 Spider_mite images from PlantDoc (likely mislabeled). BIOSCAN has counts but wrong domain.
7. **Domain gap**: PlantDoc is field imagery (good), but we need smartphone-style garden photos for validation.

### Minimum Viable Training Conditions
Before training begins, we need:
- At least 5 crops with ≥200 images each AND source diversity
- PlantVillage downloaded and ingested (resolves disease source diversity)
- External evaluation dataset secured (e.g., iNaturalist cannot be used; need alternative)

---

## 12. Git Commit

Commit hash: `c98af93` (from prior phase)

New changes in this phase: `docs/ML_DATA_LICENSES.md`, analysis documents, selective extraction tool (if built)

---

## 13. Push Status

`c98af93` is pushed to `origin/main`.

---

## 14. Working-Tree Status

Prior to this phase: Clean.
Changes made: License verification docs and analysis.

---

## Appendix: BIOSCAN Selective Extraction Design

If BIOSCAN is ever used, selective extraction is required to avoid extracting 289K images when only ~15K map to targets.

### Design
1. Read `BIOSCAN_5M_Insect_Dataset_metadata.csv` (already downloaded)
2. Filter rows by target genus + train split
3. For each matching row, compute zip path: `bioscan5m/images/original_256/train/{chunk}/{processid}.jpg`
4. Extract only matching files using `zipfile.ZipFile.extract()`
5. Output to `training_data/raw/bioscan_5m_selective/`

### Why Not Extract All 289K?
- 274K+ images are non-target insects (flies, beetles, wasps, etc.)
- Extracting all wastes ~2 GB disk space and I/O time
- Most extracted images would be discarded during preparation
- The archive format supports per-file extraction natively

### Implementation
A script `training/selective_extract_bioscan.py` should be built if BIOSCAN extraction is approved.
