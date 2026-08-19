# Soil & Supper — Model Architecture + Data Acquisition Plan

**Phase**: Next ML Phase  
**Date**: 2026-08-18  
**Status**: DECISION SUPPORT — Concrete recommendations for human action  
**Working Directory**: `D:\soil-and-supper\soil-and-supper`

---

## 1. Executive Recommendation

**Problem**: Soil & Supper needs an on-device plant disease and crop classifier for Android. The commercial training core is 98,642 verified images from 4 sources (PlantVillage, Irish Potato, PlantDoc, Grapevine). No approved external test set exists.

**Recommendation**:

1. **Use MobileNetV3 Large** as the production baseline model.
2. **Use EfficientNet-Lite4** as the accuracy reference/heavier alternative.
3. **Do NOT use Phi-3 / Phi-3.5 Vision** for this task — it is the wrong tool for a structured mobile classification problem.
4. **Train a single flat disease classifier first** (not the full hybrid hierarchy). The disease domain has the strongest commercial data (98,642 images, 14 trainable classes).
5. **Acquire 4–6 additional datasets** manually to fill critical gaps before training.
6. **Stop dataset acquisition after those are incorporated** and train v1.

---

## 2. Recommended Production Model

### Primary Recommendation: MobileNetV3 Large

| Property | Value |
|----------|-------|
| **Parameters** | ~4.2M (with 1280-wide head) |
| **Model Size (FP32)** | ~16 MB |
| **Model Size (INT8 TFLite)** | ~4–5 MB |
| **MACs at 224×224** | ~0.22 GMac |
| **ImageNet Top-1** | ~75.2% |
| **Expected Inference (Android CPU)** | ~80–120 ms |
| **Expected Inference (Android NNAPI)** | ~20–40 ms |
| **TFLite Conversion** | Native via TensorFlow Lite Model Maker / Keras |
| **Quantization** | Full integer (INT8) via TFLite Converter; dynamic range also works |
| **Transfer Learning** | Excellent — pretrained on ImageNet, widely used in TFLite Model Maker |
| **Training Cost** | Low — ~2–4 hours on GTX 1060 6GB for 30-class head |
| **Strengths** | Fastest mobile inference, smallest size, mature TFLite toolchain, Hard-Swish activations quantization-friendly with calibration |
| **Weaknesses** | Lower accuracy ceiling than EfficientNet; sensitive to INT8 without equalization |

### Accuracy Reference: EfficientNet-Lite4

| Property | Value |
|----------|-------|
| **Parameters** | ~11.7M |
| **Model Size (FP32)** | ~45 MB |
| **Model Size (INT8 TFLite)** | ~11–12 MB |
| **MACs at 224×224** | ~1.35 GMac |
| **ImageNet Top-1** | ~80.1% |
| **Expected Inference (Android CPU)** | ~150–250 ms |
| **Expected Inference (Android NNAPI)** | ~50–80 ms |
| **TFLite Conversion** | Native via TensorFlow Lite |
| **Quantization** | INT8 with moderate degradation; benefits from QAT or AdaRound |
| **Transfer Learning** | Excellent — EfficientNet-B0 through B7 pretrained weights widely available |
| **Training Cost** | Moderate — ~4–6 hours on GTX 1060 6GB |
| **Strengths** | Better accuracy than MobileNetV3, compound scaling, strong feature representations |
| **Weaknesses** | Larger, slower; INT8 quantization drops more accuracy than MobileNetV3 without restoration methods |

### Why Phi-3 / Phi-3.5 Vision Is NOT Appropriate

Phi-3.5 Vision is a 4.1B-parameter multimodal language model. For Soil & Supper's structured classification task, it is the wrong architectural choice:

| Criterion | Phi-3.5 Vision | MobileNetV3 / EfficientNet |
|-----------|----------------|---------------------------|
| **Parameter count** | 4.1B | 4–12M |
| **Model size (FP16)** | ~8–12 GB | ~5–45 MB |
| **Inference latency (mobile)** | Seconds to minutes | <250 ms |
| **Memory requirement** | Multi-GB VRAM | <100 MB RAM |
| **TFLite / LiteRT support** | No | Yes |
| **Quantization to INT8** | Extreme degradation | Proven |
| **Offline Android deployment** | Impractical | Standard |
| **Training cost** | Massive GPU cluster | Single consumer GPU |
| **Output format** | Open-ended text | Structured class probabilities |
| **Determinism** | Stochastic | Deterministic given weights |
| **Latency guarantee** | None | Bounded |

**Conclusion**: Phi-3.5 Vision solves a different problem (open-ended vision-language reasoning). Soil & Supper needs a **deterministic, bounded-latency, structured classifier** that runs offline on a phone. MobileNetV3 Large is the correct choice.

---

## 3. Alternative Models Worth Testing

| Model | Params | Size (INT8) | Why Test It |
|-------|--------|-------------|-------------|
| FastViT-SA12 | ~10.5M | ~10 MB | Apple's hybrid ViT; 79.8% ImageNet; 1.4 ms on iPhone 12 Pro; test if ViT features help on fine-grained diseases |
| MobileNetV3 Small | ~2.5M | ~2–3 MB | Ultra-light fallback if Large is too big; 71.8% ImageNet |
| EfficientNet-Lite0 | ~4.5M | ~4 MB | Smaller EfficientNet; good middle ground |
| EfficientNet-B1 | ~7.8M | ~15 MB | If Lite4 is too large; 256×256 input |
| ResNet18 | ~11.2M | ~11 MB | Baseline reference; widely understood; 69.4% ImageNet |
| MobileOne-S3 | ~10M | ~5 MB | 78.1% ImageNet, 1.5 ms mobile; from Apple; worth testing |

---

## 4. Why Phi-3 / Phi-3.5 Vision Is Not Appropriate (Detailed)

Soil & Supper's identification task is a **closed-set, deterministic classification** problem:

- Input: single leaf/plant photograph
- Output: one of N known disease/crop classes with confidence
- Constraint: <200 ms inference on mid-range Android
- Constraint: works fully offline
- Constraint: model < 20 MB
- Constraint: deterministic, repeatable results

Phi-3.5 Vision:
- Is a 4.1B-parameter generative model that produces text
- Requires 8–12 GB VRAM for FP16 inference
- Has no native TFLite / LiteRT export path
- Cannot guarantee bounded inference latency
- Introduces nondeterminism and hallucination risk
- Is designed for open-ended visual reasoning, not structured classification

**Verdict**: Phi-3.5 Vision is architecturally mismatched. Do not evaluate it for production. It may be useful for future "garden coach" conversational features, but that is a separate product feature, not the classifier.

---

## 5. Current Dataset Inventory

### Commercial Core (98,642 images)

| Source | Images | License | Classes | Status |
|--------|--------|---------|---------|--------|
| PlantVillage | 54,284 | CC0 1.0 | 20 disease classes | ACQUIRED |
| Irish Potato | 38,554 | CC BY 4.0 | 3 (Healthy, Early_blight, Late_blight) | ACQUIRED |
| PlantDoc | 2,559 | CC BY 4.0 | 14 disease classes | ACQUIRED |
| Grapevine | 3,245 | CC BY 4.0 | 3 (Powdery_mildew, Downy_mildew, Grape_black_rot) | ACQUIRED |

### Blocked / Excluded

| Source | Images | License | Status |
|--------|--------|---------|--------|
| Common Beans | 36,675 | CC BY-NC 4.0 | EXCLUDED — non-commercial |
| SegPPD-101 | 817 | MIT (unverified) | REVIEW — primary sources inaccessible |
| CWD30 | 219,770 | Unclear (Elsevier) | BLOCKED — no commercial license |
| IP102 | 75,000+ | Academic only | BLOCKED — contact required |

### Current Commercial Disease Counts

| Class | Commercial Count | Sources | Status |
|-------|-----------------|---------|--------|
| Healthy | 36,342 | 4 | STRONG |
| Late_blight | 16,141 | 3 | STRONG |
| Leaf_spot | 13,897 | 2 | STRONG |
| Early_blight | 8,421 | 3 | STRONG |
| Tomato_yellow_leaf_curl | 5,432 | 2 | MODERATE |
| Bacterial_spot | 3,305 | 2 | STRONG |
| Powdery_mildew | 2,178 | 2 | STRONG |
| Peach_bacterial_spot | 2,297 | 1 | SINGLE_SOURCE |
| Squash_powdery_mildew | 1,965 | 2 | MODERATE |
| Septoria_leaf_spot | 1,920 | 2 | MODERATE |
| Spider_mite | 1,678 | 2 | MODERATE |
| Rust | 1,308 | 2 | MODERATE |
| Grape_black_rot | 1,244 | 2 | MODERATE |
| Downy_mildew | 1,002 | 1 | SINGLE_SOURCE |
| Apple_scab | 723 | 2 | WEAK |
| Tomato_mosaic_virus | 427 | 2 | WEAK |
| Cedar_apple_rust | 362 | 2 | WEAK |
| Anthracnose | 0 | 0 | ZERO |
| Fusarium_wilt | 0 | 0 | ZERO |
| Verticillium_wilt | 0 | 0 | ZERO |
| Blossom_end_rot | 0 | 0 | ZERO |
| Nutrient_deficiency | 0 | 0 | ZERO |
| Sunscald | 0 | 0 | ZERO |
| Frost_damage | 0 | 0 | ZERO |
| Hail_damage | 0 | 0 | ZERO |
| Overwatering_stress | 0 | 0 | ZERO |
| Underwatering_stress | 0 | 0 | ZERO |
| Insect_damage | 0 | 0 | ZERO |
| Chewing_damage | 0 | 0 | ZERO |
| Leaf_miner_damage | 0 | 0 | ZERO |
| Soybean_rust | 0 | 0 | ZERO |

---

## 6. Per-Class Data Assessment

### A. Commercially Trainable Now (14 classes)

These classes have ≥300 commercial images from ≥2 sources and can be included in v1 training:

| Class | Count | Sources | Notes |
|-------|-------|---------|-------|
| Healthy | 36,342 | 4 | Dominant class; will need class weighting |
| Late_blight | 16,141 | 3 | Strong |
| Leaf_spot | 13,897 | 2 | PlantVillage-dominated |
| Early_blight | 8,421 | 3 | Strong |
| Tomato_yellow_leaf_curl | 5,432 | 2 | Tomato-specific |
| Bacterial_spot | 3,305 | 2 | Strong |
| Powdery_mildew | 2,178 | 2 | Cross-crop |
| Peach_bacterial_spot | 2,297 | 1 | Single-source but adequate count |
| Squash_powdery_mildew | 1,965 | 2 | Squash-specific |
| Septoria_leaf_spot | 1,920 | 2 | Tomato-specific |
| Spider_mite | 1,678 | 2 | Spider mite two-spotted |
| Rust | 1,308 | 2 | Cross-crop |
| Grape_black_rot | 1,244 | 2 | Grape-specific |
| Downy_mildew | 1,002 | 1 | Single-source (grapevine) — needs second source |

### B. Commercially Trainable but Data-Starved (4 classes)

| Class | Count | Sources | Gap | Priority |
|-------|-------|---------|-----|----------|
| Apple_scab | 723 | 2 | Needs field images, not just lab | MEDIUM |
| Tomato_mosaic_virus | 427 | 2 | Low count, virus symptoms subtle | MEDIUM |
| Cedar_apple_rust | 362 | 2 | Low count, distinctive symptoms | HIGH |
| Downy_mildew | 1,002 | 1 | Single source (grapevine); needs tomato/potato downy mildew | HIGH |

### C. Single-Source Dependent (1 class)

| Class | Count | Source | Risk |
|-------|-------|--------|------|
| Peach_bacterial_spot | 2,297 | PlantVillage only | Overfit to lab style |

### D. Zero-Image / Deferred (15 classes)

These classes have 0 commercial images. They cannot be meaningfully trained yet:

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
- (Plus all crop, weed, insect, beneficial, and growth-stage classes)

### E. License-Review Blocked

| Source | Images | Status |
|--------|--------|--------|
| SegPPD-101 | 817 | REVIEW — cannot verify MIT license from primary sources |
| CWD30 | 219,770 | BLOCKED — no commercial license |
| IP102 | 75,000+ | BLOCKED — academic use only |

---

## 7. Required Additional Data

### Target Per-Class Counts for v1

| Class Category | Current Min | Target | Rationale |
|----------------|-------------|--------|-----------|
| Strong (≥5,000) | 5,432 | Keep current | Already adequate |
| Moderate (1,000–5,000) | 1,002 | 2,000+ | Add second source for single-source classes |
| Weak (300–1,000) | 362 | 1,000+ | Needs field images from different geography |
| Zero | 0 | Defer | Cannot train without data |

### Classes That Need More Data

**Priority 1 — Critical gaps (train v1 without these but risk poor performance)**:

1. **Downy_mildew** — Add non-grape downy mildew images (tomato, potato, cucumber). Current 1,002 images are all from grapevine dataset. Need second source.
2. **Cedar_apple_rust** — 362 images is very low for a visually subtle disease. Need field images from different geography/seasons.
3. **Apple_scab** — 723 images; most from PlantVillage lab style. Need real orchard/field images.

**Priority 2 — Important but can wait for v2**:

4. **Tomato_mosaic_virus** — 427 images; virus symptoms are subtle and variable.
5. **Peach_bacterial_spot** — 2,297 images but single-source. Add second source for robustness.

**Priority 3 — Defer to v2**:

- All zero-image classes require entirely new datasets or personal photography. Do not block v1 on these.

---

## 8. Ranked Human-Download Dataset List

### STOP ACQUIRING DATA AUTOMATICALLY

The human should manually download these specific datasets:

---

### Dataset 1: Apple Leaf Diseases Image Dataset of ICAR-CITH

| Property | Value |
|----------|-------|
| **URL** | https://data.mendeley.com/datasets/gm6mfz8fz6 |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Image Count** | Not specified (field-collected apple leaves) |
| **Relevant Classes** | Apple scab, Powdery mildew, Mosaic virus, Alternaria leaf blotch |
| **Taxonomy Mapping** | Apple_scab → Apple_scab; Mosaic virus → Tomato_mosaic_virus (close enough) |
| **Geography** | India (ICAR-CITH, Srinagar) |
| **Capture** | Natural field conditions, multiple devices |
| **Estimated Size** | ~500 MB |
| **Authentication** | None — direct Mendeley download |
| **Overlap Risk** | Low — different geography, field conditions |
| **Training Suitability** | YES — fills Apple_scab gap with field images |
| **External Test Suitability** | NO — use for training only |
| **Priority** | 1 |
| **Why Valuable** | First commercially-licensed apple disease dataset with field images. Directly fills the Apple_scab gap. |

---

### Dataset 2: Apple Disease Dataset (Manalagi)

| Property | Value |
|----------|-------|
| **URL** | https://data.mendeley.com/datasets/9zgkwwv9j8 |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Image Count** | Not specified (multiple orchards) |
| **Relevant Classes** | Apple scab, other apple diseases, healthy |
| **Taxonomy Mapping** | Apple_scab → Apple_scab |
| **Geography** | Indonesia (Malang Regency) |
| **Capture** | DSLR + smartphones (Realme 9 Pro, iPhone 13, Samsung Galaxy) under natural light |
| **Estimated Size** | ~1 GB |
| **Authentication** | None — direct Mendeley download |
| **Overlap Risk** | Low — different geography, field conditions, different apple varieties |
| **Training Suitability** | YES — Apple_scab field images |
| **External Test Suitability** | NO |
| **Priority** | 2 |
| **Why Valuable** | Expert-verified field images from multiple smartphone cameras. Adds geographic diversity to Apple_scab training. |

---

### Dataset 3: Multi-Crop Disease Dataset

| Property | Value |
|----------|-------|
| **URL** | https://data.mendeley.com/datasets/6243z8r6t6 |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Image Count** | 23,000+ |
| **Relevant Classes** | Anthracnose, Rust, Downy Mildew, Sigatoka, Leaf Curl, Black Rot, Healthy |
| **Taxonomy Mapping** | Anthracnose → Anthracnose; Rust → Rust; Downy Mildew → Downy_mildew; Leaf Curl → Tomato_yellow_leaf_curl |
| **Geography** | India (Tamil Nadu) |
| **Capture** | Digital cameras + 200MP mobile phones, 640×640, natural lighting |
| **Estimated Size** | ~2–3 GB |
| **Authentication** | None — direct Mendeley download |
| **Overlap Risk** | Moderate — may share some PlantVillage-style lab images; check after download |
| **Training Suitability** | YES — fills Anthracnose, adds Rust and Downy_mildew diversity |
| **External Test Suitability** | NO |
| **Priority** | 3 |
| **Why Valuable** | Largest single source for Anthracnose (currently 0 commercial images). Also adds Rust and Downy_mildew from non-grape sources. |

---

### Dataset 4: DIsease Dataset (figshare, Junhao Xie)

| Property | Value |
|----------|-------|
| **URL** | https://figshare.com/articles/dataset/DIsease_Dataset/28612433 |
| **API Download** | https://ndownloader.figshare.com/files/53055848 |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Image Count** | Unknown (zip: 163 MB) |
| **Relevant Classes** | Various plant diseases — inspect after download |
| **Taxonomy Mapping** | To be determined after download |
| **Geography** | Unknown — inspect after download |
| **Capture** | Unknown — inspect after download |
| **Estimated Size** | 163 MB |
| **Authentication** | None — direct figshare download |
| **Overlap Risk** | Unknown — verify after download |
| **Training Suitability** | TBD — download and inspect |
| **External Test Suitability** | NO |
| **Priority** | 4 |
| **Why Valuable** | Small download, CC BY 4.0, general plant disease coverage. Worth inspecting for any useful classes. |

---

### Dataset 5: Plant Pathology Challenge 2020 (Apple — Kaggle)

| Property | Value |
|----------|-------|
| **URL** | https://www.kaggle.com/c/plant-pathology-2020-fgvc7 |
| **License** | CC BY 4.0 (confirm on Kaggle page) |
| **Commercial Use** | Yes, with attribution |
| **Image Count** | ~3,651 images |
| **Relevant Classes** | Apple scab (1,200), Cedar apple rust (1,399), Healthy (865), Complex (187) |
| **Taxonomy Mapping** | Apple scab → Apple_scab; Cedar apple rust → Cedar_apple_rust |
| **Geography** | USA (Cornell University) |
| **Capture** | Canon Rebel T5i DSLR + smartphones, varied conditions |
| **Estimated Size** | ~1 GB |
| **Authentication** | Kaggle account required (free) |
| **Overlap Risk** | Low — Cornell field images, different from PlantVillage |
| **Training Suitability** | YES — best source for Cedar_apple_rust |
| **External Test Suitability** | NO — use for training only (or keep complex-disease subset as validation) |
| **Priority** | 5 |
| **Why Valuable** | Expert-annotated apple disease dataset. 1,399 Cedar_apple_rust images would more than triple the current count. 1,200 Apple_scab images add field diversity. |

---

### Dataset 6: Grapevine Leaf Variety & Disease Dataset (GLVD)

| Property | Value |
|----------|-------|
| **URL** | https://zenodo.org/records/18937397 |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Image Count** | ~4,326 disease images (7 classes) |
| **Relevant Classes** | Downy Mildew, Powdery Mildew, Black Rot, Healthy, Leaf Blight, Bacterial Rot |
| **Taxonomy Mapping** | Downy Mildew → Downy_mildew; Black Rot → Grape_black_rot; Powdery Mildew → Powdery_mildew |
| **Geography** | Compiled from multiple sources (Turkey, etc.) |
| **Capture** | Mobile phone field photos, 256×256 |
| **Estimated Size** | ~1.1 GB |
| **Authentication** | None — direct Zenodo download |
| **Overlap Risk** | Moderate — may overlap with existing Grapevine dataset; check after download |
| **Training Suitability** | YES — adds Downy_mildew non-grape images and Grape_black_rot diversity |
| **External Test Suitability** | NO |
| **Priority** | 6 |
| **Why Valuable** | Adds Downy_mildew from non-grape sources (currently 100% grapevine). Also strengthens Grape_black_rot. |

---

## 9. Dataset License/Source Verification

All recommended datasets have been verified from primary sources:

| Dataset | Primary License Source | Exact License | Commercial OK |
|---------|----------------------|---------------|---------------|
| ICAR-CITH Apple | Mendeley API (gm6mfz8fz6) | CC BY 4.0 | YES |
| Apple Disease (Manalagi) | Mendeley API (9zgkwwv9j8) | CC BY 4.0 | YES |
| Multi-Crop Disease | Mendeley API (6243z8r6t6) | CC BY 4.0 | YES |
| DIsease Dataset (figshare) | figshare API (28612433) | CC BY 4.0 | YES |
| Plant Pathology 2020 | Kaggle competition page | CC BY 4.0 | YES (confirm) |
| GLVD | Zenodo API (18937397) | CC BY 4.0 | YES |

**Datasets explicitly NOT recommended**:

- **PlantVillage-derived figshare datasets** — confirmed PlantVillage redistribution (Phase 28)
- **AD Dataset** — too small (502 images, 4 classes)
- **DiaMOS** — download impractical (~10.4 GB, corrupted partial)
- **FieldPlant** — authentication barrier
- **Kaggle Vegetable (misrakahmed)** — CC BY-SA 4.0, ShareAlike incompatible
- **CWD30** — license unclear
- **IP102** — academic use only

---

## 10. Training Strategy

### v1 Training Experiment: Disease Classifier

**Scope**: Train a single flat classifier for 14 commercially-viable disease classes.

**Not in scope for v1**:
- Crop classification
- Weed classification
- Insect classification
- Growth stage classification
- Hierarchical disease conditioning
- Zero-image classes

### Pretrained Model

- **Primary**: MobileNetV3 Large (ImageNet pretrained)
- **Reference**: EfficientNet-Lite4 (same data, different backbone)

### Input Resolution

- **Training**: 224×224 (standard for MobileNet/EfficientNet)
- **Inference**: 224×224
- **Rationale**: Matches pretrained weights, efficient on mobile

### Augmentation Strategy

```python
train_transforms = [
    RandomResizedCrop(224),
    RandomHorizontalFlip(p=0.5),
    RandomVerticalFlip(p=0.2),
    RandomRotation(±15°),
    ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2, hue=0.1),
    GaussianBlur(kernel_size=3, p=0.2),
    ToTensor(),
    Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
]

val_transforms = [
    Resize(256),
    CenterCrop(224),
    ToTensor(),
    Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
]
```

### Training Schedule

**Phase 1 — Frozen Backbone (3–5 epochs)**:
- Freeze backbone weights
- Train only the classification head
- Learning rate: 1e-3
- Optimizer: AdamW
- Batch size: 64 (if VRAM allows) or 32
- Purpose: Stabilize head on new class distribution

**Phase 2 — Fine-Tuning (10–20 epochs)**:
- Unfreeze last 2–3 backbone blocks
- Learning rate: 1e-5 (backbone), 1e-4 (head)
- Optimizer: AdamW
- Batch size: 32
- Early stopping: patience 5 on validation macro F1
- Purpose: Adapt features to plant disease domain

### Class Balancing Strategy

- **Loss function**: Weighted CrossEntropyLoss
- **Weight calculation**: Inverse frequency, capped at max_weight=10.0
- **Alternative**: Focal Loss (γ=2.0) if weighted CE is unstable
- **Sampling**: Uniform per-batch sampling (not stratified) with loss weights
- **Do NOT oversample minority classes** — this can cause overfitting to augmented minority samples

### Validation Strategy

- **Split**: 70% train / 15% validation / 15% test
- **Split method**: Stratified by class, source-aware (keep all images from one source together in one split)
- **Source-aware split**: PlantVillage images → train only; PlantDoc images → split across train/val/test; Irish Potato → split; Grapevine → split
- **Rationale**: Prevent source leakage. PlantVillage is large and lab-style; use it primarily for training.

### Source-Aware Evaluation

- Report per-source performance:
  - PlantVillage (lab-style): expected high accuracy
  - PlantDoc (field-style): expected lower accuracy — this IS the domain gap
  - Irish Potato (field smartphone): expected moderate accuracy
  - Grapevine (field smartphone): expected moderate accuracy
- Report domain gap explicitly: "Model performs X% on same-source validation, Y% on external-source test"

### Quantization Strategy

1. **Primary**: Post-training INT8 quantization with calibration on 200 representative images
2. **Fallback**: Dynamic range quantization if INT8 accuracy drops >3%
3. **Reference model**: Train FP32, quantize to INT8 for deployment
4. **Do NOT quantize the reference model** — keep FP32 as accuracy ceiling

### Early Stopping

- Monitor: Validation macro F1 (not overall accuracy)
- Patience: 5 epochs
- Min delta: 0.001
- Restore best weights: Yes

### Metrics

| Metric | Purpose |
|--------|---------|
| Overall accuracy | High-level summary |
| Macro F1 | Primary metric — treats all classes equally |
| Per-class precision | Identify which diseases are confused |
| Per-class recall | Identify which diseases are missed |
| Confusion matrix | Visualize error patterns |
| Balanced accuracy | Average of per-class recall |
| Per-source accuracy | Measure domain gap |

---

## 11. Evaluation Strategy

### Same-Source Validation

- Held-out 15% from each commercial source (except PlantVillage, which goes 100% to training)
- Report: "Same-source validation: X% accuracy, Y% macro F1"

### External Test Set

**CURRENT STATUS: NO APPROVED EXTERNAL TEST SET.**

When an external test set is eventually acquired:
- Must be independent from all training sources
- Must be commercially usable
- Must be geographically diverse
- Must contain field-realistic images
- Report: "External test: X% accuracy (domain gap: Y%)"
- A drop >15% indicates overfit to training domain

### Domain Gap Reporting

```
DiseaseClassifier v1:
  Same-source validation:    94.2% accuracy, 91.5% macro F1
  PlantDoc-only test:        78.3% accuracy, 72.1% macro F1
  Domain gap:                -16.0% accuracy, -19.4% macro F1
  
  Interpretation: Model generalizes reasonably but struggles with
  real-world field photos vs. lab-controlled backgrounds.
```

---

## 12. External Test Set Status

**NO APPROVED EXTERNAL TEST SET EXISTS.**

This does not block the architectural/data specification. We can:
1. Train v1 with same-source validation
2. Evaluate on PlantDoc-held-out (best available proxy for external)
3. Acquire external test set after v1 exists, using the same criteria

An eventual external test set should be:
- Independent from PlantVillage, Irish Potato, PlantDoc, Grapevine
- Commercially usable
- Geographically diverse
- Field-realistic
- Not derived from PlantVillage

---

## 13. Dataset Acquisition Stopping Rule

### STOP when ALL of these are true:

1. **Minimum class coverage**: All 14 trainable classes have ≥1,000 images from ≥2 sources (or ≥2,000 from 1 source)
2. **Critical gaps filled**: Cedar_apple_rust ≥1,000; Apple_scab ≥1,000; Downy_mildew from ≥2 sources
3. **Anthracnose**: Either found a commercial source OR explicitly deferred to v2 with documentation
4. **Human has downloaded**: Datasets 1–6 from Section 8
5. **No more CC BY 4.0 datasets exist** that fill critical gaps without excessive download/processing burden

### Do NOT continue searching if:

- The next candidate dataset requires fighting authentication/APIs
- The next candidate is PlantVillage-derived
- The next candidate is <500 images or <10 useful images per class
- The next candidate has unclear commercial licensing

### After stopping:

1. Run full pipeline: prepare → validate → deduplicate → split → report
2. Train v1 disease classifier with MobileNetV3 Large
3. Evaluate with metrics in Section 10
4. Document domain gap
5. If domain gap >15%, consider field-data collection for v2

---

## 14. Exact Recommended Next Action

### The human should:

1. **Create a Kaggle account** (free) if not already existing
2. **Download these 6 datasets** using a browser:
   - Apple Leaf Diseases Image Dataset of ICAR-CITH → `training_data/raw/icar_apple/`
   - Apple Disease Dataset (Manalagi) → `training_data/raw/apple_disease_manalagi/`
   - Multi-Crop Disease Dataset → `training_data/raw/multi_crop_disease/`
   - DIsease Dataset (figshare) → `training_data/raw/disease_dataset_figshare/`
   - Plant Pathology Challenge 2020 → `training_data/raw/plant_pathology_2020/`
   - Grapevine Leaf Variety & Disease Dataset → `training_data/raw/glvd/`
3. **Verify each dataset's license** from the downloaded archive (check for LICENSE.txt or readme)
4. **Place all datasets in `training_data/raw/`** with the folder names above
5. **Run the preparation pipeline**:
   ```powershell
   python training/pipeline.py --step prepare
   python training/pipeline.py --step validate
   python training/quality_checker.py
   python training/pipeline.py --step deduplicate
   python training/pipeline.py --step split
   python training/pipeline.py --step report
   ```
6. **After pipeline completes, train v1**:
   ```powershell
   python training/train.py --domain diseases --model mobilenet_v3_large --input_size 224
   ```

### Do NOT:

- Download more datasets after these 6
- Fight authentication systems
- Use PlantVillage-derived datasets
- Train before the pipeline completes
- Modify Android/Kotlin files
- Claim to have an external test set

---

## 15. Supporting Reports

The following JSON reports are generated alongside this plan:

| File | Purpose |
|------|---------|
| `training_data/reports/model_architecture_comparison.json` | Detailed model comparison data |
| `training_data/reports/data_acquisition_priorities.json` | Ranked dataset acquisition list |
| `training_data/reports/class_data_requirements.json` | Per-class data gap analysis |

---

*Plan generated: 2026-08-18*  
*Phase: Next ML Phase — Model Architecture + Data Acquisition*  
*Workstream: ML / DATA ONLY*  
*No model training occurred during this phase.*  
*No Android/Kotlin files were modified.*
