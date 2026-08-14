# Phase 14 — Archive Inspection and Ingestion Report

## Executive Summary

Phase 14 inspected the three existing archives in `training_data/raw/` without modifying them, then ran the improved acquisition diagnostics. None of the three archives contain usable training images.

---

## 1. Archive Inspection Results

### plantvillage.zip
- **Size**: 669,873 bytes (0.64 MB)
- **Archive valid**: YES
- **Files in archive**: 10
- **Actual image files**: 5 (sample/histogram PNGs, not the dataset)
- **Contents**:
  - `downsampled-plant-disease-dataset-main/LICENSE`
  - `downsampled-plant-disease-dataset-main/README.md`
  - `downsampled-plant-disease-dataset-main/downsample_script.py`
  - `downsampled-plant-disease-dataset-main/imgs/plant-labels-histogram.png`
  - `downsampled-plant-disease-dataset-main/imgs/plant256.png`
  - `downsampled-plant-disease-dataset-main/imgs/plant32.png`
  - `downsampled-plant-disease-dataset-main/imgs/plant64.png`
  - `downsampled-plant-disease-dataset-main/imgs/plant96.png`
- **Verdict**: This is the GitHub repository for the downsampled PlantVillage subset, NOT the full 54,306-image PlantVillage dataset. It contains only code and sample/histogram images. **NOT usable for training.**

### bdflower.zip
- **Size**: 21,177 bytes (0.02 MB)
- **Archive valid**: NO
- **Actual file type**: HTML page (Google reCAPTCHA challenge)
- **Contents**: `<html><head><base href="https://www.google.com/recaptcha/challengepage/">`
- **Verdict**: The Mendeley/PMC download URL returned a CAPTCHA page instead of the actual dataset archive. **NOT usable for training.**

### deepweeds_images.zip
- **Size**: 2,427 bytes (0 MB)
- **Archive valid**: NO
- **Actual file type**: HTML page (Google Drive virus scan warning)
- **Contents**: `<title>Google Drive - Virus scan warning</title>`
- **Verdict**: The Google Drive download link returned a virus scan warning page instead of the 468 MB image archive. **NOT usable for training.**

---

## 2. Actual Images on Disk

| Source | Format | Count |
|--------|--------|-------|
| USDA ARS (scraped) | JPG | 20 |
| plantvillage.zip | PNG (samples only) | 5 |
| bdflower.zip | HTML (not images) | 0 |
| deepweeds_images.zip | HTML (not images) | 0 |

**Total usable training images: 20**

---

## 3. Actual Classes Discovered

| Class | Source | Count | Status |
|-------|--------|-------|--------|
| Unknown (USDA ARS unlabeled) | USDA ARS | 20 | INSUFFICIENT |

No class directories exist. The USDA ARS images are unlabeled gallery downloads.

---

## 4. What the Pipeline Now Does Correctly

1. **`verify_acquisition.py --scan`** correctly identifies:
   - Valid archives vs HTML pages
   - Actual image counts inside archives
   - Empty directories
   - Unsupported files

2. **`verify_acquisition.py --status`** produces a per-dataset status table showing READY / MISSING / ARCHIVE / HTML / INVALID

3. **`pipeline.py --step prepare`** now fails with exit code 1 when zero images are found, printing `0 images — NO SOURCE DATA FOUND` instead of silently claiming "already prepared"

4. **`.gitignore`** correctly excludes `training_data/raw/`, archives, and generated data, including `*.7z`

---

## 5. Remaining Datasets Status

| Dataset | Status | Action Required |
|---------|--------|-----------------|
| PlantVillage | ARCHIVE (sample only) | Manual download of full dataset |
| DeepWeeds | HTML (Google Drive blocked) | Manual download from Google Drive |
| Bangladesh Vegetables | MISSING | Manual download |
| Smartphone Vegetable | MISSING | Manual download |
| BanglaVeg | MISSING | Manual download |
| VegNet | MISSING | Manual download |
| PlantDoc | MISSING | Manual download |
| Plant Growth Stage | MISSING | Manual download |
| BDFlower | HTML (CAPTCHA) | Manual download |
| Sunflower Growth | MISSING | Manual download |
| Early-Stage Crops | MISSING | Manual download |
| USDA ARS | READY | 20 images acquired |
| UC IPM Weeds | MISSING | Manual download |
| USDA NRCS | MISSING | Manual download |
| UC IPM Insects | MISSING | Manual download |
| UC IPM Beneficials | MISSING | Manual download |
| Cornell Herbarium | MISSING | Manual download |
| Zenodo Plant Disease | MISSING | Manual download |
| Zenodo Insects | MISSING | Manual download |
| Mendeley Expanded | MISSING | Manual download |

---

## 6. Pipeline Code Changes

### Files Modified
- `training/verify_acquisition.py` — Added HTML detection, improved archive scanning, clearer status reporting (HTML vs ARCHIVE vs INVALID)
- `training/pipeline.py` — Added `acquisition_status` step
- `training/prepare_dataset.py` — Added generic ingestion adapter supporting common directory layouts (`dataset/class/image.jpg`, `dataset/train/class/image.jpg`, `dataset/images/...`), label file parsing (CSV/JSON), and unlabeled image preservation to `hold/`
- `training/prepare_dataset.py` — Loud failure on zero images, exit code 1
- `.gitignore` — Added `*.7z` coverage

### Files Created
- `training/verify_acquisition.py` — Standalone acquisition verification tool
- `docs/PHASE14_ARCHIVE_INSPECTION.md` — This report

---

## 7. Exact Next Steps

**Do not train. Do not download new datasets automatically.**

The repository now accurately tells us what we have:

```powershell
# 1. Check current state
python training/pipeline.py --step acquisition_status
python training/verify_acquisition.py --scan

# 2. After manually downloading datasets into training_data/raw/
python training/pipeline.py --step prepare
python training/pipeline.py --step validate
python training/quality_checker.py
python training/pipeline.py --step deduplicate
python training/pipeline.py --step split
python training/pipeline.py --step report
```

---

## 8. Manual Downloads Still Required

See `docs/PHASE12_MANUAL_DOWNLOAD_MANIFEST.md` for the complete list. The most critical are:

1. **PlantVillage** — Full 54K image dataset from Mendeley
2. **DeepWeeds images** — 468 MB from Google Drive
3. **Bangladesh Vegetables** — 4,730 images
4. **Smartphone Vegetable** — 3,534 images
5. **VegNet** — 6,850 images
6. **PlantDoc** — 2,569 images
7. **Plant Growth Stage Detection** — 7,306 images

---

## 9. Git Status

- **Latest commit**: `6b5b8017`
- **Branch**: `main`
- **Working tree**: Modified (code + docs changes pending commit)
- **Large files in git**: None (all archives gitignored)
- **Changes staged for commit**: None yet
