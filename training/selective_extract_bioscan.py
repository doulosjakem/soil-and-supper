#!/usr/bin/env python3
"""
Selective extractor for BIOSCAN-5M archive.

Extracts only images that map to target insect classes using the metadata CSV.
Avoids extracting all 289K images when only ~15K are relevant.
"""

import csv
import zipfile
from pathlib import Path
from typing import Dict, List, Set

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
RAW_DIR = TRAINING_DATA_DIR / "raw"
ARCHIVE_PATH = RAW_DIR / "bioscan_5m.zip"
OUTPUT_DIR = RAW_DIR / "bioscan_5m_selective"
METADATA_PATH = RAW_DIR / "bioscan_metadata" / "bioscan5m" / "metadata" / "csv" / "BIOSCAN_5M_Insect_Dataset_metadata.csv"

TARGET_GENERA = {
    "Aphid": {"Aphis", "Rhopalosiphum", "Acyrthosiphon", "Myzus", "Macrosiphum", "Sitobion", "Cinara"},
    "Whitefly": {"Bemisia", "Trialeurodes"},
    "Spider_mite": {"Tetranychus", "Panonychus", "Oligonychus"},
    "Leafminer": {"Liriomyza", "Phytomyza", "Calycomyza", "Pseudonapomyza", "Agromyza", "Ophiomyia"},
    "Ladybug": {"Hippodamia", "Coleomegilla", "Coccinella", "Harmonia", "Adalia", "Propylea"},
    "Green_lacewing": {"Chrysoperla", "Chrysopa", "Ceraeochrysa", "Mallada", "Plesiochrysa"},
    "Honey_bee": {"Apis"},
    "Hoverfly": {"Toxomerus", "Paragus", "Sphaerophoria", "Eupeodes", "Episyrphus", "Eristalinus"},
    "Praying_mantis": {"Mantis", "Tenodera", "Hierodula", "Orthodera", "Stagmomantis"},
    "Spider": set(),
    "Thrips": {"Frankliniella", "Thrips", "Scirtothrips"},
    "Cutworm": {"Spodoptera", "Agrotis", "Peridroma", "Euxoa", "Feltia"},
    "Corn_earworm": {"Helicoverpa", "Heliothis"},
    "Squash_bug": {"Anasa", "Leptoglossus"},
    "Stink_bug": {"Halyomorpha", "Nezara", "Acrosternum", "Euschistus", "Thyanta", "Banasa"},
    "Flea_beetle": {"Chaetocnema", "Epitrix", "Phyllotreta", "Longitarsus"},
    "Blister_beetle": {"Meloe", "Epicauta", "Lytta", "Hycleus"},
}


def get_target_for_row(row: Dict) -> str | None:
    genus = row.get("genus", "")
    order = row.get("order", "")
    for target, genera in TARGET_GENERA.items():
        if target == "Spider":
            if order == "Araneae":
                return target
        elif genus in genera:
            return target
    return None


def select_bioscan_images(metadata_path: Path, split: str = "train") -> Dict[str, List[str]]:
    target_images: Dict[str, List[str]] = {t: [] for t in TARGET_GENERA}
    with open(metadata_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("split", "") != split:
                continue
            target = get_target_for_row(row)
            if target:
                processid = row.get("processid", "")
                chunk = row.get("chunk", "")
                if processid and chunk:
                    zip_path = f"bioscan5m/images/original_256/{split}/{chunk}/{processid}.jpg"
                    target_images[target].append(zip_path)
    return target_images


def extract_selected(archive_path: Path, target_images: Dict[str, List[str]], output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    with zipfile.ZipFile(archive_path, "r") as zf:
        for target, paths in target_images.items():
            target_dir = output_dir / target
            target_dir.mkdir(parents=True, exist_ok=True)
            for zip_path in paths:
                try:
                    data = zf.read(zip_path)
                    out_path = target_dir / Path(zip_path).name
                    if not out_path.exists():
                        with open(out_path, "wb") as f:
                            f.write(data)
                        total += 1
                except KeyError:
                    pass
    return total


if __name__ == "__main__":
    print("Selecting BIOSCAN-5M images for target classes...")
    target_images = select_bioscan_images(METADATA_PATH)
    counts = {t: len(p) for t, p in target_images.items() if p}
    print(f"Selected images: {sum(counts.values())}")
    for target, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {target}: {count}")
    
    print("\nExtracting selected images...")
    extracted = extract_selected(ARCHIVE_PATH, target_images, OUTPUT_DIR)
    print(f"Extracted {extracted} new images to {OUTPUT_DIR}")
