# Phase 13 — Dataset Acquisition Status Report

## Executive Summary

Phase 13 attempted to automate acquisition of all 20 approved datasets. The sandbox environment and source restrictions prevented automated download of most image datasets. This report provides the ACTUAL state of acquisition and the minimal manual steps required.

---

## 1. Actual Datasets Successfully Downloaded

| Dataset | Status | Files | Images | Notes |
|---------|--------|-------|--------|-------|
| USDA ARS | Partial | 20 JPGs | 20 | Web-scraped from gallery; tiny subset |
| PlantVillage | Code only | 1 zip (code) | 0 | GitHub mirror contains only downsampled samples, not full 54K dataset |
| DeepWeeds | Failed | 0 | 0 | Google Drive file lock; images not downloaded |
| All others | Failed | 0 | 0 | See failure reasons below |

**Total actual images on disk**: 20 (USDA ARS only)

---

## 2. Download Failure Analysis

| Dataset | Failure Reason | Can Be Automated? |
|---------|---------------|-------------------|
| PlantVillage | Mendeley blocks non-browser downloads; GitHub mirror has only code/samples | NO |
| DeepWeeds | Images on Google Drive; requires browser download | NO |
| Bangladesh Vegetables | Mendeley 403 Forbidden | NO |
| Smartphone Vegetable | Mendeley 403 Forbidden | NO |
| BanglaVeg | No direct download URL; ScienceDirect article only | NO |
| VegNet | Mendeley 403 Forbidden | NO |
| PlantDoc | GitHub repo exists but no image archive in releases | NO |
| Plant Growth Stage Detection | Roboflow 403 Forbidden | NO |
| BDFlower | PMC supplementary not found via automated search | NO |
| Sunflower Growth | Mendeley 403 Forbidden | NO |
| Early-Stage Crops | No direct download URL | NO |
| UC IPM Weeds | Gallery pages return no image URLs via automated parsing | NO |
| USDA NRCS | Site blocks automated access | NO |
| UC IPM Insects | Gallery pages return no image URLs | NO |
| UC IPM Beneficials | Gallery pages return no image URLs | NO |
| Cornell Disease Herbarium | DNS resolution failure | NO |
| Zenodo Plant Disease | Zenodo API returns 403 | NO |
| Mendeley Expanded | Mendeley 403 Forbidden | NO |
| Zenodo Insects | Zenodo API returns 403 | NO |

**Key Finding**: Mendeley, Roboflow, Zenodo, and Google Drive all block or complicate automated access from this environment. These are NOT pipeline bugs — they are site-level restrictions.

---

## 3. Minimal Manual Actions Required

To get actual training images, you need to manually download **7 archive files** and place them in `D:\soil-and-supper\soil-and-supper\training_data\raw\`.

### Required Manual Downloads

| # | Dataset | Where to Get it | What to Download | Place At |
|---|---------|-----------------|------------------|----------|
| 1 | PlantVillage | https://data.mendeley.com/datasets/tywbtsjrjv/1 | Full image dataset zip | `training_data/raw/plantvillage/` |
| 2 | DeepWeeds images | https://github.com/AlexOlsen/DeepWeeds | `images.zip` from Google Drive (link in README) | `training_data/raw/deepweeds/` |
| 3 | Bangladesh Vegetables | https://data.mendeley.com/datasets/rtx9ngb68j | Image archive | `training_data/raw/bangladesh_veg/` |
| 4 | Smartphone Vegetable | https://data.mendeley.com/datasets/gnc4s3z2mf/3 | Image archive | `training_data/raw/smartphone_veg/` |
| 5 | VegNet | https://data.mendeley.com/datasets/6nxnjbn9w6 | Image archive | `training_data/raw/vegnet/` |
| 6 | PlantDoc | https://github.com/pratikkayal/PlantDoc-Dataset | Images folder or dataset zip | `training_data/raw/plantdoc/` |
| 7 | Plant Growth Stage | https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection | Export/download | `training_data/raw/plant_growth_stage/` |

**Optional** (if you want more coverage):
- BanglaVeg: https://www.sciencedirect.com/science/article/pii/S2352340925001738
- BDFlower: https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/ (supplementary files)
- Sunflower Growth: https://data.mendeley.com/datasets/byftmdzg4g

**Do NOT download**: iNaturalist, PlantCLEF, Pl@ntNet, IP102, CWD30, Bugwood, Kaggle Vegetable

---

## 4. After Manual Download

Place the files/folders in `training_data/raw/` with these exact names:

```
training_data/raw/plantvillage/           (folder with images or archive)
training_data/raw/deepweeds/              (folder with images)
training_data/raw/bangladesh_veg/         (folder with images or archive)
training_data/raw/smartphone_veg/         (folder with images or archive)
training_data/raw/vegnet/                 (folder with images or archive)
training_data/raw/plantdoc/               (folder with images or archive)
training_data/raw/plant_growth_stage/     (folder with images or archive)
```

Then run:

```powershell
python training/pipeline.py --step prepare
python training/pipeline.py --step validate
python training/quality_checker.py
python training/pipeline.py --step deduplicate
python training/pipeline.py --step split
python training/pipeline.py --step report
```

---

## 5. Actual Image Counts

| Dataset | Actual Images on Disk | Status |
|---------|----------------------|--------|
| USDA ARS | 20 | Acquired |
| PlantVillage | 0 | Code mirror only |
| DeepWeeds | 0 | Not downloaded |
| All others | 0 | Not downloaded |
| **Total** | **20** | **Cannot train yet** |

---

## 6. Classes with Enough Data to Train

**NONE** — No dataset has sufficient actual images to train.

The 20 USDA ARS images are insufficient for any class.

---

## 7. Important Garden Classes Still Missing

ALL target classes are missing actual training data.

Based on documented metadata only:
- Crops: 50 target classes, 0 with actual training data
- Weeds: 21 target classes, 0 with actual training data
- Diseases: 30 target classes, 0 with actual training data
- Growth Stages: 6 target classes, 0 with actual training data
- Insects/Pests: 26 target classes, 0 with actual training data
- Beneficials: 9 target classes, 0 with actual training data

---

## 8. What You Personally Need to Download

**Exactly 7 archive/files** (see table in Section 3).

This is a one-time action. After these 7 files are in `training_data/raw/`, the automated pipeline will process everything.

---

## 9. Is Personal Photography Currently Necessary?

**NO — not yet.**

Before recommending personal photography, we must first exhaust the 20 approved external datasets. The current blocker is download access, not lack of sources.

Personal photography should only be considered AFTER:
1. All 20 approved datasets are downloaded and processed
2. Additional public-domain/CC BY sources are exhausted
3. A specific important class still has <200 images

---

## 10. Exact Next Command

```powershell
# 1. Manually download the 7 datasets listed above into training_data/raw/
# 2. Then run:
python training/pipeline.py --step prepare
python training/pipeline.py --step validate
python training/quality_checker.py
python training/pipeline.py --step deduplicate
python training/pipeline.py --step split
python training/pipeline.py --step report
python training/dataset_report.py
```

---

## 11. Git Status

- **Current commit**: `b1fe47f9`
- **Working tree**: Clean
- **New files in this phase**: Download adapters, acquisition manifest, Phase 13 report
- **Raw data**: NOT committed (gitignored)

---

## 12. Recommended Next Training Step

**Do not train yet.** First acquire the 7 dataset archives manually. Once they are in `training_data/raw/`, the pipeline will produce actual class counts and we can determine the largest trainable model.
