# Soil & Supper — ML Acquisition Queue

**Date**: 2026-08-18  
**Phase**: Human-Directed Dataset Acquisition  
**Scope**: ML/DATA ONLY  
**Status**: AWAITING HUMAN APPROVAL — no datasets downloaded

---

## 1. Executive Summary

This document is the **human approval gate** for dataset acquisition. It translates the strategy in `docs/ML_MODEL_STRATEGY.md` into a concrete, prioritized acquisition queue.

**Do not download anything until the human approves specific entries.**

### Current State
- Commercial core: 98,642 images (4 sources)
- Effective diverse images: ~28,000
- Trainable disease classes: 14 of 30
- Zero-image classes: 15
- Target additional images: 5,000–10,000 targeted images

### Model Decision (Locked)
- Production: MobileNetV3 Large
- Reference: EfficientNet-Lite4
- v1 architecture: One flat 14-class disease classifier
- Phi-3.5 Vision: NOT appropriate

---

## 2. Acquisition Queue Summary

| # | Dataset | Priority | Status | Est. Useful Images | Est. Size | Auth Required |
|---|---------|----------|--------|-------------------|-----------|---------------|
| 1 | Plant Pathology Challenge 2020 | P0 | APPROVED | 2,600 | ~1 GB | Yes (Kaggle) |
| 2 | Apple Leaf Diseases ICAR-CITH | P0 | APPROVED | 800 | ~500 MB | No |
| 3 | Multi-Crop Disease Dataset | P0 | APPROVED | 5,000 | ~2–3 GB | No |
| 4 | Apple Disease Dataset (Manalagi) | P1 | APPROVED | 500 | ~1 GB | No |
| 5 | Bangladesh Comprehensive Vegetables | P1 | APPROVED | 3,000 | ~800 MB | No |
| 6 | Grapevine Leaf Variety & Disease (GLVD) | P1 | APPROVED | 1,500 | ~1.1 GB | No |
| 7 | DIsease Dataset (figshare) | P2 | REVIEW | 200 | 163 MB | No |

### Rejected / Blocked
- PlantVillage-derived figshare datasets → REJECTED (Phase 28 SHA256)
- AD Dataset → REJECTED (too small)
- DiaMOS → BLOCKED (download impractical)
- FieldPlant → BLOCKED (authentication barrier)
- CWD30 → REJECTED (license unclear)
- IP102 → REJECTED (academic only)
- DeepWeeds → REJECTED (wrong geography/domain)
- PlantSeg → REJECTED (CC BY-NC 4.0)

---

## 3. Detailed Acquisition Cards

### Card 1 — Plant Pathology Challenge 2020

| Field | Value |
|-------|-------|
| **Dataset** | Plant Pathology Challenge 2020 |
| **Official Source** | Kaggle Competition / Cornell University |
| **URL** | https://www.kaggle.com/c/plant-pathology-2020-fgvc7 |
| **Primary License Source** | Kaggle competition page + Cornell paper (IEEE/CVF CVPR Workshop 2020) |
| **License** | CC BY 4.0 |
| **License Confidence** | MEDIUM — claimed on Kaggle; primary Cornell source does not explicitly state license in the paper PDF |
| **Commercial Use** | Yes, with attribution (per Kaggle) |
| **Approximate Total Images** | 3,651 |
| **Approximate Relevant Images** | 2,600 (after removing "Complex" class and non-mappable) |
| **Relevant Soil & Supper Classes** | `Apple_scab`, `Cedar_apple_rust`, `Healthy` |
| **New Classes / Coverage** | Cedar_apple_rust (+1,399 images, triples current count), Apple_scab (+1,200 field images) |
| **Field vs Lab** | FIELD — real orchard conditions, Canon Rebel T5i DSLR + smartphones, varied lighting |
| **Geographic Diversity** | USA (Cornell University, New York) — different from Tanzania/India/Portugal |
| **Expected Usefulness** | VERY HIGH — highest-value single dataset. Expert-annotated. Fills two critical gaps. |
| **Estimated Download Size** | ~1 GB |
| **Acquisition Mechanism** | Kaggle download (train.csv + images folder) |
| **Authentication Requirements** | Free Kaggle account required |
| **Known Barriers** | Kaggle account required; accept competition rules |
| **Overlap Risk** | LOW — different geography, field images, expert-annotated, not PlantVillage-derived |
| **Recommended for Acquisition** | YES |
| **Priority** | P0 |
| **Exact Reason** | 1,399 Cedar_apple_rust images would more than triple current count. 1,200 Apple_scab field images add geographic diversity. Expert-annotated by Cornell. This is the single highest-value dataset for filling critical gaps. |

---

### Card 2 — Apple Leaf Diseases Image Dataset of ICAR-CITH

| Field | Value |
|-------|-------|
| **Dataset** | Apple Leaf Diseases Image Dataset of ICAR-CITH |
| **Official Source** | Mendeley Data |
| **URL** | https://data.mendeley.com/datasets/gm6mfz8fz6 |
| **Primary License Source** | Mendeley dataset page (API verified) |
| **License** | CC BY 4.0 |
| **License Confidence** | HIGH — verified from Mendeley API record |
| **Commercial Use** | Yes, with attribution |
| **Approximate Total Images** | Not specified (field-collected apple leaves) |
| **Approximate Relevant Images** | 800 |
| **Relevant Soil & Supper Classes** | `Apple_scab`, `Tomato_mosaic_virus` (Mosaic virus), `Leaf_spot` (Alternaria leaf blotch) |
| **New Classes / Coverage** | Apple_scab field images from India; Mosaic virus images |
| **Field vs Lab** | FIELD — natural field conditions, multiple devices, ICAR-CITH experimental farm |
| **Geographic Diversity** | India (Srinagar, Kashmir) — new region |
| **Expected Usefulness** | HIGH — first commercially-licensed apple disease dataset with field images from India. Directly fills Apple_scab gap with non-PlantVillage, non-lab images. |
| **Estimated Download Size** | ~500 MB |
| **Acquisition Mechanism** | Direct Mendeley download |
| **Authentication Requirements** | None |
| **Known Barriers** | None |
| **Overlap Risk** | LOW — different geography, field conditions, apple varieties |
| **Recommended for Acquisition** | YES |
| **Priority** | P0 |
| **Exact Reason** | Fills Apple_scab gap with non-PlantVillage, non-lab field images. Adds geographic diversity (India). Also provides Mosaic virus images. |

---

### Card 3 — Multi-Crop Disease Dataset

| Field | Value |
|-------|-------|
| **Dataset** | Multi-Crop Disease Dataset |
| **Official Source** | Mendeley Data |
| **URL** | https://data.mendeley.com/datasets/6243z8r6t6 |
| **Primary License Source** | Mendeley dataset page (API verified) |
| **License** | CC BY 4.0 |
| **License Confidence** | HIGH — verified from Mendeley API record |
| **Commercial Use** | Yes, with attribution |
| **Approximate Total Images** | 23,000+ |
| **Approximate Relevant Images** | 5,000 (after mapping to Soil & Supper taxonomy) |
| **Relevant Soil & Supper Classes** | `Anthracnose`, `Rust`, `Downy_mildew`, `Tomato_yellow_leaf_curl` (Leaf curl), `Grape_black_rot` (Black rot) |
| **New Classes / Coverage** | Anthracnose (first commercial source), Rust (non-PlantVillage), Downy_mildew (non-grape) |
| **Field vs Lab** | FIELD — digital cameras + 200MP mobile phones, 640×640, natural lighting, Tamil Nadu farms |
| **Geographic Diversity** | India (Tamil Nadu) — new region |
| **Expected Usefulness** | VERY HIGH — largest single source for Anthracnose. Also adds Rust and Downy_mildew from non-grape, non-PlantVillage sources. |
| **Estimated Download Size** | ~2–3 GB |
| **Acquisition Mechanism** | Direct Mendeley download |
| **Authentication Requirements** | None |
| **Known Barriers** | None |
| **Overlap Risk** | MODERATE — may share some PlantVillage-style lab images; verify after download |
| **Recommended for Acquisition** | YES |
| **Priority** | P0 |
| **Exact Reason** | Largest single source for Anthracnose (currently 0 commercial images). Also adds Rust and Downy_mildew from non-grape, non-PlantVillage sources. 23,000 images across 5 crops. 200MP mobile phone images. |

---

### Card 4 — Apple Disease Dataset (Manalagi)

| Field | Value |
|-------|-------|
| **Dataset** | Apple Disease Dataset (Manalagi) |
| **Official Source** | Mendeley Data |
| **URL** | https://data.mendeley.com/datasets/9zgkwwv9j8 |
| **Primary License Source** | Mendeley dataset page (API verified) |
| **License** | CC BY 4.0 |
| **License Confidence** | HIGH — verified from Mendeley API record |
| **Commercial Use** | Yes, with attribution |
| **Approximate Total Images** | Not specified (multiple orchards) |
| **Approximate Relevant Images** | 500 |
| **Relevant Soil & Supper Classes** | `Apple_scab`, `Healthy` (apple) |
| **New Classes / Coverage** | Apple_scab field images from Indonesia |
| **Field vs Lab** | FIELD — DSLR + smartphones (Realme 9 Pro, iPhone 13, Samsung Galaxy) under natural light |
| **Geographic Diversity** | Indonesia (Malang Regency) — new region |
| **Expected Usefulness** | MODERATE — expert-verified field images from multiple smartphone cameras. Adds geographic and device diversity to Apple_scab. |
| **Estimated Download Size** | ~1 GB |
| **Acquisition Mechanism** | Direct Mendeley download |
| **Authentication Requirements** | None |
| **Known Barriers** | None |
| **Overlap Risk** | LOW — different geography, field conditions, different apple varieties |
| **Recommended for Acquisition** | YES |
| **Priority** | P1 |
| **Exact Reason** | Expert-verified field images from multiple smartphone cameras. Adds geographic diversity (Indonesia) and device diversity to Apple_scab training. |

---

### Card 5 — Bangladesh Comprehensive Vegetables

| Field | Value |
|-------|-------|
| **Dataset** | Bangladesh Comprehensive Vegetables |
| **Official Source** | Mendeley Data |
| **URL** | https://data.mendeley.com/datasets/rtx9ngb68j |
| **Primary License Source** | Mendeley dataset page (API verified) + peer-reviewed publication (DOI: 10.17632/rtx9ngb68j) |
| **License** | CC BY 4.0 |
| **License Confidence** | HIGH — verified from Mendeley API + publication DOI |
| **Commercial Use** | Yes, with attribution |
| **Approximate Total Images** | 4,730 |
| **Approximate Relevant Images** | 3,000 (crop recognition images) |
| **Relevant Soil & Supper Classes** | `Tomato`, `Pepper_sweet`, `Cucumber`, `Eggplant`, `Potato`, `Onion`, `Carrot`, `Radish`, `Bean`, `Pumpkin` |
| **New Classes / Coverage** | Crop recognition diversity for future expansion |
| **Field vs Lab** | FIELD — Poco F3 smartphone, natural light, market/field photos, multiple angles |
| **Geographic Diversity** | Bangladesh — new region |
| **Expected Usefulness** | MODERATE — adds crop recognition diversity with real-world smartphone images. Useful for future crop classifier expansion, not immediately for disease v1. |
| **Estimated Download Size** | ~800 MB |
| **Acquisition Mechanism** | Direct Mendeley download |
| **Authentication Requirements** | None |
| **Known Barriers** | None |
| **Overlap Risk** | MODERATE — some overlap with PlantVillage crop images; check after download |
| **Recommended for Acquisition** | YES |
| **Priority** | P1 |
| **Exact Reason** | Adds crop recognition diversity with real-world smartphone images from Bangladesh. Different geography and capture conditions from PlantVillage. Useful for future crop classifier expansion. |

---

### Card 6 — Grapevine Leaf Variety & Disease Dataset (GLVD)

| Field | Value |
|-------|-------|
| **Dataset** | Grapevine Leaf Variety & Disease Dataset (GLVD) |
| **Official Source** | Zenodo |
| **URL** | https://zenodo.org/records/18937397 |
| **Primary License Source** | Zenodo API record |
| **License** | CC BY 4.0 |
| **License Confidence** | HIGH — verified from Zenodo API record |
| **Commercial Use** | Yes, with attribution |
| **Approximate Total Images** | 4,326 disease images |
| **Approximate Relevant Images** | 1,500 |
| **Relevant Soil & Supper Classes** | `Downy_mildew`, `Powdery_mildew`, `Grape_black_rot` |
| **New Classes / Coverage** | Downy_mildew from non-grape sources (currently 100% grapevine in commercial core) |
| **Field vs Lab** | FIELD — mobile phone field photos, 256×256, natural lighting |
| **Geographic Diversity** | Compiled from multiple sources (Turkey, etc.) |
| **Expected Usefulness** | MODERATE — adds Downy_mildew diversity beyond grapevine-only. Also strengthens Grape_black_rot. |
| **Estimated Download Size** | ~1.1 GB |
| **Acquisition Mechanism** | Direct Zenodo download |
| **Authentication Requirements** | None |
| **Known Barriers** | None |
| **Overlap Risk** | MODERATE — may overlap with existing Grapevine dataset; check after download |
| **Recommended for Acquisition** | YES |
| **Priority** | P1 |
| **Exact Reason** | Adds Downy_mildew from non-grape sources (currently 100% grapevine in commercial core). Also strengthens Grape_black_rot with mobile phone field images. |

---

### Card 7 — DIsease Dataset (figshare, Junhao Xie)

| Field | Value |
|-------|-------|
| **Dataset** | DIsease Dataset |
| **Official Source** | figshare |
| **URL** | https://figshare.com/articles/dataset/DIsease_Dataset/28612433 |
| **API Download** | https://ndownloader.figshare.com/files/53055848 |
| **Primary License Source** | figshare API record 28612433 |
| **License** | CC BY 4.0 |
| **License Confidence** | HIGH — verified from figshare API |
| **Commercial Use** | Yes, with attribution |
| **Approximate Total Images** | Unknown (zip: 163 MB) |
| **Approximate Relevant Images** | 200 (estimate — inspect after download) |
| **Relevant Soil & Supper Classes** | Various — inspect after download |
| **New Classes / Coverage** | Unknown — inspect after download |
| **Field vs Lab** | Unknown — inspect after download |
| **Geographic Diversity** | Unknown — inspect after download |
| **Expected Usefulness** | UNKNOWN — very small download, worth inspecting but may be redundant or low-quality |
| **Estimated Download Size** | 163 MB |
| **Acquisition Mechanism** | Direct figshare download |
| **Authentication Requirements** | None |
| **Known Barriers** | None |
| **Overlap Risk** | Unknown — verify after download |
| **Recommended for Acquisition** | REVIEW |
| **Priority** | P2 |
| **Exact Reason** | Small download, CC BY 4.0, general plant disease coverage. Worth inspecting after P0/P1 datasets. May contain useful classes or may be redundant. Low cost to evaluate. |

---

## 4. Rejected / Blocked Candidates

| Dataset | Status | Reason |
|---------|--------|--------|
| PlantVillage-derived figshare datasets | REJECTED | Confirmed PlantVillage redistribution via SHA256 hash comparison (Phase 28) |
| AD Dataset | REJECTED | Too small (502 images, 4 classes, Early Blight has 11 images) |
| DiaMOS Plant Dataset | BLOCKED | Download impractical (~10.4 GB, corrupted partial download) |
| FieldPlant | BLOCKED | Authentication barrier (Roboflow API key required) |
| CWD30 | REJECTED | License unclear — published in Elsevier journal, no explicit commercial license |
| IP102 | REJECTED | Academic use only — commercial requires contacting author |
| DeepWeeds | REJECTED | Australian weeds only — not relevant to North American garden context |
| PlantSeg | REJECTED | CC BY-NC 4.0 — non-commercial |

---

## 5. Human Approval Gate

### Recommended Acquisition Order

1. **Plant Pathology Challenge 2020** — Highest value. Triples Cedar_apple_rust. Adds Apple_scab field images.
2. **Multi-Crop Disease Dataset** — Largest Anthracnose source. Adds Rust and Downy_mildew diversity.
3. **Apple Leaf Diseases ICAR-CITH** — Apple_scab field images from India.
4. **Apple Disease Dataset Manalagi** — Apple_scab diversity from Indonesia.
5. **Bangladesh Comprehensive Vegetables** — Crop diversity for future expansion.
6. **Grapevine Leaf Variety & Disease (GLVD)** — Downy_mildew non-grape sources.
7. **DIsease Dataset figshare** — Optional, inspect first.

### Estimated Contribution Toward 5,000–10,000 Image Target

| Dataset | Est. Useful Images | Contribution |
|---------|-------------------|--------------|
| Plant Pathology 2020 | 2,600 | Critical gaps (Cedar_apple_rust, Apple_scab) |
| Multi-Crop Disease | 5,000 | Anthracnose, Rust, Downy_mildew |
| ICAR-CITH | 800 | Apple_scab, Mosaic virus |
| Manalagi | 500 | Apple_scab diversity |
| Bangladesh Vegetables | 3,000 | Crop diversity (future) |
| GLVD | 1,500 | Downy_mildew, Grape_black_rot |
| figshare (optional) | 200 | Unknown |
| **Total P0+P1** | **13,400** | Exceeds target |
| **Total P0 only** | **8,400** | Exceeds target |

### Top 3 Candidates and Why

1. **Plant Pathology Challenge 2020** — 1,399 Cedar_apple_rust images (triple current count) + 1,200 Apple_scab field images. Expert-annotated. No other dataset fills more critical gaps.

2. **Multi-Crop Disease Dataset** — 5,000+ relevant images including Anthracnose (currently 0 commercial images), Rust, and Downy_mildew from non-grape sources. Largest single source for Anthracnose.

3. **Apple Leaf Diseases ICAR-CITH** — First commercially-licensed apple disease dataset with field images from India. Directly fills Apple_scab gap with non-PlantVillage, non-lab images.

### Candidates Requiring Human Credentials/Contact

- **Plant Pathology Challenge 2020** — Requires free Kaggle account. No payment required.

All other P0/P1 candidates require no authentication.

### Exact Next Human Decision Required

**Please approve which dataset(s) to acquire.**

Suggested approvals:
- **Minimum viable**: Approve #1 (Plant Pathology 2020) + #3 (Multi-Crop Disease) — fills most critical gaps
- **Recommended**: Approve #1, #2, #3, #4 — fills Apple_scab, Cedar_apple_rust, Anthracnose, Downy_mildew gaps
- **Full acquisition**: Approve #1–#6 — maximum diversity, exceeds 5,000–10,000 target

**Do not approve #7 (figshare) until P0/P1 datasets are inspected.** It is low-priority and unknown value.

---

## 6. Post-Approval Workflow

Once the human approves dataset(s):

1. **Download** the approved dataset(s) to `training_data/raw/<dataset_name>/`
2. **Verify** archive integrity (SHA256 of downloaded archive)
3. **Run preparation pipeline**:
   ```powershell
   python training/pipeline.py --step prepare
   python training/pipeline.py --step validate
   python training/quality_checker.py
   python training/pipeline.py --step deduplicate
   python training/pipeline.py --step split
   python training/pipeline.py --step report
   ```
4. **Update manifests** in `training_data/manifests/`
5. **Update license ledger** in `training_data/manifests/license_verification.jsonl`
6. **Do NOT train yet** — wait for pipeline completion and human review

---

## 7. External Test Set Status

**NO APPROVED EXTERNAL TEST SET EXISTS.**

This is documented and does not block training corpus acquisition. The external test set workflow remains separate.

Current external test candidates:
- DiaMOS: CC BY 4.0 verified, but acquisition blocked by download size (~13.1 GB)
- FieldPlant: CC BY 4.0 verified, but acquisition blocked by Roboflow API authentication

Do not promote training data to external test set merely because it is useful training data.

---

## 8. Strict Boundaries

This phase does NOT:
- Download any datasets
- Train any model
- Modify Android/Kotlin/Compose files
- Modify Garden UI/UX
- Claim to have an external test set
- Commit or push changes

This phase ONLY:
- Produces a human-approval acquisition queue
- Documents license status from primary sources
- Quantifies expected value per dataset
- Prioritizes by information gain

---

*Acquisition queue generated: 2026-08-18*  
*Phase: Human-Directed Dataset Acquisition*  
*Workstream: ML / DATA ONLY*  
*Awaiting human approval before any download or training.*
