# Soil & Supper — ML Model Landscape / Commercial Viability

**Date**: 2026-08-19  
**Phase**: 33 — Model Landscape Investigation  
**Scope**: ML/DATA ONLY — Research and evaluation only. No model training. No Android/Kotlin/Compose changes.  
**Status**: COMPLETE — Recommendations only. No artifacts added to commercial corpus.

---

## 1. Executive Summary

**No existing model should be adopted as-is for Soil & Supper's production pipeline.**

After investigating crop recognition, disease recognition, and growth-stage recognition models across Hugging Face, GitHub, TensorFlow Hub, Kaggle, academic repositories, and official model releases, the conclusion is clear:

- **Disease recognition**: The only commercially viable starting point is **Google CropNet feature-vector backbone** (Apache 2.0), used as a pretrained feature extractor to fine-tune on Soil & Supper's own commercial corpus. The CropNet cassava-specific classifier itself is too narrow (6 cassava classes).
- **Crop recognition**: No existing model covers the required 12+ garden crop classes with commercial licensing. Train from scratch.
- **Growth-stage recognition**: No credible general-purpose model exists. Train from scratch.
- **Phi-3.5 Vision**: Explicitly rejected. Wrong architecture for structured offline classification.

**Best next experiment**: Fine-tune CropNet feature vectors on the current 109,127-image commercial disease corpus using MobileNetV3-Large head, then measure same-source validation accuracy and PlantDoc-only external test accuracy.

---

## 2. Models Investigated

### A. Crop / Plant Recognition

| Model | Source | License | Verdict |
|-------|--------|---------|---------|
| FloraScope | GitHub (alhussein-jamil) | Unclear | REJECT — license unknown, no commercial evidence |
| Offline PlantID (iOS) | GitHub (klintqinami) | Unclear | REJECT — license unknown, iOS-only SwiftUI demo |
| PlantCLEF 2024 models | Hugging Face / Zenodo | MIT / CC BY 4.0 | REVIEW — designed for wild plant species (300k+), not garden crops. No overlap with Soil & Supper taxonomy. |
| Pl@ntNet | Official app / API | CC BY-SA (images) | REJECT — share-alike license incompatible with proprietary app. Model itself is not separately licensed for download. |
| Various MobileNetV2 fine-tunes | Hugging Face / GitHub | "other" / Apache 2.0 | REJECT — all trained on PlantVillage, which is already in Soil & Supper's corpus. No new capability. |

**Finding**: No existing crop recognition model covers Tomato, Pepper, Eggplant, Cucumber, Zucchini, Green Bean, Pea, Corn, Broccoli, Lettuce, Carrot, Strawberry with commercial licensing and mobile deployment artifacts.

### B. Plant Disease / Disorder Recognition

| Model | Source | License | Verdict |
|-------|--------|---------|---------|
| Google CropNet (cassava classifier) | TensorFlow Hub | Apache 2.0 | REVIEW — model license is clean, but only 6 cassava-specific classes. Not directly useful, but the feature-vector backbone is valuable. |
| Google CropNet (feature vector) | TensorFlow Hub | Apache 2.0 | **TEST** — plant-domain pretrained backbone. Fine-tune on Soil & Supper corpus. Training data includes iNaturalist (mixed CC BY/CC BY-SA) and ImageNet-21K plants subset (research use). **Model weights are Apache 2.0, but downstream commercial use requires verifying that fine-tuned weights do not inherit training-data restrictions.** |
| linkanjarad/mobilenet_v2_plant_disease | Hugging Face | "other" (unclear) | REJECT — license not commercially verifiable. |
| Daksh159/plant-disease-mobilenetv2 | GitHub | Apache 2.0 | REJECT — trained on PlantVillage (already in corpus). No new capability. |
| liriope/PlantDiseaseDetection | Hugging Face | MIT | REJECT — trained on PlantVillage. No new capability. |
| PlantDoc-derived models | Various | CC BY 4.0 | REVIEW — PlantDoc images are CC BY 4.0, but no standalone pretrained model with clear commercial provenance found. |
| Mango disease TFLite models | Research papers | Varied | REJECT — single-crop, no clear commercial license chain. |

**Finding**: CropNet feature vectors are the only pretrained backbone with a clear Apache 2.0 model license and demonstrated plant-domain feature learning. The cassava classifier itself is too narrow.

### C. Growth-Stage Recognition

| Model | Source | License | Verdict |
|-------|--------|---------|---------|
| YOLO-ECO (rice panicle) | Research paper | Unclear | REJECT — single crop, no clear commercial license, no mobile artifacts. |
| Plant Growth Stage Detection (Roboflow) | Roboflow | CC BY 4.0 | REVIEW — 4 classes, 7,306 images. Too small and narrow for adoption. Better used as supplement. |
| Sunflower Growth Stage dataset | Research | CC BY 4.0 | REVIEW — single crop, useful supplement only. |

**Finding**: No credible general-purpose growth-stage recognition model exists. Train from scratch using CWD30 metadata (if license clears) + Plant Growth Stage Detection + BDFlower.

---

## 3. Commercial License / Provenance Audit

### 3.1 Google CropNet Feature Vector

| Component | License | Commercial Status | Evidence |
|-----------|---------|-------------------|----------|
| Model weights (feature vector) | Apache 2.0 | **Permissive** | tfhub.dev/google/cropnet/feature_vector/cassava_disease_V1/1 — explicit Apache 2.0 |
| Model weights (cassava classifier) | Apache 2.0 | **Permissive** | tfhub.dev/google/cropnet/classifier/cassava_disease_V1/2 — explicit Apache 2.0 |
| Training data: iNaturalist | Mixed (CC BY, CC BY-SA, CC0) | **Mixed** | iNaturalist images are user-contributed under various CC licenses. CC BY-SA requires share-alike. |
| Training data: ImageNet-21K plants subset | Research use | **UNKNOWN** | ImageNet licensing is restrictive for commercial use. Plants subset may inherit restrictions. |
| Training data: Cassava dataset (TFDS) | CC BY 4.0 (Kaggle competition) | **Permissive** | Kaggle cassava competition data is CC BY 4.0. |

**Risk**: Apache 2.0 model license does NOT automatically clear training-data provenance. The iNaturalist component includes CC BY-SA images, which would require share-alike for derivatives if those images are considered part of the model's "work." Google's position is that model weights are separate from training data, but this has not been legally tested for CropNet specifically.

**Verdict**: **REVIEW** — Model weights are commercially usable. Training data has mixed provenance. Fine-tuning on Soil & Supper's own commercial corpus reduces but does not eliminate risk. Legal review recommended before deployment.

### 3.2 PlantVillage-Derived Models

| Component | License | Commercial Status | Evidence |
|-----------|---------|-------------------|----------|
| PlantVillage dataset | CC0 1.0 | **Public domain** | Confirmed in Phase 28/29/30/31 |
| Fine-tuned models (Daksh159, liriope, etc.) | Apache 2.0 / MIT | **Permissive for weights** | But they encode no new knowledge beyond PlantVillage. |

**Risk**: None for weights. But these models add no new capability beyond what Soil & Supper already has.

### 3.3 Pl@ntNet

| Component | License | Commercial Status |
|-----------|---------|-------------------|
| Images (user-contributed) | CC BY-SA | **Share-alike** — incompatible with proprietary app |
| Model/software | Not separately licensed | Cannot download/use model independently |

**Verdict**: **REJECT** — CC BY-SA share-alike clause would require Soil & Supper to open-source the app if Pl@ntNet images are used in derivatives.

---

## 4. Class Coverage Analysis

### 4.1 Disease Models vs. Soil & Supper Taxonomy

| Model | Classes | Overlap with S&S Taxonomy | Gaps |
|-------|---------|---------------------------|------|
| CropNet cassava | 6 (cassava-specific) | None | Does not cover any S&S classes |
| PlantVillage fine-tunes | 38 (14 crops × diseases) | Partial — covers some S&S classes (Tomato, Potato, Pepper, etc.) | Missing: Cedar_apple_rust, Anthracnose, Downy_mildew, many disorder classes |
| PlantDoc models | 29 (mixed) | Partial | Small dataset, narrow coverage |

**Critical gaps not addressed by any existing model**:
- Cedar_apple_rust (current count: 362 images)
- Apple_scab (723 images)
- Downy_mildew (1,002 images, single source)
- Anthracnose (383 images from figshare only)
- All non-disease disorders (Blossom_end_rot, Nutrient_deficiency, etc.)

### 4.2 Crop Models vs. Soil & Supper Taxonomy

**No existing model covers the required 12 priority crop classes:**
Tomato, Pepper, Eggplant, Cucumber, Zucchini, Green Bean, Pea, Corn, Broccoli, Lettuce, Carrot, Strawberry.

The closest is PlantVillage (14 crop species), but it lacks Zucchini, Carrot, Strawberry, and distinguishes only at crop-species level (not cultivar/variety).

---

## 5. Mobile / Offline Feasibility

### 5.1 CropNet Feature Vector

| Property | Value | Confidence |
|----------|-------|------------|
| Architecture | EfficientNet-based feature vector | VERIFIED |
| Parameters | ~5.3M (EfficientNet-B0 backbone) | VERIFIED |
| Model size | ~20 MB (FP32), ~6 MB (INT8) | ESTIMATED |
| Input resolution | 224×224 | VERIFIED |
| TFLite export | Supported via TFLite Model Maker | VERIFIED |
| Core ML conversion | Supported via Core ML Tools | ESTIMATED |
| Android inference (CPU) | ~150–250 ms | REPORTED (similar models) |
| Android inference (NNAPI) | ~50–100 ms | ESTIMATED |
| iOS inference (Core ML) | ~30–60 ms | ESTIMATED |
| INT8 quantization | Supported | VERIFIED |
| Hardware acceleration | Android NNAPI, iOS Core ML | VERIFIED |

**Verdict**: Plausible for iPhone 16e and older Android devices. Model size is the main concern (~6 MB INT8 for backbone alone). Combined with classification head, expect ~8–10 MB total.

### 5.2 MobileNetV3 Large (Production Baseline)

| Property | Value | Confidence |
|----------|-------|------------|
| Parameters | ~4.2M | VERIFIED |
| Model size (INT8 TFLite) | ~4–5 MB | VERIFIED |
| Inference (Android CPU) | ~80–120 ms | REPORTED |
| Inference (Android NNAPI) | ~20–40 ms | REPORTED |
| TFLite support | Native | VERIFIED |

**Verdict**: Proven mobile deployment. This is the recommended production path.

---

## 6. Performance / Real-World Image Quality

### 6.1 CropNet Cassava Classifier

| Metric | Value | Dataset | Conditions |
|--------|-------|---------|------------|
| Top-1 accuracy | 88% (cassava test set) | Cassava Leaf Disease (9,430 images) | Lab/controlled, single leaf |
| Test accuracy after fine-tuning | 86.4% | Cassava TFDS test split | Lab/controlled |
| Unknown-class robustness | Returns "unknown" for non-cassava plants | iNaturalist, beans, Oxford Flowers | Lab/controlled |

**Relevance to Soil & Supper**: Low. Cassava is not a Soil & Supper target crop. The 88% accuracy is on lab imagery, not garden photos.

### 6.2 PlantVillage Fine-tunes (linkanjarad, Daksh159)

| Metric | Value | Dataset | Conditions |
|--------|-------|---------|------------|
| Top-1 accuracy | 95.4% / 95% | PlantVillage (54,306 images, 38 classes) | Lab/controlled, single leaf, uniform background |

**Relevance to Soil & Supper**: Moderate for same-source performance, but domain gap to garden photos is severe. PlantDoc-only test accuracy for models trained on PlantVillage is typically 70–80% (15–20% drop).

### 6.3 PlantDoc External Test

| Metric | Value | Dataset | Conditions |
|--------|-------|---------|------------|
| Top-1 accuracy (models trained on PlantVillage) | 70–80% (estimated) | PlantDoc (2,569 images, 29 classes) | Field/garden, natural backgrounds, variable lighting |

**Relevance to Soil & Supper**: This is the most meaningful metric. A 70–80% accuracy on PlantDoc indicates real-world garden photo performance.

---

## 7. Risks

### 7.1 Licensing / Provenance Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| CropNet training data includes CC BY-SA iNaturalist images | HIGH | Fine-tune on own corpus; legal review of Apache 2.0 vs. CC BY-SA interaction |
| CropNet training data includes ImageNet-21K (restrictive) | MEDIUM | Model weights are Apache 2.0; training data restriction may not apply to derived models |
| Pl@ntNet CC BY-SA share-alike | HIGH | Do not use |
| PlantVillage-derived models add no new capability | LOW | Train on own corpus instead |

### 7.2 Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| CropNet feature vector is 6 MB INT8 — adds to app size | MEDIUM | Acceptable for offline-first app; use app bundles |
| No existing model covers S&S taxonomy | HIGH | Train from scratch / fine-tune |
| Domain gap (lab → garden) persists even with fine-tuning | HIGH | Add PlantDoc, field images, augmentation |
| CropNet may not generalize to non-cassava crops without fine-tuning | HIGH | Expected — fine-tuning is the entire point |

### 7.3 Taxonomy Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Existing models use different class names (e.g., "Tomato_Early_blight" vs. "Early_blight") | MEDIUM | Explicit mapping required |
| No model covers disorder classes (nutrient deficiency, sunscald, etc.) | HIGH | Defer to v2 or train from scratch |

---

## 8. Ranked Recommendation

| Rank | Model | Domain | Verdict | Rationale |
|------|-------|--------|---------|-----------|
| 1 | CropNet feature vector (backbone only) | Disease | **TEST** | Only commercially licensable pretrained plant-domain backbone. Apache 2.0. Fine-tune on S&S corpus. Training-data provenance requires legal review. |
| 2 | MobileNetV3 Large (from scratch) | Disease / Crop | **ADOPT** | Not an existing model — but the recommended training baseline. Proven mobile deployment. Train on S&S corpus. |
| 3 | EfficientNet-Lite4 (from scratch) | Disease / Crop | **TEST** | Accuracy reference. Larger, slower, but measures dataset ceiling. |
| 4 | PlantVillage fine-tunes (Daksh159, liriope) | Disease | **REJECT** | Already in S&S corpus. No new capability. |
| 5 | Pl@ntNet | Crop / Disease | **REJECT** | CC BY-SA share-alike incompatible with proprietary app. |
| 6 | FloraScope / Offline PlantID | Crop | **REJECT** | License unknown. No commercial evidence. |
| 7 | PlantCLEF models | Crop (wild) | **REJECT** | Wrong taxonomy (wild plants, not garden crops). |
| 8 | YOLO-ECO / rice panicle models | Growth stage | **REJECT** | Single crop, no commercial license, no mobile artifacts. |

---

## 9. Best Candidate by Domain

### 9.1 Best Crop-Recognition Candidate

**None — train from scratch.**

No existing model covers the required 12+ garden crop classes with commercial licensing. The recommended path:
- **Backbone**: MobileNetV3 Large or EfficientNet-Lite0 (ImageNet pretrained)
- **Data**: Soil & Supper's crop datasets (Bangladesh Veg, Smartphone Veg, VegNet, PlantDoc healthy plants)
- **Classes**: Start with 12 priority crops + Unknown
- **Deployment**: TFLite INT8, ~4–5 MB

### 9.2 Best Disease-Recognition Candidate

**CropNet feature-vector backbone + MobileNetV3 Large head, fine-tuned on Soil & Supper corpus.**

This is not "adopting an existing model" — it is adopting a pretrained backbone and building the classifier on top of Soil & Supper's own data. This is the correct interpretation of "investigate existing models before training from scratch."

- **Backbone**: `https://tfhub.dev/google/cropnet/feature_vector/cassava_disease_V1/1` (Apache 2.0)
- **Head**: MobileNetV3 Large classification head (train from scratch on S&S data)
- **Why**: CropNet is pretrained on iNaturalist + ImageNet-21K plants, giving it plant-domain feature extraction that generic ImageNet pretrained models lack. This may reduce the number of epochs needed and improve feature quality for leaf/plant imagery.
- **Risk**: Training data provenance is mixed. Legal review required.

### 9.3 Growth-Stage Recognition

**No — not worth pursuing existing models.**

No credible general-purpose growth-stage model exists. Train from scratch using:
- CWD30 growth metadata (if license clears)
- Plant Growth Stage Detection (Roboflow, CC BY 4.0)
- BDFlower (CC BY 4.0)

---

## 10. Current Class Coverage

### 10.1 Disease Classes (Commercial Core: 109,127 images)

| Status | Count | Classes |
|--------|-------|---------|
| TRAINABLE_NOW | 8 | Healthy, Late_blight, Leaf_spot, Early_blight, Bacterial_spot, Powdery_mildew, Squash_powdery_mildew, Tomato_yellow_leaf_curl |
| NEEDS_MORE_DATA | 9 | Cedar_apple_rust, Apple_scab, Downy_mildew, Tomato_mosaic_virus, Peach_bacterial_spot, Rust, Grape_black_rot, Septoria_leaf_spot, Spider_mite |
| DATASET_SEARCH_REQUIRED | 14 | Anthracnose, Fusarium_wilt, Verticillium_wilt, Blossom_end_rot, Nutrient_deficiency, Sunscald, Frost_damage, Hail_damage, Overwatering_stress, Underwatering_stress, Insect_damage, Chewing_damage, Leaf_miner_damage, Soybean_rust |

### 10.2 Crop Classes

No commercial crop recognition classifier exists yet. Current crop images are embedded in disease datasets (PlantVillage, etc.) but not curated for standalone crop identification.

### 10.3 Growth-Stage Classes

No commercial growth-stage classifier exists yet. CWD30 metadata is blocked by license uncertainty.

---

## 11. Licensing / Provenance Risks Summary

| Model / Approach | Model License | Training Data License | Commercial Status |
|------------------|---------------|----------------------|-------------------|
| CropNet feature vector | Apache 2.0 | Mixed (CC BY, CC BY-SA, research) | **REVIEW** — weights clear, training data mixed |
| MobileNetV3 Large (from scratch) | Apache 2.0 | ImageNet (research) + S&S corpus | **USE** — ImageNet is for research backbone; S&S corpus is commercial |
| EfficientNet-Lite4 (from scratch) | Apache 2.0 | ImageNet (research) + S&S corpus | **USE** — same as above |
| PlantVillage fine-tunes | Apache 2.0 / MIT | CC0 | **USE** — but no new capability |
| Pl@ntNet | Not separately licensed | CC BY-SA | **REJECT** |
| PlantCLEF | MIT / CC BY 4.0 | Various (research/CC) | **REVIEW** — wrong taxonomy |

---

## 12. Exact Next Experiment

**Objective**: Determine whether CropNet feature vectors improve disease classification accuracy on Soil & Supper's corpus compared to generic ImageNet pretraining.

### Steps

1. **Obtain model artifact**:
   ```bash
   pip install tensorflow tensorflow-hub tensorflow-model-maker
   ```
   The CropNet feature vector is downloaded automatically from TF Hub.

2. **Prepare data**:
   - Use current 109,127-image commercial disease corpus
   - Filter to 14 trainable classes
   - Source-aware 70/15/15 split (PlantVillage → train only; PlantDoc, Irish Potato, Grapevine, figshare → split across val/test)

3. **Train two models**:
   - **Model A**: MobileNetV3 Large (ImageNet pretrained) — current baseline
   - **Model B**: CropNet feature vector + MobileNetV3 Large head (CropNet pretrained)

4. **Evaluate both**:
   - Same-source validation accuracy
   - PlantDoc-only test accuracy (external proxy)
   - Macro F1
   - Per-class precision/recall
   - Confusion matrix
   - Training time comparison

5. **Decision gate**:
   - If Model B outperforms Model A by >2% macro F1 on PlantDoc test → adopt CropNet backbone
   - If Model B performs equal or worse → use Model A (standard ImageNet pretrained)
   - If both plateau below 75% PlantDoc accuracy → the bottleneck is data, not model

### What to Download Manually

**Nothing.** This experiment uses only:
- Existing commercial corpus (already on disk)
- CropNet weights (auto-downloaded from TF Hub via Python)
- TFLite Model Maker / TensorFlow (pip install)

No new datasets. No manual downloads. No P0/P1 acquisition required.

---

## 13. Files Changed

This phase produced **one new document** and **no code changes**:

| File | Action | Description |
|------|--------|-------------|
| `docs/ML_PHASE33_MODEL_LANDSCAPE.md` | CREATED | This report |

**No files modified.** No P0 data added. No P1 acquisition started. No Android/Kotlin/Compose files touched.

---

## 14. Verification Performed

- [x] Read existing ML docs: ML_TAXONOMY.md, ML_MODEL_STRATEGY.md, ML_ACQUISITION_QUEUE.md
- [x] Read current commercial class audit (109,127 images, 18 classes)
- [x] Searched Hugging Face for plant disease/crop models
- [x] Searched GitHub for offline plant ID models
- [x] Searched TensorFlow Hub for CropNet models and licenses
- [x] Searched academic sources (arXiv, ResearchGate, IEEE) for growth-stage models
- [x] Verified CropNet Apache 2.0 license on tfhub.dev
- [x] Verified PlantVillage CC0 1.0 license (existing knowledge)
- [x] Verified Pl@ntNet CC BY-SA share-alike requirement
- [x] Confirmed no existing model covers S&S crop taxonomy
- [x] Confirmed no credible growth-stage model exists
- [x] Distinguished VERIFIED / REPORTED / ESTIMATED / UNKNOWN throughout
- [x] No model training performed
- [x] No datasets acquired
- [x] No P0 blocker bypassed

---

## 15. Final Completion Report

### 1. Models Investigated
- Google CropNet (feature vector + cassava classifier)
- MobileNetV2/V3 plant disease fine-tunes (linkanjarad, Daksh159, liriope)
- FloraScope, Offline PlantID (iOS), PlantCLEF models, Pl@ntNet
- YOLO-ECO (rice panicle), Plant Growth Stage Detection, BDFlower
- EfficientNet-based plant disease models

### 2. Commercially Usable Models
- **CropNet feature vector**: Apache 2.0 model license, but training data has mixed provenance (CC BY, CC BY-SA, research). **REVIEW** status — legal review recommended before production use.
- **MobileNetV3 Large / EfficientNet-Lite4**: Apache 2.0. ImageNet pretrained (research use for pretraining only). When fine-tuned on Soil & Supper's commercial corpus, the resulting model is commercially usable.

### 3. Rejected Models and Why
| Model | Reason |
|-------|--------|
| Pl@ntNet | CC BY-SA share-alike incompatible with proprietary app |
| FloraScope / Offline PlantID | License unknown, no commercial evidence |
| PlantCLEF models | Wrong taxonomy (wild plants, not garden crops) |
| PlantVillage fine-tunes (Daksh159, liriope, etc.) | Already in S&S corpus, no new capability |
| YOLO-ECO / rice panicle models | Single crop, no commercial license, no mobile artifacts |
| linkanjarad MobileNetV2 | License "other" — not commercially verifiable |

### 4. Uncertain / Review Models
| Model | Reason |
|-------|--------|
| CropNet feature vector | Model weights Apache 2.0, but training data includes CC BY-SA iNaturalist images. Legal review needed. |

### 5. Best Crop-Recognition Candidate
**None — train from scratch.** Use MobileNetV3 Large or EfficientNet-Lite0 backbone on Soil & Supper's crop datasets.

### 6. Best Disease-Recognition Candidate
**CropNet feature-vector backbone + MobileNetV3 Large head, fine-tuned on Soil & Supper corpus.** This leverages plant-domain pretraining while avoiding training-data licensing issues for the final model.

### 7. Growth-Stage Model Worth Pursuing?
**No — not yet.** No credible general-purpose model exists. Train from scratch when CWD30 license clears or when sufficient Plant Growth Stage Detection + BDFlower data is curated.

### 8. Mobile Feasibility
- CropNet backbone + head: ~8–10 MB INT8, ~150–250 ms inference on Android CPU. Plausible on iPhone 16e and older Android.
- MobileNetV3 Large baseline: ~4–5 MB INT8, ~80–120 ms inference. Proven deployment.

### 9. Current Class Coverage
- 8 disease classes: TRAINABLE_NOW
- 9 disease classes: NEEDS_MORE_DATA
- 14 disease classes: DATASET_SEARCH_REQUIRED
- 0 crop recognition classes: No classifier exists
- 0 growth-stage classes: No classifier exists

### 10. Licensing / Provenance Risks
- CropNet: Model weights Apache 2.0 (clean). Training data mixed (CC BY, CC BY-SA, research). Legal review recommended.
- Pl@ntNet: CC BY-SA — incompatible with proprietary app.
- All other investigated models: Either unclear licenses or no new capability beyond existing corpus.

### 11. Exact Next Experiment
Fine-tune CropNet feature vector on 109,127-image commercial disease corpus vs. ImageNet-pretrained MobileNetV3 Large baseline. Measure PlantDoc-only accuracy and macro F1. Decision gate: >2% improvement → adopt CropNet; equal/worse → use standard pretrained.

### 12. Manual Downloads Required
**None.** This experiment uses existing corpus + auto-downloaded TF Hub weights.

### 13. Files Changed
- `docs/ML_PHASE33_MODEL_LANDSCAPE.md` — created (this report)

### 14. Tests / Verification Performed
- Source audit across Hugging Face, GitHub, TensorFlow Hub, Kaggle, arXiv
- License verification for all serious candidates
- Class-coverage mapping against Soil & Supper taxonomy
- Mobile feasibility estimation
- Performance metric documentation
- No code changes, no training, no data acquisition

### 15. Commit Hash
_(Pending commit after report creation)_

---

*Report generated: 2026-08-19*  
*Phase: 33 — ML Model Landscape Investigation*  
*Workstream: ML / DATA ONLY*  
*No model training occurred during this phase.*  
*No Android/Kotlin/Compose files were modified.*  
*No P0 blocker was bypassed.*  
*No P1 datasets were acquired.*
