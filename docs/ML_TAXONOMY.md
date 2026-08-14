# Soil & Supper — ML Taxonomy (Revised)

## 1. Recommended Recognition Architecture

### Constraint Analysis
- Target: Android-first, offline, TensorFlow Lite
- Hardware: NVIDIA GTX 1060 6GB, 24GB RAM
- Must be mobile-friendly: small model size, fast inference
- Must be extensible: add new categories over time without retraining everything

### Chosen Architecture: **Specialized Single-Classifier per Domain**

Do NOT build one enormous flat classifier covering crops + weeds + insects + diseases.

Instead, use **separate lightweight TFLite classifiers** for each domain:

```
Stage 1 (UI routing): User selects what they are photographing
  OR
Stage 1 (automatic): A tiny "domain router" classifier predicts:
  - Crop / Weed / Insect / Disease / GrowthStage / Unknown

Stage 2 (domain classifier): Run the appropriate specialized model
  - CropClassifier: 50 crop classes + Unknown
  - WeedClassifier: 25 weed classes + Unknown  
  - InsectClassifier: 20 pest/beneficial classes + Unknown
  - DiseaseClassifier: 30 disease/problem classes + Unknown
  - GrowthStageClassifier: 6 growth stages (separate attribute)
```

**Why this approach:**
1. Each model stays small and trainable on GTX 1060
2. Poor data in one domain does not degrade another
3. Easy to update one domain without touching others
4. Matches how gardeners think: "Is this a weed? Is this a pest?"
5. Each model can be optimized independently
6. TFLite Model Maker supports this workflow natively

**Why NOT hierarchical:**
- Adds complexity without proven benefit for this use case
- Error propagation between stages
- Harder to debug and iterate
- Mobile inference time increases

**Why NOT single flat classifier:**
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
- Add 2–4 explicit "negative" classes per domain where licensing permits (e.g., "Other Weed", "Non-target Insect", "Healthy Leaf" for disease)
- UI should encourage multiple photos (leaf + fruit + whole plant) when confidence is low

**Rationale**: Unknown classes trained on random images degrade known-class performance. Confidence thresholding is simpler, more honest, and easier to tune.

### Growth Stage Strategy
**Do NOT create separate classes like `Tomato_Seedling`, `Tomato_Flowering`.**

Instead:
- Train a **single GrowthStageClassifier** with 6 classes: Seedling, Vegetative, Flowering, Fruiting, Mature/Harvest, Senescing
- This model predicts the growth stage regardless of crop type
- The Android app runs this alongside the crop classifier when the user selects "Check growth stage"
- This requires a dataset with multiple crop types at multiple stages (see CWD30, Plant Growth Stage Detection)

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

| # | Class | Target Crops | Priority | Est. Images | Source |
|---|-------|-------------|----------|-------------|--------|
| 1 | Healthy | All crops | Critical | 15,000+ | PlantVillage, PlantDoc |
| 2 | Powdery_mildew | Many crops | High | 4,000+ | PlantVillage, PlantDoc |
| 3 | Downy_mildew | Many crops | Medium | 2,000+ | PlantDoc |
| 4 | Early_blight | Tomato, Potato | High | 2,000+ | PlantVillage, PlantDoc |
| 5 | Late_blight | Tomato, Potato | High | 2,000+ | PlantVillage, PlantDoc |
| 6 | Septoria_leaf_spot | Tomato | Medium | 1,000+ | PlantDoc |
| 7 | Bacterial_spot | Pepper, Tomato | Medium | 1,000+ | PlantVillage |
| 8 | Fusarium_wilt | Many crops | Medium | 1,500+ | PlantVillage |
| 9 | Verticillium_wilt | Many crops | Medium | 1,000+ | PlantVillage |
| 10 | Anthracnose | Many crops | Medium | 1,000+ | PlantVillage |
| 11 | Rust | Many crops | Medium | 1,500+ | PlantVillage |
| 12 | Leaf_spot | Many crops | Medium | 1,500+ | PlantDoc |
| 13 | Blossom_end_rot | Tomato, Pepper | Medium | 500+ | PlantDoc, web images |
| 14 | Nutrient_deficiency | General | Low | 500+ | Web images, extension services |
| 15 | Sunscald | Tomato, Pepper | Low | 300+ | Web images |
| 16 | Frost_damage | General | Low | 300+ | Web images |
| 17 | Hail_damage | General | Low | 200+ | Web images |
| 18 | Overwatering_stress | General | Low | 300+ | Web images |
| 19 | Underwatering_stress | General | Low | 300+ | Web images |
| 20 | Insect_damage | General | Low | 500+ | IP102, Bugwood |
| 21 | Chewing_damage | General | Low | 400+ | Bugwood |
| 22 | Leaf_miner_damage | General | Low | 300+ | Bugwood |
| 23 | Apple_scab | Apple | Low | 500+ | PlantVillage |
| 24 | Cedar_apple_rust | Apple | Low | 500+ | PlantVillage |
| 25 | Grape_black_rot | Grape | Low | 500+ | PlantDoc |
| 26 | Peach_bacterial_spot | Peach | Low | 300+ | PlantDoc |
| 27 | Soybean_rust | Soybean | Low | 300+ | PlantVillage |
| 28 | Squash_powdery_mildew | Squash | Low | 500+ | PlantVillage |
| 29 | Tomato_mosaic_virus | Tomato | Low | 300+ | PlantDoc |
| 30 | Tomato_yellow_leaf_curl | Tomato | Low | 300+ | PlantDoc |

**Primary source**: PlantVillage (CC0 1.0) — 54,306 images, 38 classes covering 14 crop species with healthy + disease combinations. This is the single most important disease dataset.

**Supplement**: PlantDoc (CC BY 4.0) — 2,569 images, 29 classes, real-world field images with natural backgrounds. Complements PlantVillage's controlled-background images.

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
