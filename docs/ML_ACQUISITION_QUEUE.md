# Soil & Supper — ML Acquisition Queue (Updated Phase 30)

**Date**: 2026-08-19  
**Phase**: P0 Acquisition Resolution — Phase 30 Intake Path Ready  
**Scope**: ML/DATA ONLY  
**Status**: 1 ACQUIRED, 3 BLOCKED (2 placeholder archives on disk), intake infrastructure complete

---

## 1. Current State Summary

| Metric | Value |
|--------|-------|
| Commercial core (original) | 98,642 images |
| Commercial core (after figshare) | 109,127 images |
| Added from figshare | +10,485 images |
| Trainable disease classes | 18 (was 14, Anthracnose now has 383) |
| Zero-image classes | 14 (was 15) |
| Sources | 5 (added figshare_disease) |
| Intake infrastructure | COMPLETE (dataset_intake.py + per-dataset templates) |

---

## 2. Acquisition Queue

### ACQUIRED

#### 4. DIsease Dataset (figshare) — UPGRADED FROM P2

| Field | Value |
|-------|-------|
| **Dataset** | DIsease Dataset |
| **URL** | https://figshare.com/articles/dataset/DIsease_Dataset/28612433 |
| **License** | CC BY 4.0 |
| **Status** | ACQUIRED |
| **Acquired Date** | 2026-08-18 |
| **Images** | 5,482 |
| **Useful Mapped** | 11,495 (label counts) |
| **New Classes** | Anthracnose (+383), Rust (+2,332), Leaf_spot (+4,366), Powdery_mildew (+2,423), Early_blight (+493), Spider_mite (+488) |
| **Auth Required** | No |
| **Duplicates vs Core** | 0 exact duplicates |

---

### BLOCKED — REQUIRES MANUAL AUTH

#### 1. Plant Pathology Challenge 2020

| Field | Value |
|-------|-------|
| **Dataset** | Plant Pathology Challenge 2020 |
| **URL** | https://www.kaggle.com/c/plant-pathology-2020-fgvc7 |
| **License** | CC BY 4.0 |
| **Status** | BLOCKED — MANUAL AUTH REQUIRED |
| **Blocker** | No Kaggle credentials available |
| **Est. Useful Images** | 2,600 |
| **Auth Required** | Free Kaggle account |
| **Action Required** | Human creates Kaggle account, downloads, places in `training_data/raw/plant_pathology_2020/` |

#### 2. Multi-Crop Disease Dataset

| Field | Value |
|-------|-------|
| **Dataset** | Multi-Crop Disease Dataset |
| **URL** | https://data.mendeley.com/datasets/6243z8r6t6 |
| **License** | CC BY 4.0 |
| **Status** | BLOCKED — MANUAL AUTH REQUIRED |
| **Blocker** | Mendeley returns HTTP 403 Forbidden |
| **Est. Useful Images** | 5,000 |
| **Auth Required** | Mendeley account |
| **Action Required** | Human creates Mendeley account, downloads, places in `training_data/raw/multi_crop_disease/` |
| **Current Disk State** | Placeholder archive only (102 KB HTML error file) |

**Alternative**: Zenodo "Web sourced dataset for plant disease detection" (14051480) — CC BY 4.0, 538.8 MB. Download stalled in this environment. Human can attempt direct download.

#### 3. Apple Leaf Diseases ICAR-CITH

| Field | Value |
|-------|-------|
| **Dataset** | Apple Leaf Diseases Image Dataset of ICAR-CITH |
| **URL** | https://data.mendeley.com/datasets/gm6mfz8fz6 |
| **License** | CC BY 4.0 |
| **Status** | BLOCKED — MANUAL AUTH REQUIRED |
| **Blocker** | Mendeley returns HTTP 403 Forbidden |
| **Est. Useful Images** | 800 |
| **Auth Required** | Mendeley account |
| **Action Required** | Human creates Mendeley account, downloads, places in `training_data/raw/icar_apple/` |
| **Current Disk State** | Placeholder archive only (102 KB HTML error file) |

**Alternative**: AppleLeaf9-Enhanced Edition (figshare 23606010) — CC BY 4.0, 26,755 images, 2.28 GB. Download stalled. Contains synthetic/augmented images.

---

### READY (P1 — Not Yet Approved)

| # | Dataset | Priority | Status | Est. Useful Images | Auth Required |
|---|---------|----------|--------|-------------------|---------------|
| 5 | Apple Disease Dataset (Manalagi) | P1 | READY | 500 | None |
| 6 | Bangladesh Comprehensive Vegetables | P1 | READY | 3,000 | None |
| 7 | Grapevine Leaf Variety & Disease (GLVD) | P1 | READY | 1,500 | None |

---

## 3. Phase 30 Intake Infrastructure

### Completed

| Component | Status | Description |
|-----------|--------|-------------|
| `training/dataset_intake.py` | COMPLETE | Generic intake script: scans raw directories, reports files, corrupt images, dimensions, SHA256 hashes, exact duplicates vs core and figshare, class directories, image counts by class. Does NOT add to training data or mark commercially usable. |
| `training/process_plant_pathology_2020.py` | COMPLETE | Template for Kaggle Plant Pathology 2020 (train.csv + images/). Parses CSV, maps to Soil & Supper taxonomy, checks duplicates. Activates when `training_data/raw/plant_pathology_2020/` exists. |
| `training/process_multi_crop_disease.py` | COMPLETE | Template for Multi-Crop Disease. Discovers class directories, validates images, computes hashes, checks duplicates. Activates when `training_data/raw/multi_crop_disease/` contains real data. |
| `training/process_icar_cith.py` | COMPLETE | Template for ICAR-CITH. Discovers class directories, validates images, computes hashes, checks duplicates. Includes synthetic imagery flag. Activates when `training_data/raw/icar_apple/` contains real data. |

### Intake Process Contract

For every manually acquired dataset:

1. Place downloaded data under `training_data/raw/<dataset_id>/`
2. Run `python training/dataset_intake.py <path>` for generic scan
3. Run the dataset-specific template for structured analysis
4. Verify license from primary source (do NOT infer from platform claims)
5. Record license evidence in `docs/DATASET_LICENSE_LEDGER.md`
6. If license verified and commercial-use permitted: proceed to manifest generation and duplicate audit
7. If license cannot be verified: set status = REVIEW, do not add to training data

### Current Disk State

| Directory | Archive | Status |
|-----------|---------|--------|
| `training_data/raw/multi_crop_disease/` | `multi_crop_disease.zip` (102 KB) | HTML error — not valid data |
| `training_data/raw/icar_apple/` | `icar_apple.zip` (102 KB) | HTML error — not valid data |
| `training_data/raw/plant_pathology_2020/` | *missing* | Awaiting manual acquisition |

## 4. Rejected / Blocked Candidates

| Dataset | Status | Reason |
|---------|--------|--------|
| PlantVillage-derived figshare datasets | REJECTED | Confirmed PlantVillage redistribution (Phase 28 SHA256) |
| AD Dataset | REJECTED | Too small (502 images, 4 classes) |
| DiaMOS Plant Dataset | BLOCKED | Download impractical (~10.4 GB, corrupted) |
| FieldPlant | BLOCKED | Authentication barrier (Roboflow API) |
| CWD30 | REJECTED | License unclear (Elsevier) |
| IP102 | REJECTED | Academic use only |
| DeepWeeds | REJECTED | Australian weeds only |
| PlantSeg | REJECTED | CC BY-NC 4.0 |
| AppleLeaf9-Enhanced Edition | EVALUATED | 2.28 GB, download stalled, contains synthetic images |
| Zenodo Web Sourced Dataset | EVALUATED | 538.8 MB, download stalled at ~84 MB |

---

## 4. Exact Next Human Decision Required

**Acquire these 3 datasets manually:**

1. **Plant Pathology Challenge 2020** via Kaggle
   - Creates free account at kaggle.com
   - Accepts competition rules
   - Downloads train.csv + images folder
   - Places in `training_data/raw/plant_pathology_2020/`

2. **Multi-Crop Disease Dataset** via Mendeley
   - Creates free account at mendeley.com
   - Goes to dataset page
   - Clicks "Download All"
   - Places in `training_data/raw/multi_crop_disease/`

3. **Apple Leaf Diseases ICAR-CITH** via Mendeley
   - Uses same Mendeley account
   - Goes to dataset page
   - Clicks "Download All"
   - Places in `training_data/raw/icar_apple/`

**Do not acquire P1 datasets until P0 is complete.**

---

*Acquisition queue updated: 2026-08-19*  
*Phase: P0 Acquisition Resolution*  
*Workstream: ML / DATA ONLY*
