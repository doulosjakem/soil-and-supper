# ML Phase 35 — Dataset Intake Documentation

## 1. What Was Repaired

`training/phase35_intake.py` contained structural corruption from two merged implementations:

- **Duplicate function definitions**: `generate_gap_report`, `write_acquisition_report`, and `main` were each defined twice.
- **Dangling orphaned code**: Lines after the first `if __name__ == "__main__": main()` block referenced undefined variables (`ledger_entries`, `approved`, `review`, `rejected`, `not_yet`) and were unreachable.
- **Missing symbols**: Constants (`INPUTS_DIR`, `GAP_REPORT`, `CLASS_COVERAGE`, `ACQUISITION_REPORT`, `PHASE35_LEDGER`, `PHASE35_IMAGE_MANIFEST`, `TIER1_CLASSES`, `PLANNED_DATASETS`) and functions (`load_ledger`, `save_ledger_entry`, `find_ledger_entry`, `append_image_manifest`, `identify_dataset`, `ingest_candidate`, `generate_class_coverage`) were referenced but undefined.
- **Inconsistent signatures**: `generate_gap_report` used an old 4-argument style in one copy and a new `ledger_entries` style in another.

The repair reconciled these into a single coherent implementation:

- One definition of each function.
- One `main()` and one `__main__` entry point.
- All referenced constants and functions are defined.
- Added `--dry-run` mode for safe validation.
- Added `timezone` import for UTC timestamps.

## 2. How the Intake Pipeline Works

### 2.1 Directory Layout

| Directory | Role |
|-----------|------|
| `inputs/` | Immutable staging area for human-downloaded archives and extracted folders |
| `training_data/raw/<dataset_id>/` | Extracted dataset working copies |
| `training_data/manifests/` | Ledger, image manifest, gap report, class coverage |
| `training_data/reports/` | Human-readable acquisition report |

### 2.2 Workflow

1. **Discovery**: Scan `inputs/` for candidate directories or archives.
2. **Identification**: Match candidates to known dataset definitions by filename/path.
3. **Archive verification**: Reject HTML/login placeholders and corrupt archives.
4. **Extraction**: Datasets are processed in place under `training_data/raw/<dataset_id>/`.
5. **Validation**: Every image is checked for corruption, minimum size (64px), extreme aspect ratio (>10), and blank content.
6. **Deduplication**: SHA-256 hashes are checked against `exact_dedup_manifest.jsonl` and `figshare_disease_manifest.jsonl`.
7. **Taxonomy mapping**: Source class names are mapped to Phase 34B Tier 1 classes. Unmapped classes are recorded as `unmapped_classes`.
8. **Commercial readiness**: Datasets with approved licenses and valid, mapped, unique images are marked `APPROVED`. Datasets with unverified licenses are marked `REVIEW`. Non-commercial or invalid datasets are `REJECTED`.
9. **Ledger update**: Append-only ledger records each dataset by fingerprint for resumability.
10. **Reporting**: Gap report, class coverage, and acquisition report are generated.

### 2.3 Resumability

The ledger (`phase35_dataset_ledger.jsonl`) tracks datasets by content fingerprint. Re-running the tool skips already-processed datasets. New datasets are appended. Manifests are append-only and never overwritten.

## 3. License Policy

### Approved

- Apache-2.0
- MIT
- CC0
- CC BY

### Rejected

- CC BY-NC
- CC BY-NC-SA
- CC BY-SA
- research-only
- unknown / unverifiable

Attribution is acceptable. The tool does **not** infer image licensing from platform licensing or repository licensing.

## 4. Input / Output Semantics

### Inputs

- `inputs/` is read-only. The tool never modifies, overwrites, or deletes files placed here.
- Both archive files (`.zip`, `.tar.gz`, `.tar`) and pre-extracted directories are supported.

### Outputs

| Output | Path | Description |
|--------|------|-------------|
| Dataset ledger | `training_data/manifests/phase35_dataset_ledger.jsonl` | Append-only dataset audit trail |
| Image manifest | `training_data/manifests/phase35_image_manifest.jsonl` | Per-image provenance records |
| Gap report | `training_data/manifests/phase35_gap_report.json` | Tier 1 class gap analysis |
| Class coverage | `training_data/manifests/phase35_class_coverage.json` | Tier 1 coverage matrix |
| Acquisition report | `training_data/reports/phase35_acquisition_report.md` | Human-readable status |

## 5. Manifest Semantics

- **Ledger entries**: One JSON object per line. Key fields: `dataset_id`, `status`, `fingerprint`, `license`, `commercial_ok`, `total_images`, `valid_images`, `approved_images`, `rejected_images`, `mapped_class_counts`, `unmapped_classes`, `duplicates_vs_core`, `duplicates_vs_figshare`, `new_unique_images`, `errors`, `notes`.
- **Image manifest entries**: One JSON object per image. Key fields: `path`, `filename`, `dataset_id`, `source_class`, `target_class`, `valid`, `corrupt`, `too_small`, `extreme_aspect`, `blank`, `width`, `height`, `hash`, `duplicate_vs_core`, `duplicate_vs_figshare`, `commercial_ready`, `license`, `attribution_required`, `attribution_text`.
- **Append-only**: Existing entries are never modified or deleted.

## 6. How to Resume an Interrupted Intake

```bash
# Check current state
python training/phase35_intake.py --all --json

# If new datasets are present in inputs/, they will be processed automatically
# Review the generated acquisition report
cat training_data/reports/phase35_acquisition_report.md
```

## 7. How Failed / Review Datasets Are Handled

- **REVIEW**: License or commercial status is unverified (e.g., CC0 claimed but not primary-source verified). Data is recorded but not merged into the commercial corpus.
- **REJECTED**: Archive is invalid, dataset directory is missing, license is non-commercial, or all images are corrupt/duplicate/unmapped. Errors are recorded in the ledger.
- **NOT_YET_RECEIVED**: Planned dataset is not present in `inputs/`. Recorded in the ledger but not processed.
- One bad dataset does not abort the entire intake. Errors are isolated per dataset.

## 8. Exact Commands Used for Verification

```bash
# Syntax validation
python -m py_compile training/phase35_intake.py

# Help output
python training/phase35_intake.py --help

# Dry run (no manifest modifications)
python training/phase35_intake.py --all --dry-run

# Full intake
python training/phase35_intake.py --all --json

# Single dataset
python training/phase35_intake.py --dataset inputs/some_dataset --json
```

## 9. Taxonomy

Phase 34B Tier 1 taxonomy: **51 classes**

- Vegetables (28): Tomato, Pepper, Eggplant, Potato, Cucumber, Summer Squash / Zucchini, Winter Squash / Pumpkin, Corn, Bean, Pea, Carrot, Beet, Radish, Turnip, Onion, Garlic, Leek, Broccoli, Cabbage, Cauliflower, Brussels Sprouts, Kale, Lettuce, Spinach, Swiss Chard, Sweet Potato, Watermelon, Cantaloupe
- Berries (4): Strawberry, Raspberry / Blackberry, Blueberry, Grape
- Fruit Trees (7): Apple, Pear, Peach, Cherry, Plum, Apricot, Nectarine
- Herbs (8): Basil, Cilantro, Parsley, Dill, Chives, Mint, Rosemary, Thyme
- Other (4): Asparagus, Rhubarb, Hops, Sunflower

Datasets containing classes outside this taxonomy record them as `unmapped_classes`. They are not discarded.

## 10. Commercial Corpus Safety

The existing `training_data/manifests/commercial_manifest.jsonl` (98,642 images) is never modified by this tool. New data enters the approved commercial corpus only after:

1. License verification
2. Taxonomy mapping
3. Image validation
4. Duplicate audit
5. Commercial-readiness decision

If any of these steps cannot be completed safely, the data is placed in a candidate/review state instead.
