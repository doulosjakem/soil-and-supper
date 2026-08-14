# Soil & Supper — ML Dataset Tooling

This directory contains the Python-based dataset preparation and model training tooling for the Soil & Supper Android application.

## Structure

```
ml/
├── src/
│   ├── acquire.py          # Dataset acquisition utilities
│   ├── curate.py           # Dataset curation and filtering
│   ├── quality_control.py  # Image quality checks
│   ├── split.py            # Train/val/test split generation
│   ├── manifest.py         # Dataset manifest generation
│   └── train.py            # Transfer learning training pipeline
├── data/
│   ├── raw/                # Raw downloaded datasets (gitignored)
│   ├── processed/          # Processed and cleaned images (gitignored)
│   └── manifests/          # Dataset manifests and metadata (gitignored)
├── models/                 # Trained model checkpoints (gitignored)
├── notebooks/              # Jupyter notebooks for experimentation
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.9+
- PyTorch 2.0+ (for training)
- TensorFlow 2.15+ (for TFLite conversion)
- NVIDIA GPU with CUDA (GTX 1060 recommended)

## Usage

### 1. Acquire datasets

```bash
python src/acquire.py
```

### 2. Curate datasets

```bash
python src/curate.py
```

### 3. Generate splits

```bash
python src/split.py
```

### 4. Train model

```bash
python src/train.py
```

### 5. Convert to TFLite

```bash
python src/convert_tflite.py
```

## Dataset Strategy

See `../DESIGN.md` sections 7, 20, and 21 for the full dataset and ML strategy.

## Important Notes

- Do NOT download datasets into Git.
- All data directories are gitignored.
- Dataset licenses must be verified before use.
- See `../MANUAL_DOWNLOAD_GUIDE.md` for manual download instructions.
