# Soil & Supper — ML Phase 35 Handoff

**Date**: 2026-08-20  
**Phase**: 35 — Incremental Commercial Dataset Intake + Crop Corpus Preparation  
**Status**: IN PROGRESS — intake tooling complete, awaiting dataset downloads  
**Workstream**: ML / DATA ONLY

---

## 1. What Was Accomplished This Session

### 1.1 Infrastructure Created

| Component | Location | Description |
|-----------|----------|-------------|
| Intake tool | `training/phase35_intake.py` | Incremental, resumable dataset intake pipeline |
| Ledger | `training_data/manifests/phase35_dataset_ledger.jsonl` | Append-only dataset audit trail |
| Image manifest | `training_data/manifests/phase35_image_manifest.jsonl` | Per-image provenance records |
| Class coverage | `training_data/manifests/phase35_class_coverage.json` | Tier 1 class coverage matrix |
| Gap report | `training_data/manifests/phase35_gap_report.json` | Data gap analysis |
| Acquisition report | `training_data/reports/phase35_acquisition_report.md` | Human-readable acquisition status |
| Documentation | `docs/ML_PHASE35_DATASET_INTAKE.md` | Phase 35 intake documentation |
| Attributions | `docs/ML_DATASET_ATTRIBUTIONS.md` | Attribution requirements for approved sources |
| Staging dir | `inputs/` | Immutable staging area for human-downloaded archives |

### 1.2 Key Design Decisions

1. **`inputs/` is immutable** — the human drops archives here; the tool never modifies or deletes them.
2. **Resumable by design** — the ledger tracks datasets by content fingerprint (archive hash or directory hash). Rerunning skips already-processed datasets.
3. **Missing datasets recorded as `NOT_YET_RECEIVED`** — not treated as failures.
4. **Append-only manifests** — prior audit decisions are never overwritten.
5. **No training performed** — Phase 35 is intake only. Model training is explicitly deferred to Phase 36.

### 1.3 Current State

- **`inputs/`**: Empty. No datasets have been downloaded yet.
- **Ledger**: Contains `NOT_YET_RECEIVED` entries for all 8 planned datasets.
- **Commercial corpus**: Unchanged from previous phases (98,642 approved images from 4 sources).
- **New approved images**: 0 (no new data processed yet).

---

## 2. Planned Datasets (Awaiting Download)

The intake tool expects these datasets in `inputs/`:

| # | Dataset ID | Name | License | Commercial OK | Status |
|---|------------|------|---------|---------------|--------|
| 1 | `bangladesh_veg` | Bangladesh Comprehensive Vegetables | CC BY 4.0 | YES | NOT_YET_RECEIVED |
| 2 | `smartphone_veg` | Smartphone Vegetable Detection | CC BY 4.0 | YES | NOT_YET_RECEIVED |
| 3 | `vegnet` | VegNet Vegetable Quality Dataset | CC BY 4.0 | YES | NOT_YET_RECEIVED |
| 4 | `banglaveg` | BanglaVeg | CC BY 4.0 | YES | NOT_YET_RECEIVED |
| 5 | `early_stage_crops` | Early-Stage Vegetable Crops | CC BY 4.0 | YES | NOT_YET_RECEIVED |
| 6 | `images_cv_vegetables` | Vegetables Image Classification (images.cv) | CC0 (claimed) | REVIEW | NOT_YET_RECEIVED |
| 7 | `kaggle_fruit_veg` | Fruit and Vegetables Classification (Kaggle) | CC0 (claimed) | REVIEW | NOT_YET_RECEIVED |
| 8 | `images_cv_herbs` | Herbs Image Classification (images.cv) | CC0 (claimed) | REVIEW | NOT_YET_RECEIVED |

**Note**: Datasets 6-8 are marked `REVIEW` because their CC0 claims require primary-source verification before commercial approval.

---

## 3. How to Resume

### 3.1 When the human downloads datasets

1. Place downloaded archives or extracted directories into `inputs/`
2. Run: `python training/phase35_intake.py --all --json`
3. The tool will:
   - Identify each dataset by filename/path matching
   - Inspect archives for HTML/error placeholders
   - Extract to `training_data/raw/<dataset_id>/`
   - Validate all images (corrupt, too small, blank, extreme aspect)
   - Map source classes to Soil & Supper taxonomy
   - Detect duplicates against existing commercial corpus
   - Produce per-dataset status: APPROVED, APPROVED_WITH_ATTRIBUTION, REVIEW, REJECTED
   - Update ledger and manifests
   - Generate gap report and acquisition report

### 3.2 Rerunning after partial acquisition

- The tool is safe to rerun. Already-processed datasets are skipped via ledger fingerprint matching.
- New datasets are appended to manifests.
- Gap report and coverage are regenerated.

---

## 4. Current Tier 1 Coverage

**Taxonomy**: Phase 34B Tier 1 (51 classes)

**Current status**: 0 of 51 classes have new approved images from Phase 35 intake.

Existing commercial corpus (from prior phases) provides baseline coverage for some classes via disease datasets:
- PlantVillage: 54,284 images (CC0)
- Irish Potato: 38,554 images (CC BY 4.0)
- PlantDoc: 2,559 images (CC BY 4.0)
- Grapevine: 3,245 images (CC BY 4.0)

**Total commercial core**: 98,642 images

**New data needed**: The 5 Priority 1 CC BY 4.0 datasets (Bangladesh Veg, Smartphone Veg, VegNet, BanglaVeg, Early-Stage Crops) are expected to add ~22,000 images covering 12-15 Tier 1 classes.

---

## 5. Readiness Assessment

**Recommendation**: `NOT READY — MORE DATA NEEDED`

Reasoning:
- No new crop datasets have been acquired yet.
- `inputs/` is empty.
- Phase 35 remains open until the human downloads datasets and the intake pipeline processes them.
- Do not train the crop-recognition model yet.

**Next milestone**: Once Priority 1 datasets are acquired and processed, re-evaluate coverage. If Tier 1 coverage is sufficient, proceed to Phase 36 (First Real Soil & Supper Crop Model).

---

## 6. Human Actions Required

1. **Download the 5 Priority 1 datasets** into `inputs/`:
   - [Bangladesh Comprehensive Vegetables](https://data.mendeley.com/datasets/rtx9ngb68j)
   - [Smartphone Vegetable Detection](https://data.mendeley.com/datasets/gnc4s3z2mf/3)
   - [VegNet](https://data.mendeley.com/datasets/6nxnjbn9w6)
   - [BanglaVeg](https://doi.org/10.1016/j.dcha.2025.100058)
   - [Early-Stage Crops](https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/)

2. **Run the intake tool**: `python training/phase35_intake.py --all --json`

3. **Review outputs**:
   - `training_data/reports/phase35_acquisition_report.md`
   - `training_data/manifests/phase35_gap_report.json`
   - `training_data/manifests/phase35_class_coverage.json`

4. **Optional**: If CC0 verification is completed for images.cv and Kaggle datasets, download those as well.

---

## 7. Files Modified/Created This Session

| File | Action | Description |
|------|--------|-------------|
| `training/phase35_intake.py` | CREATED | Incremental intake tool (~992 lines) |
| `docs/ML_PHASE35_DATASET_INTAKE.md` | CREATED | Phase 35 documentation |
| `docs/ML_DATASET_ATTRIBUTIONS.md` | CREATED | Attribution requirements |
| `inputs/` | CREATED | Immutable staging directory |
| `training_data/manifests/phase35_dataset_ledger.jsonl` | CREATED | Dataset audit ledger |
| `training_data/manifests/phase35_image_manifest.jsonl` | CREATED | Image provenance manifest |
| `training_data/manifests/phase35_class_coverage.json` | CREATED | Class coverage matrix |
| `training_data/manifests/phase35_gap_report.json` | CREATED | Gap analysis |
| `training_data/reports/phase35_acquisition_report.md` | CREATED | Human-readable report |

---

## 8. What NOT to Do

- **Do NOT train the crop model** — Phase 35 is intake only.
- **Do NOT modify `inputs/` contents** — treat as immutable source material.
- **Do NOT commit ZIP archives** — they are gitignored.
- **Do NOT overwrite manifests** — they are append-only.
- **Do NOT use NC/SA datasets** for commercial training.

---

## 9. Verification Performed

- [x] Inspected repository structure and existing manifests
- [x] Verified `inputs/` directory did not exist; created it
- [x] Built resumable intake tool with ledger, dedup, class mapping, and reporting
- [x] Confirmed tool is syntactically valid (help output works)
- [x] Generated initial `NOT_YET_RECEIVED` ledger entries for all planned datasets
- [x] Created documentation and attribution files
- [x] Did not train any model
- [x] Did not modify any application code (Android/CMP/iOS)

---

## 10. Next Session Start

To resume:

```bash
# 1. Check current state
python training/phase35_intake.py --all --json

# 2. If new datasets are in inputs/, they will be processed automatically
# 3. Review the generated acquisition report
cat training_data/reports/phase35_acquisition_report.md
```

---

*Phase 35 remains open. Acquisition is ongoing. Do not train crop model yet.*
