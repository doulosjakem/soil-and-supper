# Soil & Supper — ML Taxonomy (Revised)

## 1. Recommended Recognition Architecture

### Constraint Analysis
- Target: Android-first, offline, TensorFlow Lite
- Hardware: NVIDIA GTX 1060 6GB, 24GB RAM
- Must be mobile-friendly: small model size, fast inference
- Must be extensible: add new categories over time without retraining everything

### Chosen Architecture: **Hybrid Domain Router + Hierarchical Disease Classifier**

Do NOT build one enormous flat classifier covering crops + weeds + insects + diseases.

Instead, use **specialized lightweight TFLite classifiers** with conditional hierarchy:

```
Stage 1 (domain router): User selects what they are photographing
  OR
Stage 1 (automatic): A tiny "domain router" predicts:
  - Crop / Weed / Insect / Disease / GrowthStage / Unknown

Stage 2a (crop identification): CropClassifier identifies the crop type
  Input: Image
  Output: Crop class (e.g., "Tomato", "Corn", "Rose")

Stage 2b (disease — HIERARCHICAL): DiseaseClassifier conditioned on crop
  Input: Image + Crop prediction
  Output: Disease class (e.g., "Early_blight", "Healthy")
  Rationale: "Early_blight" on tomato looks different from "Early_blight" on potato.
             Conditioning on crop reduces confusion and reduces per-head class count.

Stage 2c (insects): InsectClassifier (flat)
  Input: Image + optional crop hint
  Output: Pest / Beneficial / Other + specific insect class
  Rationale: Insects appear on many crops; conditioning is less important.

Stage 2d (weeds): WeedClassifier (flat)
  Input: Image
  Output: Weed class + Unknown
  Rationale: Weeds are visually distinct from crops; flat classification works.

Stage 2e (growth stages): GrowthStageClassifier (flat, per-crop optional)
  Input: Image + optional crop hint
  Output: Seedling / Vegetative / Flowering / Fruiting / Mature_Harvest / Senescing
```

**Why hybrid:**
1. Domain router keeps models small and trainable
2. Hierarchical disease classifier reduces confusion across crops
3. Error propagation is bounded: if crop ID is wrong, disease classifier gets wrong context but can still fall back to flat prediction
4. Each model can be optimized independently
5. TFLite Model Maker supports this workflow
6. Matches agronomic knowledge: farmers diagnose diseases in crop context

**Why NOT fully flat:**
- 100+ classes with wildly different visual characteristics
- Severe class imbalance
- Some domains have strong data, others weak
- Hard to extend without retraining entire model

### Android Model Strategy
- **Training backbone**: EfficientNet-Lite0 or MobileNetV3-Small via TFLite Model Maker
- **Input resolution**: 224×224 (mobile-friendly)
- **Quantization**: Full integer quantization for TFLite
- **Expected model size**: 2–8 MB per classifier
- **Inference time**: <200ms on modern Android phone (CPU)
- **On-device personalization**: Optional fine-tuning via TFLite on-device training

### Unknown / OOD Strategy
**Primary mechanism**: Confidence thresholding + explicit "Uncertain" output.

Implementation:
- If top-1 confidence < 0.40, display "Uncertain — try a clearer photo"
- Optionally show top-3 predictions with confidence bars
- Do NOT create a catch-all "Unknown" class from random images
- Add explicit "negative" classes per domain where licensing permits
- UI should encourage multiple photos (leaf + fruit + whole plant) when confidence is low

**Rationale**: Unknown classes trained on random images degrade known-class performance. Confidence thresholding is simpler, more honest, and easier to tune.

### Growth Stage Strategy
Train a **single GrowthStageClassifier** with 6 classes: Seedling, Vegetative, Flowering, Fruiting, Mature/Harvest, Senescing. This model predicts the growth stage regardless of crop type. The Android app runs this alongside the crop classifier when the user selects "Check growth stage". This requires a dataset with multiple crop types at multiple stages.

### External Validation Strategy
- **Train**: Dataset A (primary) + selected Dataset B (supplement)
- **Validation**: Held-out portion of Dataset A (same source)
- **External Test**: Dataset C never used for training (different source, different geography)
- **Report domain shift explicitly**: "Model performs 93% on same-source validation, 78% on external-source test"
- **Never use personal garden photos as required validation** — optional supplement only

---

## 2. Final Recommended Taxonomy

### Tier 1 — Core Crops (MVP Priority)

50 classes retained from previous taxonomy, evaluated for American home garden relevance:

| # | Class | Scientific Name | Priority | Est. Images |
|---|-------|----------------|----------|-------------|
| 1 | Tomato | Solanum lycopersicum | Critical | 8,000+ |
| 2 | Pepper_sweet | Capsicum annuum | Critical | 5,000+ |
| 3 | Pepper_hot | Capsicum annuum | High | 1,500+ |
| 4 | Cucumber | Cucumis sativus | High | 4,000+ |
| 5 | Bean | Phaseolus vulgaris | High | 4,000+ |
| 6 | Carrot | Daucus carota | High | 2,500+ |
| 7 | Corn | Zea mays | High | 3,000+ |
| 8 | Onion | Allium cepa | High | 2,000+ |
| 9 | Potato | Solanum tuberosum | High | 2,500+ |
| 10 | Broccoli | Brassica oleracea var. italica | Medium | 2,000+ |
| 11 | Cabbage | Brassica oleracea var. capitata | Medium | 1,500+ |
| 12 | Lettuce | Lactuca sativa | Medium | 1,500+ |
| 13 | Spinach | Spinacia oleracea | Medium | 1,000+ |
| 14 | Pea | Pisum sativum | Medium | 1,500+ |
| 15 | Radish | Raphanus sativus | Medium | 1,500+ |
| 16 | Summer_squash | Cucurbita pepo | Medium | 2,000+ |
| 17 | Winter_squash | Cucurbita spp. | Medium | 1,500+ |
| 18 | Watermelon | Citrullus lanatus | Low | 1,000+ |
| 19 | Cantaloupe | Cucumis melo var. cantalupensis | Low | 800+ |
| 20 | Pumpkin | Cucurbita pepo | Low | 1,000+ |
| 21 | Beet | Beta vulgaris | Medium | 1,500+ |
| 22 | Turnip | Brassica rapa subsp. rapa | Low | 800+ |
| 23 | Sweet_potato | Ipomoea batatas | Low | 600+ |
| 24 | Basil | Ocimum basilicum | Medium | 500+ |
| 25 | Cilantro | Coriandrum sativum | Medium | 400+ |
| 26 | Parsley | Petroselinum crispum | Low | 300+ |
| 27 | Dill | Anethum graveolens | Low | 200+ |
| 28 | Chives | Allium schoenoprasum | Low | 200+ |
| 29 | Rosemary | Salvia rosmarinus | Low | 300+ |
| 30 | Thyme | Thymus vulgaris | Low | 200+ |
| 31 | Oregano | Origanum vulgare | Low | 200+ |
| 32 | Sage | Salvia officinalis | Low | 200+ |
| 33 | Strawberry | Fragaria × ananassa | Medium | 2,000+ |
| 34 | Blueberry | Vaccinium corymbosum | Low | 800+ |
| 35 | Grape | Vitis spp. | Low | 600+ |
| 36 | Marigold | Tagetes spp. | Low | 400+ |
| 37 | Zinnia | Zinnia elegans | Low | 300+ |
| 38 | Nasturtium | Tropaeolum majus | Low | 200+ |
| 39 | Sunflower | Helianthus annuus | Low | 500+ |
| 40 | Cosmos | Cosmos bipinnatus | Low | 200+ |
| 41 | Petunia | Petunia spp. | Low | 300+ |
| 42 | Begonia | Begonia spp. | Low | 200+ |
| 43 | Eggplant | Solanum melongena | Low | 1,000+ |
| 44 | Okra | Abelmoschus esculentus | Low | 600+ |
| 45 | Asparagus | Asparagus officinalis | Low | 400+ |
| 46 | Rhubarb | Rheum rhabarbarum | Low | 300+ |
| 47 | Celery | Apium graveolens | Low | 400+ |
| 48 | Leek | Allium ampeloprasum var. porrum | Low | 300+ |
| 49 | Fennel | Foeniculum vulgare | Low | 200+ |
| 50 | Artichoke | Cynara cardunculus var. scolymus | Low | 200+ |

**Additions to consider for v2 (not MVP):**
- Tree fruits (Apple, Pear, Peach, Plum) — require different imaging context (tree/fruit vs. whole plant)
- More specific herb varieties
- More specific flower varieties

### Tier 2 — Common Garden Weeds (MVP Priority)

20 weed classes + 1 "Other Weed" catch-all:

| # | Class | Scientific Name | Priority | Est. Images | Source |
|---|-------|----------------|----------|-------------|--------|
| 1 | Dandelion | Taraxacum officinale | Critical | 2,000+ | Bugwood, DeepWeeds supplement |
| 2 | Crabgrass | Digitaria sanguinalis | High | 1,500+ | CWD30, DeepWeeds |
| 3 | White_clover | Trifolium repens | High | 1,000+ | DeepWeeds, CWD30 |
| 4 | Purslane | Portulaca oleracea | High | 800+ | CWD30 |
| 5 | Lambsquarters | Chenopodium album | High | 800+ | CWD30 |
| 6 | Chickweed | Stellaria media | Medium | 600+ | CWD30 |
| 7 | Pigweed | Amaranthus spp. | Medium | 1,000+ | CWD30 |
| 8 | Plantain | Plantago spp. | Medium | 600+ | CWD30 |
| 9 | Nutsedge | Cyperus spp. | Medium | 500+ | CWD30 |
| 10 | Ragweed | Ambrosia artemisiifolia | Medium | 600+ | CWD30 |
| 11 | Bindweed | Calystegia sepium | Medium | 400+ | CWD30 |
| 12 | Foxtail | Setaria spp. | Medium | 500+ | CWD30 |
| 13 | Thistle | Cirsium spp. | Medium | 500+ | CWD30 |
| 14 | Poison_ivy | Toxicodendron radicans | Low | 400+ | Bugwood |
| 15 | Garlic_mustard | Alliaria petiolata | Low | 300+ | CWD30 |
| 16 | Knotweed | Polygonum spp. | Low | 300+ | CWD30 |
| 17 | Ground_ivy | Glechoma hederacea | Low | 300+ | CWD30 |
| 18 | Woodsorrel | Oxalis spp. | Low | 300+ | CWD30 |
| 19 | Johnsongrass | Sorghum halepense | Low | 300+ | CWD30 |
| 20 | Quackgrass | Elymus repens | Low | 200+ | CWD30 |
| 21 | Other_weed | Unknown | Low | — | Negative examples |

**Note**: DeepWeeds contains 8 Australian species (Chinee apple, Snake weed, Lantana, Prickly acacia, Siam weed, Parthenium, Rubber vine, Parkinsonia). These are NOT common American garden weeds. Use DeepWeeds as supplementary data only; prioritize CWD30 for North American relevance.

### Tier 3 — Insect Pests (MVP Priority)

18 pest classes + 1 "Other Pest" catch-all:

| # | Class | Scientific Name | Priority | Est. Images | Source |
|---|-------|----------------|----------|-------------|--------|
| 1 | Aphid | Aphididae spp. | Critical | 3,000+ | IP102, Bugwood |
| 2 | Japanese_beetle | Popillia japonica | High | 1,000+ | Bugwood, extension services |
| 3 | Colorado_potato_beetle | Leptinotarsa decemlineata | High | 1,000+ | IP102, Bugwood |
| 4 | Cucumber_beetle | Acalymma vittatum / Diabrotica spp. | High | 800+ | IP102, Bugwood |
| 5 | Cabbage_worm | Pieris rapae | High | 1,000+ | IP102 |
| 6 | Tomato_hornworm | Manduca quinquemaculata | High | 800+ | IP102, Bugwood |
| 7 | Squash_bug | Anasa tristis | Medium | 600+ | IP102, Bugwood |
| 8 | Whitefly | Aleyrodidae spp. | Medium | 1,000+ | IP102 |
| 9 | Spider_mite | Tetranychidae spp. | Medium | 800+ | IP102, Bugwood |
| 10 | Thrips | Thysanoptera spp. | Medium | 800+ | IP102 |
| 11 | Leafminer | Liriomyza spp. | Medium | 600+ | IP102 |
| 12 | Cutworm | Noctuidae spp. | Medium | 600+ | IP102 |
| 13 | Stink_bug | Pentatomidae spp. | Medium | 800+ | IP102, Bugwood |
| 14 | Flea_beetle | Chrysomelidae spp. | Medium | 500+ | IP102 |
| 15 | Mexican_bean_beetle | Epilachna varivestis | Low | 400+ | IP102 |
| 16 | Corn_earworm | Helicoverpa zea | Low | 500+ | IP102 |
| 17 | Squash_vine_borer | Melittia cucurbitae | Low | 300+ | Bugwood |
| 18 | Blister_beetle | Meloidae spp. | Low | 300+ | Bugwood |
| 19 | Other_pest | Unknown | Low | — | Negative examples |

**Data source note**: IP102 contains 75,000+ images across 102 pest classes. The dataset is hierarchical — pests are grouped by crop (rice, corn, wheat, etc.). We will extract only the pest classes relevant to our target crops. IP102 license requires contacting the author for non-academic use. **Mark as "contact required" — do not use for commercial model until permission is obtained.**

### Tier 4 — Beneficial Insects (MVP Priority)

7 beneficial insect classes:

| # | Class | Scientific Name | Priority | Est. Images | Source |
|---|-------|----------------|----------|-------------|--------|
| 1 | Ladybug | Coccinellidae spp. | High | 800+ | Bugwood, iNaturalist supplement (CC0 only) |
| 2 | Green_lacewing | Chrysoperla carnea | Medium | 400+ | Bugwood |
| 3 | Honey_bee | Apis mellifera | Medium | 600+ | Bugwood |
| 4 | Hoverfly | Syrphidae spp. | Medium | 300+ | Bugwood |
| 5 | Praying_mantis | Mantis religiosa | Medium | 400+ | Bugwood |
| 6 | Spider | Araneae spp. | Medium | 500+ | Bugwood |
| 7 | Earthworm | Lumbricidae spp. | Low | 200+ | Bugwood |

**Important**: Include beneficial insects so the model does not classify every insect as a pest. This is critical for garden-app trust.

### Tier 5 — Plant Diseases and Disorders (MVP Priority)

30 disease/problem classes, organized by crop where appropriate:

| # | Class | Target Crops | Priority | Actual Count | Sources | Readiness |
|---|-------|-------------|----------|-------------|---------|-----------|
| 1 | Healthy | All crops | Critical | 15,931 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 2 | Powdery_mildew | Many crops | High | 1,052 | PlantVillage | NEEDS_MORE_DATA |
| 3 | Downy_mildew | Many crops | Medium | 0 | None | DATASET_SEARCH_REQUIRED |
| 4 | Early_blight | Tomato, Potato | High | 2,204 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 5 | Late_blight | Tomato, Potato | High | 3,125 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 6 | Septoria_leaf_spot | Tomato | Medium | 1,922 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 7 | Bacterial_spot | Pepper, Tomato | Medium | 3,305 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 8 | Fusarium_wilt | Many crops | Medium | 0 | None | DATASET_SEARCH_REQUIRED |
| 9 | Verticillium_wilt | Many crops | Medium | 0 | None | DATASET_SEARCH_REQUIRED |
| 10 | Anthracnose | Many crops | Medium | 0 | None | DATASET_SEARCH_REQUIRED |
| 11 | Rust | Many crops | Medium | 1,308 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 12 | Leaf_spot | Many crops | Medium | 13,900 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 13 | Blossom_end_rot | Tomato, Pepper | Medium | 0 | None | DATASET_SEARCH_REQUIRED |
| 14 | Nutrient_deficiency | General | Low | 0 | None | DATASET_SEARCH_REQUIRED |
| 15 | Sunscald | Tomato, Pepper | Low | 0 | None | DATASET_SEARCH_REQUIRED |
| 16 | Frost_damage | General | Low | 0 | None | DATASET_SEARCH_REQUIRED |
| 17 | Hail_damage | General | Low | 0 | None | DATASET_SEARCH_REQUIRED |
| 18 | Overwatering_stress | General | Low | 0 | None | DATASET_SEARCH_REQUIRED |
| 19 | Underwatering_stress | General | Low | 0 | None | DATASET_SEARCH_REQUIRED |
| 20 | Insect_damage | General | Low | 0 | None | DATASET_SEARCH_REQUIRED |
| 21 | Chewing_damage | General | Low | 0 | None | DATASET_SEARCH_REQUIRED |
| 22 | Leaf_miner_damage | General | Low | 0 | None | DATASET_SEARCH_REQUIRED |
| 23 | Apple_scab | Apple | Low | 723 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 24 | Cedar_apple_rust | Apple | Low | 363 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 25 | Grape_black_rot | Grape | Low | 1,244 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 26 | Peach_bacterial_spot | Peach | Low | 2,297 | PlantVillage | NEEDS_MORE_DATA |
| 27 | Soybean_rust | Soybean | Low | 0 | None | DATASET_SEARCH_REQUIRED |
| 28 | Squash_powdery_mildew | Squash | Low | 1,965 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 29 | Tomato_mosaic_virus | Tomato | Low | 427 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |
| 30 | Tomato_yellow_leaf_curl | Tomato | Low | 5,432 | PlantVillage, PlantDoc | NEEDS_MORE_DATA |

**Primary source**: PlantVillage (CC0 1.0) — 54,306 images, 38 classes covering 14 crop species with healthy + disease combinations. This is the single most important disease dataset.

**Supplement**: PlantDoc (CC BY 4.0) — 2,569 images, 29 classes, real-world field images with natural backgrounds. Complements PlantVillage's controlled-background images.

**Post-PlantVillage Readiness Summary**:
- **TRAINABLE_NOW**: 0 classes (all classes fail one or more readiness criteria)
- **NEEDS_MORE_DATA**: 15 classes have data but fail readiness criteria (field-vs-lab ratio, capture diversity, label consensus)
- **DATASET_SEARCH_REQUIRED**: 117 classes have no current usable source
- **Main blockers**: Insufficient field imagery diversity, lack of growth-stage data, no crop/weed/beneficial-insect data

### Tier 6 — Growth Stages (Separate Attribute Model)

6 growth stage classes (NOT per-crop):

| # | Class | Description | Priority | Est. Images | Source |
|---|-------|-------------|----------|-------------|--------|
| 1 | Seedling | Cotyledon/early leaves | Medium | 2,000+ | CWD30, Plant Growth Stage Detection |
| 2 | Vegetative | Leaf growth, no flowers/fruit | Medium | 3,000+ | CWD30 |
| 3 | Flowering | Flowers present | Medium | 2,000+ | CWD30, BDFlower |
| 4 | Fruiting | Fruit developing | Medium | 2,000+ | CWD30 |
| 5 | Mature_Harvest | Ripe fruit, ready | Medium | 1,500+ | CWD30 |
| 6 | Senescing | Declining, yellowing | Low | 800+ | CWD30 |

**Feasibility**: CWD30 contains growth stage metadata for 219,770 images across 30 species. This is sufficient to train a general growth stage classifier. BDFlower (CC BY 4.0, 3,889 images, 8 flowers × 3 stages) is a good supplement.

**Design note**: Growth stage is a SEPARATE model, not embedded in crop/disease/weed models. The UI can run it alongside any other identification.

### Tier 7 — Deferred to Post-MVP

- Tree fruits (Apple, Pear, Peach, Plum, Cherry) — different imaging context
- Grains (Corn already included, but wheat/barley/oat are niche)
- Mushrooms — not plants, different domain
- Beneficial nematodes, soil organisms — too small to photograph reliably
- Specific pest life stages (egg/larva/pupa/adult) — too fine-grained for MVP
- Regional/state-specific noxious weeds — defer to v2

## 2.5 Training Readiness Thresholds

Replace the old "≥200 images = trainable" heuristic with the following framework.

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

## 2.6 External Evaluation Strategy

### Principle
Evaluate on held-out external datasets, NOT on same-source data alone. Report domain shift explicitly.

### Per-Domain Evaluation Plan

| Domain | Training Sources | Validation Source | External Test Source | Leakage Prevention |
|--------|-----------------|-------------------|---------------------|-------------------|
| Crops | Bangladesh Veg, Smartphone Veg, VegNet, PlantDoc (healthy plants) | Same-source 15% holdout | PlantVillage (different source, different geography) | Near-duplicate hash across splits |
| Weeds | DeepWeeds, CWD30, Bugwood | Same-source 15% holdout | NDSU Weed-crop dataset | Geographic split (AU vs US) |
| Insects | BIOSCAN-5M (selective, specimen only), Bugwood | Same-source 15% holdout | Roboflow Insect Pest (if license clears) | Taxonomic split (never mix same species across splits) |
| Diseases | PlantVillage, PlantDoc | Same-source 15% holdout | iNaturalist disease observations (CC BY only) | Crop-split: train on Tomato diseases, test on Pepper diseases |
| Growth Stages | CWD30, BDFlower, Plant Growth Stage Detection | Same-source 15% holdout | Sunflower Growth Stage dataset | Species split |

### Domain Shift Measurement
- Report same-source validation accuracy
- Report external-test accuracy
- Report drop: "Model performs X% on same-source validation, Y% on external-source test (drop: Z%)"
- A drop >15% indicates the model is overfit to training domain

### Domain Shift Concerns
- **PlantVillage-style controlled lab photos** vs **real garden photographs** (PlantDoc): PlantDoc images have soil, multiple plants, shadows, clutter. This is the desired target domain.
- **BIOSCAN specimen microscopy** vs **smartphone garden photos**: Severe domain shift. Do NOT evaluate garden-photo performance on BIOSCAN.
- **Smartphone datasets** (Bangladesh Veg, Smartphone Veg, VegNet): These use phone cameras but in controlled settings. Closer to target domain than lab photos.

### No Personal Photographs
- Do not use personal garden photos for required validation
- Personal photos may be used as informal post-deployment sanity checks only
- All formal evaluation must use publicly available, licensed datasets

## 2.7 BIOSCAN-5M Analysis

### Archive Structure
- **Format**: ZIP
- **Compressed size**: 2,119.7 MB
- **Contents**: `bioscan5m/images/original_256/train/{chunk}/{processid}.jpg`
- **Chunks**: 16 numeric subdirectories, ~17,900-18,300 images each
- **Total images in archive**: 289,203 (train split only)
- **Image format**: RGB JPEG, 341×256 pixels
- **Image source**: Keyence VHX-7000 microscope, cropped/resized from 1024×768 originals

### Metadata
- **Metadata file**: `BIOSCAN_5M_Insect_Dataset_metadata_MultiTypes.zip` (2 GB compressed, 4 GB CSV)
- **Columns**: processid, sampleid, taxon, phylum, class, order, family, subfamily, genus, species, dna_bin, dna_barcode, country, province_state, coord-lat, coord-lon, image_measurement_value, area_fraction, scale_factor, inferred_ranks, split, index_bioscan_1M_insect, chunk
- **Total records**: 5,150,850
- **Records with species labels**: 473,094 (9.2%)
- **Records with genus labels**: 1,226,765 (23.8%)

### Taxonomic Coverage (train split, 289,203 images)
| Rank | Categories | Labelled |
|------|-----------|----------|
| phylum | 1 | 100% |
| class | 10 | 99.9% |
| order | 55 | 99.7% |
| family | 934 | 95.8% |
| genus | 7,605 | 23.8% |
| species | 22,622 | 9.2% |

### Defensible Target-Class Mappings (genus-level only)

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
| Japanese_beetle | Popillia | 0 | 0 |
| Colorado_potato_beetle | Leptinotarsa | 0 | 0 |
| Cucumber_beetle | Diabrotica | 0 | 0 |
| Mexican_bean_beetle | Epilachna | 0 | 0 |
| Tomato_hornworm | Manduca | 0 | 0 |
| Cabbage_worm | Pieris, Artogeia | 0 | 0 |
| Squash_vine_borer | Melittia | 0 | 0 |

### Domain Shift Verdict
BIOSCAN-5M images are **specimen-style microscope photographs** with plain backgrounds, controlled lighting, and no environmental context. This is a **severe domain shift** from smartphone garden photos. **BIOSCAN is NOT useful for direct training**. It may be useful for self-supervised pre-learning of low-level insect features, but only if paired with heavy domain adaptation.

### Selective Extraction
Do NOT extract all 289K images. Use `training/selective_extract_bioscan.py` to extract only genus-matched images after verifying the target class list with the team.

---

## 3. Class Aliases and Synonyms

### Crops (selected examples)
| Model Class | Aliases / Synonyms |
|-------------|-------------------|
| Tomato | tomato, tomatoes |
| Pepper_sweet | bell pepper, sweet pepper, capsicum |
| Pepper_hot | chili pepper, chile pepper, jalapeño, habanero |
| Cucumber | cucumber, cukes |
| Bean | bean, green bean, snap bean, wax bean, pole bean, bush bean |
| Corn | corn, sweet corn, maize |
| Summer_squash | summer squash, zucchini, yellow squash, courgette |
| Winter_squash | winter squash, butternut, spaghetti squash, acorn squash |
| Basil | basil, sweet basil, Thai basil |
| Cilantro | cilantro, coriander, Chinese parsley |

### Weeds
| Model Class | Aliases / Synonyms |
|-------------|-------------------|
| Dandelion | dandelion, lion's tooth |
| Crabgrass | crabgrass, smooth crabgrass, large crabgrass |
| White_clover | white clover, clover, Dutch clover |
| Purslane | purslane, common purslane, verdolaga |
| Lambsquarters | lambsquarters, lamb's quarters, goosefoot |
| Pigweed | pigweed, redroot pigweed, wild amaranth |
| Nutsedge | nutsedge, yellow nutsedge, purple nutsedge |

### Insects
| Model Class | Aliases / Synonyms |
|-------------|-------------------|
| Aphid | aphid, aphids, greenfly, blackfly |
| Japanese_beetle | Japanese beetle, beetle |
| Colorado_potato_beetle | Colorado potato beetle, potato beetle |
| Ladybug | ladybug, ladybird, lady beetle |
| Honey_bee | honey bee, bee, honeybee |

### Diseases
| Model Class | Aliases / Synonyms |
|-------------|-------------------|
| Powdery_mildew | powdery mildew, mildew, white mildew |
| Early_blight | early blight, Alternaria |
| Late_blight | late blight, Phytophthora |
| Bacterial_spot | bacterial spot, bacterial speck |
| Healthy | healthy, no disease, no problem |

---

## 4. Likely Confusion Pairs

### Crops
1. Summer_squash ↔ Winter_squash (both Cucurbita)
2. Cucumber ↔ Summer_squash (both cucurbits)
3. Watermelon ↔ Cantaloupe (both melons)
4. Tomato ↔ Eggplant (both Solanum)
5. Spinach ↔ Lettuce (both leafy greens)
6. Cilantro ↔ Parsley (similar leaf shapes)
7. Dill ↔ Fennel (feathery foliage)
8. Thyme ↔ Oregano (small-leaf herbs)
9. Onion ↔ Leek (both Allium)
10. Bean ↔ Pea (both legumes)

### Weeds
1. White_clover ↔ Woodsorrel (three-leaf clovers)
2. Lambsquarters ↔ Pigweed (similar leaf shape)
3. Nutsedge ↔ Grass (grassy appearance)
4. Bindweed ↔ Morning_glory (convolvulus family)
5. Foxtail ↔ Crabgrass (grass weeds)

### Insects
1. Aphid ↔ Whitefly (small, soft-bodied)
2. Ladybug ↔ Mexican_bean_beetle (both beetles, similar size)
3. Cucumber_beetle ↔ Ladybug (both spotted beetles)
4. Spider_mite ↔ Spider (both arachnids, very different size)

### Diseases
1. Powdery_mildew ↔ Downy_mildew (both white fungal growth)
2. Early_blight ↔ Leaf_spot (both leaf spots)
3. Nutrient_deficiency ↔ Disease_damage (both cause discoloration)

---

## 5. Data Sufficiency Assessment

### Crops
| Status | Classes | Count |
|--------|---------|-------|
| Strong (>5,000 images) | Tomato, Pepper_sweet, Cucumber, Bean | 4 |
| Moderate (2,000–5,000) | Corn, Carrot, Onion, Potato, Broccoli, Strawberry, Summer_squash | 7 |
| Marginal (1,000–2,000) | Cabbage, Lettuce, Spinach, Pea, Radish, Winter_squash, Eggplant, Beet | 8 |
| Weak (<1,000) | Watermelon, Cantaloupe, Pumpkin, Turnip, Sweet_potato, Blueberry, Grape | 7 |
| Very Weak (<500) | Most herbs (9), Flowers (7), Okra, Asparagus, Rhubarb, Celery, Leek, Fennel, Artichoke | 20 |

### Weeds
| Status | Classes | Count | Source |
|--------|---------|-------|--------|
| Strong (>1,000) | Dandelion, Crabgrass, White_clover, Purslane, Lambsquarters, Pigweed | 6 | CWD30 + DeepWeeds |
| Moderate (500–1,000) | Chickweed, Plantain, Nutsedge, Ragweed, Bindweed, Foxtail, Thistle | 7 | CWD30 |
| Weak (<500) | Most remaining | 8 | CWD30 + Bugwood supplement |

**Key gap**: CWD30 contains 20 weed classes but is geographically Korean/Australian. Some species overlap with North America, but several do not. We will filter to the 21 target weeds and supplement with Bugwood images.

### Insects/Pests
| Status | Classes | Count | Source |
|--------|---------|-------|--------|
| Strong (>1,000) | Aphid | 1 | IP102 (if license resolved) |
| Moderate (500–1,000) | Japanese_beetle, Colorado_potato_beetle, Cucumber_beetle, Cabbage_worm, Whitefly, Stink_bug | 6 | IP102 + Bugwood |
| Weak (<500) | Most remaining pests | 12 | Bugwood, extension services |
| Beneficials | All 7 classes | All <500 | Bugwood |

**Critical gap**: IP102 is the only large-scale pest dataset (75,000 images), but its license requires contacting the author for commercial use. Bugwood has many insect images but requires photographer approval for commercial use. This is the **biggest data gap**.

### Diseases
| Status | Classes | Count | Source |
|--------|---------|-------|--------|
| Strong (>2,000) | Healthy, Powdery_mildew, Early_blight, Late_blight, Rust | 5 | PlantVillage (CC0) |
| Moderate (1,000–2,000) | Downy_mildew, Bacterial_spot, Fusarium_wilt, Leaf_spot | 4 | PlantVillage + PlantDoc |
| Weak (<1,000) | Most specific diseases | 21 | PlantDoc + web images |

**Key finding**: PlantVillage provides excellent coverage for 14 crop species × diseases. PlantDoc adds real-world field images with natural backgrounds. Combined, we have strong disease data for the most common garden crops.

### Growth Stages
| Status | Classes | Count | Source |
|--------|---------|-------|--------|
| Moderate | All 6 stages | 2,000–3,000 each | CWD30 (primary) |
| Supplement | Flower stages | 3,889 | BDFlower |

**Feasibility**: CWD30's growth stage metadata across 30 species is sufficient for a general growth stage classifier. No need for personal photography.

---

## 6. Data Gaps and Personal Photography Requirement

### Data Gaps (Classes Needing Additional Data)

| Category | Class | Gap Severity | Recommended Action |
|----------|-------|-------------|-------------------|
| Crop | Herbs (9 classes) | HIGH | Supplement with Bugwood + targeted web scraping (CC BY/CC0 only) |
| Crop | Flowers (7 classes) | HIGH | Supplement with Bugwood + targeted web scraping |
| Crop | Watermelon, Cantaloupe | MEDIUM | Supplement with USDA ARS + web images |
| Crop | Okra, Asparagus, Rhubarb | MEDIUM | Supplement with web images + extension services |
| Weed | 8 weak weed classes | MEDIUM | Supplement with Bugwood + CWD30 filtering |
| Insect | 12 weak pest classes | HIGH | Supplement with Bugwood (requires approval workflow) |
| Insect | All 7 beneficial classes | MEDIUM | Supplement with Bugwood |
| Disease | 21 weak disease classes | MEDIUM | Supplement with PlantDoc + web images (CC BY only) |
| Disease | Non-disease problems | HIGH | No good dataset exists; web images + extension services |

### Personal Photography Requirement

**Minimal to none for MVP.**

The automated pipeline can acquire:
- ~25,000 crop images from existing CC BY 4.0 / CC0 datasets
- ~15,000 weed images from CWD30 + DeepWeeds
- ~5,000 disease images from PlantVillage + PlantDoc
- ~2,000 growth stage images from CWD30 + BDFlower

**Personal photography is ONLY recommended if:**
1. After training the baseline, evaluation shows a specific class has <200 images and is performing poorly
2. No alternative dataset can be found with acceptable license
3. The class is critical for MVP (e.g., a major crop disease with no dataset)

**Do NOT photograph personal garden images for validation.** Use external test sets only.

---

## 7. External Evaluation Strategy

### Train/Validation/Test Protocol

For each domain model:

| Split | Source | Purpose |
|-------|--------|---------|
| Train | Dataset A (primary) + Dataset B (supplement) | Model training |
| Validation | Held-out 15% of Dataset A | Hyperparameter tuning, early stopping |
| External Test | Dataset C (never in train/val) | Final generalization estimate |

### Domain Shift Reporting

Always report:
- **Same-source accuracy**: Validation on held-out portion of training dataset
- **External accuracy**: Test on completely separate dataset
- **Domain gap**: Difference between same-source and external accuracy

Example:
```
CropClassifier:
  Same-source validation: 94.2%
  External test (USDA ARS): 81.5%
  Domain gap: 12.7%
  
  Interpretation: Model generalizes well but struggles with 
  professional field photos vs. market/consumer photos.
```

### Recommended External Test Sources

| Domain | External Test Source | Rationale |
|--------|---------------------|-----------|
| Crops | USDA ARS Image Gallery | Professional field photos, public domain, never used in training |
| Weeds | Bugwood WeedImages | Different geography, different photographers |
| Diseases | PlantDoc | Real-world field images vs. PlantVillage's controlled backgrounds |
| Insects | Bugwood InsectImages | Professional insect photography vs. field snapshots |

---

## 8. Android Model Recommendation

### MVP Model Stack

| Model | Domain | Classes | Backbone | Size | Inference |
|-------|--------|---------|----------|------|-----------|
| CropClassifier | Crops | 50 + Unknown | EfficientNet-Lite0 | ~4 MB | ~150ms |
| WeedClassifier | Weeds | 21 + Unknown | MobileNetV3-Small | ~3 MB | ~100ms |
| DiseaseClassifier | Diseases | 30 + Unknown | EfficientNet-Lite0 | ~4 MB | ~150ms |
| GrowthStageClassifier | Growth | 6 | MobileNetV3-Small | ~2 MB | ~80ms |

**Total**: ~13 MB model bundle, <500ms inference for full pipeline.

### Training Workflow

```bash
# 1. Prepare crop data
python training/prepare_dataset.py --domain crops

# 2. Prepare weed data
python training/prepare_dataset.py --domain weeds

# 3. Prepare disease data
python training/prepare_dataset.py --domain diseases

# 4. Prepare growth stage data
python training/prepare_dataset.py --domain growth_stages

# 5. Train crop classifier
python training/train.py --domain crops --model efficientnet_lite0

# 6. Train weed classifier
python training/train.py --domain weeds --model mobilenet_v3_small

# 7. Train disease classifier
python training/train.py --domain diseases --model efficientnet_lite0

# 8. Train growth stage classifier
python training/train.py --domain growth_stages --model mobilenet_v3_small

# 9. Export all to TFLite
python training/export.py --all
```

### Compute Feasibility (GTX 1060 6GB)

| Model | Training Time (est.) | VRAM Required |
|-------|---------------------|---------------|
| CropClassifier (50 classes, 25K images) | 2–4 hours | ~4 GB |
| WeedClassifier (21 classes, 15K images) | 1–2 hours | ~3 GB |
| DiseaseClassifier (30 classes, 20K images) | 2–3 hours | ~4 GB |
| GrowthStageClassifier (6 classes, 10K images) | 30–60 min | ~2 GB |

**All models trainable on GTX 1060 6GB with 24GB system RAM.**

---

## 9. Data Sources Summary by Domain

### Crops
| Dataset | License | Images | Classes | Status |
|---------|---------|--------|---------|--------|
| Bangladesh Vegetables | CC BY 4.0 | 4,730 | 12 | USE |
| Smartphone Vegetable Detection | CC BY 4.0 | 3,534 | 10 | USE |
| BanglaVeg | CC BY 4.0 | 4,319 | 8 | USE |
| VegNet | CC BY 4.0 | 6,850 | 4 | USE (supplement) |
| USDA ARS | Public Domain | 6,500+ | 15+ | SUPPLEMENT |
| Early-Stage Crops | CC BY 4.0 | 2,801 | 3 | SUPPLEMENT |

### Weeds
| Dataset | License | Images | Classes | Status |
|---------|---------|--------|---------|--------|
| CWD30 | Unclear (Elsevier) | 219,770 | 20 weeds | REJECT until license clarified |
| DeepWeeds | CC BY 4.0 | 17,509 | 8 weeds + negative | USE (supplement, Australia-specific) |
| Bugwood WeedImages | Mixed (per-photographer) | Unknown | Many | SUPPLEMENT (requires approval workflow) |

**Note on CWD30**: Published in Elsevier journal, no explicit license on GitHub. Do NOT assume commercial usability. Contact authors before using.

### Diseases
| Dataset | License | Images | Classes | Status |
|---------|---------|--------|---------|--------|
| PlantVillage | CC0 1.0 | 54,306 | 38 | USE (primary) |
| PlantDoc | CC BY 4.0 | 2,569 | 29 | USE (supplement) |

### Growth Stages
| Dataset | License | Images | Classes | Status |
|---------|---------|--------|---------|--------|
| CWD30 | Unclear | 219,770 | Growth metadata | REJECT until license clarified |
| Plant Growth Stage Detection (Roboflow) | CC BY 4.0 | 7,306 | 4 | USE |
| BDFlower | CC BY 4.0 | 3,889 | 3 stages × 8 flowers | USE |

### Insects/Pests
| Dataset | License | Images | Classes | Status |
|---------|---------|--------|---------|--------|
| IP102 | Contact required | 75,000+ | 102 | REJECT for now — contact author |
| Bugwood InsectImages | Mixed | Unknown | Many | SUPPLEMENT (requires approval) |

### Beneficial Insects
| Dataset | License | Images | Classes | Status |
|---------|---------|--------|---------|--------|
| Bugwood InsectImages | Mixed | Unknown | Many | SUPPLEMENT (requires approval) |

---

## 10. Implementation Priority

### Phase A: MVP Crop Classifier (No personal photos needed)
1. Acquire Bangladesh Vegetables, Smartphone Veg, BanglaVeg, VegNet
2. Prepare and curate 50-class crop dataset
3. Train CropClassifier with EfficientNet-Lite0
4. Evaluate on external test set (USDA ARS)
5. Deploy to Android

### Phase B: Weed Classifier (Minimal personal photos)
1. Filter CWD30 for target weed classes (if license clarified)
2. Use DeepWeeds as supplement
3. Supplement with Bugwood CC BY images
4. Train WeedClassifier
5. Target: 500+ images per weed class

### Phase C: Disease Classifier (No personal photos needed)
1. Use PlantVillage (CC0) as primary
2. Supplement with PlantDoc (CC BY 4.0)
3. Train DiseaseClassifier
4. Target: 1,000+ images per disease class

### Phase D: Growth Stage Classifier (No personal photos needed)
1. Use CWD30 growth metadata (if license clarified)
2. Supplement with Plant Growth Stage Detection + BDFlower
3. Train GrowthStageClassifier

### Phase E: Insect/Pest Classifier (Likely needs personal photos or licensing negotiation)
1. Contact IP102 author for commercial use permission
2. If denied, use Bugwood + extension service images
3. Train InsectClassifier
4. Likely requires personal photography for weak classes

---

## 11. Revision History

- 2026-08-14: Initial taxonomy v1 — 50 crop classes
- 2026-08-14: Revised taxonomy v2 — expanded to 150+ classes across 6 domains, architecture recommendation, data sufficiency assessment, MVP phasing
- 2026-08-14: Phase 14 update — class-level readiness assessment, dataset acquisition status, taxonomy refinements

---

## 12. Class-Level Readiness Assessment (Phase 14)

Each class is classified by current data availability and commercial-license status:

| Status | Meaning |
|--------|---------|
| **TRAINABLE_NOW** | ≥500 validated, labeled, license-compatible images available |
| **NEEDS_MORE_DATA** | Some images exist but <500 or from limited sources |
| **DATASET_SEARCH_REQUIRED** | No current dataset; need to find or curate alternative |
| **LICENSE_BLOCKED** | Best source exists but license prohibits commercial use |
| **DEFERRED** | Post-MVP; not critical for initial product scope |

### Crops

| Class | Status | Est. Images | Primary Source | Notes |
|-------|--------|-------------|----------------|-------|
| Tomato | TRAINABLE_NOW | 8,000+ | PlantVillage + Bangladesh Veg + Smartphone Veg + VegNet | Strong multi-source coverage |
| Pepper_sweet | TRAINABLE_NOW | 5,000+ | PlantVillage + Bangladesh Veg + Smartphone Veg + VegNet | Map Capsicum/Bell Pepper |
| Pepper_hot | NEEDS_MORE_DATA | 1,500+ | VegNet + Smartphone Veg | Limited hot pepper images |
| Cucumber | TRAINABLE_NOW | 4,000+ | PlantVillage + Bangladesh Veg + Smartphone Veg | Strong coverage |
| Bean | TRAINABLE_NOW | 4,000+ | PlantVillage + Bangladesh Veg + Smartphone Veg + Early Stage | Good multi-source |
| Carrot | TRAINABLE_NOW | 2,500+ | Bangladesh Veg + Smartphone Veg + VegNet | Adequate |
| Corn | TRAINABLE_NOW | 3,000+ | PlantVillage + Early Stage + VegNet | Good coverage |
| Onion | TRAINABLE_NOW | 2,000+ | Bangladesh Veg + Smartphone Veg | Adequate |
| Potato | TRAINABLE_NOW | 2,500+ | PlantVillage + Bangladesh Veg | Good disease + crop coverage |
| Broccoli | NEEDS_MORE_DATA | 2,000+ | Bangladesh Veg | Limited sources |
| Cabbage | NEEDS_MORE_DATA | 1,500+ | Bangladesh Veg + Smartphone Veg | Adequate but thin |
| Lettuce | NEEDS_MORE_DATA | 1,500+ | Smartphone Veg + VegNet | Limited |
| Spinach | NEEDS_MORE_DATA | 1,000+ | Smartphone Veg + VegNet | Limited |
| Pea | NEEDS_MORE_DATA | 1,500+ | Early Stage + Smartphone Veg | Limited |
| Radish | NEEDS_MORE_DATA | 1,500+ | Bangladesh Veg + Smartphone Veg + VegNet | Adequate |
| Summer_squash | NEEDS_MORE_DATA | 2,000+ | PlantVillage + Bangladesh Veg + VegNet | Map Zucchini |
| Winter_squash | NEEDS_MORE_DATA | 1,500+ | PlantVillage + Bangladesh Veg | Limited |
| Watermelon | DATASET_SEARCH_REQUIRED | 500+ | VegNet (partial) | Need more sources |
| Cantaloupe | DATASET_SEARCH_REQUIRED | 400+ | VegNet (partial) | Need more sources |
| Pumpkin | NEEDS_MORE_DATA | 1,000+ | PlantVillage + Bangladesh Veg | Adequate |
| Beet | NEEDS_MORE_DATA | 1,500+ | Smartphone Veg + VegNet | Limited |
| Turnip | DATASET_SEARCH_REQUIRED | 400+ | VegNet (partial) | Need more sources |
| Sweet_potato | DATASET_SEARCH_REQUIRED | 300+ | Smartphone Veg (partial) | Need more sources |
| Basil | DATASET_SEARCH_REQUIRED | 500+ | Herb datasets (CC BY 4.0) | Herb-specific datasets available |
| Cilantro | DATASET_SEARCH_REQUIRED | 400+ | Herb datasets (CC BY 4.0) | Herb-specific datasets available |
| Parsley | DATASET_SEARCH_REQUIRED | 300+ | Herb datasets (CC BY 4.0) | Herb-specific datasets available |
| Dill | DATASET_SEARCH_REQUIRED | 200+ | Herb datasets (CC BY 4.0) | Herb-specific datasets available |
| Chives | DATASET_SEARCH_REQUIRED | 200+ | Herb datasets (CC BY 4.0) | Herb-specific datasets available |
| Rosemary | DATASET_SEARCH_REQUIRED | 300+ | Herb datasets (CC BY 4.0) | Herb-specific datasets available |
| Thyme | DATASET_SEARCH_REQUIRED | 200+ | Herb datasets (CC BY 4.0) | Herb-specific datasets available |
| Oregano | DATASET_SEARCH_REQUIRED | 200+ | Herb datasets (CC BY 4.0) | Herb-specific datasets available |
| Sage | DATASET_SEARCH_REQUIRED | 200+ | Herb datasets (CC BY 4.0) | Herb-specific datasets available |
| Strawberry | TRAINABLE_NOW | 2,000+ | PlantVillage + Smartphone Veg | Good coverage |
| Blueberry | NEEDS_MORE_DATA | 800+ | PlantVillage + Smartphone Veg | Limited |
| Grape | NEEDS_MORE_DATA | 600+ | PlantVillage | Limited |
| Marigold | DATASET_SEARCH_REQUIRED | 200+ | images.cv plants | Need to verify license |
| Zinnia | DATASET_SEARCH_REQUIRED | 200+ | images.cv plants | Need to verify license |
| Nasturtium | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Sunflower | NEEDS_MORE_DATA | 500+ | PlantVillage + Sunflower Growth Stage | Limited |
| Cosmos | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Petunia | DATASET_SEARCH_REQUIRED | 200+ | images.cv plants | Need to verify license |
| Begonia | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Eggplant | TRAINABLE_NOW | 1,000+ | PlantVillage + Bangladesh Veg + Smartphone Veg | Good coverage |
| Okra | NEEDS_MORE_DATA | 600+ | Bangladesh Veg + Smartphone Veg | Limited |
| Asparagus | DATASET_SEARCH_REQUIRED | 200+ | Web images | Very limited |
| Rhubarb | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Celery | NEEDS_MORE_DATA | 400+ | Smartphone Veg | Limited |
| Leek | NEEDS_MORE_DATA | 300+ | Early Stage + Smartphone Veg | Limited |
| Fennel | DATASET_SEARCH_REQUIRED | 100+ | Herb datasets | Very limited |
| Artichoke | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |

### Weeds

| Class | Status | Est. Images | Primary Source | Notes |
|-------|--------|-------------|----------------|-------|
| Dandelion | NEEDS_MORE_DATA | 1,000+ | DeepWeeds (supplement) + UC IPM | Need NA-specific images |
| Crabgrass | NEEDS_MORE_DATA | 800+ | DeepWeeds (supplement) + UC IPM | Need NA-specific images |
| White_clover | NEEDS_MORE_DATA | 600+ | DeepWeeds (supplement) | Need NA-specific images |
| Purslane | NEEDS_MORE_DATA | 600+ | DeepWeeds (supplement) + UC IPM | Need NA-specific images |
| Lambsquarters | NEEDS_MORE_DATA | 600+ | DeepWeeds (supplement) + UC IPM | Need NA-specific images |
| Chickweed | NEEDS_MORE_DATA | 400+ | UC IPM | Limited |
| Pigweed | NEEDS_MORE_DATA | 800+ | DeepWeeds (supplement) + UC IPM | Need NA-specific images |
| Plantain | NEEDS_MORE_DATA | 400+ | UC IPM | Limited |
| Nutsedge | NEEDS_MORE_DATA | 400+ | UC IPM | Limited |
| Ragweed | NEEDS_MORE_DATA | 500+ | DeepWeeds (supplement) + UC IPM | Need NA-specific images |
| Bindweed | NEEDS_MORE_DATA | 300+ | UC IPM | Limited |
| Foxtail | NEEDS_MORE_DATA | 400+ | UC IPM | Limited |
| Thistle | NEEDS_MORE_DATA | 400+ | UC IPM | Limited |
| Poison_ivy | DATASET_SEARCH_REQUIRED | 200+ | Bugwood (requires approval) | Need alternative |
| Garlic_mustard | DATASET_SEARCH_REQUIRED | 100+ | UC IPM (partial) | Very limited |
| Knotweed | DATASET_SEARCH_REQUIRED | 100+ | UC IPM (partial) | Very limited |
| Ground_ivy | DATASET_SEARCH_REQUIRED | 100+ | UC IPM (partial) | Very limited |
| Woodsorrel | DATASET_SEARCH_REQUIRED | 100+ | UC IPM (partial) | Very limited |
| Johnsongrass | DATASET_SEARCH_REQUIRED | 100+ | UC IPM (partial) | Very limited |
| Quackgrass | DATASET_SEARCH_REQUIRED | 100+ | UC IPM (partial) | Very limited |
| Other_weed | TRAINABLE_NOW | 5,000+ | DeepWeeds Negative + UC IPM | Strong negative examples |

### Insects / Pests

| Class | Status | Est. Images | Primary Source | Notes |
|-------|--------|-------------|----------------|-------|
| Aphid | NEEDS_MORE_DATA | 1,000+ | BIOSCAN-5M + Roboflow | Curation required from 5M dataset |
| Japanese_beetle | DATASET_SEARCH_REQUIRED | 200+ | Bugwood (requires approval) | No bulk dataset |
| Colorado_potato_beetle | DATASET_SEARCH_REQUIRED | 200+ | Bugwood (requires approval) | No bulk dataset |
| Cucumber_beetle | DATASET_SEARCH_REQUIRED | 200+ | Bugwood (requires approval) | No bulk dataset |
| Cabbage_worm | DATASET_SEARCH_REQUIRED | 200+ | Bugwood (requires approval) | No bulk dataset |
| Tomato_hornworm | DATASET_SEARCH_REQUIRED | 200+ | Bugwood (requires approval) | No bulk dataset |
| Squash_bug | DATASET_SEARCH_REQUIRED | 200+ | Bugwood (requires approval) | No bulk dataset |
| Whitefly | NEEDS_MORE_DATA | 800+ | BIOSCAN-5M + Roboflow | Curation required |
| Spider_mite | NEEDS_MORE_DATA | 600+ | BIOSCAN-5M + Roboflow | Curation required |
| Thrips | NEEDS_MORE_DATA | 600+ | BIOSCAN-5M + Roboflow | Curation required |
| Leafminer | DATASET_SEARCH_REQUIRED | 300+ | Roboflow + web images | Very limited |
| Cutworm | DATASET_SEARCH_REQUIRED | 200+ | Bugwood (requires approval) | No bulk dataset |
| Stink_bug | DATASET_SEARCH_REQUIRED | 300+ | Bugwood (requires approval) | No bulk dataset |
| Flea_beetle | DATASET_SEARCH_REQUIRED | 200+ | Bugwood (requires approval) | No bulk dataset |
| Mexican_bean_beetle | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Corn_earworm | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Squash_vine_borer | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Blister_beetle | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Other_pest | TRAINABLE_NOW | 5,000+ | BIOSCAN-5M non-target | Strong negative examples |

### Beneficial Insects

| Class | Status | Est. Images | Primary Source | Notes |
|-------|--------|-------------|----------------|-------|
| Ladybug | NEEDS_MORE_DATA | 600+ | BIOSCAN-5M + UC IPM + Roboflow | Curation required |
| Green_lacewing | DATASET_SEARCH_REQUIRED | 200+ | BIOSCAN-5M + web images | Very limited |
| Honey_bee | NEEDS_MORE_DATA | 500+ | BIOSCAN-5M + UC IPM | Curation required |
| Hoverfly | DATASET_SEARCH_REQUIRED | 200+ | BIOSCAN-5M | Very limited |
| Praying_mantis | NEEDS_MORE_DATA | 400+ | BIOSCAN-5M + UC IPM | Curation required |
| Spider | NEEDS_MORE_DATA | 500+ | BIOSCAN-5M + UC IPM | Curation required |
| Earthworm | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |

### Diseases

| Class | Status | Est. Images | Primary Source | Notes |
|-------|--------|-------------|----------------|-------|
| Healthy | TRAINABLE_NOW | 15,000+ | PlantVillage + PlantDoc | Excellent coverage |
| Powdery_mildew | TRAINABLE_NOW | 4,000+ | PlantVillage + PlantDoc | Strong multi-crop coverage |
| Downy_mildew | NEEDS_MORE_DATA | 1,500+ | PlantVillage + PlantDoc | Limited |
| Early_blight | TRAINABLE_NOW | 2,000+ | PlantVillage + PlantDoc | Good tomato/potato coverage |
| Late_blight | TRAINABLE_NOW | 2,000+ | PlantVillage + PlantDoc | Good tomato/potato coverage |
| Septoria_leaf_spot | NEEDS_MORE_DATA | 1,000+ | PlantVillage + PlantDoc | Tomato-specific |
| Bacterial_spot | NEEDS_MORE_DATA | 1,000+ | PlantVillage + PlantDoc | Pepper/tomato |
| Fusarium_wilt | NEEDS_MORE_DATA | 1,500+ | PlantVillage | Multiple crops |
| Verticillium_wilt | NEEDS_MORE_DATA | 1,000+ | PlantVillage | Multiple crops |
| Anthracnose | NEEDS_MORE_DATA | 1,000+ | PlantVillage + PlantDoc | Multiple crops |
| Rust | NEEDS_MORE_DATA | 1,500+ | PlantVillage | Multiple crops |
| Leaf_spot | NEEDS_MORE_DATA | 1,500+ | PlantDoc + web images | Generic; may overlap with other classes |
| Blossom_end_rot | DATASET_SEARCH_REQUIRED | 300+ | PlantDoc (partial) + web images | Very limited |
| Nutrient_deficiency | DATASET_SEARCH_REQUIRED | 200+ | Web images | Very limited; hard to distinguish from disease |
| Sunscald | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Frost_damage | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Hail_damage | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Overwatering_stress | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Underwatering_stress | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Insect_damage | DATASET_SEARCH_REQUIRED | 200+ | IP102 (blocked) + web images | Hard to distinguish from disease |
| Chewing_damage | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Leaf_miner_damage | DATASET_SEARCH_REQUIRED | 100+ | Web images | Very limited |
| Apple_scab | NEEDS_MORE_DATA | 500+ | PlantVillage + PlantDoc | Limited |
| Cedar_apple_rust | NEEDS_MORE_DATA | 500+ | PlantVillage + PlantDoc | Limited |
| Grape_black_rot | NEEDS_MORE_DATA | 500+ | PlantVillage + PlantDoc | Limited |
| Peach_bacterial_spot | NEEDS_MORE_DATA | 300+ | PlantDoc | Limited |
| Soybean_rust | NEEDS_MORE_DATA | 300+ | PlantVillage | Limited |
| Squash_powdery_mildew | NEEDS_MORE_DATA | 500+ | PlantVillage | Limited |
| Tomato_mosaic_virus | NEEDS_MORE_DATA | 300+ | PlantDoc | Limited |
| Tomato_yellow_leaf_curl | NEEDS_MORE_DATA | 300+ | PlantDoc | Limited |

### Growth Stages

| Class | Status | Est. Images | Primary Source | Notes |
|-------|--------|-------------|----------------|-------|
| Seedling | NEEDS_MORE_DATA | 1,500+ | Early Stage Crops + Plant Growth Stage Detection | Limited seedling diversity |
| Vegetative | NEEDS_MORE_DATA | 2,000+ | Plant Growth Stage Detection + BDFlower | Adequate but thin |
| Flowering | NEEDS_MORE_DATA | 1,500+ | BDFlower + Plant Growth Stage Detection | Flower-specific bias |
| Fruiting | NEEDS_MORE_DATA | 1,500+ | Plant Growth Stage Detection + BDFlower | Adequate but thin |
| Mature_Harvest | NEEDS_MORE_DATA | 1,000+ | Plant Growth Stage Detection | Limited |
| Senescing | DATASET_SEARCH_REQUIRED | 200+ | Web images | Very limited |

---

## 13. Taxonomy Improvements for ML Practicality

### Problem Classes That May Need Refactoring

**"Nutrient_deficiency", "Overwatering_stress", "Underwatering_stress"**
- These are abiotic disorders that look very similar to each other and to diseases.
- Current datasets do not have enough labeled examples to distinguish them reliably.
- **Recommendation**: Either merge into a single "Abiotic_stress" class, or defer to v2 until sufficient data is curated.
- For MVP, treat as DATASET_SEARCH_REQUIRED and do not include in initial DiseaseClassifier.

**"Insect_damage", "Chewing_damage", "Leaf_miner_damage"**
- These are damage types, not pest identifications.
- A gardener asking "what is damaging my plant?" wants to know the pest, not just the damage pattern.
- Damage patterns are often indistinguishable between pests and appear similar to disease symptoms.
- **Recommendation**: Remove from DiseaseClassifier. Instead:
  - Train InsectClassifier to identify the pest directly.
  - If damage classification is needed, create a separate DamageClassifier trained on labeled damage images (requires new dataset).

**"Leaf_spot"**
- Extremely generic. PlantVillage maps multiple specific diseases to Leaf_spot (Tomato_leaf_mold, Tomato_target_spot).
- **Recommendation**: Keep as catch-all only if specific disease data is insufficient. Otherwise, prefer specific disease names.

**Growth stage per-crop vs. general growth stage**
- The current architecture uses a single GrowthStageClassifier for all crops.
- This is correct because growth stages look similar across species (seedling is seedling regardless of crop).
- **Recommendation**: Maintain single 6-class growth stage model. Do NOT create per-crop growth stages.

### Proposed Revised Disease Taxonomy for MVP

```
DiseaseClassifier v1 (trainable now):
  - Healthy
  - Powdery_mildew
  - Downy_mildew
  - Early_blight
  - Late_blight
  - Septoria_leaf_spot
  - Bacterial_spot
  - Fusarium_wilt
  - Verticillium_wilt
  - Anthracnose
  - Rust
  - Apple_scab
  - Cedar_apple_rust
  - Grape_black_rot
  - Peach_bacterial_spot
  - Soybean_rust
  - Squash_powdery_mildew
  - Tomato_mosaic_virus
  - Tomato_yellow_leaf_curl

DiseaseClassifier v2 (after additional data curation):
  + Blossom_end_rot
  + Leaf_spot (generic)
  + Nutrient_deficiency (if merged into Abiotic_stress)
  + Sunscald
  + Frost_damage
  + Hail_damage
  + Overwatering_stress
  + Underwatering_stress
  + Insect_damage
  + Chewing_damage
  + Leaf_miner_damage
```

### Proposed Revised Insect Taxonomy for MVP

```
InsectClassifier v1 (trainable after BIOSCAN-5M curation + Roboflow):
  - Aphid
  - Whitefly
  - Spider_mite
  - Thrips
  - Ladybug
  - Honey_bee
  - Praying_mantis
  - Spider
  - Other_pest
  - Other_beneficial

InsectClassifier v2 (after Bugwood approval + web curation):
  + Japanese_beetle
  + Colorado_potato_beetle
  + Cucumber_beetle
  + Cabbage_worm
  + Tomato_hornworm
  + Squash_bug
  + Leafminer
  + Cutworm
  + Stink_bug
  + Flea_beetle
  + Green_lacewing
  + Hoverfly
  + Earthworm
```

### Key Principle

**Do not train a classifier on a class unless you have ≥200 verified, labeled, license-compatible images.**
If a class cannot reach this threshold with currently available datasets, classify it as DEFERRED or DATASET_SEARCH_REQUIRED rather than manufacturing weak training data.
