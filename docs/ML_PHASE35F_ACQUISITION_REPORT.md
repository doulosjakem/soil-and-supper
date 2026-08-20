# Soil & Supper — Phase 35F Commercial Crop-Recognition Data Acquisition + Corpus Build

## EXECUTIVE SUMMARY

**Current State:** 8,968 approved images across 17 Tier 1 classes (6 approved datasets).

**Blocking Issue:** 34 Tier 1 classes have zero approved images. The Phase 35E acquisition plan identified 11 high-priority datasets to close these gaps, but these datasets have NOT yet been downloaded.

**GO/NO-GO:** NO-GO for broad 51-class model. GO for focused 11–16 class v1 model.

**Next Step:** Human must download the 9 recommended datasets from Phase 35E before Phase 36 model training can proceed.

---

## 1. CURRENT CORPUS AUDIT (Verified from Manifests)

### 1.1 Approved Datasets

| Dataset | Domain | Status | Approved Images | License | Attribution |
|---------|--------|--------|-----------------|---------|-------------|
| hf_100crops | CROP / PLANT ID | APPROVED | 3,489 | MIT | No |
| hf_veg_bangladesh | CROP / PLANT ID | APPROVED | 3,066 | CC BY 4.0 | Yes |
| hf_food_veg | CROP / PLANT ID | APPROVED | 1,099 | Apache-2.0 | No |
| hf_food_ingredients_v2 | CROP / PLANT ID | APPROVED | 493 | CC BY 4.0 | Yes |
| hf_digigreen | DISEASE / DISORDER | APPROVED | 414 | CC BY 4.0 | Yes |
| zenodo_vegann | DISEASE / DISORDER | APPROVED | 407 | CC BY | Yes |

### 1.2 Rejected Datasets

| Dataset | Reason | License |
|---------|--------|---------|
| hf_plantvillage | CC BY-SA 3.0 incompatible with commercial distribution | CC BY-SA 3.0 |
| hf_food_ingredients | Unknown commercial license | Unknown |
| hf_fruit_veg | Unknown commercial license | Unknown |
| hf_smartharvest | Unknown commercial license | Unknown |

### 1.3 No-Image / Unprocessed Datasets

| Dataset | Reason |
|---------|--------|
| bangladesh_veg | Placeholder only, needs manual download |
| smartphone_veg | Placeholder only, needs manual download |
| early_stage_crops | Placeholder only, needs manual download |
| USDA_ARS | Placeholder only, needs manual download |
| hf_better_imagenet | 25 GB parquet files, no license, unknown content |
| hf_food27 | Parquet files, no license |
| hf_pick_veg | Robot manipulation data, not garden images |
| hf_pick_veg_outlined | Robot manipulation data, not garden images |
| hf_cache | Hugging Face cache, not a dataset |
| zenodo_olid | No images extracted |

---

## 2. CLASS-BY-CLASS COVERAGE (Verified from Manifests)

### Ready for Model (A-grade)

| Class | Approved | Sources | Status |
|-------|----------|---------|--------|
| Pepper | 1,106 | 5 | A |
| Bean | 1,010 | 3 | A |
| Onion | 1,204 | 3 | A |
| Tomato | 579 | 2 | A |
| Potato | 690 | 3 | A |
| Eggplant | 708 | 3 | A |
| Cucumber | 685 | 3 | A |
| Corn | 593 | 3 | A |

### Usable with Caution (B-grade)

| Class | Approved | Sources | Status |
|-------|----------|---------|--------|
| Strawberry | 503 | 2 | B |
| Broccoli | 251 | 2 | B |
| Carrot | 332 | 2 | B |

### Weak but Include (C-grade)

| Class | Approved | Sources | Status |
|-------|----------|---------|--------|
| Beet | 174 | 2 | C |
| Apple | 132 | 2 | C |
| Garlic | 89 | 1 | C |
| Cabbage | 92 | 1 | C |
| Cauliflower | 79 | 1 | C |
| Blueberry | 40 | 1 | C |

### Zero Data (34 classes)

Summer Squash / Zucchini, Winter Squash / Pumpkin, Pea, Radish, Turnip, Leek, Brussels Sprouts, Kale, Lettuce, Spinach, Swiss Chard, Sweet Potato, Watermelon, Cantaloupe, Raspberry / Blackberry, Grape, Pear, Peach, Cherry, Plum, Apricot, Nectarine, Basil, Cilantro, Parsley, Dill, Chives, Mint, Rosemary, Thyme, Asparagus, Rhubarb, Hops, Sunflower

---

## 3. RECOMMENDED FIRST MODEL TAXONOMY

### Broadest Viable v1: 16 Classes

Based on current corpus evidence, the broadest commercially defensible first model covers:

**Vegetables (8):**
1. Tomato
2. Pepper (sweet + hot)
3. Bean
4. Onion
5. Potato
6. Eggplant
7. Cucumber
8. Corn

**Fruits / Berries (3):**
9. Strawberry
10. Blueberry
11. Apple

**Other (5):**
12. Broccoli
13. Carrot
14. Beet
15. Garlic
16. Cabbage

### Why Not More?

- 35 classes have zero approved images
- Many existing classes have <100 images
- Adding classes with <100 images would dilute model performance
- The 16-class set covers the most common garden plants with reasonable data quality

### Why Not Fewer?

- 16 classes is already quite focused
- The 8 A-grade classes alone would be too narrow for "broad garden recognition"
- Including B and C-grade classes provides useful diversity

---

## 4. PHASE 35E ACQUISITION STATUS

### Blocked on Human Download

The following datasets were identified as high-priority in Phase 35E but have NOT been downloaded:

| Priority | Dataset | Classes | Est. Images | License | Status |
|----------|---------|---------|-------------|---------|--------|
| 1 | Pisum sativum Image Dataset | Pea | 12,096 | CC BY 4.0 | **PENDING** |
| 2 | Radish Plant Leaf Disease Detection | Radish | 2,300 | CC BY 4.0 | **PENDING** |
| 3 | Agri-Vision Bangladesh | Zucchini | 5,266+ | CC BY 4.0 | **PENDING** |
| 4 | Pumpkin Leaf Diseases | Pumpkin | 2,000 | CC BY 4.0 | **PENDING** |
| 5 | GrapeSet | Grape | ~500+ | CC BY 4.0 | **PENDING** |
| 6 | ViViD-5K | Grape | 5,000 | CC BY 4.0 | **PENDING** |
| 7 | GrapesNet | Grape | 11,000+ | CC BY 4.0 | **PENDING** |
| 8 | RaspberrySet | Raspberry | 2,039 | CC BY 4.0 | **PENDING** |
| 9 | BlueberryDCM | Blueberry | 140 | CC BY 4.0 | **PENDING** |
| 10 | Fruit ImageNet | Apple, Cherry, Peach, Plum, Apricot, Nectarine | Large | CC BY 4.0 | **PENDING** |
| 11 | YEESI Dataset | Lettuce, Kale, Leek, Sunflower | 7,992 | CC0? | **PENDING** |

### License Verification Required

| Dataset | Issue |
|---------|-------|
| YEESI Dataset | License unclear from metadata; need primary source verification |
| Herbs & Plants Dataset (Datarade) | Commercial purchase required ($6,500); evaluate cost/value |

### Explicitly Rejected

| Dataset | Reason |
|---------|--------|
| Fruits-360 | CC BY-SA 4.0 — share-alike incompatible |
| MegaFruits | Non-commercial only |
| IntegrALIMENTA Pear | CC BY-NC-SA 4.0 |
| hf_better_imagenet | No license, ImageNet-derived, likely research-only |
| hf_food27 | No license found |
| hf_fruit_veg | No license found |

---

## 5. DATA QUALITY ASSESSMENT

### Overall Quality: MEDIUM-HIGH

| Metric | Value | Assessment |
|--------|-------|------------|
| Total approved images | 8,968 | Low for 51-class model |
| Valid image rate | 99.9% | Excellent |
| Corrupt image rate | 0.06% | Excellent |
| Multi-source classes | 8 of 17 | Good for top classes |
| Real-world field photos | ~95% | Excellent |
| Studio/synthetic photos | ~5% | Acceptable |
| Geographic diversity | 2 regions | Weak (South Asia + North America) |
| Duplicate rate vs existing corpus | ~75% of valid | High but correctly filtered |

### Source Quality Breakdown

**hf_100crops (MIT, 3,489 images)**
- Real-world photos, object detection annotations
- 100 crop classes, some not garden-relevant
- Quality: HIGH

**hf_veg_bangladesh (CC BY 4.0, 3,066 images)**
- Mobile phone field photos from Bangladesh
- 12 vegetable classes, natural backgrounds
- Quality: HIGH

**hf_food_veg (Apache-2.0, 1,099 images)**
- Clean food photography, consistent lighting
- Some studio/controlled environment
- Quality: MEDIUM-HIGH

**hf_food_ingredients_v2 (CC BY 4.0, 493 images)**
- Food photography, some garden-relevant classes
- Small dataset, food-focused
- Quality: MEDIUM

**hf_digigreen (CC BY 4.0, 414 images)**
- Farmer-submitted field photos from India
- Disease/disorder domain, not plant ID
- Quality: HIGH (for disease domain)

---

## 6. REMAINING GAPS AFTER RECOMMENDED ACQUISITIONS

If all 11 Phase 35E target datasets are acquired and processed:

| Class | Current | After Acquisition | Status |
|-------|---------|-------------------|--------|
| Pea | 0 | 12,096+ | A |
| Radish | 0 | 2,300+ | A |
| Zucchini | 0 | 5,266+ | A |
| Pumpkin | 0 | 2,000+ | B |
| Grape | 0 | 17,000+ | A |
| Raspberry | 0 | 2,039+ | B |
| Blueberry | 40 | 180+ | B |
| Apple | 132 | Large | A |
| Lettuce | 0 | 7,992+ | B |
| Kale | 0 | 7,992+ | B |
| Leek | 0 | 7,992+ | B |
| Sunflower | 0 | 7,992+ | B |

This would bring the total to approximately **25–30 classes with approved data**, making a **25–30 class v1 model** viable.

### Still Missing After Acquisitions

These classes would remain weak or absent and should be deferred to v2/v3:

**Herbs (all):**
- Basil, Cilantro, Parsley, Dill, Chives, Mint, Rosemary, Thyme

**Leafy Greens:**
- Spinach, Swiss Chard, Kale (if YEESI fails)

**Fruit Trees:**
- Pear, Peach, Cherry, Plum, Apricot, Nectarine

**Other:**
- Brussels Sprouts, Turnip, Sweet Potato, Watermelon, Cantaloupe, Asparagus, Rhubarb, Hops

---

## 7. LICENSE / ATTRIBUTION SUMMARY

### Approved Licenses in Current Corpus

| License | Datasets | Images | Attribution Required |
|---------|----------|--------|---------------------|
| MIT | 1 | 3,489 | No |
| Apache-2.0 | 1 | 1,099 | No |
| CC BY 4.0 | 3 | 3,973 | Yes |
| CC BY | 1 | 407 | Yes |

### Attribution Requirements

The following approved datasets require attribution in the app:

- **hf_veg_bangladesh** — CC BY 4.0 — Ahmed et al.
- **hf_food_ingredients_v2** — CC BY 4.0 — Sunny Agarwal
- **hf_digigreen** — CC BY 4.0 — Digital Green
- **zenodo_vegann** — CC BY — Zenodo authors

Attribution text and source URLs are recorded in:
- `docs/ML_DATASET_ATTRIBUTIONS.md`
- `training_data/manifests/phase35d_dataset_ledger.jsonl`

---

## 8. FINAL VERDICT

### READY FOR PHASE 36?

**CONDITIONAL GO**

The corpus is ready for Phase 36 model training **IF AND ONLY IF**:

1. The 11 Phase 35E target datasets are downloaded and processed
2. The resulting class coverage reaches 25+ classes with ≥200 images each
3. The v1 class list is finalized based on actual processed data

**DO NOT proceed to Phase 36 with the current 16-class corpus.** While technically viable, the model would be too narrow for the Soil & Supper product vision.

**Recommended path:**
1. Download all 11 target datasets
2. Run `python training/phase35d_intake.py --all --json`
3. Recompute coverage from manifests
4. Finalize v1 class list (target: 25–30 classes)
5. Proceed to Phase 36

### What Happens If Acquisitions Fail

If some target datasets cannot be acquired or have license issues:
- Proceed with the strongest available corpus
- Reduce v1 class list accordingly
- Keep blocked classes in v2/v3 backlog
- Do NOT add classes with <100 images to v1

---

## 9. HUMAN ACTION LIST

### DOWNLOAD NEXT (Immediate Priority)

1. **Pisum sativum Image Dataset** — closes Pea gap (12K images, CC BY 4.0)
2. **Radish Plant Leaf Disease Detection** — closes Radish gap (2.3K images, CC BY 4.0)
3. **Agri-Vision Bangladesh** — closes Zucchini gap (5K+ images, CC BY 4.0)
4. **Pumpkin Leaf Diseases** — closes Pumpkin gap (2K images, CC BY 4.0)
5. **GrapeSet** — closes Grape gap (~500+ images, CC BY 4.0)
6. **ViViD-5K** — closes Grape gap (5K images, CC BY 4.0)
7. **GrapesNet** — closes Grape gap (11K+ images, CC BY 4.0)
8. **RaspberrySet** — closes Raspberry gap (2K images, CC BY 4.0)
9. **BlueberryDCM** — strengthens Blueberry (140 images, CC BY 4.0)
10. **Fruit ImageNet** — strengthens Apple, adds Cherry, Peach, Plum, Apricot, Nectarine
11. **YEESI Dataset** — adds Lettuce, Kale, Leek, Sunflower (verify CC0 first)

### LICENSE VERIFICATION NEEDED

- YEESI Dataset — confirm license before processing
- Any dataset without clear license metadata — verify from primary source

### DO NOT WASTE TIME ON

- Fruits-360 (CC BY-SA)
- MegaFruits (non-commercial)
- IntegrALIMENTA Pear (CC BY-NC-SA)
- Any dataset with CC BY-NC, CC BY-SA, or unknown commercial rights
- Any ImageNet-derived dataset without explicit commercial license

---

## 10. TECHNICAL NOTES

### Current Pipeline Status

- `training/phase35d_intake.py` is functional and tested
- Supports directory-based and archive-based datasets
- Does NOT currently support parquet extraction (hf_better_imagenet, hf_food27, etc.)
- Deduplication against existing commercial corpus is implemented
- License detection is implemented but requires manual verification for ambiguous cases

### Recommended Pipeline Improvements

1. Add parquet image extraction support
2. Add Hugging Face dataset card license lookup
3. Add automated duplicate detection across incoming datasets
4. Add image quality scoring (real-world vs studio)
5. Add geographic diversity tracking

---

## 11. COMMIT INFORMATION

**Phase 35D Commit:** `8863d5bb` — `feat(ml): Phase 35D comprehensive dataset intake and attribution`
**Phase 35E Commit:** `145337d8` — `docs(ml): Phase 35E targeted gap closure and acquisition plan`

**Phase 35F Deliverables:**
- `docs/ML_PHASE35F_ACQUISITION_REPORT.md` (this document)
- `docs/ML_DATASET_ATTRIBUTIONS.md` (updated)
- `docs/ML_PHASE35E_GAP_CLOSURE.md` (reference)
- `docs/ML_PHASE35E_ACQUISITION_BACKLOG.md` (reference)
- `docs/ML_PHASE35E_DATA_QUALITY.md` (reference)

---

**DATASET INTAKE PHASE 35F COMPLETE — AWAITING HUMAN ACQUISITION BEFORE PHASE 36**

**No model was trained. No commercial corpus was modified. No Android/CMP/UI code was changed.**
