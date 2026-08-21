# Soil & Supper — Phase 35H Autonomous Corpus Discovery & Assessment

## 1. INBOX INVENTORY

**Location:** `D:\soil-and-supper\soil-and-supper\training_data\inbox`

### Archives Discovered

| Archive | Size (MB) | Images | Status |
|---------|-----------|--------|--------|
| A Comprehensive Image Dataset of Vegetables Grown in Bangladesh.zip | 7,422 | 3,754 | Extracted |
| archive (1).zip | 69 | 4,449 | Extracted |
| archive (2).zip | 446 | 1,591 | Extracted |
| archive (3).zip | 363 | 733 | Extracted |
| archive (5).zip | 766 | 6,878 | Extracted |
| archive (6).zip | 0.1 | 0 | Extracted (CSV only) |
| archive (7).zip | 5.6 | 0 | Extracted (FAO metadata) |
| archive (8).zip | 937 | 30,000 | Extracted |
| archive (9).zip | 205 | 13,740 | Extracted |
| archive (10).zip | 627 | 50,000 | Extracted |
| archive (11).zip | 155 | 1,167 | Extracted |
| archive (13).zip | 61 | 2,616 | Extracted |
| archive.zip | 435 | 25,001 | Extracted |
| d7kbzjr83k-1.zip | 2,613 | 2,836 | Extracted |
| Vegetable Image Dataset for Classification Models A Bangladeshi Perspective.zip | 1,979 | 4,319 | Extracted |
| Vegetable Object Detection Dataset from Bangladesh.zip | 217 | 3,534 | Extracted |
| VegNet Vegetable Dataset with quality (Unripe, Ripe, Old, Dried and Damaged).zip | 121 | 6,150 | Extracted |
| last batch/archive (1).zip | 1,375 | 30,000 | Extracted |
| last batch/archive (2).zip | 7,269 | 335,456 | Extracted (Fruits-360) |
| last batch/archive (3).zip | 1,375 | 30,000 | Extracted |
| last batch/archive (4).zip | 24,237 | 176,744 | Extracted |
| last batch/archive (5).zip | 5,205 | 112,693 | Extracted |
| last batch/archive (6).zip | 3,269 | 11,078 | Extracted |
| last batch/archive (7).zip | 627 | 50,000 | Extracted |
| last batch/archive.zip | 3,269 | 11,078 | Extracted |

**Total archives:** 26
**Total extracted directories:** 26

---

## 2. DATASET IDENTIFICATION

### 2.1 Identified Datasets

| # | Archive | Likely Dataset | Classes | Images | Domain | License Status |
|---|---------|---------------|---------|--------|--------|----------------|
| 1 | A Comprehensive Image Dataset... | Agri-Vision Bangladesh / BanglaVeg | 42 vegetables | 3,754 | CROP | CC BY 4.0 (from Mendeley) |
| 2 | archive (1) | Insects (Butterfly, Dragonfly, Grasshopper, Ladybird, Mosquito) | 5 | 4,449 | INSECT | Unknown |
| 3 | archive (2) | Farm insects | 1+ | 1,591 | INSECT | Unknown |
| 4 | archive (3) | Flowers | 1+ | 733 | FLOWER | Unknown |
| 5 | archive (5) | Plant disease (Alfalfa, Asparagus, etc.) | Multiple | 6,878 | DISEASE | Unknown |
| 6 | archive (8) / last_batch_archive__1_ / last_batch_archive__7_ | 30 Plant Types (Kaggle/dima806) | 30 | 90,000 | CROP | Unknown |
| 7 | archive (9) | Flowers (14 classes) | 14 | 13,740 | FLOWER | Unknown |
| 8 | archive (10) / last_batch_archive__7_ | Fruits-30 / Fruit classification | 31 | 100,000 | FRUIT | Unknown |
| 9 | archive (11) | Bean disease (3 classes) | 3 | 1,167 | DISEASE | Unknown |
| 10 | archive (13) | Pest dataset (aphids, etc.) | Multiple | 2,616 | PEST | Unknown |
| 11 | archive | ImageClassesCombinedWithCOCOAnnotations + Insect Classes | Multiple | 25,001 | MIXED | Unknown |
| 12 | d7kbzjr83k-1 | Plant disease dataset (Mendeley ID) | Multiple | 2,836 | DISEASE | Unknown |
| 13 | Vegetable Image Dataset... | BanglaVeg (Mendeley) | 12 | 4,319 | CROP | CC BY 4.0 |
| 14 | Vegetable Object Detection... | Bangladesh vegetable detection | 22 | 3,534 | CROP | CC BY 4.0 |
| 15 | VegNet Vegetable Dataset... | VegNet quality dataset | Multiple | 6,150 | CROP | CC BY 4.0 |
| 16 | last_batch_archive | Weed classes (Black-grass, Charlock, etc.) | 13 | 11,078 | WEED | Unknown |
| 17 | last_batch_archive__2_ | **Fruits-360** | 194 | 335,456 | FRUIT | **CC BY-SA 4.0 — REJECT** |
| 18 | last_batch_archive__3_ | Duplicate of #6 | 30 | 30,000 | CROP | Unknown |
| 19 | last_batch_archive__4_ | Pathogen/bacteria dataset | Multiple | 176,744 | DISEASE | Unknown |
| 20 | last_batch_archive__5_ | Insect pest dataset | 102 | 112,693 | PEST | Unknown |
| 21 | last_batch_archive__6_ | Duplicate of #16 | 13 | 11,078 | WEED | Unknown |

### 2.2 Duplicate Detection

| Dataset | Duplicate Of | Evidence |
|---------|--------------|----------|
| last_batch_archive__3_ | archive _10_ / last_batch_archive__7_ | Same 30 classes, same structure |
| last_batch_archive__6_ | last_batch_archive | Same 13 weed classes, identical structure |

---

## 3. LICENSE VERIFICATION

### 3.1 Verified Licenses

| Dataset | License | Commercial | Attribution |
|---------|---------|------------|-------------|
| A Comprehensive Image Dataset... | CC BY 4.0 | YES | Yes |
| Vegetable Image Dataset... | CC BY 4.0 | YES | Yes |
| Vegetable Object Detection... | CC BY 4.0 | YES | Yes |
| VegNet Vegetable Dataset... | CC BY 4.0 | YES | Yes |
| **Fruits-360** | **CC BY-SA 4.0** | **NO** | **Yes (but share-alike incompatible)** |

### 3.2 Unknown Licenses

The following datasets have no README/LICENSE files and their primary source could not be immediately determined from local metadata:

- archive (1) — Insects
- archive (2) — Farm insects
- archive (3) — Flowers
- archive (5) — Plant disease
- archive (8) — 30 Plant Types
- archive (9) — Flowers
- archive (10) — Fruits-30
- archive (11) — Bean disease
- archive (13) — Pest
- archive — Mixed
- d7kbzjr83k-1 — Plant disease
- last_batch_archive — Weeds
- last_batch_archive__4_ — Pathogen
- last_batch_archive__5_ — Insect pest

**These datasets require primary-source verification before commercial approval.**

---

## 4. COMMERCIAL ASSESSMENT

### 4.1 APPROVED for Commercial Corpus

| Dataset | License | Images | Classes | Domain |
|---------|---------|--------|---------|--------|
| A Comprehensive Image Dataset... | CC BY 4.0 | 3,754 | 42 | CROP |
| Vegetable Image Dataset... | CC BY 4.0 | 4,319 | 12 | CROP |
| Vegetable Object Detection... | CC BY 4.0 | 3,534 | 22 | CROP |
| VegNet Vegetable Dataset... | CC BY 4.0 | 6,150 | Multiple | CROP |

**Total approved images from verified datasets:** 17,757

### 4.2 REJECTED

| Dataset | Reason |
|---------|--------|
| Fruits-360 (last_batch_archive__2_) | CC BY-SA 4.0 — share-alike incompatible with commercial distribution |

### 4.3 PENDING LICENSE REVIEW

All other datasets require primary-source license verification.

---

## 5. TAXONOMY MAPPING (Verified Datasets Only)

### 5.1 A Comprehensive Image Dataset of Vegetables Grown in Bangladesh

**Source classes (42):**
Arum lobe, Ash gourd, Beetroot, Bitter melon, Bottle gourd, Broccoli, Cabbage, Capsicum, Carrot, Cauliflower, Chives onion, Chili, Coconut, Coriander, Cucumber, Eggplant, Elephant foot yam, Flat bean, Garlic, Ginger, Gooseberry, Green papaya, Green spinach, Jicama, Kohlrabi, Lime, Malabar spinach seed, Okra, Onion, Plantain, Pointed gourd, Potato, Pumpkin, Radish, Radish leaves, Red amaranth, Shaluk, Snake gourd, Taro, Tomato, Yardlong bean, Zucchini

**Mapped to Soil & Supper:**
- Tomato → Tomato
- Capsicum → Pepper
- Cucumber → Cucumber
- Eggplant → Eggplant
- Broccoli → Broccoli
- Cabbage → Cabbage
- Carrot → Carrot
- Onion → Onion
- Potato → Potato
- Pumpkin → Winter Squash / Pumpkin
- Radish → Radish
- Zucchini → Summer Squash / Zucchini
- Flat bean → Bean
- Garlic → Garlic
- Kohlrabi → Kohlrabi (candidate)
- Okra → Bean
- Chili → Pepper
- Beetroot → Beet
- Cauliflower → Cauliflower
- Green spinach → Spinach
- Malabar spinach → Spinach
- Pointed gourd → (candidate)
- Bitter melon → (candidate)
- Bottle gourd → (candidate)
- Elephant foot yam → (candidate)
- Snake gourd → (candidate)
- Taro → (candidate)
- Yardlong bean → Bean
- Shaluk → (candidate)
- Jicama → (candidate)
- Coconut → (candidate)
- Lime → (candidate)
- Plantain → Banana (candidate)
- Red amaranth → (candidate)
- Gooseberry → (candidate)
- Green papaya → Papaya (candidate)
- Coriander → Cilantro
- Chives onion → Chives
- Ginger → Ginger (candidate)
- Ash gourd → (candidate)
- Arum lobe → (candidate)

### 5.2 Vegetable Image Dataset for Classification Models A Bangladeshi Perspective

**Source classes (12):**
Potato, Onion, Green Chili, Garlic, Radish, Bean, Ladies Finger, Cucumber, Pointed Gourd, Bitter Melon, Brinjal, Tomato

**Mapped to Soil & Supper:**
- Potato → Potato
- Onion → Onion
- Green Chili → Pepper
- Garlic → Garlic
- Radish → Radish
- Bean → Bean
- Ladies Finger → Bean
- Cucumber → Cucumber
- Pointed Gourd → (candidate)
- Bitter Melon → (candidate)
- Brinjal → Eggplant
- Tomato → Tomato

### 5.3 Vegetable Object Detection Dataset from Bangladesh

**Source classes (22):**
Beetroot, Bitter Gourd, Bottle Gourd, Cabbage, Capsicum, Carrots, Cauliflower, Coriander leaves, Cucumber, Eggplant, Green Banana, Green Beans, Green Chilli, Green Papaya, Lemon, Potato, Pumpkin, Radish, Snake Gourd, Spring Onion, Tomato, Turnip

**Mapped to Soil & Supper:**
- Beetroot → Beet
- Bitter Gourd → (candidate)
- Bottle Gourd → (candidate)
- Cabbage → Cabbage
- Capsicum → Pepper
- Carrots → Carrot
- Cauliflower → Cauliflower
- Coriander leaves → Cilantro
- Cucumber → Cucumber
- Eggplant → Eggplant
- Green Banana → Banana (candidate)
- Green Beans → Bean
- Green Chilli → Pepper
- Green Papaya → Papaya (candidate)
- Lemon → Lemon (candidate)
- Potato → Potato
- Pumpkin → Winter Squash / Pumpkin
- Radish → Radish
- Snake Gourd → (candidate)
- Spring Onion → Onion
- Tomato → Tomato
- Turnip → Turnip

### 5.4 VegNet Vegetable Dataset

**Source classes:** Multiple quality classes (Unripe, Ripe, Old, Dried, Damaged) for various vegetables

**Mapped to Soil & Supper:**
- Depends on actual vegetable classes in dataset
- Quality/ripeness labels are NOT plant identity labels
- Only the vegetable type should be used for taxonomy mapping

---

## 6. CLASS COVERAGE (Verified Datasets Only)

| Soil & Supper Class | A Comprehensive... | Veg Bangla... | Veg Object... | VegNet | Total |
|---------------------|-------------------|---------------|---------------|--------|-------|
| Tomato | Yes | Yes | Yes | Unknown | 3+ |
| Pepper | Yes (Capsicum, Chili) | Yes (Green Chili) | Yes (Capsicum, Green Chilli) | Unknown | 3+ |
| Eggplant | Yes | Yes (Brinjal) | Yes | Unknown | 3+ |
| Potato | Yes | Yes | Yes | Unknown | 3+ |
| Cucumber | Yes | Yes | Yes | Unknown | 3+ |
| Carrot | Yes | No | Yes (Carrots) | Unknown | 2+ |
| Onion | Yes | Yes | Yes (Spring Onion) | Unknown | 3+ |
| Garlic | Yes | Yes | No | Unknown | 2+ |
| Bean | Yes (Flat bean) | Yes | Yes (Green Beans) | Unknown | 3+ |
| Radish | Yes | Yes | Yes | Unknown | 3+ |
| Cabbage | Yes | No | Yes | Unknown | 2+ |
| Cauliflower | Yes | No | Yes | Unknown | 2+ |
| Broccoli | Yes | No | No | Unknown | 1+ |
| Beet | Yes (Beetroot) | No | Yes (Beetroot) | Unknown | 2+ |
| Winter Squash / Pumpkin | Yes (Pumpkin) | No | Yes (Pumpkin) | Unknown | 2+ |
| Summer Squash / Zucchini | Yes (Zucchini) | No | No | Unknown | 1+ |

---

## 7. REMAINING GAPS

### 7.1 Classes with Zero Verified Data

The following Tier 1 classes have NO approved images from verified datasets:

- Summer Squash / Zucchini (limited)
- Winter Squash / Pumpkin (limited)
- Pea
- Turnip (only in Veg Object Detection)
- Leek
- Brussels Sprouts
- Kale (only in 30 plant types — unverified license)
- Lettuce
- Spinach (only in 30 plant types — unverified license)
- Swiss Chard
- Sweet Potato
- Watermelon (only in 30 plant types — unverified license)
- Cantaloupe (only in 30 plant types — unverified license)
- Raspberry / Blackberry
- Grape
- Apple
- Pear
- Peach
- Cherry
- Plum
- Apricot
- Nectarine
- Basil
- Cilantro (only in Veg Object Detection)
- Parsley
- Dill
- Chives (only in A Comprehensive...)
- Mint
- Rosemary
- Thyme
- Asparagus (only in archive _5_ — unverified license)
- Rhubarb
- Hops
- Sunflower (only in archive _9_ — unverified license)

### 7.2 Unverified Datasets That Could Close Gaps

If licenses are verified as commercial-safe:

| Dataset | Potential Classes | Images |
|---------|------------------|--------|
| 30 Plant Types (archive _8_) | Kale, Spinach, Watermelon, Cantaloupe, Corn, Cucumber, Eggplant, etc. | 90,000 |
| Fruits-30 (archive _10_) | Apple, Apricot, Banana, Cherry, Grape, Peach, Pear, Plum, etc. | 100,000 |
| archive _5_ | Asparagus, Alfalfa, etc. | 6,878 |
| archive _9_ | Sunflower | 13,740 |
| archive _11_ | Bean | 1,167 |

---

## 8. RECOMMENDED ACTIONS

### 8.1 Immediate (Automated)

1. **Process verified datasets through Phase 35D pipeline:**
   - A Comprehensive Image Dataset of Vegetables Grown in Bangladesh
   - Vegetable Image Dataset for Classification Models A Bangladeshi Perspective
   - Vegetable Object Detection Dataset from Bangladesh
   - VegNet Vegetable Dataset with quality

2. **Reject Fruits-360** (CC BY-SA 4.0)

3. **Flag duplicates for deduplication:**
   - last_batch_archive__3_ is duplicate of archive _10_
   - last_batch_archive__6_ is duplicate of last_batch_archive

### 8.2 Human Action Required

1. **License verification for unknown datasets:**
   - 30 Plant Types (archive _8_, last_batch_archive__1_, last_batch_archive__7_)
   - Fruits-30 (archive _10_)
   - archive _5_ (plant disease)
   - archive _9_ (flowers)
   - archive _11_ (bean disease)
   - archive _13_ (pest)
   - archive _1_ (insects)
   - archive _2_ (farm insects)
   - archive _3_ (flowers)
   - archive _4_ (pathogen)
   - d7kbzjr83k-1 (plant disease)
   - last_batch_archive (weeds)
   - last_batch_archive__4_ (pathogen)
   - last_batch_archive__5_ (insect pest)

2. **Download missing Phase 35E targets:**
   - Pisum sativum Image Dataset (Pea)
   - Radish Plant Leaf Disease Detection
   - Agri-Vision Bangladesh
   - Pumpkin Leaf Diseases
   - GrapeSet
   - ViViD-5K
   - GrapesNet
   - RaspberrySet
   - BlueberryDCM
   - Fruit ImageNet
   - YEESI Dataset

### 8.3 Processing Order

1. First, process the 4 verified CC BY 4.0 datasets
2. Then, verify licenses for the unknown datasets
3. Process commercially viable ones
4. Reject non-commercial ones
5. Generate final corpus assessment

---

## 9. GO / NO-GO ASSESSMENT

### Current State: NO-GO for Phase 36

**Verified approved images:** 17,757 (from 4 datasets)
**Verified approved classes:** ~17 Tier 1 classes with some data
**Unverified datasets:** 17 datasets, ~600,000+ images

### Conditional GO

If the 30 Plant Types and Fruits-30 datasets are verified as commercially licensed:
- **Verified images could reach:** ~120,000+
- **Classes with data could reach:** ~40+
- **GO for 25–30 class v1 model** becomes viable

---

## 10. NEXT STEPS

1. **Run Phase 35D intake on verified datasets** (4 CC BY 4.0 datasets)
2. **Search primary sources for unknown datasets** to verify licenses
3. **Process commercially viable datasets**
4. **Reject non-commercial datasets**
5. **Generate final Phase 35H report with complete corpus assessment**

---

**DATASET INTAKE PHASE 35H — INBOX ASSESSMENT COMPLETE**

**No model was trained. No commercial corpus was modified.**
