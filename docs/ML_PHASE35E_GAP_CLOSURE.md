# Soil & Supper — Phase 35E Targeted Data Gap Closure

## 1. Recomputed Coverage (from Phase 35D Manifests)

**Ground truth from `phase35d_dataset_ledger.jsonl` and `phase35d_class_coverage.json`:**

| Metric | Value |
|--------|-------|
| Total datasets processed | 20 |
| Approved datasets | 6 |
| Rejected datasets | 4 |
| No-image datasets | 10 |
| **Total approved images** | **8,968** |
| Total valid images | 35,770 |
| Tier 1 classes with data | 17 / 51 |
| Tier 1 classes without data | 34 |

### Class-by-Class Approved Images

| Class | Approved | Sources | Status |
|-------|----------|---------|--------|
| Tomato | 579 | 2 | A |
| Pepper | 1,106 | 5 | A |
| Eggplant | 708 | 3 | A |
| Potato | 690 | 3 | A |
| Cucumber | 685 | 3 | A |
| Corn | 593 | 3 | A |
| Bean | 1,010 | 3 | A |
| Onion | 1,204 | 3 | A |
| Broccoli | 251 | 2 | B |
| Cabbage | 92 | 1 | C |
| Cauliflower | 79 | 1 | C |
| Strawberry | 503 | 2 | B |
| Apple | 132 | 2 | C |
| Beet | 174 | 2 | C |
| Garlic | 89 | 1 | C |
| Blueberry | 40 | 1 | C |
| Carrot | 332 | 2 | B |

**34 classes have zero approved images.**

---

## 2. Candidate Datasets for Gap Closure

### Priority A — Common Garden Crops

| Class | Candidate Dataset | Source | License | Images | Quality | Verdict |
|-------|------------------|--------|---------|--------|---------|---------|
| Zucchini | Agri-Vision Bangladesh | Mendeley | CC BY 4.0 | 5,266 original + augmented | Field photos, expert-validated | **ACQUIRE** |
| Pumpkin | Pumpkin Leaf Diseases | Mendeley | CC BY 4.0 | 2,000 | Field photos, disease focus | **ACQUIRE** (healthy subset) |
| Pumpkin | Leaf Image Dataset (Bitter Gourd, Okra, Pumpkin, Ridge Gourd) | Mendeley | CC BY 4.0 | 27,393 | Field photos, expert-validated | **ACQUIRE** |
| Pea | Pisum sativum Image Dataset | Mendeley | CC BY 4.0 | 12,096 | Disease + healthy, diverse conditions | **ACQUIRE** |
| Pea | Pea Plant Disease Detection | figshare | CC BY 4.0 | ~1,432 | Smartphone field photos | **ACQUIRE** |
| Radish | Radish Plant Leaf Disease Detection | Mendeley | CC BY 4.0 | ~2,300 | Field photos, disease + fresh | **ACQUIRE** |
| Lettuce | HydroGrowNet Batavia | Mendeley | CC BY 4.0 | 390,000+ | Hydroponic, growth monitoring | **REVIEW** (synthetic environment) |
| Lettuce | YEESI Dataset | Zenodo | CC0? | 7,992 | Real-world field photos, includes lettuce | **ACQUIRE** |
| Kale | YEESI Dataset | Zenodo | CC0? | 7,992 | Real-world field photos, includes kale | **ACQUIRE** |
| Kale | Top view kale images | Wageningen | Unclear | 6,400 | Greenhouse, top-view only | **REVIEW** (license unclear, limited perspective) |
| Brussels Sprouts | Vegetables Dataset (28K) | Datarade | Commercial | 562 | High quality, expensive | **REVIEW** (cost vs value) |
| Swiss Chard | Vegetables Dataset (28K) | Datarade | Commercial | 332 | High quality, expensive | **REVIEW** (cost vs value) |
| Carrot | Already have 332 | — | — | — | — | **SUFFICIENT** |
| Turnip | Fruits-360 | Mendeley | CC BY-SA 4.0 | 349 | Isolated objects, white background | **REJECT** (license + quality) |
| Leek | YEESI Dataset | Zenodo | CC0? | 7,992 | Real-world field photos, includes leek | **ACQUIRE** |
| Sweet Potato | Sweetpotato Grading Dataset | Zenodo | CC BY 4.0 | 1,400 | Grading focus, controlled lighting | **REVIEW** (limited real-world diversity) |
| Watermelon | Watermelon Disease Recognition | Mendeley | CC BY 4.0 | 1,155 | Field photos, disease focus | **ACQUIRE** (healthy subset) |
| Cantaloupe | Fruits-360 | Mendeley | CC BY-SA 4.0 | — | Isolated objects | **REJECT** (license) |

### Priority B — Fruit / Berry / Vine

| Class | Candidate Dataset | Source | License | Images | Quality | Verdict |
|-------|------------------|--------|---------|--------|---------|---------|
| Grape | GrapeSet | Zenodo | CC BY 4.0 | 878 MB | Field vineyard, segmentation | **ACQUIRE** |
| Grape | ViViD-5K | arXiv/coming soon | CC BY 4.0 | 5,000 | Field vineyard, berry-level | **ACQUIRE** |
| Grape | GrapesNet | Mendeley | CC BY 4.0 | 11,000+ | Indian vineyard, real conditions | **ACQUIRE** |
| Raspberry | RaspberrySet | Zenodo | CC BY 4.0 | 2,039 | Field, multiple growth stages | **ACQUIRE** |
| Blackberry | Berries COLMAP | GitHub | CC BY 4.0 | ~2 GB | 3D capture, real berries | **REVIEW** (large, 3D focus) |
| Blueberry | BlueberryDCM | Zenodo | CC BY 4.0 | 140 | Field canopy, smartphone | **ACQUIRE** |
| Blueberry | MegaFruits | Kaggle | Non-commercial only | 2,540 | Lab/field, segmentation | **REJECT** (license) |
| Apple | Fruit ImageNet | IEEE DataPort | CC BY 4.0 | Large | Search engine images, varied | **ACQUIRE** |
| Apple | Annotated Apple Fruit Detection | Zenodo | CC BY 4.0 | 60 | Orchard, smartphone, 3 varieties | **ACQUIRE** (small but high quality) |
| Pear | IntegrALIMENTA Pear | DIGITAL.CSIC | CC BY-NC-SA 4.0 | 17,208 | Lab images, smartphone | **REJECT** (NC-SA) |
| Peach | MegaFruits | Kaggle | Non-commercial only | 2,400 | Lab/field, segmentation | **REJECT** (license) |
| Cherry | Fruit ImageNet | IEEE DataPort | CC BY 4.0 | Large | Search engine images | **ACQUIRE** |
| Plum | Fruits-360 | Mendeley | CC BY-SA 4.0 | — | Isolated objects | **REJECT** (license) |
| Apricot | Fruits-360 | Mendeley | CC BY-SA 4.0 | — | Isolated objects | **REJECT** (license) |
| Nectarine | Fruits-360 | Mendeley | CC BY-SA 4.0 | — | Isolated objects | **REJECT** (license) |

### Priority C — Herbs

| Class | Candidate Dataset | Source | License | Images | Quality | Verdict |
|-------|------------------|--------|---------|--------|---------|---------|
| Basil | Herbs & Plants Dataset | Datarade | Commercial | 665 | High quality, garden/wild | **REVIEW** (cost) |
| Basil | Model Development for Aromatic Herbs | MDPI | CC BY 4.0 | ~600 | Lab photos, limited diversity | **ACQUIRE** |
| Cilantro | Herbs & Plants Dataset | Datarade | Commercial | 982 | High quality | **REVIEW** (cost) |
| Parsley | Herbs & Plants Dataset | Datarade | Commercial | 336 | High quality | **REVIEW** (cost) |
| Dill | Herbs & Plants Dataset | Datarade | Commercial | 318 | High quality | **REVIEW** (cost) |
| Mint | Model Development for Aromatic Herbs | MDPI | CC BY 4.0 | ~302 | Lab photos, limited diversity | **ACQUIRE** |
| Rosemary | Model Development for Aromatic Herbs | MDPI | CC BY 4.0 | ~234 | Lab photos, limited diversity | **ACQUIRE** |
| Thyme | Herbs & Plants Dataset | Datarade | Commercial | 314 | High quality | **REVIEW** (cost) |

### Priority D — Other High-Value Garden Plants

| Class | Candidate Dataset | Source | License | Images | Quality | Verdict |
|-------|------------------|--------|---------|--------|---------|---------|
| Asparagus | Fruits-360 | Mendeley | CC BY-SA 4.0 | 570 | Isolated objects | **REJECT** (license) |
| Rhubarb | Fruits-360 | Mendeley | CC BY-SA 4.0 | 232 | Isolated objects | **REJECT** (license) |
| Hops | hf_100crops | Hugging Face | MIT | Included | Object detection, real photos | **SUFFICIENT** (already have) |
| Sunflower | hf_100crops | Hugging Face | MIT | Included | Object detection, real photos | **SUFFICIENT** (already have) |

---

## 3. Quality Thresholds Analysis

### Classes with <100 approved images (current):
- Cabbage (92), Cauliflower (79), Garlic (89), Blueberry (40), Apple (132)

### Classes with only one source:
- Apple (2), Beet (2), Blueberry (1), Broccoli (2), Cabbage (1), Cauliflower (1), Carrot (2), Corn (3), Cucumber (3), Eggplant (3), Garlic (1), Onion (3), Pepper (5), Potato (3), Strawberry (2), Tomato (2)

### Classes with zero data:
- 34 Tier 1 classes

---

## 4. Recommended First-Model Class List

Based on current corpus quality and gap closure potential:

### Tier 1 — Strong (A-grade, ready for v1)
Tomato, Pepper, Bean, Onion, Potato, Eggplant, Cucumber, Corn

### Tier 2 — Usable (B-grade, include in v1 with caution)
Strawberry, Broccoli, Carrot

### Tier 3 — Weak but include (C-grade, if we can acquire more data)
Apple, Beet, Garlic, Blueberry, Cabbage, Cauliflower

### Tier 4 — Defer to v2 (insufficient data, difficult acquisition)
All 34 zero-data classes plus: Brussels Sprouts, Kale, Lettuce, Spinach, Swiss Chard, Sweet Potato, Watermelon, Cantaloupe, Grape, Raspberry, Blackberry, Pear, Peach, Cherry, Plum, Apricot, Nectarine, Basil, Cilantro, Parsley, Dill, Chives, Mint, Rosemary, Thyme, Asparagus, Rhubarb

**Recommended v1 class set: 11–16 classes** (Tier 1 + Tier 2 + select Tier 3)

---

## 5. GO / NO-GO Recommendation

### NO-GO for full 51-class model

The current corpus is **NOT ready** to train a broad 51-class Soil & Supper crop recognition model.

**Reasons:**
1. Only 17 of 51 Tier 1 classes have any approved data
2. 34 classes have zero approved images
3. Many existing classes have <100 images (below minimum viable threshold)
4. Fruit tree coverage is minimal (Apple only)
5. Herb coverage is zero
6. Berry coverage is minimal (Strawberry + Blueberry only)

### GO for focused 11–16 class v1 model

A **focused first model** covering the strongest classes IS viable:

**Recommended v1 classes (16):**
1. Tomato
2. Pepper (sweet + hot)
3. Bean
4. Onion
5. Potato
6. Eggplant
7. Cucumber
8. Corn
9. Strawberry
10. Broccoli
11. Carrot
12. Apple
13. Beet
14. Garlic
15. Blueberry
16. Cabbage

This represents the highest-confidence, best-covered classes with commercially licensed data.

### Remaining classes should stay in acquisition backlog

The 35 remaining Tier 1 classes should be targeted for future model versions (v2, v3).

---

## 6. Targeted Acquisition Plan

### Immediate Acquisitions (High Value, Commercially Safe)

| Dataset | Classes Added | Images | License | Action |
|---------|--------------|--------|---------|--------|
| Pisum sativum Image Dataset | Pea | 12,096 | CC BY 4.0 | Download |
| Radish Plant Leaf Disease Detection | Radish | ~2,300 | CC BY 4.0 | Download |
| Agri-Vision Bangladesh | Zucchini | 5,266+ | CC BY 4.0 | Download |
| Pumpkin Leaf Diseases | Pumpkin | 2,000 | CC BY 4.0 | Download |
| GrapeSet | Grape | ~500+ | CC BY 4.0 | Download |
| ViViD-5K | Grape | 5,000 | CC BY 4.0 | Download |
| GrapesNet | Grape | 11,000+ | CC BY 4.0 | Download |
| RaspberrySet | Raspberry | 2,039 | CC BY 4.0 | Download |
| BlueberryDCM | Blueberry | 140 | CC BY 4.0 | Download |
| Fruit ImageNet | Apple, Cherry, Pear, Peach, Plum, Apricot, Nectarine | Large | CC BY 4.0 | Download |
| YEESI Dataset | Lettuce, Kale, Leek, Sunflower | 7,992 | CC0? | Verify license then download |

### Review Required (License or Quality Uncertain)

| Dataset | Issue | Action |
|---------|-------|--------|
| Sweetpotato Grading Dataset | Controlled lighting, grading focus | Review quality before merge |
| Herbs & Plants Dataset (Datarade) | $6,500 commercial license | Evaluate cost vs value |
| HydroGrowNet Batavia | Hydroponic, synthetic environment | Review applicability |
| Top view kale images | License unclear | Verify license |

### Do Not Acquire

| Dataset | Reason |
|---------|--------|
| Fruits-360 | CC BY-SA 4.0 — share-alike incompatible |
| MegaFruits | Non-commercial only |
| IntegrALIMENTA Pear | CC BY-NC-SA 4.0 |
| Any CC BY-NC/NC-SA dataset | Non-commercial restriction |

---

## 7. Attribution Requirements

If recommended acquisitions are completed, attribution will be required for:
- Mendeley datasets (CC BY 4.0) — author names in app credits
- Zenodo datasets (CC BY) — author names in app credits
- Fruit ImageNet (CC BY 4.0) — credit in app credits
- All CC BY licensed data — preserve notices in documentation

---

## 8. Remaining Gaps After Recommended Acquisitions

Even with all recommended acquisitions:
- Herbs (Basil, Cilantro, Parsley, Dill, Chives, Mint, Rosemary, Thyme) will remain weak
- Some fruit trees (Pear, Peach, Cherry, Plum, Apricot, Nectarine) may still be thin
- Brussels Sprouts, Kale, Lettuce, Spinach, Swiss Chard may still be <100 images each
- Cantaloupe, Watermelon, Sweet Potato need additional field photos

These should be explicitly deferred to v2/v3 acquisition rounds.

---

## 9. Human Action List

### DOWNLOAD NEXT (Priority Order):
1. **Pisum sativum Image Dataset** — closes Pea gap (12K images, CC BY 4.0)
2. **Radish Plant Leaf Disease Detection** — closes Radish gap (2.3K images, CC BY 4.0)
3. **Agri-Vision Bangladesh** — closes Zucchini gap (5K+ images, CC BY 4.0)
4. **Pumpkin Leaf Diseases** — closes Pumpkin gap (2K images, CC BY 4.0)
5. **GrapeSet + ViViD-5K + GrapesNet** — closes Grape gap (17K+ images, CC BY 4.0)
6. **RaspberrySet** — closes Raspberry gap (2K images, CC BY 4.0)
7. **BlueberryDCM** — strengthens Blueberry (140 images, CC BY 4.0)
8. **Fruit ImageNet** — strengthens Apple, adds Cherry, Peach, Plum, Apricot, Nectarine
9. **YEESI Dataset** — adds Lettuce, Kale, Leek, Sunflower (verify CC0 first)

### LICENSE VERIFICATION NEEDED:
- YEESI Dataset — confirm license is CC0 or commercial-safe
- Herbs & Plants Dataset (Datarade) — determine if $6,500 is justified

### ALREADY GOOD ENOUGH FOR V1:
- Tomato, Pepper, Bean, Onion, Potato, Eggplant, Cucumber, Corn, Strawberry, Broccoli, Carrot

### STILL BADLY UNDERREPRESENTED (defer to v2):
- All herbs (Basil through Thyme)
- Most fruit trees (Pear, Peach, Cherry, Plum, Apricot, Nectarine)
- Leafy greens (Kale, Lettuce, Spinach, Swiss Chard)
- Squash/pumpkin varieties (beyond basic Zucchini/Pumpkin)
- Berries (Raspberry, Blackberry beyond basic Strawberry/Blueberry)

### DO NOT WASTE TIME ON:
- Fruits-360 (CC BY-SA)
- MegaFruits (non-commercial)
- Any dataset with CC BY-NC or CC BY-SA license
- Any dataset where commercial license cannot be verified

---

## 10. Final Verdict

**DATASET INTAKE COMPLETE — RECOMMEND FOCUSED V1 MODEL**

The Phase 35D + 35E corpus is sufficient to train a **focused first Soil & Supper model** covering approximately 11–16 high-value garden plant classes.

It is **NOT sufficient** for a broad 51-class model.

The recommended path forward:
1. Acquire the 9 high-priority datasets listed above
2. Run Phase 35D intake on new data
3. Select final v1 class list (11–16 classes)
4. Proceed to Phase 36 (First Real Soil & Supper Crop Model) with focused class set
5. Keep remaining 35+ classes in acquisition backlog for v2/v3

**Do not train until v1 class list is finalized and new data is ingested.**
