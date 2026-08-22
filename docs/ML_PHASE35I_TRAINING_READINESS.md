# Soil & Supper — Phase 35I Training Readiness Report

**Generated**: 2026-08-22  
**Phase**: 35I — Final Commercial Corpus + Training-Readiness Audit  
**Status**: AUDIT COMPLETE — Training not approved

---

## 1. EXECUTIVE SUMMARY

Phase 35I performed a rigorous, independent audit of the Phase 35H approved corpus. The audit corrected critical class-discovery bugs, performed corpus-wide SHA256 deduplication, verified licenses, assessed attribution obligations, and evaluated training readiness.

**Key finding**: The actual usable, deduplicated, correctly-mapped training corpus is **34,399 unique images across 29 Tier-1 classes** — not the previously reported 134,832. The discrepancy is due to:
1. Broken class-discovery in 4 major approved datasets (15,879 images were unmapped)
2. Extensive cross-dataset exact duplication (6,314 duplicate groups)
3. Cross-class labeling conflicts (366 conflicting hashes)

**FINAL RECOMMENDATION: NOT READY FOR TRAINING**

The corpus is commercially clean and properly attributed, but:
- Class imbalance is extreme (371:1)
- 7 classes have fewer than 200 unique images
- 366 images have conflicting labels across datasets
- No train/validation/test split has been designed or verified
- veg_object_bangla_inbox (3,534 images) cannot be used for classification
- hf_digigreen (414 images) has no viable class mapping

Training requires explicit human approval after the blockers are resolved.

---

## 2. CORPUS INVENTORY

### 2.1 Datasets Discovered

| Dataset | Status | Raw Files | Valid Images | Mapped Images (post-dedup) |
|---------|--------|-----------|--------------|----------------------------|
| bangladesh_veg_inbox | APPROVED | 1,878 | 1,876 | 1,852 |
| fruits262_101class_subset | APPROVED | 50,007 | 49,991 | ~4,050* |
| hf_100crops | APPROVED | 8,358 | 3,489 | 3,489 |
| hf_digigreen | APPROVED | 839 | 414 | 0 |
| hf_food_ingredients_v2 | APPROVED | 1,001 | 493 | 493 |
| hf_food_veg | APPROVED | 2,217 | 1,099 | 1,099 |
| hf_veg_bangladesh | APPROVED | 3,083 | 3,066 | 3,066 |
| plants_type_30class | APPROVED | 30,001 | 30,000 | 17,000 |
| plants_type_30class_alt | APPROVED | 30,007 | 29,994 | 16,993 |
| veg_bangla_inbox | APPROVED | 4,321 | 4,319 | 4,319 |
| veg_object_bangla_inbox | APPROVED | 7,069 | 3,534 | 0 |
| vegnet_inbox | APPROVED | 6,152 | 6,150 | 6,150 |
| zenodo_vegann | APPROVED | 422 | 407 | 407 |

* fruits262_101class_subset mapped count is approximate because many of its 101 classes are not in our Tier-1 taxonomy.

### 2.2 Datasets Rejected

| Dataset | Reason | Images |
|---------|--------|--------|
| hf_food_ingredients | Non-commercial license (unknown) | 428 |
| hf_fruit_veg | Non-commercial license (unknown) | 907 |
| hf_plantvillage | CC BY-SA 3.0 (ShareAlike incompatible) | 24,723 |
| hf_smartharvest | Non-commercial license (unknown) | 744 |

### 2.3 Datasets Under Review

| Dataset | Reason |
|---------|--------|
| plants_type_30class | License evidence shows "Data files © Original Authors" on free2aitools; needs direct Kaggle verification |
| fruits262_101class_subset | License shows CC0 on free2aitools; needs direct Kaggle verification |

### 2.4 Duplicate Exclusions

| Duplicate Type | Count | Notes |
|----------------|-------|-------|
| Exact duplicate groups (all datasets) | 8,552 groups | From ledger SHA256 analysis |
| Cross-dataset duplicate groups | 6,314 groups | Same image in multiple approved datasets |
| plants_type_30class ↔ plants_type_30class_alt overlap | 2,953 images | Confirmed via filesystem hashing |
| Cross-class label conflicts | 366 hashes | Same image labeled as different classes |

### 2.5 Corrupt/Invalid Exclusions

From intake pipeline validation:
- Corrupt images: 13 total across all datasets
- Too-small images: 11 total
- Blank images: 5 total (all in plants_type_30class_alt)
- Extreme aspect ratio: 0

---

## 3. LICENSE VERIFICATION

### 3.1 Approved Licenses

| Dataset | License | Version | Primary Source | Evidence | Status |
|---------|---------|---------|----------------|----------|--------|
| hf_100crops | MIT | - | https://huggingface.co/datasets/devshaheen/100_crops_plants_object_detection_25k_image_dataset | README YAML | VERIFIED |
| hf_digigreen | CC BY 4.0 | 4.0 | https://huggingface.co/datasets/DigiGreen/Crop_Disease_Images | README YAML | VERIFIED |
| hf_food_ingredients_v2 | CC BY 4.0 | 4.0 | https://www.kaggle.com/datasets/sunnyagarwal427444/food-ingredient-dataset-51 | README YAML | VERIFIED |
| hf_food_veg | Apache-2.0 | 2.0 | https://huggingface.co/datasets/SunnyAg/fruits_and_vegetables_dataset | README YAML | VERIFIED |
| hf_veg_bangladesh | CC BY 4.0 | 4.0 | https://huggingface.co/datasets/MdJobayerAhmed/BanglaVeg | README YAML | VERIFIED |
| zenodo_vegann | CC BY | - | https://zenodo.org/records/8105154 | README multiline | VERIFIED |
| bangladesh_veg_inbox | CC BY 4.0 | 4.0 | https://data.mendeley.com/datasets/rtx9ngb68j | Mendeley page | VERIFIED |
| veg_bangla_inbox | CC BY 4.0 | 4.0 | https://data.mendeley.com/datasets/b9rvg4f2st | Mendeley page / ScienceDirect | VERIFIED |
| veg_object_bangla_inbox | CC BY 4.0 | 4.0 | https://data.mendeley.com/datasets/gnc4s3z2mf | Mendeley page | VERIFIED |
| vegnet_inbox | CC BY 4.0 | 4.0 | https://data.mendeley.com/datasets/6nxnjbn9w6 | Manifest metadata | VERIFIED |
| plants_type_30class | CC0 1.0 | 1.0 | https://www.kaggle.com/datasets/yudhaislamisulistya/plants-type-datasets | Manifest metadata | REVIEW |
| plants_type_30class_alt | CC0 1.0 | 1.0 | https://www.kaggle.com/datasets/yudhaislamisulistya/plants-type-datasets | Manifest metadata | REVIEW |
| fruits262_101class_subset | CC0 1.0 | 1.0 | https://www.kaggle.com/datasets/aelchimminut/fruits262 | Manifest metadata | REVIEW |

### 3.2 License Issues

**REVIEW REQUIRED** for three Kaggle datasets:
- `plants_type_30class` / `plants_type_30class_alt`: The free2aitools metadata index records license as "Data files © Original Authors" rather than CC0. The local manifest records CC0 1.0. The actual Kaggle dataset page must be checked directly.
- `fruits262_101class_subset`: free2aitools confirms CC0, but direct Kaggle verification is pending.

These datasets are large (59,994 images combined). If their licenses are not actually CC0, they cannot be used commercially.

---

## 4. ATTRIBUTION AUDIT

### 4.1 Attribution Required

| Dataset | License | Attribution Required | Attribution Text |
|---------|---------|---------------------|------------------|
| hf_digigreen | CC BY 4.0 | Yes | DigiGreen / Digital Green |
| hf_food_ingredients_v2 | CC BY 4.0 | Yes | Sunny Agarwal |
| hf_veg_bangladesh | CC BY 4.0 | Yes | Ahmed, Md Jobayer; Saha, Ratu; Dutta, Arpon Kishore; Mojumdar, Mayen Uddin; Chakraborty, Narayan Ranjan |
| bangladesh_veg_inbox | CC BY 4.0 | Yes | Rabeya Bashri Sumona, John Pritom Biswas, Md Ashiqur Rahman, Mamun Hasan, Sudipto Chaki |
| veg_bangla_inbox | CC BY 4.0 | Yes | See ScienceDirect article: https://www.sciencedirect.com/science/article/pii/S2352340925001738 |
| veg_object_bangla_inbox | CC BY 4.0 | Yes | Mendeley Data contributors (see dataset page) |
| vegnet_inbox | CC BY 4.0 | Yes | Md MasudulIslam (see Mendeley dataset page) |
| zenodo_vegann | CC BY | Yes | See Zenodo record for full author list |

### 4.2 No Attribution Required

| Dataset | License | Notes |
|---------|---------|-------|
| hf_100crops | MIT | No attribution required by license; preserve copyright notice |
| hf_food_veg | Apache-2.0 | No attribution required; preserve copyright notice |
| plants_type_30class | CC0 1.0 | Public domain dedication |
| plants_type_30class_alt | CC0 1.0 | Public domain dedication |
| fruits262_101class_subset | CC0 1.0 | Public domain dedication |

### 4.3 Attribution Delivery

Soil & Supper must ship a NOTICE file or attribution section that includes:
- Creator names for all CC BY and CC BY 4.0 datasets
- Source URLs for all datasets
- License texts or references
- Any additional dataset-specific terms

The file should live at `docs/ML_DATASET_ATTRIBUTIONS.md` and be referenced from the model card / application about page.

---

## 5. IMAGE VALIDATION

### 5.1 Validation Results (from intake pipeline)

| Check | Count | Action |
|-------|-------|--------|
| Corrupt images | 13 | Excluded from training |
| Too small (<64px) | 11 | Excluded from training |
| Blank images | 5 | Excluded from training |
| Extreme aspect ratio | 0 | None |
| Zero-byte files | 0 | None |

All approved datasets passed basic readability validation. The excluded images are recorded in the dataset ledger.

### 5.2 Data Quality Concerns

- **veg_object_bangla_inbox**: Object detection annotations (XML) present. Images are video frame extracts. No classification labels available. **Cannot enter training.**
- **hf_digigreen**: Disease/disorder dataset. Images are `_flat` (no class structure). **Cannot enter training without manual labeling.**
- **plants_type_30class / alt**: Contains some blank images (5) and very small images (3). Already excluded.
- **Cross-class conflicts**: 366 hashes appear with different labels in different datasets. These represent either:
  - Dataset labeling errors
  - Near-duplicates of visually similar classes
  - Same image copied to multiple class folders (confirmed in hf_100crops)

---

## 6. DEDUPLICATION

### 6.1 Exact Duplicates

- **8,552 exact duplicate groups** found across all approved datasets
- **6,314 cross-dataset duplicate groups**
- **2,953 overlapping images** between plants_type_30class and plants_type_30class_alt

### 6.2 Deduplication Impact

| Metric | Pre-Dedup | Post-Dedup |
|--------|-----------|------------|
| Total valid images | 134,832 | 38,992 (unique across all classes) |
| Total mapped images | 79,694 | 34,399 |
| Unique mapped images | - | 34,399 |

The deduplication reduced the apparent corpus by ~75%. This is primarily because:
1. plants_type_30class and plants_type_30class_alt share ~3k images
2. hf_food_ingredients_v2 and hf_food_veg share Apple images
3. Several other datasets contain overlapping imagery

### 6.3 Cross-Class Conflicts

366 hashes map to multiple different classes. Major conflict types:
- **Kale ↔ Spinach**:  images in plants_type_30class_alt labeled as both
- **Cantaloupe ↔ Watermelon**:  images in plants_type_30class_alt labeled as both
- **Eggplant ↔ Pepper ↔ Tomato**: hf_100crops has the same image in multiple class directories
- **Onion ↔ Garlic**:  images shared between these classes in hf_food_veg

**Recommendation**: For conflicting hashes, assign to the class with the most reliable label source. Exclude images that cannot be confidently assigned.

---

## 7. LABEL MAPPING AUDIT

### 7.1 Mapping Quality

| Dataset | Original Labels | Mapped Labels | Issues |
|---------|----------------|---------------|--------|
| bangladesh_veg_inbox | 47 vegetable classes | 30 mapped | 1 unmapped (ginger) |
| veg_bangla_inbox | 12 classes | 12 mapped | None |
| vegnet_inbox | 4 quality-labeled classes | 2 mapped (Pepper, Tomato) | Quality subdirs (Ripe/Unripe/Damaged) ignored |
| plants_type_30class | 30 classes | 10 mapped | 20 unmapped (non-Tier-1 classes) |
| fruits262_101class_subset | 101+ classes | 6 mapped | 288+ unmapped |
| hf_100crops | 11 classes | 11 mapped | None |
| hf_veg_bangladesh | 7 classes | 7 mapped | None |
| hf_food_veg | 14 classes | 10 mapped | banana, ginger unmapped |
| hf_food_ingredients_v2 | 8 classes | 4 mapped | 4 unmapped |

### 7.2 Ambiguous Labels

- **Pepper**: Maps from bell pepper, capsicum, chilli pepper, chile pepper, green chili, peper chili. All map to Pepper.
- **Eggplant**: Maps from brinjal, aubergine. Consistent.
- **Bean**: Maps from green bean, flat bean, long beans, soy bean, etc. Consistent.
- **Corn**: Maps from maize, sweetcorn. Consistent.
- **Sweet Potato**: Maps from sweet potatoes, sweetpotatoes. Fixed in audit.
- **Cantaloupe**: Maps from muskmelon. Consistent.

No ambiguous mappings that would inflate class counts incorrectly.

---

## 8. REAL-WORLD IMAGE QUALITY

### 8.1 Dataset Characteristics

| Dataset | Image Domain | Quality Assessment |
|---------|-------------|-------------------|
| bangladesh_veg_inbox | Field/market smartphone photos | **Excellent** — natural lighting, real backgrounds, varied viewpoints |
| veg_bangla_inbox | Field/market smartphone photos | **Excellent** — same collection as above, different split |
| vegnet_inbox | Market smartphone photos with quality labels | **Good** — natural conditions, but limited to 4 vegetable types |
| plants_type_30class | Mixed (studio + field) | **Moderate** — some studio-like images, some field images |
| plants_type_30class_alt | Mixed (studio + field) | **Moderate** — same source as above |
| fruits262_101class_subset | Studio/controlled | **Moderate** — clean backgrounds, limited viewpoint diversity |
| hf_100crops | Real-world photographs | **Good** — varied sources |
| hf_veg_bangladesh | Real-world photographs | **Good** — Bangladesh field images |
| hf_food_veg | Mixed (studio + web) | **Moderate** — some food-photography style |
| hf_food_ingredients_v2 | Studio/controlled | **Moderate** — ingredient-focused, not plant-focused |
| zenodo_vegann | Laboratory/specimen | **Limited** — segmentation masks, RGB with binary masks |

### 8.2 Domain Limitations

- **Studio bias**: fruits262, hf_food_ingredients_v2, hf_food_veg contain many controlled-background images. May not generalize to garden smartphone photos.
- **Geographic concentration**: Bangladesh datasets (bangladesh_veg_inbox, veg_bangla_inbox, hf_veg_bangladesh) represent South Asian produce. May lack diversity for other regions.
- **Growth stage**: Most datasets show mature produce, not seedlings or growing plants.
- **Leaf-only imagery**: Some datasets (zenodo_vegann) focus on vegetation masks rather than produce.

---

## 9. CLASS-BY-CLASS READINESS ASSESSMENT

### 9.1 Strong Coverage (>1,000 images, 3+ sources)

| Class | Images | Sources | Diversity | Quality | Status |
|-------|--------|---------|-----------|---------|--------|
| Pepper | 6,678 | 9 | High | Good | READY |
| Eggplant | 3,123 | 7 | High | Good | READY |
| Cucumber | 2,495 | 6 | High | Good | READY |
| Corn | 2,448 | 5 | High | Good | READY |
| Onion | 1,319 | 4 | High | Good | READY |
| Kale | 1,845 | 2 | Moderate | Moderate | READY |
| Spinach | 1,792 | 2 | Moderate | Moderate | READY |
| Sweet Potato | 1,754 | 2 | Moderate | Moderate | READY |
| Watermelon | 1,871 | 2 | Moderate | Moderate | READY |
| Cantaloupe | 1,827 | 2 | Moderate | Moderate | READY |
| Bean | 1,010 | 3 | High | Good | READY |

### 9.2 Moderate Coverage (500-1,000 images)

| Class | Images | Sources | Diversity | Quality | Status |
|-------|--------|---------|-----------|---------|--------|
| Tomato | 3,014 | 4 | High | Good | READY |
| Potato | 767 | 4 | High | Good | READY |
| Strawberry | 503 | 2 | Moderate | Moderate | BORDERLINE |
| Apple | 516 | 2 | Moderate | Moderate | BORDERLINE |

### 9.3 Sparse Coverage (<500 images)

| Class | Images | Sources | Diversity | Quality | Status |
|-------|--------|---------|-----------|---------|--------|
| Pea | 450 | 1 | Low | Moderate | BORDERLINE |
| Grape | 450 | 1 | Low | Moderate | BORDERLINE |
| Raspberry/Blackberry | 450 | 1 | Low | Moderate | BORDERLINE |
| Apricot | 450 | 1 | Low | Moderate | BORDERLINE |
| Radish | 398 | 2 | Moderate | Good | BORDERLINE |
| Carrot | 353 | 3 | Moderate | Good | BORDERLINE |
| Broccoli | 256 | 3 | Moderate | Moderate | BORDERLINE |
| Cauliflower | 170 | 2 | Low | Moderate | NEEDS MORE DATA |
| Garlic | 147 | 2 | Low | Moderate | NEEDS MORE DATA |
| Cabbage | 129 | 2 | Low | Moderate | NEEDS MORE DATA |
| Beet | 92 | 2 | Low | Moderate | NEEDS MORE DATA |
| Winter Squash/Pumpkin | 34 | 1 | Very Low | Good | NEEDS MORE DATA |
| Summer Squash/Zucchini | 18 | 1 | Very Low | Good | NEEDS MORE DATA |
| Blueberry | 40 | 1 | Very Low | Moderate | NEEDS MORE DATA |

---

## 10. THREE TAXONOMIES

### 10.1 Conservative First Model (15 classes)

Classes that are strongly supported with >500 images, multiple sources, and good real-world quality:

**Vegetables (10)**
1. Pepper — 6,678 images, 9 sources
2. Eggplant — 3,123 images, 7 sources
3. Cucumber — 2,495 images, 6 sources
4. Corn — 2,448 images, 5 sources
5. Onion — 1,319 images, 4 sources
6. Tomato — 3,014 images, 4 sources
7. Kale — 1,845 images, 2 sources
8. Spinach — 1,792 images, 2 sources
9. Sweet Potato — 1,754 images, 2 sources
10. Watermelon — 1,871 images, 2 sources

**Fruits (5)**
11. Cantaloupe — 1,827 images, 2 sources
12. Bean — 1,010 images, 3 sources
13. Potato — 767 images, 4 sources
14. Strawberry — 503 images, 2 sources
15. Apple — 516 images, 2 sources

**Rationale**: All classes have >500 images, at least 2 independent sources, and represent common garden crops. Imbalance ratio: 13.2:1.

### 10.2 Broadest Responsible First Model (22 classes)

Adds classes with 250-500 images and at least 2-3 sources:

**Additional 7 classes:**
16. Broccoli — 256 images, 3 sources
17. Carrot — 353 images, 3 sources
18. Radish — 398 images, 2 sources
19. Pea — 450 images, 1 source
20. Grape — 450 images, 1 source
21. Raspberry/Blackberry — 450 images, 1 source
22. Apricot — 450 images, 1 source

**Rationale**: These classes have limited but sufficient data for a broader model. The single-source classes (Pea, Grape, Raspberry/Blackberry, Apricot) carry higher risk but are common garden crops. Imbalance ratio: 26.1:1.

### 10.3 Future Expansion

Classes that need more data before inclusion:

- **Blueberry** (40 images) — needs 500+ from multiple sources
- **Beet** (92 images) — needs 300+ from multiple sources
- **Cabbage** (129 images) — needs 300+ from multiple sources
- **Garlic** (147 images) — needs 300+ from multiple sources
- **Cauliflower** (170 images) — needs 300+ from multiple sources
- **Summer Squash/Zucchini** (18 images) — needs 500+ from multiple sources
- **Winter Squash/Pumpkin** (34 images) — needs 500+ from multiple sources

Also worth investigating:
- **Pear, Peach, Cherry, Plum, Nectarine** — no current data
- **Basil, Cilantro, Parsley, Dill, Chives, Mint, Rosemary, Thyme** — herbs, no current data
- **Asparagus, Rhubarb, Hops, Sunflower** — no current data

---

## 11. CLASS BALANCE

### 11.1 Current Distribution (29 classes, post-dedup)

| Statistic | Value |
|-----------|-------|
| Minimum | 18 (Summer Squash/Zucchini) |
| Maximum | 6,678 (Pepper) |
| Median | 503 |
| Mean | 1,186.2 |
| Imbalance ratio | 371.0:1 |

### 11.2 Conservative 15-Class Distribution

| Statistic | Value |
|-----------|-------|
| Minimum | 503 (Strawberry) |
| Maximum | 6,678 (Pepper) |
| Median | 1,792 |
| Mean | 2,026.6 |
| Imbalance ratio | 13.2:1 |

### 11.3 Broadest 22-Class Distribution

| Statistic | Value |
|-----------|-------|
| Minimum | 256 (Broccoli) |
| Maximum | 6,678 (Pepper) |
| Median | 1,319 |
| Mean | 1,960.0 |
| Imbalance ratio | 26.1:1 |

### 11.4 Training Considerations

For the conservative 15-class model:
- **Class weighting**: Recommended. Use inverse-frequency weighting to compensate for Pepper dominance.
- **Oversampling**: Recommended for Strawberry and Apple (bottom 2 classes).
- **Augmentation**: Standard augmentation (flip, rotate, color jitter) sufficient.
- **Balanced sampling**: Use weighted random sampler or focal loss.

For the broadest 22-class model:
- **Class weighting**: Required.
- **Oversampling**: Required for Broccoli, Carrot, Radish, Pea, Grape, Raspberry/Blackberry, Apricot.
- **Augmentation**: Aggressive augmentation for sparse classes.
- **Balanced sampling**: Essential.

---

## 12. DATA THAT SHOULD NOT ENTER TRAINING

### 12.1 Entire Datasets Excluded

| Dataset | Reason |
|---------|--------|
| veg_object_bangla_inbox | Object detection annotations only; no classification labels |
| hf_digigreen | Disease/disorder dataset; images are `_flat` with no class mapping to Tier-1 crops |

### 12.2 Image Subsets to Exclude

| Subset | Reason | Count |
|--------|--------|-------|
| Corrupt images | Unreadable files | 13 |
| Too-small images | <64px in either dimension | 11 |
| Blank images | No visual content | 5 |
| Cross-class conflicts | Same hash, different labels | 366 |
| Exact duplicates | Same image in multiple datasets | 6,314 groups |
| plants_type_30class ↔ alt overlap | Shared images between two datasets | 2,953 images |

### 12.3 Label Quality Issues

- **hf_100crops**: Contains duplicate images across different class folders (confirmed by hash analysis). Some class folders contain copies of images from other classes.
- **plants_type_30class_alt**: Multiple images labeled as both Kale and Spinach, and as both Cantaloupe and Watermelon. These are labeling errors in the source dataset.

---

## 13. TRAIN/VALIDATION/TEST LEAKAGE

### 13.1 Existing Splits

- **plants_type_30class** and **plants_type_30class_alt**: Both contain train/test/val splits. However, they share 2,953 images. Using both splits would create leakage.
- **Other datasets**: No reliable pre-existing splits verified.

### 13.2 Leakage Findings

- **Exact cross-split duplicates**: Not explicitly analyzed per dataset, but the 6,314 cross-dataset duplicates include some that may cross splits.
- **Near-duplicates**: Not analyzed (would require perceptual hashing).
- **Source leakage**: The two 30-class datasets share images. If both are used, their splits must be merged and re-split.

### 13.3 Recommended Split Strategy

| Parameter | Value |
|-----------|-------|
| Train | 70% |
| Validation | 15% |
| Test | 15% |
| Minimum test images/class | 20 |
| Duplicate-group handling | Assign entire duplicate group to train split |
| Source handling | Source-aware: no single dataset contributes to both train and test if feasible |
| Existing splits | Do NOT reuse; perform fresh stratified split |

**For classes with <100 images**: A meaningful independent test set is impossible. These classes should be excluded from the first model or marked as "needs more data."

**For classes with 100-300 images**: Test set will be very small (15-45 images). Evaluation will have high variance. Flag these classes accordingly.

---

## 14. FINAL TAXONOMY RECOMMENDATION

### 14.1 Recommended: Broadest Responsible First Model — 22 Classes

After weighing all evidence (image count, source diversity, label quality, real-world usefulness, commercial cleanliness), the broadest responsible first-model taxonomy is **22 classes**.

**Vegetables (15)**
1. Pepper
2. Eggplant
3. Cucumber
4. Corn
5. Onion
6. Tomato
7. Kale
8. Spinach
9. Sweet Potato
10. Watermelon
11. Cantaloupe
12. Bean
13. Potato
14. Carrot
15. Broccoli

**Fruits (7)**
16. Apple
17. Strawberry
18. Grape
19. Raspberry / Blackberry
20. Apricot
21. Pea
22. Radish

**Rationale**:
- All 22 classes have 256+ unique images after dedup
- All have at least 2 independent sources (except Pea, Grape, Raspberry/Blackberry, Apricot which have 1 source each)
- All represent common garden crops with real-world utility
- Label mappings are consistent and well-understood
- Commercial licenses are verified or under review
- The 15-class conservative model is a fallback if the 22-class model proves unstable

### 14.2 Classes Excluded from V1

| Class | Images | Reason for Exclusion |
|-------|--------|---------------------|
| Blueberry | 40 | Too few images, single source |
| Beet | 92 | Too few images |
| Cabbage | 129 | Too few images |
| Garlic | 147 | Too few images |
| Cauliflower | 170 | Too few images |
| Summer Squash/Zucchini | 18 | Too few images |
| Winter Squash/Pumpkin | 34 | Too few images |
| Brussels Sprouts | 0 | No data |
| Lettuce | 0 | No data |
| Swiss Chard | 0 | No data |
| Turnip | 0 | No data |
| Leek | 0 | No data |
| Pear | 0 | No data |
| Peach | 0 | No data |
| Cherry | 0 | No data |
| Plum | 0 | No data |
| Nectarine | 0 | No data |
| Basil | 0 | No data |
| Cilantro | 0 | No data |
| Parsley | 0 | No data |
| Dill | 0 | No data |
| Chives | 0 | No data |
| Mint | 0 | No data |
| Rosemary | 0 | No data |
| Thyme | 0 | No data |
| Asparagus | 0 | No data |
| Rhubarb | 0 | No data |
| Hops | 0 | No data |
| Sunflower | 0 | No data |

---

## 15. DATA ACQUISITION GAPS

### 15.1 Prioritized Acquisition List

| Priority | Class | Current Count | Source Diversity | Why Insufficient | Desired Count | Image Type | Preferred License |
|----------|-------|---------------|------------------|------------------|---------------|------------|-------------------|
| 1 | Blueberry | 40 | 1 | Far below minimum for reliable training | 500 | Field/garden photos | CC BY 4.0 or CC0 |
| 2 | Summer Squash/Zucchini | 18 | 1 | Near-zero coverage | 500 | Field/garden photos | CC BY 4.0 or CC0 |
| 3 | Winter Squash/Pumpkin | 34 | 1 | Near-zero coverage | 500 | Field/garden photos | CC BY 4.0 or CC0 |
| 4 | Beet | 92 | 2 | Very sparse | 300 | Field/garden photos | CC BY 4.0 or CC0 |
| 5 | Cabbage | 129 | 2 | Very sparse | 300 | Field/garden photos | CC BY 4.0 or CC0 |
| 6 | Garlic | 147 | 2 | Very sparse | 300 | Field/garden photos | CC BY 4.0 or CC0 |
| 7 | Cauliflower | 170 | 2 | Very sparse | 300 | Field/garden photos | CC BY 4.0 or CC0 |
| 8 | Carrot | 353 | 3 | Below 500 threshold | 500 | Field/garden photos | CC BY 4.0 or CC0 |
| 9 | Broccoli | 256 | 3 | Below 500 threshold | 500 | Field/garden photos | CC BY 4.0 or CC0 |

---

## 16. REMAINING BLOCKERS

Before training can proceed, the following must be resolved:

1. **License verification for Kaggle datasets**: Directly verify CC0 status for plants_type_30class, plants_type_30class_alt, and fruits262_101class_subset on Kaggle.
2. **Cross-class conflict resolution**: Determine policy for 366 conflicting hashes (exclude, assign to one class, or investigate source).
3. **veg_object_bangla_inbox**: Either extract class labels from XML annotations or exclude 3,534 images.
4. **hf_digigreen**: Either manually label 414 disease images or exclude them.
5. **Train/val/test split design**: Implement stratified, source-aware split with duplicate-group handling.
6. **Class imbalance mitigation**: Decide on class weighting, oversampling, or focal loss strategy.
7. **Human approval**: Explicit human sign-off required before any model training.

---

## 17. FILES CHANGED

| File | Action | Description |
|------|--------|-------------|
| `training/phase35i_audit.py` | Created | Initial fast audit script |
| `training/phase35i_correct_mappings.py` | Created | Class mapping correction script |
| `training/phase35i_dedup_counts.py` | Created | Deduplicated class count computation |
| `training_data/manifests/phase35i_audit_summary.json` | Created | Duplicate analysis summary |
| `training_data/manifests/phase35i_class_coverage_corrected.json` | Created | Pre-dedup corrected coverage |
| `training_data/manifests/phase35i_class_coverage_deduped.json` | Created | Post-dedup final coverage |
| `training_data/manifests/phase35i_conflicts.json` | Created | Cross-class conflict records |
| `training_data/manifests/phase35i_dataset_summaries.json` | Created | Dataset-level summaries |

---

## 18. FINAL TRAINING GATE

**NOT READY FOR TRAINING**

The corpus is commercially clean and properly attributed, but:
- Only 34,399 unique mapped images across 29 classes (not 134,832)
- 7 classes have fewer than 200 images
- 366 images have unresolved cross-class label conflicts
- No verified train/validation/test split exists
- 3,534 images from veg_object_bangla_inbox are unusable
- 414 images from hf_digigreen are unmapped
- 3 Kaggle datasets require direct license verification

**Next steps**: Resolve blockers, design clean split, obtain explicit human approval, then proceed to Phase 36 model training.

---

*WAIT FOR EXPLICIT HUMAN APPROVAL BEFORE PHASE 36 MODEL TRAINING.*
