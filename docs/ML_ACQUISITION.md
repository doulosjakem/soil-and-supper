# Soil & Supper — ML Data Acquisition

## 1. Purpose

This document describes the automated and manual data acquisition workflow for the Soil & Supper ML pipeline. It covers:

- How the pipeline attempts to acquire datasets automatically
- What to do when automatic acquisition fails
- How to verify acquired data
- How to run the full preparation pipeline

## 2. Acquisition Workflow

### Automated (Preferred)

```powershell
# Run the full automated acquisition pipeline
python training/pipeline.py --step download
```

The pipeline will:
1. Check each dataset's license (only commercially-approved datasets)
2. Attempt download using the appropriate adapter
3. Verify the downloaded file is actually a dataset (not HTML, CAPTCHA, error page)
4. Record the acquisition attempt in `training_data/manifests/acquisition_manifest.jsonl`
5. Preserve failed downloads as `.failed` files for diagnosis

### Manual (When Automated Fails)

Some datasets cannot be downloaded automatically due to:
- Google Drive virus scan warnings
- reCAPTCHA challenges
- Login requirements
- Broken download URLs

For these, place the manually downloaded file in `training_data/raw/` with a matching filename:
- `deepweeds_images.zip` for DeepWeeds
- `bdflower.zip` for BDFlower
- `{dataset_id}.zip` for others

Then run:
```powershell
python training/pipeline.py --step prepare
```

## 3. Current Acquisition Status

Run this command at any time to see the complete state:

```powershell
python training/verify_acquisition.py --detailed
```

Or for a compact table:

```powershell
python training/verify_acquisition.py --status
```

Or from the main pipeline:

```powershell
python training/pipeline.py --step acquisition_status
```

### Status Values

| Status | Meaning |
|--------|---------|
| `DOCUMENTED` | Dataset is planned but not yet downloaded |
| `ACQUIRED` | Images are on disk and labeled |
| `ARCHIVE_VALID` | Archive downloaded and verified |
| `HTML_ERROR` | Downloaded file is an error page (CAPTCHA, 404, etc.) |
| `ARCHIVE_INVALID` | Downloaded but corrupt or wrong format |
| `MISSING` | Not present on disk |
| `EMPTY` | Directory exists but contains no images |
| `LICENSE_BLOCKED` | License prohibits commercial use |
| `DATASET_SEARCH_REQUIRED` | No viable source found; needs research |

## 4. Dataset-Specific Instructions

### PlantVillage (CC0 1.0)
- **Primary URL**: Mendeley (often stale)
- **Fallback URL**: HuggingFace `https://huggingface.co/datasets/mohanty/PlantVillage/resolve/main/data.zip`
- **Status**: ACQUIRED — Downloaded from HuggingFace, 54,303 JPG images, 38 classes. Archive: `training_data/raw/plantvillage/plantvillage_hf.zip`. Extracted to `training_data/raw/plantvillage/color/`.
- **Expected**: 54,306 images, 38 classes

### DeepWeeds (CC BY 4.0)
- **Primary URL**: Zenodo `https://zenodo.org/records/7939060/files/images.zip?download=1`
- **Fallback URL**: Google Drive (often blocked by virus scan)
- **If Zenodo fails**: Download manually from Zenodo page
- **Expected**: 17,509 images, 9 classes

### BDFlower (CC BY 4.0)
- **PMC Article**: https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/
- **Issue**: PMC supplementary download often returns reCAPTCHA
- **If automated fails**: Download supplementary ZIP manually from PMC article page
- **Expected**: 23,334 images (3,889 original + augmented)

### Bangladesh Vegetables (CC BY 4.0)
- **URL**: https://data.mendeley.com/datasets/rtx9ngb68j
- **Fallback**: Mendeley direct file URL (may be stale)
- **If both fail**: Download manually from Mendeley
- **Expected**: 4,730 images, 13 classes

### Smartphone Vegetable Detection (CC BY 4.0)
- **URL**: https://data.mendeley.com/datasets/gnc4s3z2mf/3
- **Note**: Pascal VOC format; pipeline will convert to classification
- **Expected**: 3,534 images, 10 classes

### BIOSCAN-5M (CC BY 3.0)
- **URL**: https://huggingface.co/datasets/bioscan-ml/BIOSCAN-5M
- **Note**: 5.15M insect specimens; requires heavy curation to extract target classes
- **Strategy**: Download full dataset, then filter to target insect classes using metadata

### images.cv Datasets (CC0)
- **Vegetables**: https://images.cv/dataset/vegetables-image-classification-dataset
- **Insects**: https://images.cv/dataset/insects-image-classification-dataset
- **Note**: Download mechanism needs investigation; may require API access

### UC IPM (CC BY 4.0)
- **URLs**: https://ipm.ucanr.edu/PMG/WEEDS/, https://ipm.ucanr.edu/PMG/INSE/, https://ipm.ucanr.edu/PMG/BENE/
- **Limitation**: No bulk download; web scraper only
- **Strategy**: Run scraper, accept limited results, supplement with other sources

## 5. Verification Checklist

After downloading, verify each dataset:

```powershell
# 1. Check acquisition status
python training/verify_acquisition.py --detailed

# 2. Verify archive integrity
python training/verify_acquisition.py --scan

# 3. Run preparation pipeline
python training/pipeline.py --step prepare

# 4. Validate images
python training/pipeline.py --step validate

# 5. Run quality checks
python training/quality_checker.py

# 6. Deduplicate
python training/pipeline.py --step deduplicate

# 7. Generate report
python training/pipeline.py --step report
```

## 6. Common Failure Modes and Fixes

| Failure | Cause | Fix |
|---------|-------|-----|
| HTML instead of archive | Website blocks automated download | Manual download |
| reCAPTCHA | Google challenge | Manual download from different source |
| Virus scan warning | Google Drive large file | Use Zenodo alternative or manual download |
| 404 / Not Found | Stale URL | Find current URL, update `discover_datasets.py` |
| Empty archive | Downloaded index page | Check Content-Type, verify URL |
| Permission denied | Server blocks bots | Add User-Agent header, slow down requests |
| Partial download | Network timeout | Resume is automatic; check `.part` files |

## 7. Provenance Requirements

Every image in the processed dataset must have a manifest entry with:
- Source dataset ID
- Original filename
- License
- Attribution text
- Download date
- Quality status

See `docs/ML_DATA_LICENSES.md` for attribution format requirements.

## 8. What NOT to Do

- Do NOT delete failed downloads — they are preserved as `.failed` files for diagnosis
- Do NOT assume documented image counts are acquired images
- Do NOT train on data that has not passed validation
- Do NOT mix commercial and non-commercial data in the same model
- Do NOT use datasets with unclear licenses for commercial training
- Do NOT photograph garden images unless explicitly instructed and no alternative exists

## 9. Next Actions (Phase 14+)

1. **Immediate**: Re-run acquisition pipeline with improved adapters
2. **Manual downloads needed**: PlantVillage (Figshare), DeepWeeds (Zenodo), BDFlower (PMC), Bangladesh Veg (Mendeley)
3. **Research needed**: images.cv download mechanism, OpenPlant license verification
4. **Contact required**: CWD30 authors, IP102 author, Bugwood photographers
5. **After data acquisition**: Run prepare → validate → deduplicate → split → report
