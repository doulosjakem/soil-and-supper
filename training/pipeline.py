#!/usr/bin/env python3
"""
Main pipeline orchestrator for Soil & Supper ML data acquisition.

Usage:
    python training/pipeline.py --step download
    python training/pipeline.py --step prepare
    python training/pipeline.py --step validate
    python training/pipeline.py --step deduplicate
    python training/pipeline.py --step split
    python training/pipeline.py --step report
    python training/pipeline.py --step all
"""

import argparse
import sys
import yaml
from pathlib import Path

TRAINING_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TRAINING_DIR.parent
CONFIG_PATH = TRAINING_DIR / "config.yaml"

sys.path.insert(0, str(TRAINING_DIR))

from license_verifier import initialize_default_verifications
from class_mapper import initialize_default_mappings


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def run_download(config):
    from download_dataset import download_dataset
    from discover_datasets import APPROVED_DATASETS
    
    print("=" * 60)
    print("STEP 1: Downloading approved datasets")
    print("=" * 60)
    
    downloaded = []
    failed = []
    
    for dataset_id, info in APPROVED_DATASETS.items():
        if not info.get("commercial_ok", False):
            print(f"[SKIP] {dataset_id}: Not commercially approved")
            continue
        try:
            success = download_dataset(dataset_id, info)
            if success:
                downloaded.append(dataset_id)
            else:
                failed.append(dataset_id)
        except Exception as e:
            print(f"[ERROR] {dataset_id}: {e}")
            failed.append(dataset_id)
    
    print(f"\nDownloaded: {len(downloaded)}")
    print(f"Failed: {len(failed)}")
    return downloaded, failed


def run_prepare(config):
    from prepare_dataset import prepare_all
    print("=" * 60)
    print("STEP 2: Preparing and normalizing datasets")
    print("=" * 60)
    prepare_all(config)


def run_validate(config):
    from validate_dataset import validate_all
    print("=" * 60)
    print("STEP 3: Validating image integrity")
    print("=" * 60)
    validate_all(config)


def run_deduplicate(config):
    from deduplicate import deduplicate_all
    print("=" * 60)
    print("STEP 4: Deduplicating images")
    print("=" * 60)
    deduplicate_all(config)


def run_split(config):
    from split_dataset import split_all
    print("=" * 60)
    print("STEP 5: Generating train/val/test splits")
    print("=" * 60)
    split_all(config)


def run_report(config):
    from dataset_report import generate_full_report
    print("=" * 60)
    print("STEP 6: Generating dataset report")
    print("=" * 60)
    generate_full_report(config)


def run_license_check():
    print("=" * 60)
    print("STEP 0: License verification")
    print("=" * 60)
    verifier = initialize_default_verifications()
    mapper = initialize_default_mappings()
    print(f"Approved datasets: {len(verifier.get_approved_datasets())}")
    print(f"HOLD datasets: {len(verifier.get_hold_datasets())}")
    print(f"Rejected datasets: {len(verifier.get_rejected_datasets())}")
    print(f"Class mappings: {len(mapper.mappings)}")
    print(f"Ambiguous mappings: {len(mapper.get_ambiguous_mappings())}")


def run_acquisition_status():
    print("=" * 60)
    print("STEP: Acquisition status")
    print("=" * 60)
    from verify_acquisition import generate_acquisition_status_table
    print(generate_acquisition_status_table())
    
    from verify_acquisition import scan_raw_directory
    report = scan_raw_directory()
    print(f"\nTotal images on disk: {report['total_images']}")
    print(f"Total archives on disk: {report['total_archives']}")
    print(f"Recognized datasets: {len(report['datasets_recognized'])}")
    print(f"Unrecognized/empty datasets: {len(report['datasets_unrecognized'])}")


def main():
    parser = argparse.ArgumentParser(description="Soil & Supper ML Pipeline")
    parser.add_argument("--step", choices=["license", "acquisition_status", "download", "prepare", "validate", "deduplicate", "split", "report", "all"], default="all")
    parser.add_argument("--skip-download", action="store_true", help="Skip download step (use existing data)")
    args = parser.parse_args()
    
    config = load_config()
    
    if args.step in ["license", "all"]:
        run_license_check()
    
    if args.step == "acquisition_status":
        run_acquisition_status()
        return
    
    if args.step == "license":
        return
    
    if args.step in ["download", "all"] and not args.skip_download:
        run_download(config)
    
    if args.step in ["prepare", "all"]:
        run_prepare(config)
    
    if args.step in ["validate", "all"]:
        run_validate(config)
    
    if args.step in ["deduplicate", "all"]:
        run_deduplicate(config)
    
    if args.step in ["split", "all"]:
        run_split(config)
    
    if args.step in ["report", "all"]:
        run_report(config)
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
