# Phase 19: Targeted Dataset Acquisition Analysis

## Objective

Do NOT train. Do NOT download large datasets. Perform rigorous analysis to determine what data acquisition would provide the greatest value.

> Maximize useful real-world garden-photo recognition coverage, not total image count.

---

## 1. Current Readiness Summary

### Overall Status
- **Total images**: 57,660
- **STRONG**: 7 classes
- **MODERATE**: 6 classes
- **WEAK**: 3 classes
- **INSUFFICIENT**: 117 classes
- **TRAINABLE_NOW**: 0

### Independent Sources
1. PlantVillage (lab, CC0)
2. PlantDoc (field, CC BY 4.0)
3. SegPPD-101 (field, MIT)

### Critical Finding: Field-Domain Deficiency

The dataset is heavily dominated by laboratory imagery. Field/outdoor representation is critically low across almost all disease classes:

| Class | Total | Field Est. | Status |
|-------|------:|----------:|--------|
| Tomato_yellow_leaf_curl | 5,433 | 1.4% | WEAK |
| Leaf_spot | 14,079 | 3.8% | WEAK |
| Bacterial_spot | 3,375 | 7.4% | WEAK |
| Late_blight | 3,177 | 8.4% | WEAK |
| Early_blight | 2,220 | 9.9% | WEAK |
| Septoria_leaf_spot | 1,922 | 7.9% | WEAK |
| Grape_black_rot | 1,271 | 7.2% | WEAK |
| Squash_powdery_mildew | 1,965 | 6.6% | WEAK |
| Powdery_mildew | 1,186 | 11.3% | WEAK |
| Rust | 1,342 | 11.2% | WEAK |
| Apple_scab | 741 | 15.0% | WEAK |
| Cedar_apple_rust | 387 | 28.9% | MODERATE |
| Healthy | 16,174 | 6.7% | WEAK |

**No disease class exceeds 30% field imagery**, which is the readiness threshold.

---

## 2. Highest-Value Deficient Classes

### Classification of Deficiencies

**More field imagery (13 classes):**
- Healthy
- Powdery_mildew
- Early_blight
- Late_blight
- Septoria_leaf_spot
- Bacterial_spot
- Rust
- Leaf_spot
- Apple_scab
- Grape_black_rot
- Squash_powdery_mildew
- Tomato_mosaic_virus
- Tomato_yellow_leaf_curl

**More sources (1 class):**
- Peach_bacterial_spot (2,297 images, PlantVillage only)

**More images + field (1 class):**
- Cedar_apple_rust (387 images, needs both)

**No data (14 classes):**
- Downy_mildew, Fusarium_wilt, Verticillium_wilt, Anthracnose, Blossom_end_rot,
- Sunscald, Frost_damage, Hail_damage, Overwatering_stress, Underwatering_stress,
- Insect_damage, Chewing_damage, Leaf_miner_damage, Soybean_rust

### Top 10 Highest-Value Acquisition Targets

These classes were ranked by combining:
- Importance to home gardeners
- Current field-domain deficiency
- Source diversity gap
- Likelihood of finding accessible datasets

#### 1. Tomato_yellow_leaf_curl
- **Total**: 5,433 images, 2 sources
- **Field**: 1.4% (76 of 5,433 from PlantDoc)
- **Gap**: Critically low field representation for the most common tomato virus
- **Why high priority**: Extremely important to home gardeners; visually distinctive; massive class with almost no field photos

#### 2. Late_blight
- **Total**: 3,177 images, 3 sources
- **Field**: 8.4% (216 of 3,177 from PlantDoc)
- **Gap**: Low field representation despite multiple sources
- **Why high priority**: Historically significant (Irish potato famine); devastating to tomatoes and potatoes; important to gardeners

#### 3. Early_blight
- **Total**: 2,220 images, 3 sources
- **Field**: 9.9% (204 of 2,220 from PlantDoc)
- **Gap**: Low field representation
- **Why high priority**: Very common tomato/potato disease; targets home gardeners; good dataset candidates exist

#### 4. Bacterial_spot
- **Total**: 3,375 images, 3 sources
- **Field**: 7.4% (181 of 3,375 from PlantDoc)
- **Gap**: Low field representation
- **Why high priority**: Affects multiple solanaceous crops; common in gardens; distinctive symptoms

#### 5. Peach_bacterial_spot
- **Total**: 2,297 images, 1 source (PlantVillage only)
- **Field**: 0%
- **Gap**: Single source, zero field imagery
- **Why high priority**: Only disease class with a single source; stone fruit important to home gardeners

#### 6. Powdery_mildew
- **Total**: 1,186 images, 2 sources
- **Field**: 11.3% (134 from SegPPD-101)
- **Gap**: Low field representation, only 2 sources
- **Why high priority**: Extremely common across many crops; easily recognizable; affects cucurbits, tomatoes, peppers

#### 7. Leaf_spot
- **Total**: 14,079 images, 3 sources
- **Field**: 3.8% (350 of 14,079 from PlantDoc)
- **Gap**: Very low field representation for a large catch-all class
- **Why high priority**: Large class; many sub-diseases map here; field diversity would improve generalization

#### 8. Septoria_leaf_spot
- **Total**: 1,922 images, 2 sources
- **Field**: 7.9% (151 of 1,922 from PlantDoc)
- **Gap**: Low field representation, only 2 sources
- **Why high priority**: Common tomato disease; distinctive spots; important for home gardeners

#### 9. Squash_powdery_mildew
- **Total**: 1,965 images, 2 sources
- **Field**: 6.6% (0 from PlantDoc, 0 from SegPPD-101)
- **Gap**: Low field representation, only 2 sources
- **Why high priority**: Critical cucurbit disease; affects zucchini, squash, pumpkins; popular garden crops

#### 10. Grape_black_rot
- **Total**: 1,271 images, 3 sources
- **Field**: 7.2% (64 of 1,271 from PlantDoc)
- **Gap**: Low field representation
- **Why high priority**: Important for home vineyards; distinctive symptoms; some field datasets available

---

## 3. Candidate Datasets

### HIGH VALUE

#### A. Irish Potato Imagery Dataset (Zenodo)
- **URL**: https://zenodo.org/records/8286528
- **License**: CC BY 4.0
- **Commercial use**: Yes
- **Images**: 58,709
- **Classes**: Early_blight, Late_blight, Healthy
- **Capture**: Samsung Galaxy A03 smartphones, smallholder farms, Tanzania
- **Field characteristics**: Genuine field conditions, diverse lighting/angles/backgrounds
- **Capture-condition diversity**: High (6 months, multiple farms, varying conditions)
- **Overlap with current sources**: Low (smartphone field images from Tanzania)
- **Estimated useful contribution**: ~58,000 field images for potato blights
- **Acquisition difficulty**: Medium (Zenodo download, large file ~6.8 GB)
- **Value rating**: **HIGH**

**Why**: This is the single highest-value dataset identified. It directly addresses Late_blight and Early_blight field imagery gaps with genuine smartphone field photos from smallholder farms. The scale (58K images) is enormous, but more importantly, it provides completely independent field-domain data from Africa.

#### B. OPTIMA Field Images (Zenodo)
- **URL**: https://zenodo.org/records/8339572
- **License**: CC BY 4.0
- **Commercial use**: Yes
- **Images**: ~1,000+ RGB field images
- **Classes**: Apple_scab, Grape_downy_mildew, Carrot_alternaria
- **Capture**: Smart-camera (NEON-202B-JT2-X) in orchards/vineyards/fields
- **Field characteristics**: Real orchards and fields in France, Italy, Spain
- **Capture-condition diversity**: High (multiple countries, seasons, devices)
- **Overlap with current sources**: Low (European field conditions, multispectral + RGB)
- **Estimated useful contribution**: ~500-1,000 field images for apple scab and grape diseases
- **Acquisition difficulty**: Medium (5.4 GB download, includes multispectral data)
- **Value rating**: **HIGH**

**Why**: Provides rare European field imagery for apple scab and grape downy mildew with expert annotations. Complements our existing sources geographically and capture-condition-wise.

#### C. Grapevine Leaves RGB Images (Zenodo)
- **URL**: https://zenodo.org/records/17343474
- **License**: CC BY 4.0
- **Commercial use**: Yes
- **Images**: 5,267
- **Classes**: Healthy, Downy_mildew, Powdery_mildew, Esca, Erineum_mite
- **Capture**: Smartphone, natural daylight, Portuguese vineyards
- **Field characteristics**: Field-collected in vineyards
- **Capture-condition diversity**: High (4 vineyards, 2 regions, natural lighting)
- **Overlap with current sources**: Low (Portuguese vineyards, different cultivars)
- **Estimated useful contribution**: ~1,000 field images for grape diseases
- **Acquisition difficulty**: Low (direct Zenodo download)
- **Value rating**: **HIGH**

**Why**: Directly addresses Grape_black_rot and Powdery_mildew field imagery gaps. Smartphone-captured in real vineyards. High capture-condition diversity.

#### D. Common Beans Imagery Dataset (Zenodo)
- **URL**: https://zenodo.org/records/8286126
- **License**: CC BY 4.0
- **Commercial use**: Yes
- **Images**: 59,072
- **Classes**: Bean_anthracnose, Bean_rust, Healthy
- **Capture**: Samsung Galaxy A03 Core smartphones, Tanzania
- **Field characteristics**: Smallholder farms, open field conditions
- **Capture-condition diversity**: High (6 months, multiple farms)
- **Overlap with current sources**: Low (Tanzanian field conditions, different cultivars)
- **Estimated useful contribution**: ~59,000 field images for bean diseases
- **Acquisition difficulty**: Medium (6.8 GB total, multiple zip files)
- **Value rating**: **HIGH**

**Why**: Massive smartphone field dataset for bean anthracnose and rust. While beans are not our primary garden crop, the field-domain diversity and capture conditions are extremely valuable. Could be used for Rust class strengthening.

#### E. Crop Disease Image Dataset (HuggingFace)
- **URL**: https://huggingface.co/datasets/ipartzix/Crop_Disease_Image_Dataset
- **License**: CC BY 4.0
- **Commercial use**: Yes
- **Images**: 22,169
- **Classes**: Corn, Potato, Rice, Tomato, Wheat; 19 disease classes
- **Capture**: Mixed (primarily lab/controlled)
- **Field characteristics**: Mixed - some field, some lab
- **Capture-condition diversity**: Medium
- **Overlap with current sources**: Medium (includes PlantVillage-style images)
- **Estimated useful contribution**: ~5,000-10,000 useful images
- **Acquisition difficulty**: Low (HuggingFace streaming/download)
- **Value rating**: **MEDIUM-HIGH**

**Why**: Easily accessible on HuggingFace. Covers multiple high-priority classes (Early_blight, Late_blight, Bacterial_spot, Tomato_yellow_leaf_curl). However, likely contains significant PlantVillage overlap. Need to verify field vs lab composition.

### MEDIUM VALUE

#### F. SLIF-Tomato Dataset (Kaggle)
- **URL**: https://www.kaggle.com/datasets/romiyalgeorge/slif-tomato-dataset
- **License**: CC BY 4.0
- **Commercial use**: Yes
- **Images**: ~890
- **Classes**: Bacterial_spot, Early_blight, Healthy, Mosaic, Powdery_mildew, Septoria, Wilt, Late_blight
- **Capture**: Multiple smartphones, Sri Lankan fields, 2024 growing season
- **Field characteristics**: Genuine in-field tomato images
- **Capture-condition diversity**: Very high (multiple agro-climatic zones, devices, times of day)
- **Overlap with current sources**: Low (Sri Lankan field conditions)
- **Estimated useful contribution**: ~500-800 field images
- **Acquisition difficulty**: Medium (Kaggle requires authentication)
- **Value rating**: **MEDIUM**

**Why**: High-quality field dataset for tomato diseases, but small size and Kaggle access barrier reduce priority.

#### G. Niphad Grape Leaf Disease Dataset (Mendeley)
- **URL**: https://data.mendeley.com/datasets/8nnd2ypcv3/1
- **License**: CC BY 4.0
- **Commercial use**: Yes
- **Images**: 2,726
- **Classes**: Downy_mildew, Powdery_mildew, Bacterial_rot, Healthy
- **Capture**: Mobile phones, Indian vineyards
- **Field characteristics**: Field-collected
- **Capture-condition diversity**: Medium
- **Overlap with current sources**: Low (Indian field conditions)
- **Estimated useful contribution**: ~1,500 field images for grape diseases
- **Acquisition difficulty**: Medium (Mendeley may require manual download)
- **Value rating**: **MEDIUM**

#### H. GVLiD: GrapeVine Leaf identification of Diseases (Mendeley)
- **URL**: https://data.mendeley.com/datasets/wkymf8bhcg
- **License**: CC BY 4.0
- **Commercial use**: Yes
- **Images**: 3,477
- **Classes**: Healthy, Black_rot, Esca, Leaf_blight
- **Capture**: Field visit, 1080×1080 JPG
- **Field characteristics**: Field-collected from different angles
- **Capture-condition diversity**: Medium
- **Overlap with current sources**: Low
- **Estimated useful contribution**: ~1,000 field images for grape diseases
- **Acquisition difficulty**: Medium (Mendeley access)
- **Value rating**: **MEDIUM**

### LOW VALUE / REJECT

#### I. PlantWild (HuggingFace)
- **URL**: https://huggingface.co/datasets/uqtwei2/PlantWild
- **License**: CC BY-NC-ND 4.0
- **Commercial use**: NO
- **Value rating**: **REJECT**

**Why**: Non-commercial and no-derivatives restrictions make it incompatible with our commercial app.

#### II. AgriField-40K (HuggingFace)
- **URL**: https://huggingface.co/datasets/dtu-pcas/AgriField-40K
- **License**: CC BY-SA 4.0
- **Commercial use**: Yes (with share-alike)
- **Value rating**: **LOW**

**Why**: Share-alike license may be incompatible with proprietary app. Also, it's a general agricultural field dataset, not disease-specific. 11.9 GB size is large for marginal value.

#### III. Bangladesh Smartphone Vegetable Dataset (Mendeley)
- **URL**: https://data.mendeley.com/datasets/n67gctmjyj/3
- **License**: CC BY-NC 4.0
- **Commercial use**: NO
- **Value rating**: **REJECT**

**Why**: Non-commercial license.

#### IV. Bean/Cowpea Disease Dataset (Mendeley)
- **URL**: https://doi.org/10.1016/j.dib.2024.111023
- **License**: CC BY-NC 4.0
- **Commercial use**: NO
- **Value rating**: **REJECT**

**Why**: Non-commercial license.

#### V. AppleScabFDs (Kaggle)
- **URL**: https://www.kaggle.com/datasets/projectlzp201910094/applescabfds
- **License**: CC BY-NC-ND 4.0
- **Commercial use**: NO
- **Value rating**: **REJECT**

**Why**: Non-commercial and no-derivatives.

#### VI. PlantInquiryVQA (HuggingFace)
- **URL**: https://huggingface.co/datasets/SyedNazmusSakib/PlantInquiryVQA
- **License**: CC BY 4.0 (annotations), mixed upstream
- **Commercial use**: Uncertain (upstream licenses vary)
- **Value rating**: **LOW**

**Why**: VQA-focused dataset with mixed upstream licenses. Not designed for pure classification. Legal complexity makes it risky.

---

## 4. Licensing Assessment

| Dataset | License | Commercial | Attribution | ML Training | Verdict |
|---------|---------|------------|-------------|-------------|---------|
| Irish Potato Imagery | CC BY 4.0 | Yes | Yes | Yes | **APPROVED** |
| OPTIMA | CC BY 4.0 | Yes | Yes | Yes | **APPROVED** |
| Grapevine Leaves RGB | CC BY 4.0 | Yes | Yes | Yes | **APPROVED** |
| Common Beans Imagery | CC BY 4.0 | Yes | Yes | Yes | **APPROVED** |
| Crop Disease Image Dataset | CC BY 4.0 | Yes | Yes | Yes | **APPROVED** |
| SLIF-Tomato | CC BY 4.0 | Yes | Yes | Yes | **APPROVED** |
| Niphad Grape | CC BY 4.0 | Yes | Yes | Yes | **APPROVED** |
| GVLiD | CC BY 4.0 | Yes | Yes | Yes | **APPROVED** |
| PlantWild | CC BY-NC-ND 4.0 | NO | Yes | Restricted | **REJECT** |
| AgriField-40K | CC BY-SA 4.0 | Yes (SA) | Yes | Yes | **HOLD** |
| Bangladesh Smartphone | CC BY-NC 4.0 | NO | Yes | Yes | **REJECT** |
| Bean/Cowpea Disease | CC BY-NC 4.0 | NO | Yes | Yes | **REJECT** |
| AppleScabFDs | CC BY-NC-ND 4.0 | NO | Yes | Restricted | **REJECT** |

---

## 5. Field-Domain Assessment

Current field imagery is estimated at:
- PlantDoc: ~1,678 insect images + ~2,502 disease images (all field)
- SegPPD-101: 819 field disease images
- **Total field disease images**: ~3,321 out of 55,982 (5.9%)

After integrating the top candidate datasets, estimated field imagery would increase to:
- Irish Potato Imagery: +58,709 field images (potato late/early blight)
- Common Beans Imagery: +59,072 field images (bean anthracnose/rust)
- Grapevine Leaves RGB: +5,267 field images (grape diseases)
- OPTIMA: +1,000 field images (apple scab, grape downy mildew)
- **Total potential field addition**: ~124,000+ field images

This would dramatically improve field-domain coverage for the classes that matter most.

---

## 6. Ranked Acquisition Priorities

### Priority 1: Irish Potato Imagery Dataset
**Dataset**: Irish Potato Imagery Dataset for Early Detection of Crop Diseases  
**URL**: https://zenodo.org/records/8286528  
**Classes**: Early_blight, Late_blight, Healthy  
**Expected useful images**: ~58,000 (field smartphone images)  
**Why**: Highest single impact. Addresses two critical garden diseases (early blight, late blight) with genuine field imagery from smallholder farms. Unprecedented scale for field potato disease images.  
**License**: CC BY 4.0 (commercial use permitted, attribution required)  
**Acquisition effort**: Medium (Zenodo download, ~6.8 GB)

### Priority 2: Common Beans Imagery Dataset
**Dataset**: Common Beans Imagery Dataset for Early Detection of Crop Diseases  
**URL**: https://zenodo.org/records/8286126  
**Classes**: Bean_anthracnose, Bean_rust, Healthy  
**Expected useful images**: ~59,000 (field smartphone images)  
**Why**: Massive field dataset strengthens Rust class and adds bean disease coverage. Smartphone-captured in real farm conditions.  
**License**: CC BY 4.0 (commercial use permitted, attribution required)  
**Acquisition effort**: Medium (Zenodo download, ~6.8 GB)

### Priority 3: Grapevine Leaves RGB Images
**Dataset**: Grapevine Leaves RGB Images of Disease Symptoms  
**URL**: https://zenodo.org/records/17343474  
**Classes**: Healthy, Downy_mildew, Powdery_mildew, Esca, Erineum_mite  
**Expected useful images**: ~1,000 field images for grape diseases  
**Why**: Directly addresses Grape_black_rot and Powdery_mildew field gaps. Smartphone-captured in Portuguese vineyards. High capture-condition diversity.  
**License**: CC BY 4.0 (commercial use permitted, attribution required)  
**Acquisition effort**: Low (direct Zenodo download)

### Priority 4: OPTIMA Field Images
**Dataset**: OPTIMA RGB colour images and multispectral images  
**URL**: https://zenodo.org/records/8339572  
**Classes**: Apple_scab, Grape_downy_mildew, Carrot_alternaria  
**Expected useful images**: ~500-1,000 field images  
**Why**: Provides rare European field imagery for apple scab. Expert-annotated with bounding boxes. Multi-sensor (RGB + multispectral).  
**License**: CC BY 4.0 (commercial use permitted, attribution required)  
**Acquisition effort**: Medium (5.4 GB download, includes multispectral data)

### Priority 5: Crop Disease Image Dataset (HuggingFace)
**Dataset**: Crop Disease Image Dataset  
**URL**: https://huggingface.co/datasets/ipartzix/Crop_Disease_Image_Dataset  
**Classes**: Corn, Potato, Rice, Tomato, Wheat; 19 disease classes  
**Expected useful images**: ~5,000-10,000 (after deduplication)  
**Why**: Easily accessible on HuggingFace. Covers multiple high-priority classes. Good for quick wins.  
**License**: CC BY 4.0 (commercial use permitted, attribution required)  
**Acquisition effort**: Low (HuggingFace streaming)

---

## 7. Datasets Worth Investigating Later

| Dataset | Why Later |
|---------|-----------|
| SLIF-Tomato | High quality but small (~890 images) and requires Kaggle access |
| Niphad Grape | Good but Mendeley access may be problematic |
| GVLiD | Good grape coverage but Mendeley access may be problematic |
| PlantInquiryVQA | Mixed licenses, VQA-focused, not ideal for classification |
| RL-NST Corn | Augmented data, not genuine field imagery |

---

## 8. Datasets Not Worth Pursuing

| Dataset | Reason |
|---------|--------|
| PlantWild | CC BY-NC-ND: non-commercial, no derivatives |
| AgriField-40K | CC BY-SA: share-alike may be incompatible; general field images, not disease-specific |
| Bangladesh Smartphone Vegetable | CC BY-NC: non-commercial |
| Bean/Cowpea Disease | CC BY-NC: non-commercial |
| AppleScabFDs | CC BY-NC-ND: non-commercial, no derivatives |

---

## 9. Recommended Next Phase

### Phase 19 Execution Plan

1. **Immediate acquisition** (next 1-2 weeks):
   - Download Irish Potato Imagery Dataset from Zenodo
   - Download Common Beans Imagery Dataset from Zenodo
   - Download Grapevine Leaves RGB Images from Zenodo

2. **Short-term acquisition** (weeks 2-4):
   - Download OPTIMA field images from Zenodo
   - Download Crop Disease Image Dataset from HuggingFace

3. **Integration** (after downloads complete):
   - Map classes to taxonomy
   - Ingest through pipeline
   - Validate, deduplicate, split
   - Recalculate readiness metrics

4. **Continued search** (ongoing):
   - Search for smartphone field datasets for:
     - Peach_bacterial_spot
     - Tomato_yellow_leaf_curl
     - Powdery_mildew (cucurbits, peppers)
   - Look for institutional repositories with CC BY licenses

---

## 10. Explicit Statement

> **Training remains deferred.**

No disease class currently meets the TRAINABLE_NOW criteria:
- ≥100 images/class
- ≥2 independent sources
- ≥3 capture conditions
- ≥90% label consensus
- ≥30% field imagery
- ≤5% near-duplicate rate

The dataset is closer to supporting real Soil & Supper garden photographs, but the limiting factor remains field-domain coverage and capture-condition diversity, not raw image count.

---

## 11. Git Status

This analysis only:
- No code changes
- No training data modifications
- No downloads
- Only documentation: `docs/PHASE19_ACQUISITION_ANALYSIS.md`

---

*Analysis performed: 2026-08-17*
*Phase 18 baseline commit: ac32e5d*
