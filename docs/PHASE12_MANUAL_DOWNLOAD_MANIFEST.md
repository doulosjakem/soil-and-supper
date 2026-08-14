# Phase 12 — Robust Dataset Acquisition: Manual Download Manifest

## Purpose

Many approved datasets block automated downloads or require browser-based access.  
This manifest tells you exactly what to download, where to put it, and what to run next.

**Do NOT download rejected/hold datasets.**

---

## Directory Structure

Place every downloaded archive or extracted folder here:

```
D:\soil-and-supper\soil-and-supper\training_data\raw\
```

If a dataset is already present in this folder, the pipeline will skip re-downloading it.

---

## Dataset Manifest

### Priority 1 — Crops

| # | Dataset ID | What to download | Preferred source / link | Notes |
|---|-----------|------------------|------------------------|-------|
| 1 | `bangladesh_veg` | Image archive | https://data.mendeley.com/datasets/rtx9ngb68j | Look for direct `.zip` or `.tar.gz` on the dataset page |
| 2 | `smartphone_veg` | Image archive | https://data.mendeley.com/datasets/gnc4s3z2mf/3 | Same as above |
| 3 | `banglaveg` | Image archive | https://www.sciencedirect.com/science/article/pii/S2352340925001738 | Check supplementary materials |
| 4 | `vegnet` | Image archive | https://data.mendeley.com/datasets/6nxnjbn9w6 | Mendeley page |
| 5 | `early_stage_crops` | Image archive | https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/ | Supplementary files |
| 6 | `USDA_ARS` | Image archive | https://www.ars.usda.gov/oc/images/image-gallery/ | Bulk download if available |

**Place files/folders at:**
- `training_data/raw/bangladesh_veg/`
- `training_data/raw/smartphone_veg/`
- `training_data/raw/banglaveg/`
- `training_data/raw/vegnet/`
- `training_data/raw/early_stage_crops/`
- `training_data/raw/USDA_ARS/`

---

### Priority 2 — Diseases

| # | Dataset ID | What to download | Preferred source / link | Notes |
|---|-----------|------------------|------------------------|-------|
| 7 | `plantvillage` | Image archive | https://data.mendeley.com/datasets/tywbtsjrjv/1 | Mendeley page |
| 8 | `plantdoc` | Image archive | https://github.com/pratikkayal/PlantDoc-Dataset | GitHub releases / repo files |
| 9 | `cornell_disease_herbarium` | Image archive | https://ppathgbif.cals.cornell.edu/ | GBIF / Cornell portal |

**Place files/folders at:**
- `training_data/raw/plantvillage/`
- `training_data/raw/plantdoc/`
- `training_data/raw/cornell_disease_herbarium/`

---

### Priority 3 — Weeds

| # | Dataset ID | What to download | Preferred source / link | Notes |
|---|-----------|------------------|------------------------|-------|
| 10 | `deepweeds` | `images.zip` | https://github.com/AlexOlsen/DeepWeeds | README links to Google Drive `images.zip` |
| 11 | `uc_ipm_weeds` | Weed image gallery pages | https://ipm.ucanr.edu/PMG/WEEDS/ | Download images from gallery pages |
| 12 | `usda_nrcs_plants` | Plant images | https://plants.usda.gov/ | Per-plant image downloads |

**Place files/folders at:**
- `training_data/raw/deepweeds/`
- `training_data/raw/uc_ipm_weeds/`
- `training_data/raw/usda_nrcs_plants/`

---

### Priority 4 — Growth Stages

| # | Dataset ID | What to download | Preferred source / link | Notes |
|---|-----------|------------------|------------------------|-------|
| 13 | `plant_growth_stage` | Dataset archive | https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection | Roboflow export |
| 14 | `bdflower` | Supplementary archive | https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/ | PMC supplementary files |
| 15 | `sunflower_growth` | Image archive | https://data.mendeley.com/datasets/byftmdzg4g | Mendeley page |

**Place files/folders at:**
- `training_data/raw/plant_growth_stage/`
- `training_data/raw/bdflower/`
- `training_data/raw/sunflower_growth/`

---

### Priority 5 — Insects / Beneficials (Optional expansion)

| # | Dataset ID | What to download | Preferred source / link | Notes |
|---|-----------|------------------|------------------------|-------|
| 16 | `uc_ipm_insects` | Insect gallery images | https://ipm.ucanr.edu/PMG/INSE/ | UC IPM site |
| 17 | `uc_ipm_beneficials` | Beneficial organism images | https://ipm.ucanr.edu/PMG/BENE/ | UC IPM site |

**Place files/folders at:**
- `training_data/raw/uc_ipm_insects/`
- `training_data/raw/uc_ipm_beneficials/`

---

## Naming Convention

Name each downloaded archive exactly as its dataset ID:

```
training_data/raw/<dataset_id>.<ext>
```

Examples:
- `training_data/raw/bangladesh_veg.zip`
- `training_data/raw/plantvillage.tar.gz`

Or, if you extract it before placing it:

```
training_data/raw/<dataset_id>/
```

Examples:
- `training_data/raw/bangladesh_veg/images/`
- `training_data/raw/plantdoc/train/`

The pipeline will detect either format.

---

## What NOT to Download

Do NOT download these:

- `inaturalist`
- `plantclef`
- `plantnet`
- `ip102`
- `cwd30`
- `bugwood`
- `kaggle_vegetable`

They are rejected or on hold for legal reasons.

---

## After You Place the Data

Run exactly these commands:

```powershell
python training/pipeline.py --step prepare
python training/pipeline.py --step validate
python training/quality_checker.py
python training/pipeline.py --step deduplicate
python training/pipeline.py --step split
python training/pipeline.py --step report
```

Then send me the output of:

```powershell
python training/dataset_report.py
```

I will then generate the actual class counts, source-diversity table, and training-ready taxonomy from the real files on disk.
