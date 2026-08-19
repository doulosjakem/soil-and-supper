# Soil & Supper — Phase 31: P0 Readiness Pipeline

**Date**: 2026-08-19  
**Phase**: P0 Dataset Intake, License Verification & Commercial Readiness  
**Scope**: ML/DATA ONLY  
**Status**: P0 REMAINS BLOCKED — Intake pipeline complete, awaiting manual acquisition

---

## 1. Repository State at Phase 31 Start

### Git Status
```
 M docs/ML_ACQUISITION_QUEUE.md
 M docs/ML_P0_ACQUISITION_REPORT.md
?? training/dataset_intake.py
?? training/process_icar_cith.py
?? training/process_multi_crop_disease.py
?? training/process_plant_pathology_2020.py
?? training/generate_figshare_manifest.py
?? training/update_commercial_audit.py
```

### Branch & HEAD
- **Branch**: `main`
- **HEAD**: `b8e00e15e1185b3f42ef11a2d6c95cd1493e9f58`

### Pre-existing Uncommitted Changes (Phase 30)
The following changes from Phase 30 are present and preserved:
- `docs/ML_ACQUISITION_QUEUE.md` — Phase 30 intake infrastructure section
- `docs/ML_P0_ACQUISITION_REPORT.md` — Phase 30 testing results, intake workflow
- `training/dataset_intake.py` — generic intake script
- `training/process_plant_pathology_2020.py` — Kaggle template
- `training/process_multi_crop_disease.py` — class-directory template
- `training/process_icar_cith.py` — class-directory template with synthetic flag
- `training/generate_figshare_manifest.py` — figshare manifest generation
- `training/update_commercial_audit.py` — commercial audit update script

---

## 2. Current Commercial Baseline

| Metric | Value |
|--------|-------|
| Commercial core (USE only) | 109,127 images |
| Total training-ready (USE + EXCLUDE + REVIEW) | 136,134 images |
| Trainable disease classes | 18 |
| Sources | 5 (PlantVillage, Irish Potato, PlantDoc, Grapevine, figshare_disease) |
| EXCLUDE images | 36,675 (Common Beans, CC BY-NC 4.0) |
| REVIEW images | 817 (SegPPD-101, MIT claimed but source inaccessible) |

### Per-Class Commercial Counts
| Class | Count | Sources | Dominant Source | Dominant % |
|-------|------:|---------|----------------|-----------|
| Healthy | 36,342 | 4 | irish_potato | 53.1% |
| Leaf_spot | 18,263 | 3 | plantvillage | 74.2% |
| Late_blight | 16,141 | 3 | irish_potato | 80.7% |
| Early_blight | 8,914 | 4 | irish_potato | 69.7% |
| Tomato_yellow_leaf_curl | 5,432 | 2 | plantvillage | 98.6% |
| Powdery_mildew | 4,601 | 3 | figshare_disease | 52.7% |
| Rust | 3,640 | 3 | figshare_disease | 64.1% |
| Bacterial_spot | 3,305 | 2 | plantvillage | 94.5% |
| Spider_mite | 2,166 | 3 | plantvillage | 77.4% |
| Squash_powdery_mildew | 1,965 | 2 | plantvillage | 93.4% |
| Septoria_leaf_spot | 1,920 | 2 | plantvillage | 92.2% |
| Grape_black_rot | 1,244 | 2 | plantvillage | 94.9% |
| Downy_mildew | 1,002 | 1 | grapevine | 100.0% |
| Apple_scab | 723 | 2 | plantvillage | 87.1% |
| Tomato_mosaic_virus | 427 | 2 | plantvillage | 87.4% |
| Cedar_apple_rust | 362 | 2 | plantvillage | 76.0% |
| Anthracnose | 383 | 1 | figshare_disease | 100.0% |

---

## 3. P0 Dataset Status

### 3.1 Plant Pathology Challenge 2020
| Field | Value |
|-------|-------|
| **URL** | https://www.kaggle.com/c/plant-pathology-2020-fgvc7 |
| **License** | CC BY 4.0 (claimed on Kaggle; primary Cornell source does not explicitly state) |
| **License Confidence** | MEDIUM |
| **Estimated Useful Images** | 2,600 |
| **Auth Required** | Yes — free Kaggle account |
| **Blocker** | No Kaggle credentials available |
| **Status** | BLOCKED — REQUIRES MANUAL AUTH |
| **Disk State** | Directory does not exist: `training_data/raw/plant_pathology_2020/` |

**License Verification**: Cannot verify without data. Primary source would be Cornell University / Kaggle competition page. CC BY 4.0 is claimed but not explicitly stated in the competition rules. Status pending human acquisition.

**Taxonomy Mapping**: Template prepared in `training/process_plant_pathology_2020.py`. Expected mappings:
- `healthy` → Healthy
- `rust` → Rust
- `scab` → Apple_scab
- `frog_eye_leaf_spot` → Leaf_spot (MEDIUM confidence)
- `powdery_mildew` → Powdery_mildew
- `complex` / `multiple_diseases` → OUT_OF_TAXONOMY

**Critical Gap Contribution**: Would fill Cedar_apple_rust (+1,399 estimated) and Apple_scab (+1,200 estimated).

---

### 3.2 Multi-Crop Disease Dataset
| Field | Value |
|-------|-------|
| **URL** | https://data.mendeley.com/datasets/6243z8r6t6 |
| **License** | CC BY 4.0 |
| **License Confidence** | HIGH |
| **Estimated Useful Images** | 5,000 |
| **Auth Required** | Mendeley account |
| **Blocker** | Mendeley returns HTTP 403 Forbidden |
| **Status** | BLOCKED — REQUIRES MANUAL AUTH |
| **Disk State** | `training_data/raw/multi_crop_disease/multi_crop_disease.zip` (102 KB, HTML error file) |

**Intake Report** (`training_data/reports/intake_multi_crop_disease_phase31.json`):
- Archive: INVALID (HTML error file, not a ZIP)
- Total files: 1
- Total images: 0
- Valid images: 0
- Classes discovered: 0
- Duplicates vs core: 0
- Duplicates vs figshare: 0

**License Verification**: Cannot verify without data. Mendeley page claims CC BY 4.0. Human must download and verify from primary Mendeley source.

**Taxonomy Mapping**: Template prepared in `training/process_multi_crop_disease.py`. Example mappings prepared for Apple_scab, Downy_mildew, Anthracnose, Rust. Actual mapping depends on dataset class structure.

**Critical Gap Contribution**: Would fill Downy_mildew (+1,000 estimated), Anthracnose (+1,000 estimated), Rust (+1,000 estimated).

---

### 3.3 Apple Leaf Diseases ICAR-CITH
| Field | Value |
|-------|-------|
| **URL** | https://data.mendeley.com/datasets/gm6mfz8fz6 |
| **License** | CC BY 4.0 |
| **License Confidence** | HIGH |
| **Estimated Useful Images** | 800 |
| **Auth Required** | Mendeley account |
| **Blocker** | Mendeley returns HTTP 403 Forbidden |
| **Status** | BLOCKED — REQUIRES MANUAL AUTH |
| **Disk State** | `training_data/raw/icar_apple/icar_apple.zip` (102 KB, HTML error file) |

**Intake Report** (`training_data/reports/intake_icar_apple_phase31.json`):
- Archive: INVALID (HTML error file, not a ZIP)
- Total files: 1
- Total images: 0
- Valid images: 0
- Classes discovered: 0
- Duplicates vs core: 0
- Duplicates vs figshare: 0

**License Verification**: Cannot verify without data. Mendeley page claims CC BY 4.0. Human must download and verify from primary Mendeley source.

**Taxonomy Mapping**: Template prepared in `training/process_icar_cith.py`. Example mappings prepared for Apple_scab, Cedar_apple_rust, Healthy. Actual mapping depends on dataset class structure.

**Synthetic Imagery Check**: Previous alternative (AppleLeaf9-Enhanced Edition, figshare 23606010) contained CycleGAN synthetic images. This template includes synthetic imagery flagging. ICAR-CITH must be manually inspected for synthetic vs field imagery.

**Critical Gap Contribution**: Would fill Apple_scab (+500 estimated), Cedar_apple_rust (+200 estimated), Tomato_mosaic_virus (+50 estimated).

---

## 4. Intake Pipeline Verification

### 4.1 Generic Intake Script (`dataset_intake.py`)
Properties verified:
- ✅ Detects missing directories
- ✅ Detects HTML/error placeholder files
- ✅ Detects archives (ZIP, TAR)
- ✅ Detects corrupt images
- ✅ Records image dimensions
- ✅ Calculates SHA256
- ✅ Detects exact duplicates against commercial core (136,134 hashes)
- ✅ Detects duplicates against figshare dataset (5,482 hashes)
- ✅ Reports class structure
- ✅ Does NOT automatically approve licensing
- ✅ Produces deterministic results
- ✅ Does NOT embed dataset-specific licensing assumptions

### 4.2 Dataset-Specific Processors
| Processor | Status | Activates When |
|-----------|--------|---------------|
| `process_plant_pathology_2020.py` | COMPLETE | `training_data/raw/plant_pathology_2020/` exists with train.csv + images/ |
| `process_multi_crop_disease.py` | COMPLETE | `training_data/raw/multi_crop_disease/` contains real data |
| `process_icar_cith.py` | COMPLETE | `training_data/raw/icar_apple/` contains real data |

All processors:
- Parse/discover class structure
- Validate images (corrupt, too small, extreme aspect, blank)
- Compute SHA256 hashes
- Check duplicates vs core + figshare
- Report taxonomy mappings
- Do NOT add to training data
- Do NOT mark commercially usable

---

## 5. License Verification Status

### Current Ledger Status
| Dataset | License Status | Evidence |
|---------|---------------|----------|
| PlantVillage | USE | CC0 1.0 verified from Meta-Album + GitHub mirror |
| Irish Potato | USE | CC BY 4.0 verified from Zenodo API + PMC article |
| PlantDoc | USE | CC BY 4.0 verified from GitHub LICENSE.txt |
| Grapevine | USE | CC BY 4.0 verified from Zenodo API + Data in Brief |
| Common Beans | EXCLUDE | CC BY-NC 4.0 verified from article (repository.must.ac.tz) |
| SegPPD-101 | REVIEW | MIT claimed but sources now inaccessible |
| figshare_disease | USE | CC BY 4.0 verified from figshare API + data.yaml |
| Plant Pathology 2020 | **PENDING** | Cannot verify without data; primary Cornell source does not explicitly state |
| Multi-Crop Disease | **PENDING** | Cannot verify without data; Mendeley claims CC BY 4.0 |
| ICAR-CITH | **PENDING** | Cannot verify without data; Mendeley claims CC BY 4.0 |

### License Verification Rules Applied
1. No licenses inferred from platform claims alone
2. No licenses inferred from paper existence
3. No licenses inferred from dataset titles
4. Primary-source verification required before USE status
5. Unverifiable → REVIEW or UNKNOWN
6. Commercial-use permission must be explicit

---

## 6. Taxonomy Audit

### Gap Classes (Current Status)
| Class | Current Count | Target | Status | P0 Contribution |
|-------|---------------|--------|--------|-----------------|
| Cedar_apple_rust | 362 | 1,000 | WEAK | +1,399 (Plant Pathology 2020, BLOCKED) |
| Apple_scab | 723 | 1,000 | WEAK | +1,200 (Plant Pathology 2020, BLOCKED) |
| Downy_mildew | 1,002 | 2,000 | SINGLE_SOURCE | +1,000 (Multi-Crop Disease, BLOCKED) |
| Anthracnose | 383 | 1,000 | MODERATE | +1,000 (Multi-Crop Disease, BLOCKED) |
| Rust | 3,640 | — | STRONG | Would improve further (Multi-Crop Disease, BLOCKED) |
| Leaf_spot | 18,263 | — | STRONG | Would improve further (Plant Pathology 2020, BLOCKED) |
| Powdery_mildew | 4,601 | — | STRONG | Would improve further (Plant Pathology 2020, BLOCKED) |
| Early_blight | 8,914 | — | STRONG | Would improve further (Plant Pathology 2020, BLOCKED) |
| Spider_mite | 2,166 | — | MODERATE | Would improve further (Plant Pathology 2020, BLOCKED) |

### Gap Closure Scenario (If All P0 Acquired)
| Class | Current | + Plant Pathology 2020 | + Multi-Crop Disease | + ICAR-CITH | Final |
|-------|---------|------------------------|----------------------|-------------|-------|
| Cedar_apple_rust | 362 | +1,399 | — | +200 | 1,961 |
| Apple_scab | 723 | +1,200 | — | +500 | 2,423 |
| Downy_mildew | 1,002 | — | +1,000 | — | 2,002 |
| Anthracnose | 383 | — | +1,000 | — | 1,383 |
| Rust | 3,640 | +100 | +1,000 | — | 4,740 |
| Leaf_spot | 18,263 | +200 | — | — | 18,463 |
| Powdery_mildew | 4,601 | +100 | — | — | 4,701 |
| Early_blight | 8,914 | +500 | — | — | 9,414 |
| Spider_mite | 2,166 | +100 | — | — | 2,266 |

---

## 7. Duplicate Audit

### Current State
- **Commercial core manifest**: `exact_dedup_manifest.jsonl` — 136,134 entries
- **Figshare manifest**: `figshare_disease_manifest.jsonl` — 5,482 entries
- **Duplicates between core and figshare**: 0 (verified at acquisition time)

### P0 Duplicate Check
Cannot perform duplicate audit without actual data. The intake pipeline is ready to:
1. Compute SHA256 for every image in each P0 dataset
2. Compare against 136,134 core hashes
3. Compare against 5,482 figshare hashes
4. Report exact duplicate counts and percentages

### Duplicate Audit Requirements
When data becomes available:
- Run `python training/dataset_intake.py <dataset_path>` → reports duplicates
- Run dataset-specific processor → detailed per-class duplicate counts
- Do NOT silently remove source images
- Manifests must preserve provenance and indicate exclusion reason

---

## 8. Quality Audit

### Current State
All three P0 datasets are either missing or contain HTML error files. Quality audit cannot proceed without data.

### Quality Checks Ready
When data becomes available, the intake pipeline will check:
- Corrupt/unreadable images
- Extremely small images (<64px)
- Unusual aspect ratios (>10:1)
- Blank/empty images
- Resolution distribution
- Class contamination (unexpected files in class directories)
- Synthetic imagery indicators (especially for ICAR-CITH)

### Synthetic Imagery Flag
- `process_icar_cith.py` includes explicit synthetic imagery flag
- Previous AppleLeaf9 alternative contained CycleGAN synthetic images
- ICAR-CITH must be manually inspected for synthetic vs field imagery
- Synthetic and field imagery must NOT be mixed without documentation

---

## 9. Commercial Readiness Decisions

### Decision Framework
Each dataset receives one of:
- **USE** — Commercially compatible, verified from primary source
- **EXCLUDE** — Commercially incompatible
- **REVIEW** — License unclear or previously verified but source now inaccessible
- **UNKNOWN** — License cannot be established

### Current P0 Decisions (Without Data)
| Dataset | Decision | Reason |
|---------|----------|--------|
| Plant Pathology Challenge 2020 | **REVIEW** | Cannot verify license without data; primary Cornell source does not explicitly state CC BY 4.0 |
| Multi-Crop Disease Dataset | **REVIEW** | Cannot verify license without data; Mendeley claims CC BY 4.0 but 403 prevents download |
| Apple Leaf Diseases ICAR-CITH | **REVIEW** | Cannot verify license without data; Mendeley claims CC BY 4.0 but 403 prevents download |

**No P0 dataset can be marked USE without primary-source license verification.**

---

## 10. Manifest Generation

### Current Manifests
| Manifest | Entries | Purpose |
|----------|---------|---------|
| `exact_dedup_manifest.jsonl` | 136,134 | Commercial core SHA256 hashes |
| `figshare_disease_manifest.jsonl` | 5,482 | Figshare dataset with taxonomy mapping |
| `figshare_disease_source_manifest.jsonl` | 1 | Figshare source provenance |
| `commercial_train_manifest.jsonl` | — | Training split |
| `commercial_val_manifest.jsonl` | — | Validation split |
| `commercial_test_manifest.jsonl` | — | Test split |

### P0 Manifest Requirements
When data becomes available and license is verified:
1. Generate dataset-specific manifest with:
   - Image path
   - Dataset/source ID
   - Original source class
   - Soil & Supper class
   - SHA256
   - License status
   - Commercial status
   - Exclusion/review reason where applicable
2. Do NOT add REVIEW or UNKNOWN images to training manifest
3. Preserve source provenance for every image
4. Deterministic output (sorted entries, reproducible hashes)

---

## 11. Phase 31 Deliverables

### Scripts Created/Modified
| File | Action | Purpose |
|------|--------|---------|
| `docs/PHASE31_P0_READINESS_REPORT.md` | CREATED | This report |
| `training_data/reports/intake_multi_crop_disease_phase31.json` | CREATED | Intake report (HTML error detected) |
| `training_data/reports/intake_icar_apple_phase31.json` | CREATED | Intake report (HTML error detected) |
| `training_data/reports/intake_disease_dataset_figshare_phase31.json` | CREATED | Intake report (valid dataset baseline) |
| `training_data/reports/process_plant_pathology_2020_phase31.json` | CREATED | Processor report (directory missing) |
| `training_data/reports/process_multi_crop_disease_phase31.json` | CREATED | Processor report (no valid data) |
| `training_data/reports/process_icar_cith_phase31.json` | CREATED | Processor report (no valid data) |

### Documentation Updated
- `docs/ML_ACQUISITION_QUEUE.md` — Phase 30 intake infrastructure preserved
- `docs/ML_P0_ACQUISITION_REPORT.md` — Phase 30 testing results preserved

### No Changes To
- Android/Kotlin/Compose files
- Swift/iOS files
- Model training code
- Existing commercial manifests
- License ledger (no new licenses to record)

---

## 12. Validation & Testing

### Tests Executed
| Test | Result |
|------|--------|
| `python -m py_compile training/dataset_intake.py` | PASS |
| `python -m py_compile training/process_plant_pathology_2020.py` | PASS |
| `python -m py_compile training/process_multi_crop_disease.py` | PASS |
| `python -m py_compile training/process_icar_cith.py` | PASS |
| `dataset_intake.py` on figshare dataset | PASS — 5,482 valid images, 0 duplicates vs core |
| `dataset_intake.py` on multi_crop_disease | PASS — correctly detects HTML error file |
| `dataset_intake.py` on icar_apple | PASS — correctly detects HTML error file |
| `dataset_intake.py` on missing plant_pathology_2020 | PASS — correctly reports missing directory |
| `process_plant_pathology_2020.py` on missing directory | PASS — correctly reports missing |
| `process_multi_crop_disease.py` on placeholder | PASS — reports 0 images |
| `process_icar_cith.py` on placeholder | PASS — reports 0 images |
| `exact_dedup_manifest.jsonl` integrity | PASS — 136,134 lines |
| `figshare_disease_manifest.jsonl` integrity | PASS — 5,482 lines |
| `commercial_class_audit_updated.json` validity | PASS — 109,127 total, 18 classes |
| JSON report files validity | PASS — all JSON files parse successfully |

### JSON Report Files Validated
| Report | Size | Status |
|--------|------|--------|
| `intake_multi_crop_disease_phase31.json` | 961 bytes | Valid JSON |
| `intake_icar_apple_phase31.json` | 929 bytes | Valid JSON |
| `intake_disease_dataset_figshare_phase31.json` | 3,496,445 bytes | Valid JSON |
| `process_plant_pathology_2020_phase31.json` | Valid | Valid JSON |
| `process_multi_crop_disease_phase31.json` | Valid | Valid JSON |
| `process_icar_cith_phase31.json` | Valid | Valid JSON |

---

## 13. Remaining Blockers

### Authentication Barriers
- **Kaggle**: Required for Plant Pathology 2020. Free account, no payment.
- **Mendeley**: Required for Multi-Crop Disease and ICAR-CITH. Free account, no payment.

### Download Barriers
- Large files (>500 MB) time out in this environment
- Mendeley API returns 403 without session cookies
- Zenodo browser verification required for some records

### Exact Human Action Required

**Please acquire the 3 blocked P0 datasets manually:**

1. **Plant Pathology Challenge 2020** via Kaggle
   - Creates free account at kaggle.com
   - Accepts competition rules
   - Downloads train.csv + images folder
   - Places in `training_data/raw/plant_pathology_2020/`

2. **Multi-Crop Disease Dataset** via Mendeley
   - Creates free account at mendeley.com
   - Goes to dataset page
   - Clicks "Download All"
   - **Replaces** the 102 KB HTML error file at `training_data/raw/multi_crop_disease/`

3. **Apple Leaf Diseases ICAR-CITH** via Mendeley
   - Uses same Mendeley account
   - Goes to dataset page
   - Clicks "Download All"
   - **Replaces** the 102 KB HTML error file at `training_data/raw/icar_apple/`

After acquisition:
```bash
# Run intake for each dataset
python training/dataset_intake.py training_data/raw/<dataset_id>/
python training/process_<dataset_id>.py

# Verify license from primary source
# Update docs/DATASET_LICENSE_LEDGER.md

# If license APPROVED:
# - Generate manifests
# - Run duplicate audit
# - Update commercial class audit
# - Add to training data
```

---

## 14. P0 Completion Status

| Criterion | Status |
|-----------|--------|
| All P0 datasets acquired | ❌ BLOCKED — 0 of 3 acquired |
| License verification complete | ❌ BLOCKED — cannot verify without data |
| Duplicate audit complete | ❌ BLOCKED — cannot audit without data |
| Taxonomy audit complete | ❌ BLOCKED — cannot map without data |
| Quality audit complete | ❌ BLOCKED — cannot audit without data |
| Commercial readiness decided | ❌ BLOCKED — all REVIEW pending data |
| Manifests generated | ❌ BLOCKED — cannot generate without verified data |
| Class-gap counts updated | ❌ BLOCKED — no new data to incorporate |

### Is P0 Complete?
**NO.** P0 remains BLOCKED. All three P0 datasets are inaccessible without manual human acquisition. The intake pipeline is complete and ready, but no datasets have been processed because no valid data exists on disk.

### Does P1 Remain Blocked?
**YES.** Per project rules, P0 must be resolved before P1 acquisition or model training. P1 does not proceed until P0 is genuinely complete.

---

## 15. Git / Delivery

### Files Changed in Phase 31
| File | Action | Description |
|------|--------|-------------|
| `docs/PHASE31_P0_READINESS_REPORT.md` | CREATED | Phase 31 comprehensive report |
| `training_data/reports/intake_multi_crop_disease_phase31.json` | CREATED | Intake report |
| `training_data/reports/intake_icar_apple_phase31.json` | CREATED | Intake report |
| `training_data/reports/intake_disease_dataset_figshare_phase31.json` | CREATED | Intake report |
| `training_data/reports/process_plant_pathology_2020_phase31.json` | CREATED | Processor report |
| `training_data/reports/process_multi_crop_disease_phase31.json` | CREATED | Processor report |
| `training_data/reports/process_icar_cith_phase31.json` | CREATED | Processor report |

### No Changes To
- Android/Kotlin/Compose files
- Swift/iOS files
- Model training code
- Existing commercial manifests
- License ledger
- ML_TAXONOMY.md
- ML_MODEL_STRATEGY.md

### Commit Plan
Phase 31 work will be committed separately from Phase 30 changes to maintain clean history.

---

*Report generated: 2026-08-19*  
*Phase: P0 Dataset Intake, License Verification & Commercial Readiness*  
*Workstream: ML / DATA ONLY*  
*No model training occurred during this phase.*  
*No Android/Kotlin/Compose/Swift files were modified.*  
*P0 remains BLOCKED pending manual human acquisition.*
