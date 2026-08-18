#!/usr/bin/env python3
"""
Dataset preparation utilities for Soil & Supper ML pipeline.
Filters, normalizes, and organizes images for training.
"""

import shutil
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import yaml
from PIL import Image

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"
TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
RAW_DIR = TRAINING_DATA_DIR / "raw"
PROCESSED_DIR = TRAINING_DATA_DIR / "processed"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
HOLD_DIR = TRAINING_DATA_DIR / "hold"

for d in [PROCESSED_DIR, MANIFESTS_DIR, HOLD_DIR]:
    d.mkdir(parents=True, exist_ok=True)

SUPPORTED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def load_config() -> Dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def normalize_filename(src: Path, class_name: str, index: int) -> str:
    """Generate normalized filename."""
    ext = src.suffix.lower()
    return f"{class_name}_{index:05d}{ext}"


def validate_image_file(img_path: Path) -> bool:
    """Verify image is readable and not corrupt."""
    try:
        with Image.open(img_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def ingest_images(
    class_name: str,
    image_paths: List[Path],
    output_dir: Path,
    dataset_id: str,
) -> int:
    """Copy and normalize validated images for a single class."""
    output_dir.mkdir(parents=True, exist_ok=True)
    existing = count_images(output_dir)
    count = 0
    manifest_entries = []

    manifest_path = MANIFESTS_DIR / f"{dataset_id}_{class_name}_manifest.jsonl"
    ingested_sources = set()
    if manifest_path.exists():
        with open(manifest_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    ingested_sources.add(entry.get("source_path"))

    for img_path in image_paths:
        if not img_path.exists():
            continue
        if str(img_path) in ingested_sources:
            continue
        if not validate_image_file(img_path):
            continue
        dest_name = normalize_filename(img_path, class_name, existing + count)
        dest_path = output_dir / dest_name
        if not dest_path.exists():
            shutil.copy2(img_path, dest_path)
            manifest_entries.append({
                "local_path": str(dest_path.relative_to(TRAINING_DATA_DIR)),
                "source_path": str(img_path),
                "source_dataset": dataset_id,
                "class": class_name,
            })
            count += 1

    if manifest_entries:
        with open(manifest_path, "a") as f:
            for entry in manifest_entries:
                f.write(json.dumps(entry) + "\n")

    return count


def count_images(directory: Path) -> int:
    """Count images in directory recursively."""
    return sum(
        1
        for ext in SUPPORTED_IMAGE_EXTS
        for _ in directory.rglob(f"*{ext}")
    )


def discover_segppd101_classes(dataset_dir: Path) -> Dict[str, List[Path]]:
    """Discover classes in SegPPD-101 flat structure with encoded filenames."""
    # Look for fullname.txt in common locations
    fullname_path = dataset_dir / "fullname.txt"
    if not fullname_path.exists():
        for subdir in ["extracted/SegPPD-101", "extracted", "SegPPD-101"]:
            candidate = dataset_dir / subdir / "fullname.txt"
            if candidate.exists():
                fullname_path = candidate
                break
        else:
            # Search recursively
            for candidate in dataset_dir.rglob("fullname.txt"):
                fullname_path = candidate
                break
    
    if not fullname_path.exists():
        return {}
    
    class_map = {}
    with open(fullname_path, "r") as f:
        for line in f:
            parts = line.strip().split(" ", 1)
            if len(parts) == 2:
                class_id = parts[0]
                class_name = parts[1]
                class_map[class_id] = class_name
    
    # Find image directory - look for common patterns
    image_dir = dataset_dir / "image"
    if not image_dir.exists():
        for subdir in ["extracted/SegPPD-101/image", "extracted/image", "SegPPD-101/image", "image"]:
            candidate = dataset_dir / subdir
            if candidate.exists():
                image_dir = candidate
                break
        else:
            # Use the directory containing fullname.txt
            image_dir = fullname_path.parent
    
    classes = {}
    for img_path in image_dir.iterdir():
        if img_path.is_file() and img_path.suffix.lower() in SUPPORTED_IMAGE_EXTS:
            class_id = img_path.stem[:3]
            if class_id in class_map:
                class_name = class_map[class_id]
                classes.setdefault(class_name, []).append(img_path)
    
    return classes


def discover_irish_potato_classes(dataset_dir: Path) -> Dict[str, List[Path]]:
    """Discover classes in Irish Potato dataset flat structure."""
    classes = {}
    for class_dir in dataset_dir.iterdir():
        if class_dir.is_dir():
            class_name = class_dir.name
            images = [
                p for p in class_dir.rglob("*")
                if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTS
            ]
            if images:
                classes[class_name] = images
    return classes


def discover_common_beans_classes(dataset_dir: Path) -> Dict[str, List[Path]]:
    """Discover classes in Common Beans dataset flat structure."""
    classes = {}
    for class_dir in dataset_dir.iterdir():
        if class_dir.is_dir():
            class_name = class_dir.name
            images = [
                p for p in class_dir.rglob("*")
                if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTS
            ]
            if images:
                classes[class_name] = images
    return classes


def discover_grapevine_classes(dataset_dir: Path) -> Dict[str, List[Path]]:
    """Discover classes in Grapevine dataset nested structure."""
    classes = {}
    # Look for resized directory - may be nested
    resized_dir = dataset_dir / "resized"
    if not resized_dir.exists():
        for subdir in dataset_dir.iterdir():
            if subdir.is_dir():
                resized_dir = subdir
                break
    
    if not resized_dir.exists():
        return {}
    
    # Check if there's a nested resized directory
    nested = resized_dir / "resized"
    if nested.exists() and nested.is_dir():
        resized_dir = nested
    
    for class_dir in resized_dir.iterdir():
        if class_dir.is_dir():
            class_name = class_dir.name
            images = [
                p for p in class_dir.rglob("*")
                if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTS
            ]
            if images:
                classes[class_name] = images
    
    return classes


def discover_dataset_structure(dataset_dir: Path) -> Dict[str, List[Path]]:
    """Auto-discover class directories in common dataset layouts.

    Supported layouts:
        dataset/class/image.jpg
        dataset/train/class/image.jpg
        dataset/val/class/image.jpg
        dataset/test/class/image.jpg
        dataset/images/train/class/image.jpg
        dataset/images/val/class/image.jpg
        dataset/images/test/class/image.jpg
        dataset/<single_subdir>/train/class/image.jpg
        dataset/<single_subdir>/class/image.jpg
    """
    classes: Dict[str, List[Path]] = {}

    def add_images(class_name: str, paths: List[Path]):
        classes.setdefault(class_name, []).extend(paths)

    image_exts = SUPPORTED_IMAGE_EXTS

    def scan_for_splits(base: Path):
        split_dirs = {}
        for split in ["train", "val", "test"]:
            split_path = base / split
            if split_path.exists() and split_path.is_dir():
                split_dirs[split] = split_path
        return split_dirs

    def scan_for_classes(base: Path):
        results = {}
        for item in base.iterdir():
            if item.is_dir():
                images = [
                    p for p in item.rglob("*")
                    if p.is_file() and p.suffix.lower() in image_exts
                ]
                if images:
                    results[item.name] = images
        return results

    # Direct splits in dataset root
    split_dirs = scan_for_splits(dataset_dir)

    # Check for images/ subdirectory with splits
    images_dir = dataset_dir / "images"
    if images_dir.exists() and images_dir.is_dir():
        for split in ["train", "val", "test"]:
            split_path = images_dir / split
            if split_path.exists() and split_path.is_dir():
                split_dirs[split] = split_path

    if split_dirs:
        for split_path in split_dirs.values():
            for class_dir in split_path.iterdir():
                if class_dir.is_dir():
                    images = [
                        p for p in class_dir.rglob("*")
                        if p.is_file() and p.suffix.lower() in image_exts
                    ]
                    if images:
                        add_images(class_dir.name, images)
        return classes

    # Check for single top-level subdirectory (common in zip extracts)
    top_level_dirs = [d for d in dataset_dir.iterdir() if d.is_dir()]
    if len(top_level_dirs) == 1:
        single_subdir = top_level_dirs[0]
        # Check for splits inside the single subdirectory
        inner_splits = scan_for_splits(single_subdir)
        if inner_splits:
            for split_path in inner_splits.values():
                for class_dir in split_path.iterdir():
                    if class_dir.is_dir():
                        images = [
                            p for p in class_dir.rglob("*")
                            if p.is_file() and p.suffix.lower() in image_exts
                        ]
                        if images:
                            add_images(class_dir.name, images)
            return classes
        # Check for class directories inside the single subdirectory
        inner_classes = scan_for_classes(single_subdir)
        if inner_classes:
            classes.update(inner_classes)
            return classes

    # Direct class directories: dataset/class/image.jpg
    for item in dataset_dir.iterdir():
        if item.is_dir():
            images = [
                p for p in item.rglob("*")
                if p.is_file() and p.suffix.lower() in image_exts
            ]
            if images:
                add_images(item.name, images)

    return classes


def parse_label_file(label_path: Path, dataset_dir: Path) -> Dict[str, List[Path]]:
    """Parse CSV or JSON annotation files into class->image mappings."""
    classes: Dict[str, List[Path]] = {}

    if label_path.suffix.lower() == ".csv":
        with open(label_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                img_file = (
                    row.get("image")
                    or row.get("filename")
                    or row.get("file")
                    or row.get("path")
                )
                label = (
                    row.get("label")
                    or row.get("class")
                    or row.get("category")
                )
                if img_file and label:
                    img_path = dataset_dir / img_file
                    if img_path.exists():
                        classes.setdefault(label, []).append(img_path)

    elif label_path.suffix.lower() == ".json":
        with open(label_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            for item in data:
                img_file = (
                    item.get("image")
                    or item.get("filename")
                    or item.get("file")
                )
                label = (
                    item.get("label")
                    or item.get("class")
                    or item.get("category")
                )
                if img_file and label:
                    img_path = dataset_dir / img_file
                    if img_path.exists():
                        classes.setdefault(label, []).append(img_path)
        elif isinstance(data, dict):
            for label, files in data.items():
                if isinstance(files, list):
                    for img_file in files:
                        img_path = dataset_dir / img_file
                        if img_path.exists():
                            classes.setdefault(label, []).append(img_path)

    return classes


def prepare_unlabeled_dataset(dataset_dir: Path, dataset_id: str) -> int:
    """Preserve unlabeled images in hold directory instead of discarding them."""
    images = [
        p for p in dataset_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTS
    ]
    if not images:
        return 0

    hold_dir = HOLD_DIR / dataset_id
    hold_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for img_path in images:
        if not validate_image_file(img_path):
            continue
        dest_name = normalize_filename(img_path, "unlabeled", count)
        dest_path = hold_dir / dest_name
        if not dest_path.exists():
            shutil.copy2(img_path, dest_path)
            count += 1

    print(f"  [HOLD] {dataset_id}: {count} unlabeled images preserved in hold/")
    return count


def scan_dataset_for_class(
    dataset_dir: Path,
    target_class: str,
    dataset_id: str,
    mapper: Optional["ClassMapper"] = None,
) -> List[Path]:
    """Generic adapter: find images in a dataset that belong to target_class."""
    discovered = discover_dataset_structure(dataset_dir)

    # Check for label files if class dirs weren't found
    if not discovered:
        for label_file in ["labels.csv", "annotations.csv", "train_labels.csv", "val_labels.csv"]:
            lf = dataset_dir / label_file
            if lf.exists():
                discovered = parse_label_file(lf, dataset_dir)
                break

    def normalize_label(label: str) -> str:
        return label.strip().lower().replace(" ", "_").replace("-", "_")

    image_paths = []
    for source_label, paths in discovered.items():
        mapped_class = None
        if mapper:
            mapped_class, _ = mapper.get_target_class(dataset_id, source_label)
            if mapped_class is None:
                mapped_class, _ = mapper.get_target_class(dataset_id, normalize_label(source_label))
        if mapped_class is None:
            mapped_class = source_label
        if mapped_class == target_class:
            image_paths.extend(paths)

    return image_paths


def prepare_all(config: Dict):
    """Prepare all approved datasets."""
    from class_mapper import initialize_default_mappings
    mapper = initialize_default_mappings()

    domain_map = {
        "crops": config["domains"]["crops"]["classes"],
        "weeds": config["domains"]["weeds"]["classes"],
        "insects": config["domains"]["insects"]["classes"],
        "diseases": config["domains"]["diseases"]["classes"],
        "growth_stages": config["domains"]["growth_stages"]["classes"],
    }

    raw_datasets = {}
    if RAW_DIR.exists():
        for item in RAW_DIR.iterdir():
            if item.is_dir():
                raw_datasets[item.name] = item

    total = 0
    for domain, classes in domain_map.items():
        print(f"\nProcessing domain: {domain}")
        for cls in classes:
            class_dir = PROCESSED_DIR / domain / cls
            existing = 0
            if class_dir.exists():
                existing = count_images(class_dir)
                if existing > 0:
                    print(f"  {cls}: {existing} images (already prepared, checking for additional sources...)")

            source_image_paths: List[Path] = []
            dataset_id = None
            class_total = 0
            ingested_in_chain = False

            # Known dataset layouts with specific source structures
            if domain == "crops" and cls in [
                "Tomato", "Pepper_sweet", "Cucumber", "Eggplant"
            ]:
                for ds in [RAW_DIR / "bangladesh_veg", RAW_DIR / "smartphone_veg"]:
                    ds_cls = ds / cls
                    if ds_cls.exists():
                        source_image_paths.extend([
                            p for p in ds_cls.rglob("*")
                            if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTS
                        ])
                        if dataset_id is None:
                            dataset_id = ds.name

            elif domain == "diseases":
                datasets_to_check = [
                    (RAW_DIR / "plantvillage", "plantvillage"),
                    (RAW_DIR / "plantdoc", "plantdoc"),
                ]
                for ds, ds_name in datasets_to_check:
                    if ds.exists():
                        found = scan_dataset_for_class(ds, cls, ds_name, mapper)
                        if found:
                            count = ingest_images(cls, found, class_dir, ds_name)
                            class_total += count
                            ingested_in_chain = True
                            if count > 0:
                                if dataset_id is None:
                                    dataset_id = ds_name
                                print(f"  {cls}: +{count} from {ds_name} (total: {existing + class_total})")

                # SegPPD-101 flat structure handling
                segppd101_dir = RAW_DIR / "segppd101"
                if segppd101_dir.exists():
                    segppd101_classes = discover_segppd101_classes(segppd101_dir)
                    for source_label, paths in segppd101_classes.items():
                        mapped_class, _ = mapper.get_target_class("segppd101", source_label)
                        if mapped_class == cls:
                            count = ingest_images(cls, paths, class_dir, "segppd101")
                            class_total += count
                            ingested_in_chain = True
                            if count > 0:
                                if dataset_id is None:
                                    dataset_id = "segppd101"
                                print(f"  {cls}: +{count} from segppd101 (total: {existing + class_total})")

                # Irish Potato dataset handling
                irish_potato_dir = RAW_DIR / "irish_potato"
                if irish_potato_dir.exists():
                    irish_potato_classes = discover_irish_potato_classes(irish_potato_dir)
                    for source_label, paths in irish_potato_classes.items():
                        mapped_class, _ = mapper.get_target_class("irish_potato", source_label)
                        if mapped_class == cls:
                            count = ingest_images(cls, paths, class_dir, "irish_potato")
                            class_total += count
                            ingested_in_chain = True
                            if count > 0:
                                if dataset_id is None:
                                    dataset_id = "irish_potato"
                                print(f"  {cls}: +{count} from irish_potato (total: {existing + class_total})")

                # Common Beans dataset handling
                common_beans_dir = RAW_DIR / "common_beans"
                if common_beans_dir.exists():
                    common_beans_classes = discover_common_beans_classes(common_beans_dir)
                    for source_label, paths in common_beans_classes.items():
                        mapped_class, _ = mapper.get_target_class("common_beans", source_label)
                        if mapped_class == cls:
                            count = ingest_images(cls, paths, class_dir, "common_beans")
                            class_total += count
                            ingested_in_chain = True
                            if count > 0:
                                if dataset_id is None:
                                    dataset_id = "common_beans"
                                print(f"  {cls}: +{count} from common_beans (total: {existing + class_total})")

                # Grapevine dataset handling
                grapevine_dir = RAW_DIR / "grapevine"
                if grapevine_dir.exists():
                    grapevine_classes = discover_grapevine_classes(grapevine_dir)
                    for source_label, paths in grapevine_classes.items():
                        mapped_class, _ = mapper.get_target_class("grapevine", source_label)
                        if mapped_class == cls:
                            count = ingest_images(cls, paths, class_dir, "grapevine")
                            class_total += count
                            ingested_in_chain = True
                            if count > 0:
                                if dataset_id is None:
                                    dataset_id = "grapevine"
                                print(f"  {cls}: +{count} from grapevine (total: {existing + class_total})")

            elif domain == "weeds" and cls == "Other_weed":
                ds = RAW_DIR / "deepweeds"
                if ds.exists():
                    discovered = discover_dataset_structure(ds)
                    for source_label, paths in discovered.items():
                        mapped_class, _ = mapper.get_target_class("deepweeds", source_label)
                        if mapped_class == "Other_weed":
                            source_image_paths.extend(paths)
                    dataset_id = "deepweeds"

            elif domain == "growth_stages" and cls in [
                "Flowering", "Vegetative", "Seedling", "Fruiting"
            ]:
                ds = RAW_DIR / "plant_growth_stage"
                ds_cls = ds / cls
                if ds_cls.exists():
                    source_image_paths.extend([
                        p for p in ds_cls.rglob("*")
                        if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTS
                    ])
                    dataset_id = "plant_growth_stage"

            else:
                # Generic discovery across all raw datasets
                for ds_name, ds_dir in raw_datasets.items():
                    found = scan_dataset_for_class(ds_dir, cls, ds_name, mapper)
                    if found:
                        count = ingest_images(cls, found, class_dir, ds_name)
                        class_total += count
                        ingested_in_chain = True
                        if count > 0:
                            if dataset_id is None:
                                dataset_id = ds_name
                            print(f"  {cls}: +{count} from {ds_name} (total: {existing + class_total})")

            if source_image_paths and not ingested_in_chain:
                count = ingest_images(cls, source_image_paths, class_dir, dataset_id or "unknown")
                class_total += count
                if count > 0:
                    print(f"  {cls}: +{count} images (total: {existing + class_total})")
                else:
                    print(f"  {cls}: 0 new valid images after validation")
            elif not ingested_in_chain:
                if existing > 0:
                    print(f"  {cls}: {existing} images (no additional sources found)")
                    class_total = existing
                else:
                    print(f"  {cls}: 0 images — NO SOURCE DATA FOUND")
            
            total += class_total

    # Handle datasets with no class structure
    print("\nChecking for unlabeled datasets...")
    for ds_name, ds_dir in raw_datasets.items():
        discovered = discover_dataset_structure(ds_dir)
        if not discovered:
            prepare_unlabeled_dataset(ds_dir, ds_name)

    print(f"\nTotal prepared: {total} images")

    if total == 0:
        print("\nERROR: Zero images prepared. Dataset acquisition is incomplete.")
        print("Run: python training/pipeline.py --step acquisition_status")
        print("Or: python training/verify_acquisition.py --scan")
        sys.exit(1)


if __name__ == "__main__":
    config = load_config()
    prepare_all(config)
