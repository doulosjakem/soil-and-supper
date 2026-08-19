# Soil & Supper — ML Phase 34B: Broad Garden Recognition Taxonomy + Commercial Data Acquisition Plan

## 0. Human Decisions Required

### QUESTION 1: Tier 1 Size Target
**QUESTION:** Is 50 classes the right target for Tier 1, or should it be expanded toward 60-70?

**OPTIONS:**
- A) 50 classes (recommended) — covers all common vegetables, berries, fruit trees, and herbs with a clear data path
- B) 60+ classes — adds more brassicas (Kale, Brussels Sprouts, Kohlrabi, Collards), more roots (Parsnip, Daikon, Fava Bean), more berries (Currant, Gooseberry), and more herbs

**RECOMMENDATION:** A) 50 classes. Adding more brassica and root classes provides diminishing visual-distinguishability returns while multiplying data-acquisition work. The 50-class set covers the plants a normal home gardener is most likely to grow.

**CONSEQUENCE IF WE CHOOSE DIFFERENTLY:** Expanding to 60+ would require additional dataset searches for classes like Parsnip, Daikon, Fava Bean, Currant, and Gooseberry — none of which have known commercial datasets. It would delay training without meaningful product coverage gain.

---

### QUESTION 2: Fruit Tree Scope
**QUESTION:** Should fruit trees (Apple, Pear, Peach, Cherry, Plum, Apricot, Nectarine) be in Tier 1?

**OPTIONS:**
- A) Include all 7 fruit trees in Tier 1 (recommended) — fruit trees are common in home gardens and PlantVillage provides baseline data
- B) Include only Apple, Peach, Cherry (3 trees with PlantVillage data) and defer Pear, Plum, Apricot, Nectarine to Tier 2
- C) Defer all fruit trees to Tier 2 — different imaging context (trees vs. garden beds)

**RECOMMENDATION:** A) Include all 7. The classifier should answer "What plant is this?" regardless of whether it's a bush or a tree. Fruit trees are first-class garden plants. Data gaps for Pear/Plum/Apricot/Nectarine can be filled with targeted acquisition.

**CONSEQUENCE IF WE CHOOSE DIFFERENTLY:** Excluding fruit trees would mean a gardener with an apple or peach tree gets no recognition help — a material product gap for a gardening app.

---

### QUESTION 3: Herb Scope
**QUESTION:** Should common culinary herbs (Basil, Cilantro, Parsley, Dill, Chives, Mint, Rosemary, Thyme, Oregano, Sage) be in Tier 1?

**OPTIONS:**
- A) Include all 10 herbs in Tier 1 (recommended) — herbs are among the most common garden plants
- B) Include only Basil, Cilantro, Parsley, Rosemary, Mint (5 herbs) and defer the rest
- C) Defer all herbs to Tier 2 — limited commercial datasets

**RECOMMENDATION:** A) Include all 10. Herbs are extremely common in home gardens. While commercial datasets are limited, the classes are visually distinct enough that even moderate training data would yield usable recognition.

**CONSEQUENCE IF WE CHOOSE DIFFERENTLY:** Excluding herbs would leave a major gap in garden coverage. A gardener growing basil or rosemary would get no recognition help.

---

### QUESTION 4: Missing-Data Strategy
**QUESTION:** For classes with no known commercial dataset after known acquisitions (~5-8 classes), should we:

**OPTIONS:**
- A) Accept as "data gaps" and train a partial model now (recommended) — the model can still be useful for the 40+ classes with data
- B) Search for additional datasets (images.cv, Kaggle) and verify licenses before any training
- C) Move gap classes to Tier 2 and train only on data-sufficient classes first

**RECOMMENDATION:** A) Train on the 40+ classes with verified or acquirable data. Do not block the entire model on 5-8 gap classes. Gap classes can be added in a subsequent model update once data is found.

**CONSEQUENCE IF WE CHOOSE DIFFERENTLY:** Blocking on gap classes would delay the first model indefinitely. A partial model covering 80% of common garden plants is more useful than no model.

---

### QUESTION 5: images.cv / Kaggle Dataset Pursuit
**QUESTION:** Should we pursue images.cv Vegetables (19,300 images, CC0 claimed) and Kaggle Fruit and Vegetables (72,000+, CC0 claimed) despite unclear download mechanisms and provenance?

**OPTIONS:**
- A) Pursue both — attempt to verify CC0 claims and download; if verified, they fill most remaining gaps
- B) Pursue only images.cv — smaller, more manageable, covers key gap classes
- C) Do not pursue — only use datasets with already-verified licenses

**RECOMMENDATION:** A) Pursue both. The potential coverage is too valuable to ignore. Mark as REVIEW until CC0 is verified from primary sources.

**CONSEQUENCE IF WE CHOOSE DIFFERENTLY:** Without these datasets, 15-20 Tier 1 classes would remain data-gaps, reducing the model's practical usefulness significantly.

---

## 1. Product Rationale

The classifier should answer: **"What plant/crop is this?"** for things a normal home gardener is likely to photograph.

The taxonomy should optimize for:
- common home-garden crops (vegetables, berries, fruit trees, herbs)
- things the gardener would reasonably expect Soil & Supper to recognize
- visually distinguishable categories
- usefulness to the Garden DB
- commercially usable training-data availability
- eventual offline mobile inference

### Relationship to Existing App Taxonomy

The application layer (`CropKnowledge.kt`) currently has structured knowledge for **10 crops**:
Carrot, Radish, Lettuce, Spinach, Bush Bean, Broccoli, Tomato, Cucumber, Potato, Garlic.

The ML pipeline has a **50-class crop taxonomy** in `training/config.yaml` and `docs/ML_TAXONOMY.md`.

The proposed Phase 34B taxonomy expands both to cover the full range of common home-garden plants while remaining grounded in what can actually be trained with commercially available data.

---

## 1.5 Exact Class Count Verification

### Programmatic Count

| Tier | Documented Count | Actually Listed | Discrepancy |
|------|-----------------|-----------------|-------------|
| Tier 1 | 51 | 51 | None |
| Tier 2 | 12 | 12 | None |
| Deferred | 7 | 7 | None |

### Tier 1 Breakdown

| Section | Listed Classes | Count |
|---------|---------------|-------|
| Vegetables | Tomato, Pepper, Eggplant, Potato, Cucumber, Summer Squash/Zucchini, Winter Squash/Pumpkin, Corn, Bean, Pea, Carrot, Beet, Radish, Turnip, Onion, Garlic, Leek, Broccoli, Cabbage, Cauliflower, Brussels Sprouts, Kale, Lettuce, Spinach, Swiss Chard, Sweet Potato, Watermelon, Cantaloupe | 28 |
| Berries | Strawberry, Raspberry/Blackberry, Blueberry, Grape | 4 |
| Fruit Trees | Apple, Pear, Peach, Cherry, Plum, Apricot, Nectarine | 7 |
| Herbs | Basil, Cilantro, Parsley, Dill, Chives, Mint, Rosemary, Thyme | 8 |
| Other | Asparagus, Rhubarb, Hops, Sunflower | 4 |
| **Total** | | **51** |

### Noted Discrepancies

1. **Herbs section header** originally stated "7 classes" while listing 8 classes. Corrected to "8 classes."
2. **Oregano and Sage** appear in the existing taxonomy mapping table as Tier 1 "Exact" mappings, and in the Deferred section as "Moved to Tier 1," but are **not listed in the Tier 1 taxonomy tables.** This is a documentation inconsistency. The mapping table intent is that they belong in Tier 1, but the authoritative class count of 51 does not include them.
3. **Recommendation:** Resolve Oregano/Sage placement before finalizing the taxonomy. Either add them to the Tier 1 tables (bringing the count to 53) or move them to Tier 2 / Deferred.

### Status

This is a **recommended taxonomy — pending final human approval.** No classes have been committed to training. Data acquisition should proceed for the 51 listed classes while the Oregano/Sage discrepancy is resolved.

### Vegetables (28 classes)

| # | Proposed Class | Canonical Class (existing ML taxonomy) | Mapping Type | Rationale |
|---|---------------|----------------------------------------|-------------|-----------|
| 1 | Tomato | Tomato | Exact | Critical garden crop |
| 2 | Pepper | Pepper_sweet + Pepper_hot | Merged | All peppers look identical as plants; variety tracked in Garden DB |
| 3 | Eggplant | Eggplant | Exact | Common nightshade |
| 4 | Potato | Potato | Exact | Critical garden crop |
| 5 | Cucumber | Cucumber | Exact | Common cucurbit |
| 6 | Summer Squash / Zucchini | Summer_squash | Renamed | Same species (Cucurbita pepo); visually identical |
| 7 | Winter Squash / Pumpkin | Winter_squash + Pumpkin | Merged | Pumpkins are winter squash; visually similar when mature |
| 8 | Corn | Corn | Exact | Common grain/vegetable |
| 9 | Bean | Bean | Exact (merged scope) | Green bean + dry bean are same species |
| 10 | Pea | Pea | Exact | Common legume |
| 11 | Carrot | Carrot | Exact | Root vegetable |
| 12 | Beet | Beet | Exact | Root vegetable |
| 13 | Radish | Radish | Exact | Root vegetable |
| 14 | Turnip | Turnip | Exact | Root vegetable |
| 15 | Onion | Onion | Exact | Allium |
| 16 | Garlic | Garlic | Exact | Allium |
| 17 | Leek | Leek | Exact | Allium |
| 18 | Broccoli | Broccoli | Exact | Brassica |
| 19 | Cabbage | Cabbage | Exact | Brassica |
| 20 | Cauliflower | Cauliflower | Exact | Brassica |
| 21 | Brussels Sprouts | — | NEW | Common brassica |
| 22 | Kale | — | NEW | Common brassica/green |
| 23 | Lettuce | Lettuce | Exact | Leafy green |
| 24 | Spinach | Spinach | Exact | Leafy green |
| 25 | Swiss Chard | — | NEW | Common leafy green |
| 26 | Sweet Potato | Sweet_potato | Renamed | Root vegetable |
| 27 | Watermelon | Watermelon | Exact | Space-intensive but common |
| 28 | Cantaloupe | Cantaloupe | Exact | Space-intensive but common |

### Berries (4 classes)

| # | Proposed Class | Canonical Class | Mapping Type | Rationale |
|---|---------------|----------------|-------------|-----------|
| 29 | Strawberry | Strawberry | Exact | Common berry |
| 30 | Raspberry / Blackberry | — | NEW (merged) | Both Rubus; visually similar on canes |
| 31 | Blueberry | Blueberry | Exact | Common berry |
| 32 | Grape | Grape | Exact | Common fruit |

### Fruit Trees (7 classes)

| # | Proposed Class | Canonical Class | Mapping Type | Rationale |
|---|---------------|----------------|-------------|-----------|
| 33 | Apple | — | NEW | Common fruit tree; PlantVillage has data |
| 34 | Pear | — | NEW | Common fruit tree |
| 35 | Peach | Peach | Exact (from existing) | Common fruit tree; PlantVillage has data |
| 36 | Cherry | Cherry | Exact | Common fruit tree; PlantVillage has data |
| 37 | Plum | — | NEW | Common fruit tree |
| 38 | Apricot | — | NEW | Common fruit tree |
| 39 | Nectarine | — | NEW | Common fruit tree |

### Herbs (8 classes)

| # | Proposed Class | Canonical Class | Mapping Type | Rationale |
|---|---------------|----------------|-------------|-----------|
| 40 | Basil | Basil | Exact | Most common culinary herb |
| 41 | Cilantro | Cilantro | Exact | Common culinary herb |
| 42 | Parsley | Parsley | Exact | Common culinary herb |
| 43 | Dill | Dill | Exact | Common culinary herb |
| 44 | Chives | Chives | Exact | Common culinary herb |
| 45 | Mint | — | NEW | Extremely common garden herb |
| 46 | Rosemary | Rosemary | Exact | Common perennial herb |
| 47 | Thyme | Thyme | Exact | Common perennial herb |

### Other Common Garden Crops (4 classes)

| # | Proposed Class | Canonical Class | Mapping Type | Rationale |
|---|---------------|----------------|-------------|-----------|
| 48 | Asparagus | Asparagus | Exact | Common perennial vegetable |
| 49 | Rhubarb | Rhubarb | Exact | Common perennial |
| 50 | Hops | — | NEW | Common home garden crop (brewing) |
| 51 | Sunflower | Sunflower | Exact | Common garden plant |

**Total Tier 1: 51 classes**

---

## 4. Recommended Tier 2 Taxonomy — 12 Classes

Tier 2 contains useful but non-essential classes. These are either less common in home gardens, have very limited training data, or require additional data acquisition beyond the immediate gaps.

| # | Proposed Class | Canonical Class | Rationale for Tier 2 |
|---|---------------|----------------|---------------------|
| 52 | Fava Bean | — | Niche legume; limited data |
| 53 | Parsnip | — | Less common root vegetable |
| 54 | Daikon | — | Niche radish variety |
| 55 | Shallot | — | Less common allium |
| 56 | Arugula | — | Niche leafy green |
| 57 | Collards | — | Regional (Southern US); similar to Kale |
| 58 | Kohlrabi | — | Niche brassica |
| 59 | Currant | — | Niche berry in North America |
| 60 | Gooseberry | — | Niche berry in North America |
| 61 | Celery | Celery | Difficult home garden crop |
| 62 | Fennel | Fennel | Herb-like; limited data |
| 63 | Artichoke | Artichoke | Regional; limited data |

**Total Tier 2: 12 classes**

**Combined Tier 1 + Tier 2: 63 classes**

---

## 5. Deferred Classes

The following classes from the existing 50-class taxonomy are intentionally deferred to post-v1:

| Canonical Class | Reason for Deferral |
|----------------|---------------------|
| Marigold | Ornamental, not food crop |
| Zinnia | Ornamental, not food crop |
| Nasturtium | Ornamental (though edible), niche |
| Cosmos | Ornamental, not food crop |
| Petunia | Ornamental, not food crop |
| Begonia | Ornamental, not food crop |
| Okra | Regional (Southern US); limited data |
| Oregano | Moved to Tier 1 (was in existing 50-class) |
| Sage | Moved to Tier 1 (was in existing 50-class) |

---

## 6. Intentionally Excluded Classes

The following were considered but excluded from Tier 1 and Tier 2:

| Class | Reason for Exclusion |
|-------|---------------------|
| Soybean | Field crop, not home garden |
| Wheat / Barley / Oat | Grain field crops, not garden |
| Rice | Not a home garden crop |
| Cotton | Not a food crop |
| Mushrooms | Not plants; different domain |
| Tomato varieties (Roma, Cherry, etc.) | Variety tracking belongs in Garden DB |
| Pepper varieties (Bell, Jalapeño, etc.) | Variety tracking belongs in Garden DB |
| Corn varieties (Sweet, Field, Flour) | Visually identical; variety in Garden DB |
| Apple varieties (Honeycrisp, Gala, etc.) | Variety tracking belongs in Garden DB |

---

## 7. Classes Intentionally Merged

| Merged Classes | Proposed Unified Class | Rationale |
|---------------|----------------------|-----------|
| Pepper_sweet + Pepper_hot | Pepper | Bell peppers and hot peppers look identical as plants. Fruit color/shape varies, but from leaf-level photos they're indistinguishable. |
| Summer_squash → Summer Squash / Zucchini | Same species (Cucurbita pepo). Visually identical at all growth stages. |
| Winter_squash + Pumpkin | Winter Squash / Pumpkin | Pumpkins are a subset of winter squash. Many varieties blur the line (sugar pumpkins, cheese pumpkins). |
| Raspberry + Blackberry | Raspberry / Blackberry | Both Rubus with aggregate fruits on canes. Hollow vs. solid fruit core requires picking the fruit — unreliable from photos. |

---

## 8. Existing Taxonomy Mapping

### Mapping to Canonical ML Taxonomy (training/config.yaml)

| Canonical Class | Proposed Phase 34B Class | Mapping Type |
|----------------|-------------------------|-------------|
| Tomato | Tomato | Exact |
| Pepper_sweet | Pepper | Renamed + merged |
| Pepper_hot | Pepper | Merged into Pepper |
| Cucumber | Cucumber | Exact |
| Bean | Bean | Exact (merged scope) |
| Carrot | Carrot | Exact |
| Corn | Corn | Exact |
| Onion | Onion | Exact |
| Potato | Potato | Exact |
| Broccoli | Broccoli | Exact |
| Cabbage | Cabbage | Exact |
| Lettuce | Lettuce | Exact |
| Spinach | Spinach | Exact |
| Pea | Pea | Exact |
| Radish | Radish | Exact |
| Summer_squash | Summer Squash / Zucchini | Renamed |
| Winter_squash | Winter Squash / Pumpkin | Renamed + merged |
| Pumpkin | Winter Squash / Pumpkin | Merged |
| Watermelon | Watermelon | Exact |
| Cantaloupe | Cantaloupe | Exact |
| Beet | Beet | Exact |
| Turnip | Turnip | Exact |
| Sweet_potato | Sweet Potato | Renamed |
| Basil | Basil | Exact |
| Cilantro | Cilantro | Exact |
| Parsley | Parsley | Exact |
| Dill | Dill | Exact |
| Chives | Chives | Exact |
| Rosemary | Rosemary | Exact |
| Thyme | Thyme | Exact |
| Oregano | Oregano | Exact |
| Sage | Sage | Exact |
| Strawberry | Strawberry | Exact |
| Blueberry | Blueberry | Exact |
| Grape | Grape | Exact |
| Marigold | — | Deferred (ornamental) |
| Zinnia | — | Deferred (ornamental) |
| Nasturtium | — | Deferred (ornamental) |
| Sunflower | Sunflower | Exact |
| Cosmos | — | Deferred (ornamental) |
| Petunia | — | Deferred (ornamental) |
| Begonia | — | Deferred (ornamental) |
| Eggplant | Eggplant | Exact |
| Okra | — | Deferred (regional) |
| Asparagus | Asparagus | Exact |
| Rhubarb | Rhubarb | Exact |
| Celery | Celery | Tier 2 |
| Leek | Leek | Exact |
| Fennel | Fennel | Tier 2 |
| Artichoke | Artichoke | Tier 2 |
| — | Pepper | NEW (merged) |
| — | Winter Squash / Pumpkin | NEW (merged) |
| — | Brussels Sprouts | NEW |
| — | Kale | NEW |
| — | Swiss Chard | NEW |
| — | Raspberry / Blackberry | NEW (merged) |
| — | Apple | NEW |
| — | Pear | NEW |
| — | Apricot | NEW |
| — | Nectarine | NEW |
| — | Mint | NEW |
| — | Hops | NEW |

### Mapping to App CropKnowledge Catalog

| App CropKnowledge Class | Phase 34B Class | Status |
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

## 9. Commercial Data Coverage

### Verified Commercial Sources (Auto-Downloadable)

| Source | License | Images | Commercial OK | Status |
|--------|---------|--------|---------------|--------|
| PlantVillage | CC0 1.0 | 54,306 | YES | ACQUIRED — healthy crop images usable for recognition |
| PlantDoc | CC BY 4.0 | 2,569 | YES | ACQUIRED — real-world field images |
| Irish Potato | CC BY 4.0 | 117,418 | YES | ACQUIRED — smartphone field images |
| Grapevine | CC BY 4.0 | 5,267 | YES | ACQUIRED — smartphone field images |
| SegPPD-101 | MIT (REVIEW) | 817 | REVIEW | REVIEW — primary sources inaccessible |

### Manual-Download Sources (CC BY 4.0)

| Source | License | Images | Commercial OK | Status |
|--------|---------|--------|---------------|--------|
| Bangladesh Vegetables | CC BY 4.0 | ~4,730 | YES | MANUAL DOWNLOAD REQUIRED |
| Smartphone Vegetable Detection | CC BY 4.0 | ~3,534 | YES | MANUAL DOWNLOAD REQUIRED |
| VegNet | CC BY 4.0 | ~6,850 | YES | MANUAL DOWNLOAD REQUIRED |
| BanglaVeg | CC BY 4.0 | ~4,319 | YES | MANUAL DOWNLOAD REQUIRED |
| Early-Stage Crops | CC BY 4.0 | ~2,801 | YES | MANUAL DOWNLOAD REQUIRED |

### Candidate Sources (License Unverified)

| Source | License | Images | Commercial OK | Status |
|--------|---------|--------|---------------|--------|
| images.cv Vegetables | CC0 (claimed) | 19,300 | REVIEW | DATASET_SEARCH_REQUIRED |
| Kaggle Fruit and Vegetables | CC0 (claimed) | 72,000+ | REVIEW | DATASET_SEARCH_REQUIRED |
| OpenPlant | Unclear | 635,000 | BLOCKED | LICENSE_BLOCKED |
| USDA ARS | Public Domain | 6,500+ | YES | ACQUIRED (unlabeled supplement) |

---

## 10. Data Coverage Matrix

| Class | Tier | Existing USE | Candidate Sources | License | Field/Garden Images | Estimated Gap | Status |
|-------|------|-------------|-------------------|---------|---------------------|---------------|--------|
| Tomato | 1 | 4,224 | PlantVillage, PlantDoc, +5 manual | CC0, CC BY 4.0 | Yes (PlantDoc) | None | SUFFICIENT |
| Pepper | 1 | 3,186 | PlantVillage, PlantDoc, VegNet, +4 manual | CC0, CC BY 4.0 | Yes (PlantDoc) | None | SUFFICIENT |
| Corn | 1 | 3,022 | PlantVillage, PlantDoc, Early-Stage | CC0, CC BY 4.0 | Yes (PlantDoc) | None | SUFFICIENT |
| Potato | 1 | ~40,000 | Irish Potato, PlantVillage, +4 manual | CC BY 4.0, CC0 | Yes (Irish Potato) | None | SUFFICIENT |
| Strawberry | 1 | 912 | PlantVillage | CC0 | No | Low | LOW |
| Blueberry | 1 | 1,502 | PlantVillage | CC0 | No | Low | LOW |
| Grape | 1 | ~3,000 | PlantVillage, Grapevine | CC0, CC BY 4.0 | Yes (Grapevine) | None | SUFFICIENT |
| Apple | 1 | ~2,500 | PlantVillage | CC0 | No | Low | LOW |
| Peach | 1 | ~2,700 | PlantVillage | CC0 | No | Low | LOW |
| Cherry | 1 | ~2,000 | PlantVillage | CC0 | No | Low | LOW |
| Raspberry/Blackberry | 1 | 371 | PlantVillage | CC0 | No | Moderate | LOW |
| Summer Squash/Zucchini | 1 | 248 | PlantDoc, +2 manual | CC BY 4.0 | Yes | Low | LOW |
| Eggplant | 1 | 0 | +3 manual | CC BY 4.0 | No | Moderate | ACQUIRABLE |
| Cucumber | 1 | 0 | +3 manual | CC BY 4.0 | No | Moderate | ACQUIRABLE |
| Bean | 1 | 0 | +4 manual | CC BY 4.0 | No | Moderate | ACQUIRABLE |
| Carrot | 1 | 0 | +3 manual | CC BY 4.0 | No | Moderate | ACQUIRABLE |
| Radish | 1 | 0 | +3 manual | CC BY 4.0 | No | Moderate | ACQUIRABLE |
| Onion | 1 | 0 | +3 manual | CC BY 4.0 | No | Moderate | ACQUIRABLE |
| Broccoli | 1 | 0 | +1 manual, images.cv | CC BY 4.0, CC0 (claimed) | No | Moderate | ACQUIRABLE |
| Cabbage | 1 | 0 | +1 manual, images.cv | CC BY 4.0, CC0 (claimed) | No | Moderate | ACQUIRABLE |
| Leek | 1 | 0 | Early-Stage, +2 manual, images.cv | CC BY 4.0, CC0 (claimed) | No | Moderate | ACQUIRABLE |
| Winter Squash/Pumpkin | 1 | 0 | +3 manual | CC BY 4.0 | No | Moderate | ACQUIRABLE |
| Pea | 1 | 0 | images.cv, Kaggle | CC0 (claimed) | No | High | REVIEW |
| Beet | 1 | 0 | images.cv, Kaggle | CC0 (claimed) | No | High | REVIEW |
| Garlic | 1 | 0 | Kaggle | CC0 (claimed) | No | High | REVIEW |
| Lettuce | 1 | 0 | images.cv, Kaggle | CC0 (claimed) | No | High | REVIEW |
| Spinach | 1 | 0 | images.cv, Kaggle | CC0 (claimed) | No | High | REVIEW |
| Cauliflower | 1 | 0 | images.cv, Kaggle | CC0 (claimed) | No | High | REVIEW |
| Turnip | 1 | 0 | images.cv, Kaggle | CC0 (claimed) | No | High | REVIEW |
| Sweet Potato | 1 | 0 | Kaggle | CC0 (claimed) | No | High | REVIEW |
| Watermelon | 1 | 0 | VegNet (partial) | CC BY 4.0 | No | High | REVIEW |
| Cantaloupe | 1 | 0 | VegNet (partial) | CC BY 4.0 | No | High | REVIEW |
| Brussels Sprouts | 1 | 0 | No known source | — | — | High | MISSING |
| Kale | 1 | 0 | No known source | — | — | High | MISSING |
| Swiss Chard | 1 | 0 | No known source | — | — | High | MISSING |
| Asparagus | 1 | 0 | images.cv | CC0 (claimed) | No | High | REVIEW |
| Rhubarb | 1 | 0 | No known source | — | — | High | MISSING |
| Hops | 1 | 0 | No known source | — | — | High | MISSING |
| Sunflower | 1 | 0 | No known source | — | — | High | MISSING |
| Basil | 1 | 0 | Herb datasets (CC BY 4.0) | CC BY 4.0 | No | High | REVIEW |
| Cilantro | 1 | 0 | Herb datasets (CC BY 4.0) | CC BY 4.0 | No | High | REVIEW |
| Parsley | 1 | 0 | Herb datasets (CC BY 4.0) | CC BY 4.0 | No | High | REVIEW |
| Dill | 1 | 0 | Herb datasets (CC BY 4.0) | CC BY 4.0 | No | High | REVIEW |
| Chives | 1 | 0 | Herb datasets (CC BY 4.0) | CC BY 4.0 | No | High | REVIEW |
| Mint | 1 | 0 | Herb datasets (CC BY 4.0) | CC BY 4.0 | No | High | REVIEW |
| Rosemary | 1 | 0 | Herb datasets (CC BY 4.0) | CC BY 4.0 | No | High | REVIEW |
| Thyme | 1 | 0 | Herb datasets (CC BY 4.0) | CC BY 4.0 | No | High | REVIEW |
| Pear | 1 | 0 | No known source | — | — | High | MISSING |
| Plum | 1 | 0 | No known source | — | — | High | MISSING |
| Apricot | 1 | 0 | No known source | — | — | High | MISSING |
| Nectarine | 1 | 0 | No known source | — | — | High | MISSING |

---

## 11. Dataset Acquisition Plan

### Priority 1: Verified Manual Downloads (5 datasets)

These datasets are commercially approved (CC BY 4.0) and would fill the majority of Tier 1 vegetable gaps:

| Dataset | Source | URL | License | Classes Supplied | Approx. Images |
|---------|--------|-----|---------|------------------|---------------|
| Bangladesh Vegetables | Mendeley Data | https://data.mendeley.com/datasets/rtx9ngb68j | CC BY 4.0 | Tomato, Pepper, Cucumber, Eggplant, Broccoli, Cabbage, Carrot, Onion, Potato, Pumpkin, Radish, Zucchini, Bean | ~4,730 |
| Smartphone Vegetable Detection | Mendeley Data | https://data.mendeley.com/datasets/gnc4s3z2mf/3 | CC BY 4.0 | Tomato, Pepper, Cucumber, Eggplant, Potato, Pumpkin, Radish, Bean, Carrot, Onion | ~3,534 |
| VegNet | Mendeley Data | https://data.mendeley.com/datasets/6nxnjbn9w6 | CC BY 4.0 | Bell Pepper, Tomato, Chili Pepper | ~6,850 |
| BanglaVeg | Mendeley Data | https://data.mendeley.com/datasets/... | CC BY 4.0 | Tomato, Pepper, Cucumber, Eggplant, Potato, Onion, Radish, Bean, Chili | ~4,319 |
| Early-Stage Crops | PMC | https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/ | CC BY 4.0 | Corn, Bean, Leek | ~2,801 |

### Priority 2: License Verification Required

These datasets claim CC0 but require primary-source verification before commercial use:

| Dataset | Source | URL | Claimed License | Classes Supplied | Approx. Images | Action Required |
|---------|--------|-----|----------------|------------------|---------------|-----------------|
| images.cv Vegetables | images.cv | https://images.cv/dataset/vegetables-image-classification-dataset | CC0 (claimed) | Tomato, Potato, Cucumber, Bean, Carrot, Onion, Capsicum, Eggplant, Broccoli, Cabbage, Cauliflower, Pumpkin, Radish, Turnip, Sweetcorn, Beetroot, Pea, Asparagus, Celery, Leek, Lettuce, Spinach | ~19,300 | Verify CC0 from primary source; resolve download mechanism |
| Kaggle Fruit and Vegetables | Kaggle | https://www.kaggle.com/datasets/youssefsalahzakria/fruit-and-vegetables-classification | CC0 (claimed) | Apple, Broccoli, Cabbage, Capsicum, Carrot, Cauliflower, Corn, Cucumber, Eggplant, Garlic, Lettuce, Onion, Peas, Pepper, Potato, Radish, Spinach, Sweet Potato, Tomato, Turnip | ~72,000+ | Verify CC0 from primary source; confirm Kaggle download access |
| Herb Dataset (images.cv) | images.cv | https://images.cv/dataset/herbs-image-classification-dataset | CC0 (claimed) | Basil, Cilantro, Parsley, Dill, Mint, Rosemary, Sage, Thyme | ~5,000+ | Verify CC0; resolve download mechanism |

### Priority 3: Additional Acquisition Needed

For classes with no known commercial dataset:

| Class | Gap | Candidate Strategy |
|-------|-----|-------------------|
| Pear, Plum, Apricot, Nectarine | No known dataset | Search USDA ARS, extension services, targeted web scraping (CC BY/CC0 only) |
| Brussels Sprouts, Kale, Swiss Chard | No known dataset | Search USDA ARS, extension services, specialty vegetable datasets |
| Hops | No known dataset | Search brewing/hops associations, extension services |
| Rhubarb | No known dataset | Search extension services, specialty plant databases |
| Sunflower | No known dataset | Search USDA ARS, sunflower grower associations |
| Currant, Gooseberry | No known dataset | Search extension services, specialty berry datasets |

### Acquisition Sequence

1. **Week 1:** Manually download Priority 1 datasets (5 datasets, ~22K images)
2. **Week 2-3:** Verify CC0 claims for images.cv and Kaggle datasets; download if verified (~91K images)
3. **Week 4:** Process and integrate all acquired data into commercial manifests
4. **Week 5-6:** Search for additional datasets for remaining gap classes
5. **Week 7:** Finalize Tier 1 class list based on acquired data
6. **Week 8:** Train and evaluate

---

## 12. Licensing / Provenance Assessment

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
| USDA ARS | Public Domain | No | VERIFIED |

### Requires Verification

| Source | Issue |
|--------|-------|
| images.cv Vegetables | Claims CC0 but download mechanism and exact provenance unclear |
| Kaggle Fruit and Vegetables | Claims CC0 but Kaggle hosting terms are not sufficient evidence; need primary-source verification |
| images.cv Herb Dataset | Claims CC0 but download mechanism unclear |
| SegPPD-101 | MIT claimed at acquisition time, primary sources now inaccessible |

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

## 13. Recommended Acquisition Sequence

### Phase 1: Immediate (Manual Download)
1. Bangladesh Vegetables
2. Smartphone Vegetable Detection
3. VegNet
4. BanglaVeg
5. Early-Stage Crops

**Expected outcome:** ~22,000 additional images covering 12-15 Tier 1 classes

### Phase 2: License Verification
1. Verify images.cv Vegetables CC0 claim
2. Verify Kaggle Fruit and Vegetables CC0 claim
3. Verify images.cv Herb Dataset CC0 claim
4. Download if verified

**Expected outcome:** ~96,000 additional images covering 20+ Tier 1 classes

### Phase 3: Targeted Search
1. Search for fruit tree datasets (Pear, Plum, Apricot, Nectarine)
2. Search for brassica datasets (Brussels Sprouts, Kale, Swiss Chard)
3. Search for specialty crops (Hops, Rhubarb, Sunflower)
4. Search for berry datasets (Currant, Gooseberry)

**Expected outcome:** Variable; may require web scraping or extension service partnerships

### Phase 4: Model Training
1. Train on all verified, commercially compatible data
2. Evaluate on external test set
3. Iterate based on performance gaps

---

## 14. Recommended Next Phase

### Decision: "Recommended taxonomy — pending final human approval"

The proposed Tier 1 taxonomy is **51 classes** covering the most common home-garden vegetables, berries, fruit trees, herbs, and specialty crops. This is a practical, commercially defensible set that:

- Maps cleanly onto the existing 50-class ML taxonomy (with merges and renames)
- Covers all 10 crops in the app's CropKnowledge catalog
- Can be trained with commercially approved data for 11 classes from auto-downloadable sources
- Requires manual acquisition of 5 datasets for 10 more classes
- Has 19 classes with unverified CC0 claims (REVIEW)
- Has 10 classes with no known commercial dataset (MISSING)

### Specific decisions requiring human approval (from Section 0):

1. **Tier 1 size:** 50-51 classes (recommended) vs. 60+ classes
2. **Fruit tree scope:** Include all 7 (recommended) vs. defer some
3. **Herb scope:** Include all 8 (recommended) vs. defer some
4. **Missing-data strategy:** Train partial model now (recommended) vs. wait for all data
5. **images.cv / Kaggle pursuit:** Pursue with REVIEW status (recommended) vs. exclude
6. **Oregano/Sage placement:** Add to Tier 1 tables (53 classes) or move to Tier 2/Deferred

### If the taxonomy is approved:

The next phase should:
1. Manually download the 5 Priority 1 datasets
2. Verify CC0 claims for images.cv and Kaggle datasets
3. Process and integrate all data into commercial manifests
4. Train the crop-recognition classifier on approved Tier 1 classes
5. Evaluate and export to mobile format

---

## 15. Decision Format

EXACT TIER 1 CLASS COUNT: **51 classes** (as listed in taxonomy tables)

EXACT TIER 2 CLASS COUNT: **12 classes**

CURRENTLY DATA-SUFFICIENT (auto-downloadable): **11 classes** (Tomato, Pepper, Corn, Potato, Strawberry, Blueberry, Grape, Apple, Peach, Cherry, Summer Squash)

REQUIRES DATA ACQUISITION (manual download, CC BY 4.0): **10 classes** (Eggplant, Cucumber, Bean, Carrot, Radish, Onion, Broccoli, Cabbage, Leek, Winter Squash/Pumpkin)

REQUIRES LICENSE REVIEW (unverified CC0 claims): **19 classes** (Pea, Beet, Garlic, Lettuce, Spinach, Cauliflower, Turnip, Sweet Potato, Watermelon, Cantaloupe, Asparagus, Basil, Cilantro, Parsley, Dill, Chives, Mint, Rosemary, Thyme)

REQUIRES ADDITIONAL DATASET SEARCH: **10 classes** (Pear, Plum, Apricot, Nectarine, Brussels Sprouts, Kale, Swiss Chard, Hops, Rhubarb, Sunflower)

ESTIMATED TOTAL COMMERCIAL TRAINING IMAGES AFTER PRIORITY 1 ACQUISITION: **~115,000** (98,642 existing + ~22,000 from manual downloads + ~15,000 from re-splitting)

ESTIMATED TOTAL COMMERCIAL TRAINING IMAGES AFTER PRIORITY 1 + 2 ACQUISITION: **~200,000+** (adding ~96,000 from verified CC0 datasets)

**Recommendation: Recommended taxonomy — pending final human approval**

The taxonomy is well-defined, grounded in home-gardener use, and has a clear data path for 21 of 51 Tier 1 classes from verified commercial sources. The remaining 30 gap classes are identified with specific acquisition strategies. Human approval is needed on 6 product decisions (Section 0 + Oregano/Sage placement), but none of them block beginning Priority 1 dataset acquisition.

---

## 16. Git / Repository Hygiene

This phase is research and documentation only. No Android, CMP, iOS, Garden UI, or disease P0 files were modified. No datasets were downloaded. No commercial manifests were altered. Only this document was created.
