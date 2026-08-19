# Soil & Supper — ML Model Strategy

**Date**: 2026-08-18  
**Phase**: ML Model Architecture + Data Strategy  
**Scope**: ML/DATA ONLY — No Android/Kotlin/Compose changes  
**Status**: Decision support — concrete recommendations for human action

---

## 1. Executive Summary

Soil & Supper needs an on-device plant disease classifier that runs offline on Android. The current commercial training core is **98,642 images from 4 sources**, but this number is misleading: **~39% is potato-only imagery** from a single dataset, and **97.4% is lab/controlled photography** that looks nothing like what a gardener will photograph.

**The core problem is not image count. The core problem is source diversity and domain realism.**

This document answers:

1. **What model to use?** → MobileNetV3 Large (production), EfficientNet-Lite4 (reference)
2. **Is Phi-3 appropriate?** → No. Wrong tool for structured classification.
3. **One model or many?** → Start with one flat disease classifier. Modular classifiers are v2.
4. **How much more data is needed?** → ~5,000–10,000 targeted images, not millions.
5. **Which datasets should the human acquire?** → 5–7 specific datasets listed in Section 5.

---

## 2. Current Corpus: The Truth Behind the Numbers

### 2.1 Commercial Core Summary

| Metric | Value | Reality Check |
|--------|-------|---------------|
| Total commercial images | 98,642 | Inflated by potato concentration |
| Effective diverse images | ~28,000 | After removing lab-only and potato-biased images |
| Lab/controlled images | 97.4% | Mostly PlantVillage |
| Field/garden images | 2.6% | PlantDoc + Grapevine + Irish Potato subset |
| Number of sources | 4 | But 2 sources dominate (PlantVillage 55%, Irish Potato 39%) |
| Trainable disease classes | 14 of 30 | 15 classes have zero commercial images |
| Single-source-dependent classes | 2 | Downy_mildew (100% grapevine), Peach_bacterial_spot (100% PlantVillage) |

### 2.2 The Potato Problem

The Irish Potato dataset contributes **117,424 raw images** (38,554 commercial). However, it only covers **3 classes**: Healthy, Early_blight, Late_blight. This means:

- Late_blight has 16,141 images — excellent count, but **80.7% from potato fields in Tanzania**
- Early_blight has 8,421 images — good count, but **73.8% from potato fields in Tanzania**
- Healthy has 36,342 images — but **19,308 are potato leaves from Tanzania**

A model trained on this corpus will be excellent at identifying potato diseases in Tanzanian field conditions, but may fail on:
- Tomato late blight in a US home garden
- Potato late blight in different lighting/angle
- Any non-potato crop

### 2.3 The Lab Photography Problem

PlantVillage contributes **54,305 images (55.1% of commercial core)**. These are:
- Single leaf per image
- Uniform gray/black background
- Controlled lab lighting
- No environmental context
- No soil, no clutter, no multiple plants

**This is not what a Soil & Supper user will photograph.** A user will photograph:
- Whole plants in garden beds
- Mixed with other plants
- Variable lighting (sun, shade, flash)
- Natural backgrounds (soil, mulch, other leaves)
- Multiple symptoms on one plant

The domain gap between PlantVillage and real garden photos is **the central challenge** for this project.

### 2.4 Source Diversity Matrix

| Class | PlantVillage | Irish Potato | PlantDoc | Grapevine | Source Diversity |
|-------|-------------|--------------|----------|-----------|-----------------|
| Healthy | 15,071 | 19,308 | 846 | 1,117 | STRONG |
| Late_blight | 2,901 | 13,029 | 211 | 0 | STRONG |
| Early_blight | 2,000 | 6,217 | 204 | 0 | STRONG |
| Leaf_spot | 13,550 | 0 | 347 | 0 | WEAK |
| Tomato_yellow_leaf_curl | 5,357 | 0 | 75 | 0 | WEAK |
| Bacterial_spot | 3,124 | 0 | 181 | 0 | WEAK |
| Powdery_mildew | 1,052 | 0 | 0 | 1,126 | MODERATE |
| Peach_bacterial_spot | 2,297 | 0 | 0 | 0 | SINGLE_SOURCE |
| Squash_powdery_mildew | 1,835 | 0 | 130 | 0 | WEAK |
| Septoria_leaf_spot | 1,771 | 0 | 149 | 0 | WEAK |
| Spider_mite | 1,676 | 0 | 2 | 0 | ESSENTIALLY_SINGLE |
| Rust | 1,192 | 0 | 116 | 0 | WEAK |
| Grape_black_rot | 1,180 | 0 | 64 | 0 | WEAK |
| Downy_mildew | 0 | 0 | 0 | 1,002 | SINGLE_SOURCE |
| Apple_scab | 630 | 0 | 93 | 0 | WEAK |
| Tomato_mosaic_virus | 373 | 0 | 54 | 0 | WEAK |
| Cedar_apple_rust | 275 | 0 | 87 | 0 | WEAK |
| Anthracnose | 0 | 0 | 0 | 0 | ZERO |

### 2.5 Classes Already Sufficiently Represented

These 8 classes have adequate counts AND reasonable source diversity for v1:

| Class | Count | Sources | Status |
|-------|-------|---------|--------|
| Healthy | 36,342 | 4 | STRONG (but dominant — needs class weighting) |
| Late_blight | 16,141 | 3 | STRONG (potato-biased but high count) |
| Leaf_spot | 13,897 | 2 | STRONG (lab-dominated) |
| Early_blight | 8,421 | 3 | STRONG (potato-biased) |
| Tomato_yellow_leaf_curl | 5,432 | 2 | MODERATE |
| Bacterial_spot | 3,305 | 2 | ADEQUATE |
| Powdery_mildew | 2,178 | 2 | ADEQUATE |
| Squash_powdery_mildew | 1,965 | 2 | ADEQUATE |

### 2.6 Classes That Need More Data

| Class | Count | Gap | Priority |
|-------|-------|-----|----------|
| Cedar_apple_rust | 362 | Very low count, subtle symptoms | HIGH |
| Apple_scab | 723 | Low count, mostly lab | HIGH |
| Downy_mildew | 1,002 | Single source (grape only) | HIGH |
| Tomato_mosaic_virus | 427 | Low count, subtle symptoms | MEDIUM |
| Peach_bacterial_spot | 2,297 | Single source (PlantVillage only) | MEDIUM |
| Rust | 1,308 | Moderate count, mostly lab | MEDIUM |
| Grape_black_rot | 1,244 | Moderate count, mostly lab | MEDIUM |
| Septoria_leaf_spot | 1,920 | Moderate count, mostly lab | LOW |
| Spider_mite | 1,678 | Essentially single source | LOW |

### 2.7 Classes That Cannot Be Trained Yet

15 disease classes have **zero commercial images**:
- Anthracnose
- Fusarium_wilt
- Verticillium_wilt
- Blossom_end_rot
- Nutrient_deficiency
- Sunscald
- Frost_damage
- Hail_damage
- Overwatering_stress
- Underwatering_stress
- Insect_damage
- Chewing_damage
- Leaf_miner_damage
- Soybean_rust

These require entirely new datasets or personal photography. **Defer to v2.**

---

## 3. Model Architecture Recommendation

### 3.1 Problem Classification

Soil & Supper's recognition task is **structured closed-set image classification**:

- Input: single photograph of a plant/leaf
- Output: one of N known classes with confidence score
- Constraint: <200 ms inference on mid-range Android
- Constraint: works fully offline
- Constraint: model < 20 MB
- Constraint: deterministic, repeatable results
- Constraint: TensorFlow Lite / LiteRT deployment

This is **not** an open-ended vision-language task. It is **not** object detection. It is **not** segmentation.

### 3.2 Why NOT Phi-3 / Phi-3.5 Vision

Phi-3.5 Vision is a **4.1B-parameter multimodal language model**. It is the wrong architectural choice for this problem:

| Criterion | Phi-3.5 Vision | MobileNetV3 Large |
|-----------|----------------|------------------|
| Parameters | 4.1 billion | 4.2 million |
| Model size (FP16) | ~8–12 GB | ~16 MB (FP32), ~5 MB (INT8) |
| Inference latency (mobile) | Seconds to minutes | ~80–120 ms (CPU), ~20–40 ms (NNAPI) |
| VRAM requirement | Multi-GB | <100 MB |
| TFLite/LiteRT support | None | Native |
| INT8 quantization | Extreme degradation | Proven |
| Offline Android deployment | Impractical | Standard |
| Output format | Open-ended text | Structured class probabilities |
| Determinism | Stochastic | Deterministic |
| Training cost | Massive GPU cluster | Single consumer GPU |

**Phi-3.5 Vision solves a different problem**: open-ended visual reasoning, document understanding, multi-image QA. Soil & Supper needs a **deterministic, bounded-latency, structured classifier**.

**Verdict**: Do not evaluate Phi-3 for production classification. It may be useful for future "garden coach" conversational features, but that is a separate product feature.

### 3.3 Production Baseline: MobileNetV3 Large

| Property | Value |
|----------|-------|
| **Parameters** | ~4.2M |
| **Model Size (FP32)** | ~16 MB |
| **Model Size (INT8 TFLite)** | ~4–5 MB |
| **MACs at 224×224** | ~0.22 GMac |
| **ImageNet Top-1** | ~75.2% |
| **Expected Inference (Android CPU)** | ~80–120 ms |
| **Expected Inference (Android NNAPI)** | ~20–40 ms |
| **TFLite Conversion** | Native via TFLite Model Maker / Keras |
| **Quantization** | Full integer (INT8) with calibration |
| **Transfer Learning** | Excellent — ImageNet pretrained |
| **Training Cost** | Low — ~2–4 hours on GTX 1060 6GB |
| **Android Compatibility** | Excellent — native TFLite, NNAPI, Qualcomm SNPE |

**Why MobileNetV3 Large for v1:**
- Smallest viable model — fastest inference, smallest download
- Mature TFLite toolchain with extensive documentation
- Hard-Swish activations work well with INT8 calibration
- Low VRAM requirement allows larger batch sizes
- Proven in production image classification apps
- Can be deployed immediately without experimental deployment paths

### 3.4 Accuracy Reference: EfficientNet-Lite4

| Property | Value |
|----------|-------|
| **Parameters** | ~11.7M |
| **Model Size (INT8 TFLite)** | ~11–12 MB |
| **MACs at 224×224** | ~1.35 GMac |
| **ImageNet Top-1** | ~80.1% |
| **Expected Inference (Android CPU)** | ~150–250 ms |
| **Quantization** | INT8 with moderate degradation; benefits from QAT or AdaRound |

**Why EfficientNet-Lite4 as reference:**
- Better accuracy than MobileNetV3 (~5% ImageNet improvement)
- Same TFLite deployment path
- Useful for measuring the accuracy ceiling of the current dataset
- If EfficientNet-Lite4 plateaus at the same accuracy as MobileNetV3, the bottleneck is data, not model capacity

### 3.5 Other Candidates Worth Testing

| Model | Why Test It |
|-------|-------------|
| FastViT-SA12 | Apple's hybrid ViT; 79.8% ImageNet; strong on fine-grained features. No native TFLite — requires ONNX path. Evaluate only if MobileNet/EfficientNet plateau. |
| MobileNetV3 Small | Ultra-light fallback if Large is too big for some devices. ~2.5M params, ~2–3 MB INT8. |
| EfficientNet-Lite0 | Smaller EfficientNet; good middle ground. ~4.5M params, ~4 MB INT8. |

### 3.6 Modular vs Monarchical Classifier

The existing `ML_TAXONOMY.md` proposes a **hybrid domain router + hierarchical disease classifier**. For v1, this is **over-engineered**.

**Recommendation for v1:**
- **One flat disease classifier** for 14 trainable classes
- Single model, single head, no routing
- Input: 224×224 image
- Output: 14 class probabilities

**Why flat for v1:**
1. Disease data is the strongest commercial core (98,642 images)
2. Crop/weed/insect data is too weak or missing for specialized classifiers
3. Hierarchical conditioning requires a working crop classifier first
4. Domain router adds latency and failure modes
5. Flat classifier is simpler to debug, evaluate, and iterate
6. Can migrate to modular architecture in v2 once each domain has sufficient data

**v2 architecture path:**
1. Train flat disease classifier (v1)
2. Train crop classifier when crop datasets are acquired
3. Add domain router
4. Condition disease classifier on crop prediction
5. Add insect/weed classifiers

---

## 4. Training Strategy

### 4.1 What the Current Dataset Can Accomplish

The current 98,642-image commercial core can train a **reasonable v1 disease classifier** for 14 classes, with these expectations:

| Expected Performance | Metric |
|---------------------|--------|
| Same-source validation accuracy | 92–96% |
| Same-source validation macro F1 | 88–94% |
| PlantDoc-only test accuracy | 70–80% |
| Domain gap | 15–20% |

**The domain gap is the key metric.** A 15–20% drop from lab validation to field test is expected and acceptable for v1. The goal is to minimize this gap, not maximize lab accuracy.

### 4.2 Transfer-Learning Requirements

For a pretrained MobileNetV3/EfficientNet backbone with standard augmentation:

| Class Category | Current Min | Minimum Viable | Good | Strong |
|----------------|-------------|----------------|------|--------|
| Strong (≥5,000) | 5,432 | 500 | 1,000 | 2,000 |
| Moderate (1,000–5,000) | 1,002 | 300 | 500 | 1,000 |
| Weak (300–1,000) | 362 | 200 | 300 | 500 |
| Zero | 0 | N/A | N/A | N/A |

**Key insight**: Under transfer learning, we do NOT need 10,000 images per class. The pretrained backbone already knows generic visual features. We need enough images to:
1. Learn the disease-specific features
2. Adapt to the domain gap (lab → field)
3. Avoid overfitting to source-specific artifacts

For most classes, **500–1,000 diverse images is sufficient** for a strong v1 model. The bottleneck is diversity, not quantity.

### 4.3 Source Diversity > Image Count

A class with 10,000 nearly identical PlantVillage images is **less valuable** than 1,000 diverse field photographs from different geographies, cameras, and conditions.

**Why source diversity matters more:**
- PlantVillage images all share: uniform background, single leaf, lab lighting, specific camera
- A model trained on 10,000 PlantVillage images will learn PlantVillage-specific features (background color, leaf positioning) rather than disease features
- Field images from different sources force the model to learn invariant disease features

### 4.4 Class Complexity Adjustments

Some classes are visually similar and need more data:

| Class Pair | Confusion Risk | Adjustment |
|------------|---------------|------------|
| Powdery_mildew ↔ Downy_mildew | HIGH | Both are white fungal growth; need clear examples of each |
| Early_blight ↔ Leaf_spot | HIGH | Both cause leaf spots; need target-like vs. concentric ring examples |
| Bacterial_spot ↔ Early_blight | MODERATE | Both cause dark spots; need context examples |
| Tomato_yellow_leaf_curl ↔ Tomato_mosaic_virus | MODERATE | Both cause leaf deformation; need distinct symptom examples |

**Recommendation**: For high-confusion pairs, ensure at least 500 images per class with clear visual distinction. If confusion persists after training, consider merging or hierarchical conditioning.

### 4.5 Experiment Plan

#### BASELINE
- **Model**: MobileNetV3 Large (ImageNet pretrained)
- **Data**: Current 98,642-image commercial core
- **Augmentation**: Standard (RandomResizedCrop, HorizontalFlip, ColorJitter, GaussianBlur)
- **Taxonomy**: 14 disease classes (flat classifier)
- **Split**: 70/15/15 stratified by class, source-aware

**Expected**: 92–96% same-source accuracy, 70–80% PlantDoc-only accuracy

#### EXPERIMENT A: Balanced Training Subset
- **Model**: MobileNetV3 Large
- **Data**: Same as baseline, but with class-balanced sampling
- **Change**: Weighted CrossEntropyLoss or Focal Loss to compensate for Healthy class dominance (36,342 images vs. 362 for Cedar_apple_rust)
- **Expected**: Improved macro F1, possibly slightly lower overall accuracy

#### EXPERIMENT B: Add Diverse Datasets
- **Model**: MobileNetV3 Large
- **Data**: Baseline + 5 human-acquired datasets (Plant Pathology 2020, ICAR-CITH, Multi-Crop Disease, Manalagi, GLVD)
- **Change**: ~5,000–10,000 additional images with field diversity and new geographic sources
- **Expected**: Reduced domain gap (PlantDoc test accuracy improves to 75–85%)

#### EXPERIMENT C: Stronger Augmentation
- **Model**: MobileNetV3 Large
- **Data**: Baseline
- **Change**: Add MixUp, CutMix, stronger color jitter, random erasing
- **Expected**: Improved robustness to domain shift, especially if dataset B is not yet available

### 4.6 Metrics

| Metric | Purpose |
|--------|---------|
| Overall accuracy | High-level summary |
| **Macro F1** | **Primary metric** — treats all classes equally |
| Per-class precision | Identify which diseases are confused |
| Per-class recall | Identify which diseases are missed |
| Confusion matrix | Visualize error patterns |
| Balanced accuracy | Average of per-class recall |
| Per-source accuracy | Measure domain gap (PlantVillage vs PlantDoc vs Irish Potato) |
| Top-3 accuracy | Useful for gardener-facing UI (show top 3 suggestions) |

### 4.7 Preventing Source Leakage

**Critical**: The current corpus has severe source concentration. Source leakage will inflate validation scores and produce a model that fails in production.

**Rules**:
1. **Never mix images from the same source across train/val/test splits.** All PlantVillage images → train only. PlantDoc, Irish Potato, Grapevine → split across train/val/test.
2. **Report per-source performance separately.** "On PlantDoc-only test: 78% accuracy. On PlantVillage-only test: 96% accuracy."
3. **Use PlantDoc as the proxy external test set.** It is the only source with real field/garden images. Even though it's in the commercial core, hold out 100% of PlantDoc for testing, or at minimum the test split.
4. **Document domain gap explicitly.** "Model performs 94% on same-source validation, 78% on field-style test (gap: 16%)."

---

## 5. Dataset Recommendations for Human Acquisition

**STOP searching for more datasets after acquiring these 5–7.**

### 5.1 P0 — Strongly Recommended (Acquire First)

#### 1. Plant Pathology Challenge 2020
- **URL**: https://www.kaggle.com/c/plant-pathology-2020-fgvc7
- **License**: CC BY 4.0 (verify on Kaggle page)
- **Size**: ~1 GB
- **Images**: 3,651
- **Classes**: Apple scab (1,200), Cedar apple rust (1,399), Healthy (865), Complex (187)
- **Why**: **Highest-value dataset.** 1,399 Cedar_apple_rust images would more than triple the current count. 1,200 Apple_scab field images add geographic diversity. Expert-annotated by Cornell University.
- **Acquisition**: Free Kaggle account required. Download train.csv + images folder.

#### 2. Apple Leaf Diseases Image Dataset of ICAR-CITH
- **URL**: https://data.mendeley.com/datasets/gm6mfz8fz6
- **License**: CC BY 4.0
- **Size**: ~500 MB
- **Images**: Field-collected apple leaves (count not specified)
- **Classes**: Apple scab, Powdery mildew, Mosaic virus, Alternaria leaf blotch
- **Why**: First commercially-licensed apple disease dataset with field images from India. Directly fills Apple_scab gap with non-PlantVillage, non-lab images.
- **Acquisition**: Direct Mendeley download, no authentication.

#### 3. Multi-Crop Disease Dataset
- **URL**: https://data.mendeley.com/datasets/6243z8r6t6
- **License**: CC BY 4.0
- **Size**: ~2–3 GB
- **Images**: 23,000+
- **Classes**: Anthracnose, Rust, Downy Mildew, Leaf Curl, Black Rot, Healthy (across Banana, Chilli, Radish, Groundnut, Cauliflower)
- **Why**: **Largest single source for Anthracnose** (currently 0 commercial images). Also adds Rust and Downy_mildew from non-grape, non-PlantVillage sources. 200MP mobile phone images.
- **Acquisition**: Direct Mendeley download, no authentication.

### 5.2 P1 — Useful (Acquire After P0)

#### 4. Apple Disease Dataset (Manalagi)
- **URL**: https://data.mendeley.com/datasets/9zgkwwv9j8
- **License**: CC BY 4.0
- **Size**: ~1 GB
- **Images**: Not specified (multiple orchards)
- **Classes**: Apple scab and other apple diseases
- **Why**: Expert-verified field images from multiple smartphone cameras (Realme 9 Pro, iPhone 13, Samsung Galaxy). Adds geographic diversity (Indonesia) and device diversity.
- **Acquisition**: Direct Mendeley download, no authentication.

#### 5. Bangladesh Comprehensive Vegetables
- **URL**: https://data.mendeley.com/datasets/rtx9ngb68j
- **License**: CC BY 4.0
- **Size**: ~800 MB
- **Images**: 4,730
- **Classes**: 12 vegetable types (Tomato, Capsicum, Cucumber, Eggplant, Potato, Onion, Carrot, Radish, Bean, Pumpkin, etc.)
- **Why**: Adds crop recognition diversity with real-world smartphone images from Bangladesh. Useful for future crop classifier expansion. Poco F3 smartphone, natural light, market/field photos.
- **Acquisition**: Direct Mendeley download, no authentication.

#### 6. Grapevine Leaf Variety & Disease Dataset (GLVD)
- **URL**: https://zenodo.org/records/18937397
- **License**: CC BY 4.0
- **Size**: ~1.1 GB
- **Images**: 4,326 disease images
- **Classes**: Downy Mildew, Powdery Mildew, Black Rot, Healthy, Leaf Blight, Bacterial Rot
- **Why**: Adds Downy_mildew from non-grape sources (currently 100% grapevine in commercial core). Also strengthens Grape_black_rot with mobile phone field images.
- **Acquisition**: Direct Zenodo download, no authentication.

### 5.3 P2 — Optional (Inspect First)

#### 7. DIsease Dataset (figshare, Junhao Xie)
- **URL**: https://figshare.com/articles/dataset/DIsease_Dataset/28612433
- **License**: CC BY 4.0
- **Size**: 163 MB
- **Images**: Unknown
- **Why**: Very small download, CC BY 4.0, general plant disease coverage. Worth inspecting after the P0/P1 datasets. May contain useful classes or may be redundant.
- **Acquisition**: Direct figshare download, no authentication.

### 5.4 Explicitly Excluded

| Dataset | Reason |
|---------|--------|
| PlantVillage-derived figshare datasets | Confirmed PlantVillage redistribution (Phase 28 SHA256) |
| AD Dataset | Too small (502 images, 4 classes) |
| DiaMOS | Download impractical (~10.4 GB, corrupted) |
| FieldPlant | Authentication barrier (Roboflow API) |
| CWD30 | License unclear (Elsevier) |
| IP102 | Academic use only |
| DeepWeeds | Australian weeds only — not relevant to v1 disease classifier |
| PlantSeg | CC BY-NC 4.0 — non-commercial |

---

## 6. External Test Set Status

**NO APPROVED EXTERNAL TEST SET EXISTS.**

This is documented and accepted. The lack of an external test set does not block the architectural/data specification.

**What an ideal external test set would look like:**
- Independent from PlantVillage, Irish Potato, PlantDoc, Grapevine
- Commercially usable (CC0, CC BY, Public Domain)
- Geographically diverse (USA, Europe, Asia)
- Field-realistic (garden photos, not lab)
- Gardener-like photographs (whole plants, natural backgrounds, variable lighting)
- Minimum 500 images per class
- Not derived from PlantVillage

**Practical path forward:**
1. Train v1 with same-source validation
2. Use PlantDoc-held-out as the best available proxy for external performance
3. After v1 exists, actively seek an external test set using the same criteria
4. Do NOT use PlantVillage-derived datasets as external test (already confirmed as redistribution)

---

## 7. How Much Additional Data Is Actually Needed?

### 7.1 The Short Answer

**We need ~5,000–10,000 additional targeted images, not millions.**

The current 98,642-image corpus is sufficient for a **reasonable v1** for 8–10 classes. The problem is not quantity — it is **diversity and source independence**.

### 7.2 Targeted Needs by Class

| Class | Current | Minimum Needed | Good Target | Source Needed |
|-------|---------|---------------|-------------|---------------|
| Cedar_apple_rust | 362 | 500 | 1,000 | Field images, different geography |
| Apple_scab | 723 | 500 | 1,000 | Field orchard images |
| Downy_mildew | 1,002 | 500 | 1,000 | Non-grape sources (tomato, potato, cucumber) |
| Anthracnose | 0 | 500 | 1,000 | Any crop, field images |
| Tomato_mosaic_virus | 427 | 300 | 500 | Diverse field images |
| Peach_bacterial_spot | 2,297 | 0 | 500 | Second source for robustness |
| Rust | 1,308 | 0 | 500 | Non-PlantVillage sources |
| Grape_black_rot | 1,244 | 0 | 500 | Field grape images |
| Spider_mite | 1,678 | 0 | 500 | Non-PlantVillage sources |

**Total additional images needed**: ~5,000–8,000 targeted images across 9 classes.

### 7.3 What Type of Images Are Needed

Not just "more images." We need:

1. **Field images for lab-dominated classes**: 80% of our corpus is lab photography. Classes like Bacterial_spot, Leaf_spot, Tomato_yellow_leaf_curl need field images showing symptoms in real garden context.

2. **Geographic diversity**: 55% of images are from one source (PlantVillage, USA). Need images from different climates, lighting conditions, and camera types.

3. **Second sources for single-source classes**: Downy_mildew (100% grapevine) and Peach_bacterial_spot (100% PlantVillage) are dangerous.

4. **Entirely new classes**: Anthracnose and 14 other disease classes have zero images. These require new dataset discovery or personal photography.

---

## 8. Model + Data Experiment Plan

### Phase 1: Data Acquisition (Human Action Required)

The human downloads these datasets:
1. Plant Pathology Challenge 2020 → `training_data/raw/plant_pathology_2020/`
2. ICAR-CITH Apple Disease → `training_data/raw/icar_apple/`
3. Multi-Crop Disease Dataset → `training_data/raw/multi_crop_disease/`
4. Apple Disease Manalagi → `training_data/raw/apple_disease_manalagi/`
5. Bangladesh Vegetables → `training_data/raw/bangladesh_veg/`
6. GLVD → `training_data/raw/glvd/`

### Phase 2: Pipeline Execution

```powershell
python training/pipeline.py --step prepare
python training/pipeline.py --step validate
python training/quality_checker.py
python training/pipeline.py --step deduplicate
python training/pipeline.py --step split
python training/pipeline.py --step report
```

### Phase 3: Baseline Training

```powershell
python training/train.py --domain diseases --model mobilenet_v3_large --input_size 224
```

- Frozen backbone: 3–5 epochs, LR 1e-3
- Fine-tuning: 10–20 epochs, LR 1e-5 (backbone), 1e-4 (head)
- Early stopping: patience 5 on validation macro F1
- Class weighting: inverse frequency, capped at 10.0

### Phase 4: Evaluation

- Same-source validation: 70/15/15 split, source-aware
- PlantDoc-only test: held-out external proxy
- Metrics: accuracy, macro F1, per-class precision/recall, confusion matrix
- Report domain gap explicitly

### Phase 5: Iteration

If baseline macro F1 < 0.80 on same-source validation:
- Run Experiment A (class balancing)
- Run Experiment C (stronger augmentation)

If PlantDoc test accuracy < 70%:
- Run Experiment B (add diverse datasets)
- Consider field data collection for worst-performing classes

---

## 9. Answers to the Big Question

### 1. What base model should we use?

**MobileNetV3 Large** for production. **EfficientNet-Lite4** as accuracy reference.

### 2. Why?

- Smallest viable model (~5 MB INT8) — fastest inference on Android
- Mature TFLite toolchain — no experimental deployment paths
- Proven transfer-learning performance on image classification
- Low training cost (~2–4 hours on GTX 1060)
- Hard-Swish activations quantization-friendly

### 3. Is Phi-3 appropriate? Why or why not?

**No.** Phi-3.5 Vision is a 4.1B-parameter multimodal language model designed for open-ended visual reasoning. Soil & Supper needs a deterministic, bounded-latency, structured classifier that runs offline on a phone. Phi-3 requires 8–12 GB VRAM, has no TFLite export path, cannot guarantee bounded latency, and introduces hallucination risk. It solves a different problem.

### 4. Should we use one model or multiple specialized models?

**One flat disease classifier for v1.** The existing modular architecture (domain router + hierarchical classifiers) is architecturally sound but over-engineered for v1. Disease data is the strongest domain (98,642 images). Crop/weed/insect data is too weak or missing. Start with one model, prove the pipeline, then modularize in v2.

### 5. How many classes should v1 actually contain?

**14 disease classes.** These are the only classes with ≥300 commercial images from ≥2 sources. The other 15 disease classes have zero images and cannot be trained.

### 6. Which existing classes already have enough data?

8 classes are strong: Healthy, Late_blight, Leaf_spot, Early_blight, Bacterial_spot, Powdery_mildew, Squash_powdery_mildew, Tomato_yellow_leaf_curl.

### 7. Which classes need more data?

9 classes need additional data: Cedar_apple_rust, Apple_scab, Downy_mildew, Tomato_mosaic_virus, Peach_bacterial_spot, Rust, Grape_black_rot, Septoria_leaf_spot, Spider_mite.

### 8. Approximately how many additional images are actually needed?

**5,000–10,000 targeted images.** Not millions. The pretrained backbone reduces the per-class requirement to 500–1,000 diverse images for most classes. The bottleneck is diversity, not quantity.

### 9. What type of images are needed rather than merely what quantity?

- **Field images** for lab-dominated classes (Bacterial_spot, Leaf_spot, Tomato_yellow_leaf_curl)
- **Geographic diversity** (currently 55% USA via PlantVillage)
- **Second sources** for single-source classes (Downy_mildew, Peach_bacterial_spot)
- **Real garden context** (whole plants, soil, mixed backgrounds)

### 10. Which 5–10 datasets should the human acquire?

See Section 5. The prioritized list is:
1. Plant Pathology Challenge 2020 (P0)
2. ICAR-CITH Apple Disease Dataset (P0)
3. Multi-Crop Disease Dataset (P0)
4. Apple Disease Dataset Manalagi (P1)
5. Bangladesh Comprehensive Vegetables (P1)
6. Grapevine Leaf Variety & Disease Dataset (P1)
7. DIsease Dataset figshare (P2, optional)

### 11. Which one should the human acquire FIRST?

**Plant Pathology Challenge 2020.** It provides 1,399 Cedar_apple_rust images (tripling current count) and 1,200 Apple_scab field images. No other single dataset fills more critical gaps.

### 12. What experiment should we run immediately after acquisition?

**Baseline training** with MobileNetV3 Large on the expanded dataset:
- Frozen backbone: 3–5 epochs
- Fine-tuning: 10–20 epochs
- Class-weighted loss
- Source-aware 70/15/15 split
- Report same-source accuracy, PlantDoc-only accuracy, and domain gap

---

## 10. Dataset Acquisition Stopping Rule

**STOP when:**
1. Human has downloaded datasets 1–6 from Section 5
2. All 14 trainable classes have ≥500 images from ≥2 sources (or ≥1,000 from 1 source)
3. Cedar_apple_rust ≥ 500, Apple_scab ≥ 500, Downy_mildew from ≥2 sources
4. Anthracnose either found OR explicitly deferred to v2

**Do NOT continue searching if:**
- Next candidate requires authentication barriers
- Next candidate is PlantVillage-derived
- Next candidate is <500 images or <10 useful images per class
- Next candidate has unclear commercial licensing

**After stopping:**
1. Run full pipeline: prepare → validate → deduplicate → split → report
2. Train v1 disease classifier
3. Evaluate with metrics in Section 4
4. Document domain gap
5. If domain gap >15%, consider field-data collection for v2

---

## 11. External Test Set Status

**NO APPROVED EXTERNAL TEST SET EXISTS.**

This is documented and does not block progress. See Section 6 for details.

---

## 12. Exact Recommended Next Action

1. **Human downloads 5 datasets** (Plant Pathology 2020, ICAR-CITH, Multi-Crop Disease, Manalagi, Bangladesh Vegetables) using a browser
2. **Human places datasets** in `training_data/raw/` with appropriate folder names
3. **Run preparation pipeline**: `python training/pipeline.py --step prepare`
4. **Train v1**: `python training/train.py --domain diseases --model mobilenet_v3_large --input_size 224`
5. **Evaluate**: Report same-source accuracy, PlantDoc-only accuracy, domain gap

**Do NOT:**
- Download more datasets after these 5
- Fight authentication systems
- Use PlantVillage-derived datasets
- Train before pipeline completes
- Modify Android/Kotlin files
- Claim to have an external test set

---

*Strategy generated: 2026-08-18*  
*Phase: ML Model Architecture + Data Strategy*  
*Workstream: ML / DATA ONLY*  
*No model training occurred during this phase.*  
*No Android/Kotlin files were modified.*
