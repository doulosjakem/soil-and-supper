# Soil & Supper — Training Pipeline

This directory contains the automated dataset preparation and model training pipeline.

## Structure

```
training/
├── README.md
├── requirements.txt
├── config.yaml
├── discover_datasets.py
├── download_dataset.py
├── prepare_dataset.py
├── deduplicate.py
├── validate_dataset.py
├── split_dataset.py
└── dataset_report.py
```

## Usage

```bash
# 1. Discover available datasets
python training/discover_datasets.py

# 2. Download approved datasets
python training/download_dataset.py --dataset bangladesh_veg
python training/download_dataset.py --dataset smartphone_veg

# 3. Prepare and curate datasets
python training/prepare_dataset.py

# 4. Validate images
python training/validate_dataset.py

# 5. Deduplicate
python training/deduplicate.py

# 6. Split into train/val/test
python training/split_dataset.py

# 7. Generate report
python training/dataset_report.py
```

## Configuration

Edit `config.yaml` to set:

- Target classes
- Data directories
- Split ratios
- Quality thresholds
- Deduplication sensitivity

## Important Notes

- Do NOT download datasets into Git.
- All data directories are gitignored.
- Dataset licenses must be verified before use.
- See `../docs/ML_DATASETS.md` for approved datasets.
- See `../docs/ML_DATA_LICENSES.md` for attribution requirements.
