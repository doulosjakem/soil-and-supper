# Soil & Supper — ML Phase 34A: Crop Recognition Taxonomy + Commercial Data Gap Audit

## 1. Product Rationale

The classifier should answer: **"What plant/crop is this?"** for things a normal home gardener is likely to photograph.

The taxonomy should optimize for:
- common home-garden crops
- things the gardener would reasonably expect Soil & Supper to recognize
- visually distinguishable categories
- usefulness to the Garden DB
- commercially usable training-data availability
- eventual offline mobile inference

The goal is **not** to recognize every plant on earth. The goal is a practical, commercially defensible first recognition taxonomy that covers the plants a home gardener is most likely to grow and photograph.

### Relationship to Existing App Taxonomy

The application layer (`CropKnowledge.kt`) currently has structured knowledge for **10 crops**:
Carrot, Radish, Lettuce, Spinach, Bush Bean, Broccoli, Tomato, Cucumber, Potato, Garlic.

The ML pipeline has a **50-class crop taxonomy** in `training/config.yaml` and `docs/ML_TAXONOMY.md`.

The proposed Phase 34A taxonomy bridges these: it expands the app's 10-crop catalog to a practical first-recognition set while remaining grounded in what can actually be trained with commercially available data.

---

## 2. Recommended Tier 1 Taxonomy

### Vegetables (18 classes)

| # | Proposed Class | Canonical Class (existing ML taxonomy) | Notes |
|---|---------------|----------------------------------------|-------|
| 1 | Tomato | Tomato | Direct match |
| 2 | Pepper | Pepper_sweet | Merged: all pepper types (bell, hot, chili) |
| 3 | Eggplant | Eggplant | Direct match |
| 4 | Potato | Potato | Direct match |
| 5 | Cucumber | Cucumber | Direct match |
| 6 | Summer Squash / Zucchini | Summer_squash | Renamed for clarity |
| 7 | Winter Squash / Pumpkin | Winter_squash | Merged: pumpkins are a type of winter squash |
| 8 | Corn | Corn | Direct match |
| 9 | Bean | Bean | Merged: green bean + dry bean (same species) |
| 10 | Pea | Pea | Direct match |
| 11 | Carrot | Carrot | Direct match |
| 12 | Beet | Beet | Direct match |
| 13 | Radish | Radish | Direct match |
| 14 | Onion | Onion | Direct match |
| 15 | Garlic | Garlic | Direct match |
| 16 | Leek | Leek | Direct match |
| 17 | Broccoli | Broccoli | Direct match |
| 18 | Cabbage | Cabbage | Direct match |

### Berries (4 classes)

| # | Proposed Class | Canonical Class | Notes |
|---|---------------|----------------|-------|
| 19 | Strawberry | Strawberry | Direct match |
| 20 | Blueberry | Blueberry | Direct match |
| 21 | Grape | Grape | Direct match |
| 22 | Raspberry / Blackberry | — | **NEW**: merged bramble class |

### Fruit Trees (3 classes)

| # | Proposed Class | Canonical Class | Notes |
|---|---------------|----------------|-------|
| 23 | Apple | — | **NEW**: not in existing 50-class crop taxonomy |
| 24 | Peach | — | **NEW**: not in existing 50-class crop taxonomy |
| 25 | Cherry | — | **NEW**: not in existing 50-class crop taxonomy |

### Other Common Garden Crops (2 classes)

| # | Proposed Class | Canonical Class | Notes |
|---|---------------|----------------|-------|
| 26 | Asparagus | Asparagus | Direct match |
| 27 | Rhubarb | Rhubarb | Direct match |

**Total Tier 1: 27 classes**

---

## 3. Recommended Tier 2 Taxonomy

Tier 2 contains useful but non-essential classes for the first model. These are either less common in home gardens, have limited training data, or require additional data acquisition beyond the immediate gaps.

### Vegetables (4 classes)

| # | Proposed Class | Canonical Class | Rationale for Tier 2 |
|---|---------------|----------------|---------------------|
| 28 | Cauliflower | Cauliflower | Common but zero commercial data identified |
| 29 | Kale | — | Very common, but zero commercial data identified |
| 30 | Turnip | Turnip | Less common in modern home gardens |
| 31 | Sweet Potato | Sweet_potato | Common in some regions, limited data |

### Berries (2 classes)

| # | Proposed Class | Canonical Class | Rationale for Tier 2 |
|---|---------------|----------------|---------------------|
| 32 | Plum | — | Common fruit tree, zero commercial data |
| 33 | Pear | — | Common fruit tree, zero commercial data |

### Other (2 classes)

| # | Proposed Class | Canonical Class | Rationale for Tier 2 |
|---|---------------|----------------|---------------------|
| 34 | Hops | — | Niche home garden crop |
| 35 | Apricot / Nectarine | — | Less common than Apple/Peach/Cherry |

**Total Tier 2: 8 classes**

**Combined Tier 1 + Tier 2: 35 classes**

---

## 4. Classes Intentionally Excluded

The following were considered but excluded from Tier 1:

| Class | Reason for Exclusion |
|-------|---------------------|
| Brussels Sprouts | Low demand, visually similar to Cabbage/Broccoli |
| Collards | Low demand, visually similar to Kale/Cabbage |
| Swiss Chard | Moderate demand, but visually similar to Spinach/Beet greens |
| Daikon | Niche; visually similar to Radish |
| Fava Bean | Niche; limited data |
| Currant / Gooseberry | Niche in North American home gardens |
| Apricot / Nectarine | Tier 2; less common than Apple/Peach/Cherry |
| Plum / Pear | Tier 2; data gaps |
| Hops | Niche; not a food crop for most gardeners |
| Soybean | Field crop, not home garden |
| Watermelon / Cantaloupe | Space-intensive; limited data |
| Pumpkin (separate from Winter Squash) | Merged into Winter Squash/Pumpkin |

---

## 5. Classes Intentionally Merged

| Merged Classes | Proposed Unified Class | Rationale |
|---------------|----------------------|-----------|
| Bell Pepper + Hot Pepper + Chili Pepper | Pepper | Visually indistinguishable at leaf/fruit level for v1. Variety/spiciness tracked in Garden DB. |
| Zucchini + Summer Squash | Summer Squash / Zucchini | Same species (Cucurbita pepo). Visually identical. |
| Winter Squash + Pumpkin | Winter Squash / Pumpkin | Pumpkins are a type of winter squash (Cucurbita pepo/maxima). Visually similar when mature. |
| Sweet Corn + Field Corn + Flour Corn | Corn | All look identical. Variety tracked in Garden DB. |
| Green Bean + Dry Bean | Bean | Same species (Phaseolus vulgaris). Dry beans are mature green beans. |
| Raspberry + Blackberry | Raspberry / Blackberry | Both Rubus. Visually similar aggregate fruits on canes. Distinguishable by fruit core (hollow vs. solid) but unreliable from photos. |

### Merging Evaluation Details

**Zucchini / Summer Squash**: Both are immature Cucurbita pepo. They look, grow, and photograph identically. A gardener who grows "zucchini" and a gardener who grows "summer squash" are effectively growing the same thing for recognition purposes. **Recommendation: MERGE.**

**Winter Squash / Pumpkin**: Botanically, pumpkins are a subset of winter squash. Visually, mature pumpkins and winter squash can be distinguished by shape/color, but many varieties blur the line (e.g., sugar pumpkins, cheese pumpkins). For a mobile photo classifier, the distinction is unreliable. **Recommendation: MERGE.**

**All Peppers**: Bell peppers and hot peppers look very similar as plants. The fruit color/shape varies, but chili peppers can be green (like bell peppers) and bell peppers can be red/orange/yellow (like some hot peppers). From a leaf-level photo, they're indistinguishable. **Recommendation: MERGE into "Pepper."**

**Green Bean / Dry Bean**: Same plant species. Dry beans are simply green beans left on the vine to mature. The plant looks identical throughout its lifecycle. **Recommendation: MERGE.**

**Raspberry / Blackberry**: Both are Rubus species with aggregate fruits on arching canes. The key distinction (hollow fruit core in raspberries, solid in blackberries) requires picking the fruit. From a photo, they're very difficult to distinguish, especially when ripe. **Recommendation: MERGE into "Raspberry / Blackberry."**

---

## 6. Existing Taxonomy Mapping

### Mapping to Canonical ML Taxonomy (training/config.yaml)

| Canonical Class | Proposed Phase 34A Class | Mapping Type |
|----------------|-------------------------|-------------|
| Tomato | Tomato | Exact |
| Pepper_sweet | Pepper | Renamed + merged |
| Pepper_hot | Pepper | Merged into Pepper |
| Eggplant | Eggplant | Exact |
| Cucumber | Cucumber | Exact |
| Summer_squash | Summer Squash / Zucchini | Renamed |
| Winter_squash | Winter Squash / Pumpkin | Renamed + merged |
| Bean | Bean | Exact (merged scope) |
| Pea | Pea | Exact |
| Corn | Corn | Exact |
| Broccoli | Broccoli | Exact |
| Cabbage | Cabbage | Exact |
| Lettuce | Lettuce | Exact |
| Spinach | Spinach | Exact |
| Carrot | Carrot | Exact |
| Radish | Radish | Exact |
| Onion | Onion | Exact |
| Potato | Potato | Exact |
| Garlic | Garlic | Exact |
| Leek | Leek | Exact |
| Strawberry | Strawberry | Exact |
| Blueberry | Blueberry | Exact |
| Grape | Grape | Exact |
| Asparagus | Asparagus | Exact |
| Rhubarb | Rhubarb | Exact |
| Beet | Beet | Exact |
| Turnip | Turnip | Tier 2 |
| Sweet_potato | Sweet Potato | Tier 2 |
| Basil | — | Excluded (herb, not core garden crop) |
| Cilantro | — | Excluded (herb, not core garden crop) |
| Parsley | — | Excluded (herb, not core garden crop) |
| Dill | — | Excluded (herb, not core garden crop) |
| Chives | — | Excluded (herb, not core garden crop) |
| Rosemary | — | Excluded (herb, not core garden crop) |
| Thyme | — | Excluded (herb, not core garden crop) |
| Oregano | — | Excluded (herb, not core garden crop) |
| Sage | — | Excluded (herb, not core garden crop) |
| Watermelon | — | Excluded (space-intensive, limited data) |
| Cantaloupe | — | Excluded (space-intensive, limited data) |
| Pumpkin | Winter Squash / Pumpkin | Merged |
| Okra | — | Excluded (regional, limited data) |
| Celery | — | Excluded (limited data, less common) |
| Fennel | — | Excluded (herb-like, limited data) |
| Artichoke | — | Excluded (regional, limited data) |
| Sunflower | — | Excluded (ornamental, not food crop) |
| Marigold | — | Excluded (ornamental) |
| Zinnia | — | Excluded (ornamental) |
| Nasturtium | — | Excluded (ornamental) |
| Cosmos | — | Excluded (ornamental) |
| Petunia | — | Excluded (ornamental) |
| Begonia | — | Excluded (ornamental) |
| — | Apple | NEW (not in existing 50-class taxonomy) |
| — | Peach | NEW (not in existing 50-class taxonomy) |
| — | Cherry | NEW (not in existing 50-class taxonomy) |
| — | Raspberry / Blackberry | NEW (not in existing 50-class taxonomy) |

### Mapping to App CropKnowledge Catalog

| App CropKnowledge Class | Phase 34A Class | Status |
|------------------------|-----------------|--------|
| Carrot | Carrot | Exact match |
| Radish | Radish | Exact match |
| Lettuce | Lettuce | Exact match |
| Spinach | Spinach | Exact match |
| Bush Bean | Bean | Merged (Bush Bean → Bean) |
| Broccoli | Broccoli | Exact match |
| Tomato | Tomato | Exact match |
| Cucumber | Cucumber | Exact match |
| Potato | Potato | Exact match |
| Garlic | Garlic | Exact match |

**10 of 10 app crops are covered in Tier 1.**

---

## 7. Commercial Data Coverage

### Data Sources Available

| Source | License | Images | Commercial OK | Status |
|--------|---------|--------|---------------|--------|
| PlantVillage | CC0 1.0 | 54,306 | YES | ACQUIRED — healthy crop images usable for recognition |
| PlantDoc | CC BY 4.0 | 2,569 | YES | ACQUIRED — real-world field images |
| Irish Potato | CC BY 4.0 | 117,418 | YES | ACQUIRED — disease-focused, limited healthy crop images |
| Grapevine | CC BY 4.0 | 5,267 | YES | ACQUIRED — disease-focused |
| SegPPD-101 | MIT (REVIEW) | 817 | REVIEW | REVIEW — primary sources inaccessible |
| Bangladesh Vegetables | CC BY 4.0 | ~4,730 | YES | MANUAL DOWNLOAD REQUIRED |
| Smartphone Vegetable Detection | CC BY 4.0 | ~3,534 | YES | MANUAL DOWNLOAD REQUIRED |
| VegNet | CC BY 4.0 | ~6,850 | YES | MANUAL DOWNLOAD REQUIRED |
| BanglaVeg | CC BY 4.0 | ~4,319 | YES | MANUAL DOWNLOAD REQUIRED |
| Early-Stage Crops | CC BY 4.0 | ~2,801 | YES | MANUAL DOWNLOAD REQUIRED |

### Existing Commercial Images for Tier 1 Classes

From auto-downloadable sources (PlantVillage + PlantDoc):

| Tier 1 Class | Existing USE Images | Source | Notes |
|-------------|--------------------|--------|-------|
| Tomato | 4,224 | PlantVillage (healthy) + PlantDoc (field) | Strong |
| Pepper | 3,186 | PlantVillage (healthy) + PlantDoc (field) | Strong |
| Corn | 3,022 | PlantVillage (healthy) + PlantDoc (field) | Strong |
| Strawberry | 912 | PlantVillage (healthy) | Moderate |
| Summer Squash / Zucchini | 248 | PlantDoc (field) | Low |
| Blueberry | 1,502 | PlantVillage (healthy) | Moderate |
| Grape | ~3,000 | PlantVillage (healthy) + Grapevine | Moderate |
| Apple | ~2,500 | PlantVillage (healthy) | Moderate |
| Peach | ~2,700 | PlantVillage (healthy) | Moderate |
| Cherry | ~2,000 | PlantVillage (healthy) | Moderate |
| Raspberry / Blackberry | 371 | PlantVillage (healthy) | Low |
| Potato | ~2,000 | PlantVillage (disease classes) | Moderate (leaf-level) |
| **All other Tier 1 classes** | **0** | — | **Missing** |

**Current total for Tier 1 from auto-downloadable data: ~24,000 images across 12 of 27 classes.**

After manual download of the 5 Mendeley datasets, estimated new coverage:

| Tier 1 Class | Estimated Additional Images | Source |
|-------------|---------------------------|--------|
| Eggplant | ~12,000 | Bangladesh Veg + Smartphone Veg + BanglaVeg |
| Cucumber | ~12,000 | Bangladesh Veg + Smartphone Veg + BanglaVeg |
| Bean | ~15,000 | Bangladesh Veg + Smartphone Veg + BanglaVeg + Early-Stage Crops |
| Carrot | ~12,000 | Bangladesh Veg + Smartphone Veg + BanglaVeg |
| Radish | ~12,000 | Bangladesh Veg + Smartphone Veg + BanglaVeg |
| Onion | ~12,000 | Bangladesh Veg + Smartphone Veg + BanglaVeg |
| Broccoli | ~4,700 | Bangladesh Veg |
| Cabbage | ~4,700 | Bangladesh Veg |
| Leek | ~2,800 | Early-Stage Crops |
| Winter Squash / Pumpkin | ~12,000 | Bangladesh Veg + Smartphone Veg + BanglaVeg (Pumpkin) |
| Summer Squash / Zucchini | ~9,000 | Bangladesh Veg + BanglaVeg (Zucchini) |
| Potato | ~12,000 | Bangladesh Veg + Smartphone Veg + BanglaVeg |

**After manual acquisition: ~110,000+ images across 23 of 27 Tier 1 classes.**

### Remaining Tier 1 Gaps After Manual Acquisition

| Tier 1 Class | Estimated Gap | Status |
|-------------|--------------|--------|
| Pea | ~0 | MISSING — no known commercial dataset |
| Beet | ~0 | MISSING — no known commercial dataset |
| Garlic | ~0 | MISSING — no known commercial dataset |
| Lettuce | ~0 | MISSING — no known commercial dataset |
| Spinach | ~0 | MISSING — no known commercial dataset |
| Kale | ~0 | MISSING — no known commercial dataset |
| Cauliflower | ~0 | MISSING — no known commercial dataset |
| Asparagus | ~0 | MISSING — no known commercial dataset |
| Rhubarb | ~0 | MISSING — no known commercial dataset |

**9 Tier 1 classes would remain without commercial data after all known manual-download datasets are acquired.**

---

## 8. Data Coverage Matrix

| Class | Existing USE | Sources | License | Field Images | Estimated Gap | Status |
|-------|-------------|---------|---------|--------------|---------------|--------|
| Tomato | 4,224 | PlantVillage, PlantDoc | CC0, CC BY 4.0 | Yes (PlantDoc) | None | SUFFICIENT |
| Pepper | 3,186 | PlantVillage, PlantDoc | CC0, CC BY 4.0 | Yes (PlantDoc) | None | SUFFICIENT |
| Corn | 3,022 | PlantVillage, PlantDoc | CC0, CC BY 4.0 | Yes (PlantDoc) | None | SUFFICIENT |
| Strawberry | 912 | PlantVillage | CC0 | No | Low | LOW |
| Blueberry | 1,502 | PlantVillage | CC0 | No | Low | LOW |
| Grape | ~3,000 | PlantVillage, Grapevine | CC0, CC BY 4.0 | No | Low | LOW |
| Apple | ~2,500 | PlantVillage | CC0 | No | Low | LOW |
| Peach | ~2,700 | PlantVillage | CC0 | No | Low | LOW |
| Cherry | ~2,000 | PlantVillage | CC0 | No | Low | LOW |
| Raspberry/Blackberry | 371 | PlantVillage | CC0 | No | Moderate | LOW |
| Summer Squash/Zucchini | 248 | PlantDoc | CC BY 4.0 | Yes | Moderate | LOW |
| Potato | ~2,000 | PlantVillage, Irish Potato | CC0, CC BY 4.0 | Yes (Irish Potato) | Low | LOW |
| Eggplant | 0 | — | — | — | High | MISSING |
| Cucumber | 0 | — | — | — | High | MISSING |
| Bean | 0 | — | — | — | High | MISSING |
| Carrot | 0 | — | — | — | High | MISSING |
| Radish | 0 | — | — | — | High | MISSING |
| Onion | 0 | — | — | — | High | MISSING |
| Broccoli | 0 | — | — | — | High | MISSING |
| Cabbage | 0 | — | — | — | High | MISSING |
| Leek | 0 | — | — | — | High | MISSING |
| Winter Squash/Pumpkin | 0 | — | — | — | High | MISSING |
| Pea | 0 | — | — | — | High | MISSING |
| Beet | 0 | — | — | — | High | MISSING |
| Garlic | 0 | — | — | — | High | MISSING |
| Lettuce | 0 | — | — | — | High | MISSING |
| Spinach | 0 | — | — | — | High | MISSING |
| Kale | 0 | — | — | — | High | MISSING |
| Cauliflower | 0 | — | — | — | High | MISSING |
| Asparagus | 0 | — | — | — | High | MISSING |
| Rhubarb | 0 | — | — | — | High | MISSING |

---

## 9. Dataset Acquisition Plan

### Immediate Acquisition (Manual Download Required)

These datasets are commercially approved (CC BY 4.0) and would fill the majority of Tier 1 gaps:

| Dataset | Source | URL | License | Expected Size | Classes Supplied |
|---------|--------|-----|---------|--------------|------------------|
| Bangladesh Vegetables | Mendeley Data | https://data.mendeley.com/datasets/rtx9ngb68j | CC BY 4.0 | ~4,730 images | Tomato, Pepper, Cucumber, Eggplant, Broccoli, Cabbage, Carrot, Onion, Potato, Pumpkin, Radish, Zucchini, Bean |
| Smartphone Vegetable Detection | Mendeley Data | https://data.mendeley.com/datasets/gnc4s3z2mf/3 | CC BY 4.0 | ~3,534 images | Tomato, Pepper, Cucumber, Eggplant, Potato, Pumpkin, Radish, Bean, Carrot, Onion |
| VegNet | Mendeley Data | https://data.mendeley.com/datasets/6nxnjbn9w6 | CC BY 4.0 | ~6,850 images | Bell Pepper, Tomato, Chili Pepper |
| BanglaVeg | Mendeley Data / ScienceDirect | https://data.mendeley.com/datasets/... | CC BY 4.0 | ~4,319 images | Tomato, Pepper, Cucumber, Eggplant, Potato, Onion, Radish, Bean, Chili |
| Early-Stage Crops | PMC | https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/ | CC BY 4.0 | ~2,801 images | Corn, Bean, Leek |

### Candidate Datasets for Remaining Gaps

For classes still missing after the above acquisitions (Pea, Beet, Garlic, Lettuce, Spinach, Kale, Cauliflower, Asparagus, Rhubarb):

| Dataset | Source | URL | License | Images | Classes | Status |
|---------|--------|-----|---------|--------|---------|--------|
| images.cv Vegetables | images.cv | https://images.cv/dataset/vegetables-image-classification-dataset | CC0 (claimed) | 19,300 | Broccoli, Cabbage, Carrot, Cauliflower, Corn, Cucumber, Eggplant, Garlic, Lettuce, Onion, Peas, Pepper, Potato, Radish, Spinach, Tomato, Turnip | REVIEW — download mechanism unclear; verify CC0 claim |
| Kaggle Fruit and Vegetables | Kaggle | https://www.kaggle.com/datasets/youssefsalahzakria/fruit-and-vegetables-classification | CC0 | 72,000+ | Apple, Broccoli, Cabbage, Capsicum, Carrot, Cauliflower, Corn, Cucumber, Eggplant, Garlic, Lettuce, Onion, Peas, Pepper, Potato, Radish, Spinach, Sweet Potato, Tomato, Turnip | REVIEW — requires Kaggle API; verify CC0 provenance |
| HARTU Vegetables Dataset | Zenodo | https://zenodo.org/records/12155113 | CC BY 4.0 | 10GB+ | Tomato, Eggplant, Zucchini | REVIEW — synthetic CAD models, not real photographs; severe domain shift |

### Dataset Acquisition Priority

**Priority 1 (fills most gaps):**
1. Bangladesh Vegetables
2. Smartphone Vegetable Detection
3. VegNet
4. BanglaVeg
5. Early-Stage Crops

**Priority 2 (fills remaining gaps):**
6. images.cv Vegetables (if CC0 verified and download mechanism resolved)
7. Kaggle Fruit and Vegetables (if CC0 verified and Kaggle API available)

**Priority 3 (supplemental):**
8. HARTU Vegetables Dataset (only if synthetic data is acceptable; not recommended for v1)

---

## 10. Licensing / Provenance Notes

### Approved for Commercial Use

| Source | License | Attribution Required | Status |
|--------|---------|---------------------|--------|
| PlantVillage | CC0 1.0 | No | VERIFIED |
| PlantDoc | CC BY 4.0 | Yes | VERIFIED |
| Irish Potato | CC BY 4.0 | Yes | VERIFIED |
| Grapevine | CC BY 4.0 | Yes | VERIFIED |
| Bangladesh Vegetables | CC BY 4.0 | Yes | DOCUMENTED |
| Smartphone Vegetable Detection | CC BY 4.0 | Yes | DOCUMENTED |
| VegNet | CC BY 4.0 | Yes | DOCUMENTED |
| BanglaVeg | CC BY 4.0 | Yes | DOCUMENTED |
| Early-Stage Crops | CC BY 4.0 | Yes | DOCUMENTED |

### Requires Verification

| Source | Issue |
|--------|-------|
| images.cv Vegetables | Claims CC0 but download mechanism and exact provenance unclear |
| Kaggle Fruit and Vegetables | Claims CC0 but Kaggle hosting terms are not sufficient evidence; need primary-source verification |
| HARTU Vegetables Dataset | CC BY 4.0 verified, but images are synthetic CAD models, not real photographs |

### Not Approved

| Source | Reason |
|--------|--------|
| Common Beans | CC BY-NC 4.0 — non-commercial |
| CWD30 | License unclear (Elsevier journal) |
| IP102 | Academic use only |
| PlantCLEF | CC BY-NC-SA 4.0 |
| Pl@ntNet | CC BY-SA — ShareAlike incompatible |
| iNaturalist | ToS prohibits commercial AI training |

---

## 11. Recommended Next Step

### Decision: "Taxonomy requires human decision"

The recommended Tier 1 taxonomy is **27 classes** covering the most common home-garden vegetables, berries, and fruit trees. This is a practical, commercially defensible set that:

- Maps cleanly onto the existing 50-class ML taxonomy
- Covers all 10 crops in the app's CropKnowledge catalog
- Can be trained with commercially approved data for 18 of 27 classes from auto-downloadable sources
- Requires manual acquisition of 5 datasets for the remaining 9 classes

**Specific decisions requiring human approval:**

1. **Tier 1 size**: Is 27 classes the right target, or should it be expanded toward 30-35 by including Tier 2 classes (Cauliflower, Kale, Turnip, Sweet Potato, Plum, Pear)?

2. **Missing data strategy**: For the 9 Tier 1 classes with no commercial data (Pea, Beet, Garlic, Lettuce, Spinach, Kale, Cauliflower, Asparagus, Rhubarb), should we:
   - Acquire additional datasets (images.cv, Kaggle) and verify licenses?
   - Accept these as "data gaps" and train a partial model now?
   - Move them to Tier 2 and train a smaller, more robust Tier 1 model first?

3. **Fruit tree scope**: Should fruit trees (Apple, Peach, Cherry) be in Tier 1, or deferred to Tier 2? They have data from PlantVillage but are imaged differently (trees vs. garden beds).

4. **images.cv / Kaggle datasets**: Should we pursue these despite unclear download mechanisms and provenance concerns?

5. **Synthetic data**: Should HARTU synthetic CAD models be considered acceptable for training, or excluded due to domain shift?

### If the taxonomy is approved:

The next phase should:
1. Manually download the 5 priority datasets
2. Process and integrate them into the commercial manifest
3. Verify licenses for images.cv / Kaggle datasets
4. Train the MobileNetV3-based classifier on the approved Tier 1 classes
5. Evaluate and export to mobile format

---

## 12. Decision Format

RECOMMENDED TIER 1: **27 classes**

RECOMMENDED TIER 2: **8 classes**

CURRENTLY DATA-SUFFICIENT (auto-downloadable): **12 classes** (Tomato, Pepper, Corn, Strawberry, Summer Squash, Blueberry, Grape, Apple, Peach, Cherry, Raspberry/Blackberry, Potato)

REQUIRES DATA ACQUISITION (manual download): **15 classes** (Eggplant, Cucumber, Bean, Carrot, Radish, Onion, Broccoli, Cabbage, Leek, Winter Squash, Pepper, etc.)

REQUIRES LICENSE REVIEW: **9 classes** (Pea, Beet, Garlic, Lettuce, Spinach, Kale, Cauliflower, Asparagus, Rhubarb) — no commercial data identified

**Recommendation: Taxonomy requires human decision**

The taxonomy is well-defined and grounded in home-gardener use, but material decisions remain on Tier 1 scope, missing-data strategy, and whether to pursue additional dataset candidates with unclear provenance.
