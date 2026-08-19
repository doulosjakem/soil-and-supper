# Soil & Supper — ML P0 Human Acquisition Checklist

**Date**: 2026-08-19  
**Phase**: P0 Acquisition Blocker + Re-entry Readiness  
**Scope**: ML/DATA ONLY  

This checklist is for the human operator who will manually acquire the three blocked P0 datasets. The ML pipeline cannot bypass authentication or access controls.

---

## How to Use This Checklist

1. Complete each acquisition step in order.
2. Place the downloaded files in the exact destination shown.
3. Do **not** place HTML pages, error screenshots, or login redirects in the destination directories.
4. After placement, run the verification command shown for each dataset.
5. Once all three datasets are verified, the ML agent will resume autonomous processing.

---

## 1. Plant Pathology Challenge 2020

### Destination
```
training_data/raw/plant_pathology_2020/
```

### Acquisition Platform
Kaggle (free account required)

### Steps
1. Go to https://www.kaggle.com/c/plant-pathology-2020-fgvc7
2. Create a free Kaggle account or sign in.
3. Accept the competition rules.
4. Download the dataset files:
   - `train.csv`
   - `images/` folder (or a ZIP containing images)
5. Extract if necessary.
6. Place the contents directly under `training_data/raw/plant_pathology_2020/`.

### Expected Structure After Placement
```
training_data/raw/plant_pathology_2020/
    train.csv
    images/
        Train_0.jpg
        Train_1.jpg
        ...
```

### What NOT to Place Here
- HTML login pages
- Kaggle error screenshots
- Empty directories
- README files without image data

### Verification Command
```bash
python training/dataset_intake.py training_data/raw/plant_pathology_2020/
python training/process_plant_pathology_2020.py
```

### Expected Output
- Intake report showing valid images
- Processor report showing class counts and duplicate counts
- If the directory is missing or contains no valid images, the scripts will report an error and exit.

---

## 2. Multi-Crop Disease Dataset

### Destination
```
training_data/raw/multi_crop_disease/
```

### Acquisition Platform
Mendeley Data (free account required)

### Steps
1. Go to https://data.mendeley.com/datasets/6243z8r6t6
2. Create a free Mendeley account or sign in.
3. Click "Download All" or the equivalent download button.
4. Save the downloaded archive.
5. Extract the archive.
6. Place the extracted contents under `training_data/raw/multi_crop_disease/`.

**Important**: There is currently a 102 KB placeholder file (`multi_crop_disease.zip`) in that directory. It is an HTML error response from a previous failed download attempt. Remove it before placing the real data.

### Expected Structure After Placement
```
training_data/raw/multi_crop_disease/
    <extracted_contents>/
        Apple/
            Apple_scab/
            Apple_healthy/
        Corn/
            Corn_rust/
            Corn_healthy/
        ...
```

The exact class/crop structure depends on the dataset. The intake script will auto-discover class directories.

### What NOT to Place Here
- HTML error pages
- Mendeley login redirects
- The existing 102 KB placeholder ZIP
- Empty directories

### Verification Command
```bash
python training/dataset_intake.py training_data/raw/multi_crop_disease/
python training/process_multi_crop_disease.py
```

### Expected Output
- Intake report showing valid images, class counts, and duplicate counts
- Processor report showing per-class breakdown
- If the directory contains no valid images, the scripts will report an error and exit.

---

## 3. Apple Leaf Diseases ICAR-CITH

### Destination
```
training_data/raw/icar_apple/
```

### Acquisition Platform
Mendeley Data (free account required)

### Steps
1. Go to https://data.mendeley.com/datasets/gm6mfz8fz6
2. Create a free Mendeley account or sign in.
3. Click "Download All" or the equivalent download button.
4. Save the downloaded archive.
5. Extract the archive.
6. Place the extracted contents under `training_data/raw/icar_apple/`.

**Important**: There is currently a 102 KB placeholder file (`icar_apple.zip`) in that directory. It is an HTML error response from a previous failed download attempt. Remove it before placing the real data.

### Expected Structure After Placement
```
training_data/raw/icar_apple/
    <extracted_contents>/
        Apple_scab/
        Cedar_apple_rust/
        Apple_healthy/
        ...
```

The exact class structure depends on the dataset. The intake script will auto-discover class directories.

### What NOT to Place Here
- HTML error pages
- Mendeley login redirects
- The existing 102 KB placeholder ZIP
- Synthetic/augmented images mixed with field images without documentation

### Synthetic Imagery Warning
A previously evaluated alternative dataset (AppleLeaf9-Enhanced Edition, figshare 23606010) contained CycleGAN synthetic images. If this ICAR-CITH dataset contains any synthetic or augmented images, document that distinction explicitly. Do not silently mix synthetic and field imagery.

### Verification Command
```bash
python training/dataset_intake.py training_data/raw/icar_apple/
python training/process_icar_cith.py
```

### Expected Output
- Intake report showing valid images, class counts, and duplicate counts
- Processor report showing per-class breakdown and synthetic imagery flag
- If the directory contains no valid images, the scripts will report an error and exit.

---

## What Happens After Verification

Once valid data is in place, the ML agent will automatically:

1. Run generic intake (`dataset_intake.py`)
2. Run dataset-specific processor (`process_<dataset_id>.py`)
3. Verify license from primary source
4. Perform taxonomy audit
5. Perform duplicate audit against commercial core and figshare
6. Perform quality audit
7. Determine USE / EXCLUDE / REVIEW / UNKNOWN
8. Generate manifests only for approved data
9. Update commercial class audit
10. Update P0 report

**No model training will occur until all three P0 datasets are processed and the commercial readiness gate is passed.**

---

## Current Blocker Summary

| Dataset | Status | Blocker | Disk State |
|---------|--------|---------|------------|
| Plant Pathology Challenge 2020 | HUMAN-BLOCKED | Kaggle auth required | Directory missing |
| Multi-Crop Disease Dataset | HUMAN-BLOCKED | Mendeley 403 / auth required | 102 KB HTML error file |
| Apple Leaf Diseases ICAR-CITH | HUMAN-BLOCKED | Mendeley 403 / auth required | 102 KB HTML error file |

---

## Contact / Escalation

If you encounter issues:
- Kaggle: https://www.kaggle.com/support
- Mendeley: https://help.mendeley.com

If a dataset cannot be acquired, document the specific blocker and do not substitute P1 datasets.

---

*Checklist created: 2026-08-19*  
*Phase: P0 Acquisition Blocker + Re-entry Readiness*  
*Workstream: ML / DATA ONLY*
