#!/usr/bin/env python3
"""
Phase 35D — Comprehensive dataset intake and commercial-readiness assessment.

Processes all acquired datasets in raw/ across multiple recognition domains.
"""

import json
import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timezone
from collections import defaultdict

from PIL import Image

TRAINING_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TRAINING_DIR.parent
TRAINING_DATA_DIR = PROJECT_ROOT / "training_data"
RAW_DIR = PROJECT_ROOT / "raw"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
REPORTS_DIR = TRAINING_DATA_DIR / "reports"

for d in [MANIFESTS_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

EXACT_DEDUP_MANIFEST = MANIFESTS_DIR / "exact_dedup_manifest.jsonl"
FIGSHARE_MANIFEST = MANIFESTS_DIR / "figshare_disease_manifest.jsonl"
PHASE35D_LEDGER = MANIFESTS_DIR / "phase35d_dataset_ledger.jsonl"
PHASE35D_IMAGE_MANIFEST = MANIFESTS_DIR / "phase35d_image_manifest.jsonl"
PHASE35D_REPORT = REPORTS_DIR / "phase35d_acquisition_report.md"
PHASE35D_GAP_REPORT = MANIFESTS_DIR / "phase35d_gap_report.json"
PHASE35D_CLASS_COVERAGE = MANIFESTS_DIR / "phase35d_class_coverage.json"
PHASE35D_ATTRIBUTIONS = REPORTS_DIR / "phase35d_attributions.md"
PHASE35D_CANDIDATE_CLASSES = MANIFESTS_DIR / "phase35d_candidate_classes.json"

TIER1_CLASSES = [
    "Tomato", "Pepper", "Eggplant", "Potato", "Cucumber",
    "Summer Squash / Zucchini", "Winter Squash / Pumpkin", "Corn", "Bean", "Pea",
    "Carrot", "Beet", "Radish", "Turnip", "Onion", "Garlic", "Leek",
    "Broccoli", "Cabbage", "Cauliflower", "Brussels Sprouts", "Kale", "Lettuce", "Spinach", "Swiss Chard", "Sweet Potato",
    "Watermelon", "Cantaloupe",
    "Strawberry", "Raspberry / Blackberry", "Blueberry", "Grape",
    "Apple", "Pear", "Peach", "Cherry", "Plum", "Apricot", "Nectarine",
    "Basil", "Cilantro", "Parsley", "Dill", "Chives", "Mint", "Rosemary", "Thyme",
    "Asparagus", "Rhubarb", "Hops", "Sunflower",
]

TIER1_CLASSES_LOWER = {c.lower(): c for c in TIER1_CLASSES}

APPROVED_LICENSES = {"apache-2.0", "mit", "cc0", "cc0 1.0", "cc0-1.0", "public domain", "public domain (us government)", "cc by", "cc by 4.0", "cc-by", "cc-by-4.0"}
REJECTED_LICENSES = {"cc by-nc", "cc by-nc-sa", "cc by-sa", "cc by-sa 3.0", "research-only", "educational-only", "non-commercial"}


def compute_sha256(file_path: Path, chunk_size: int = 65536) -> str:
    if file_path.is_dir():
        return "dir"
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def load_existing_hashes() -> Tuple[Set[str], Set[str]]:
    core_hashes: Set[str] = set()
    figshare_hashes: Set[str] = set()

    if EXACT_DEDUP_MANIFEST.exists():
        with open(EXACT_DEDUP_MANIFEST, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    h = entry.get("hash")
                    if h:
                        core_hashes.add(h)
                except json.JSONDecodeError:
                    continue

    if FIGSHARE_MANIFEST.exists():
        with open(FIGSHARE_MANIFEST, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    h = entry.get("sha256")
                    if h:
                        figshare_hashes.add(h)
                except json.JSONDecodeError:
                    continue

    return core_hashes, figshare_hashes


def load_ledger() -> List[Dict]:
    entries: List[Dict] = []
    if PHASE35D_LEDGER.exists():
        with open(PHASE35D_LEDGER, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def save_ledger_entry(entry: Dict) -> None:
    entry.setdefault("processed_at", datetime.now(timezone.utc).isoformat())
    with open(PHASE35D_LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def find_ledger_entry(ledger: List[Dict], fingerprint: str) -> Optional[Dict]:
    for entry in ledger:
        if entry.get("fingerprint") == fingerprint:
            return entry
    return None


def normalize_license(text: str) -> str:
    return text.lower().replace("-", " ").replace("_", " ").strip()


def detect_license(readme_text: str, manifest_data: Dict) -> Tuple[str, str, bool]:
    license_text = ""
    license_source = ""
    commercial_ok = False
    candidates = []

    if manifest_data.get("license"):
        candidates.append(("manifest", manifest_data["license"]))
    if manifest_data.get("licence"):
        candidates.append(("manifest", manifest_data["licence"]))
    if manifest_data.get("license_evidence"):
        candidates.append(("manifest", manifest_data["license_evidence"]))
    if manifest_data.get("attribution"):
        candidates.append(("manifest_attribution", manifest_data["attribution"]))

    import re
    m = re.search(r"^license:\s*(.+)", readme_text, re.MULTILINE | re.IGNORECASE)
    if m:
        candidates.append(("readme_yaml", m.group(1).strip().strip('"').strip("'")))

    m = re.search(r"^licence:\s*\n\s*(-\s*)?(.+)", readme_text, re.MULTILINE | re.IGNORECASE)
    if m:
        candidates.append(("readme_yaml_multiline", m.group(2).strip().strip('"').strip("'")))

    m = re.search(r"Creative Commons Attribution[^\n]*", readme_text, re.IGNORECASE)
    if m:
        candidates.append(("readme_cc", m.group(0).strip()))

    m = re.search(r"MIT[^\n]*License[^\n]*", readme_text, re.IGNORECASE)
    if m:
        candidates.append(("readme_mit", m.group(0).strip()))

    m = re.search(r"Apache[^\n]*License[^\n]*", readme_text, re.IGNORECASE)
    if m:
        candidates.append(("readme_apache", m.group(0).strip()))

    m = re.search(r"Public Domain[^\n]*", readme_text, re.IGNORECASE)
    if m:
        candidates.append(("readme_pd", m.group(0).strip()))

    for source, text in candidates:
        norm = normalize_license(text)
        if any(normalize_license(r) in norm for r in REJECTED_LICENSES):
            license_text = text
            license_source = source
            commercial_ok = False
            break
        elif any(normalize_license(a) in norm for a in APPROVED_LICENSES):
            license_text = text
            license_source = source
            commercial_ok = True
            break

    if not license_text and manifest_data.get("license"):
        license_text = manifest_data["license"]
        license_source = "manifest"
        norm = normalize_license(license_text)
        if any(normalize_license(r) in norm for r in REJECTED_LICENSES):
            commercial_ok = False
        elif any(normalize_license(a) in norm for a in APPROVED_LICENSES):
            commercial_ok = True

    if not license_text:
        license_text = "unknown"
        license_source = "none"
        commercial_ok = False

    return license_text, license_source, commercial_ok


def auto_map_class(source_label: str) -> Tuple[str, str]:
    source_lower = source_label.lower().strip()
    if source_lower in TIER1_CLASSES_LOWER:
        return TIER1_CLASSES_LOWER[source_lower], "high"

    synonyms = {
        "capsicum": "Pepper", "bell pepper": "Pepper", "chilli pepper": "Pepper", "chili pepper": "Pepper",
        "brinjal": "Eggplant", "aubergine": "Eggplant",
        "flat bean": "Bean", "green bean": "Bean", "french bean": "Bean", "kidney bean": "Bean",
        "soy bean": "Bean", "soybean": "Bean", "mung bean": "Bean", "green gram": "Bean",
        "maize": "Corn", "sweetcorn": "Corn", "sweet corn": "Corn",
        "zucchini": "Summer Squash / Zucchini", "courgette": "Summer Squash / Zucchini",
        "pumpkin": "Winter Squash / Pumpkin",
        "beet": "Beet", "beetroot": "Beet",
        "brussels sprout": "Brussels Sprouts",
        "swiss chard": "Swiss Chard", "silverbeet": "Swiss Chard",
        "sweet potato": "Sweet Potato",
        "raspberry": "Raspberry / Blackberry", "blackberry": "Raspberry / Blackberry",
        "coriander": "Cilantro",
        "muskmelon": "Cantaloupe",
        "raddish": "Radish",
        "tomato": "Tomato", "potato": "Potato", "cucumber": "Cucumber", "carrot": "Carrot",
        "onion": "Onion", "garlic": "Garlic", "pepper": "Pepper", "eggplant": "Eggplant",
        "broccoli": "Broccoli", "cabbage": "Cabbage", "cauliflower": "Cauliflower",
        "corn": "Corn", "lettuce": "Lettuce", "spinach": "Spinach",
        "strawberry": "Strawberry", "blueberry": "Blueberry", "grape": "Grape",
        "apple": "Apple", "pear": "Pear", "peach": "Peach", "cherry": "Cherry",
        "plum": "Plum", "apricot": "Apricot", "nectarine": "Nectarine",
        "basil": "Basil", "mint": "Mint", "rosemary": "Rosemary", "thyme": "Thyme",
        "parsley": "Parsley", "dill": "Dill", "chives": "Chives",
        "asparagus": "Asparagus", "rhubarb": "Rhubarb", "sunflower": "Sunflower",
    }

    if source_lower in synonyms:
        return synonyms[source_lower], "high"

    return None, "none"


def detect_domain(dataset_name: str, class_names: List[str], readme_text: str) -> str:
    name_lower = dataset_name.lower()
    text_lower = readme_text.lower()

    if any(k in name_lower for k in ["disease", "pathology", "blight", "mildew", "rust", "spot", "virus", "bacterial"]):
        return "DISEASE / DISORDER"
    if any(k in text_lower for k in ["disease", "pathology", "blight", "mildew", "rust", "spot"]):
        return "DISEASE / DISORDER"
    if any(k in name_lower for k in ["insect", "pest", "bug", "aphid", "whitefly", "beetle"]):
        return "INSECT / PEST"
    if any(k in name_lower for k in ["beneficial", "ladybug", "bee", "pollinator"]):
        return "BENEFICIAL INSECT"
    if any(k in name_lower for k in ["weed", "invasive"]):
        return "WEED"
    if any(k in name_lower for k in ["stage", "growth", "seedling", "germination"]):
        return "GROWTH STAGE"
    if any(k in name_lower for k in ["segmentation", "mask", "vegetation"]):
        return "OTHER / FUTURE"

    return "CROP / PLANT ID"


def validate_image(img_path: Path) -> Dict:
    record = {
        "path": str(img_path),
        "filename": img_path.name,
        "valid": True,
        "corrupt": False,
        "too_small": False,
        "extreme_aspect": False,
        "blank": False,
        "width": 0,
        "height": 0,
        "hash": "",
        "error": "",
    }

    try:
        with Image.open(img_path) as img:
            img.verify()
        with Image.open(img_path) as img:
            img.load()
            width, height = img.size
            record["width"] = width
            record["height"] = height

            if width < 64 or height < 64:
                record["too_small"] = True
                record["valid"] = False

            aspect = max(width, height) / max(min(width, height), 1)
            if aspect > 10:
                record["extreme_aspect"] = True
                record["valid"] = False

            extrema = img.getextrema()
            if all(e[1] - e[0] < 10 for e in extrema if len(e) == 2):
                record["blank"] = True
                record["valid"] = False

        sha256 = compute_sha256(img_path)
        record["hash"] = sha256

    except Exception as e:
        record["corrupt"] = True
        record["valid"] = False
        record["error"] = str(e)

    return record


def process_class_dir(class_dir: Path, dataset_id: str, class_name: str, core_hashes: Set[str], figshare_hashes: Set[str]) -> Dict:
    image_files = []
    for ext in SUPPORTED_IMAGE_EXTENSIONS:
        image_files.extend(class_dir.rglob(f"*{ext}"))

    valid_count = 0
    corrupt_count = 0
    too_small_count = 0
    extreme_aspect_count = 0
    blank_count = 0
    dup_core = 0
    dup_figshare = 0
    new_unique = 0
    image_records = []

    for img_path in image_files:
        record = validate_image(img_path)
        record["dataset_id"] = dataset_id
        record["source_class"] = class_name
        record["target_class"] = class_name
        record["duplicate_vs_core"] = False
        record["duplicate_vs_figshare"] = False
        record["commercial_ready"] = False

        if record["valid"]:
            valid_count += 1
            if record["hash"] in core_hashes:
                record["duplicate_vs_core"] = True
                dup_core += 1
            elif record["hash"] in figshare_hashes:
                record["duplicate_vs_figshare"] = True
                dup_figshare += 1
            else:
                new_unique += 1
            record["commercial_ready"] = True
        else:
            if record["corrupt"]:
                corrupt_count += 1
            if record["too_small"]:
                too_small_count += 1
            if record["extreme_aspect"]:
                extreme_aspect_count += 1
            if record["blank"]:
                blank_count += 1

        image_records.append(record)

    return {
        "class_name": class_name,
        "total_images": len(image_files),
        "valid_images": valid_count,
        "corrupt_images": corrupt_count,
        "too_small_images": too_small_count,
        "extreme_aspect_images": extreme_aspect_count,
        "blank_images": blank_count,
        "duplicates_vs_core": dup_core,
        "duplicates_vs_figshare": dup_figshare,
        "new_unique_images": new_unique,
        "image_records": image_records,
    }


def process_dataset(dataset_dir: Path, dataset_info: Dict, core_hashes: Set[str], figshare_hashes: Set[str]) -> Dict:
    dataset_id = dataset_info.get("dataset_id", dataset_dir.name)
    report = {
        "dataset_id": dataset_id,
        "name": dataset_info.get("name", dataset_dir.name),
        "source": dataset_info.get("source", "unknown"),
        "url": dataset_info.get("url", ""),
        "license": dataset_info.get("license", "unknown"),
        "license_evidence": dataset_info.get("license_evidence", ""),
        "commercial_ok": dataset_info.get("commercial_ok", False),
        "attribution_required": dataset_info.get("attribution_required", False),
        "attribution_text": dataset_info.get("attribution_text", ""),
        "domain": dataset_info.get("domain", "CROP / PLANT ID"),
        "ingest_timestamp": datetime.now(timezone.utc).isoformat(),
        "dataset_path": str(dataset_dir),
        "total_files": 0,
        "total_images": 0,
        "valid_images": 0,
        "corrupt_images": 0,
        "too_small_images": 0,
        "extreme_aspect_images": 0,
        "blank_images": 0,
        "classes_discovered": [],
        "class_counts": {},
        "mapped_class_counts": {},
        "unmapped_classes": [],
        "candidate_classes": [],
        "image_records": [],
        "duplicates_vs_core": 0,
        "duplicates_vs_figshare": 0,
        "new_unique_images": 0,
        "errors": [],
        "status": "MISSING",
        "notes": dataset_info.get("notes", ""),
    }

    if not dataset_dir.exists():
        report["errors"].append(f"Dataset directory does not exist: {dataset_dir}")
        return report

    exts = SUPPORTED_IMAGE_EXTENSIONS
    all_files = [f for f in dataset_dir.rglob("*") if f.is_file()]
    report["total_files"] = len(all_files)

    skip_dirs = {".cache", "extracted", "splits", "images", "leaf_grouping", "data", "train", "val", "test", "valid", "Train", "Val", "Test", "Valid"}
    split_dirs = {"train", "val", "test", "valid", "Train", "Val", "Test", "Valid", "train_set_folder", "validation_set_folder", "test_set_folder", "training_set", "validation_set", "testing_set"}

    def has_images(d: Path) -> bool:
        return any(f.is_file() and f.suffix.lower() in exts for f in d.rglob("*"))

    def find_class_dirs(root: Path) -> List[Path]:
        found = []
        for item in root.iterdir():
            if item.is_dir() and not item.name.startswith(".") and item.name not in skip_dirs:
                if has_images(item):
                    found.append(item)
        return found

    class_dirs = []

    for item in dataset_dir.iterdir():
        if not item.is_dir() or item.name.startswith("."):
            continue
        children = {sub.name.lower() for sub in item.iterdir() if sub.is_dir()}
        if children & split_dirs:
            for sub in item.iterdir():
                if sub.is_dir() and sub.name.lower() in split_dirs:
                    class_dirs.extend(find_class_dirs(sub))
        elif item.name not in skip_dirs and has_images(item):
            class_dirs.append(item)

    if not class_dirs:
        for candidate in [dataset_dir / "train", dataset_dir / "Train", dataset_dir / "images", dataset_dir / "extracted"]:
            if candidate.exists():
                class_dirs = find_class_dirs(candidate)
                if class_dirs:
                    break

    processed_parents = set()
    if class_dirs:
        processed_parents.add(class_dirs[0].parent.resolve())

    for item in dataset_dir.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name in skip_dirs:
            if item.resolve() in processed_parents:
                continue
            found = find_class_dirs(item)
            if found:
                class_dirs.extend(found)
                processed_parents.add(item.resolve())

    if class_dirs:
        report["classes_discovered"] = sorted([d.name for d in class_dirs])
        report["status"] = "READY"

        for class_dir in class_dirs:
            class_name = class_dir.name
            class_report = process_class_dir(class_dir, dataset_id, class_name, core_hashes, figshare_hashes)
            report["class_counts"][class_name] = class_report["total_images"]
            report["valid_images"] += class_report["valid_images"]
            report["corrupt_images"] += class_report["corrupt_images"]
            report["too_small_images"] += class_report["too_small_images"]
            report["extreme_aspect_images"] += class_report["extreme_aspect_images"]
            report["blank_images"] += class_report["blank_images"]
            report["duplicates_vs_core"] += class_report["duplicates_vs_core"]
            report["duplicates_vs_figshare"] += class_report["duplicates_vs_figshare"]
            report["new_unique_images"] += class_report["new_unique_images"]
            report["image_records"].extend(class_report["image_records"])

            mapped_class, confidence = auto_map_class(class_name)
            if mapped_class:
                report["mapped_class_counts"][mapped_class] = report["mapped_class_counts"].get(mapped_class, 0) + class_report["valid_images"]
            else:
                report["unmapped_classes"].append(class_name)
                if class_report["valid_images"] > 0:
                    report["candidate_classes"].append({
                        "source_label": class_name,
                        "count": class_report["valid_images"],
                        "suggested_target": None,
                        "domain": report["domain"],
                    })
    else:
        flat_images = [f for f in dataset_dir.rglob("*") if f.is_file() and f.suffix.lower() in exts]
        if flat_images:
            report["total_images"] = len(flat_images)
            report["status"] = "READY"
            report["classes_discovered"] = ["_flat"]
            report["class_counts"]["_flat"] = len(flat_images)

            valid_count = 0
            for img_path in flat_images:
                record = validate_image(img_path)
                record["dataset_id"] = dataset_id
                record["source_class"] = "_flat"
                record["target_class"] = "UNMAPPED"
                record["duplicate_vs_core"] = record["hash"] in core_hashes
                record["duplicate_vs_figshare"] = record["hash"] in figshare_hashes
                record["commercial_ready"] = False
                if record["valid"]:
                    valid_count += 1
                    if record["hash"] in core_hashes:
                        report["duplicates_vs_core"] += 1
                    elif record["hash"] in figshare_hashes:
                        report["duplicates_vs_figshare"] += 1
                    else:
                        report["new_unique_images"] += 1
                else:
                    if record["corrupt"]:
                        report["corrupt_images"] += 1
                    if record["too_small"]:
                        report["too_small_images"] += 1
                    if record["extreme_aspect"]:
                        report["extreme_aspect_images"] += 1
                    if record["blank"]:
                        report["blank_images"] += 1
                report["image_records"].append(record)
            report["valid_images"] = valid_count
        else:
            report["status"] = "NO_IMAGES"
            report["errors"].append("No recognizable image files found")

    report["total_images"] = report["valid_images"] + report["corrupt_images"] + report["too_small_images"] + report["extreme_aspect_images"] + report["blank_images"]

    if report["status"] == "READY":
        if report["commercial_ok"]:
            report["approved_images"] = report["new_unique_images"]
            report["rejected_images"] = report["corrupt_images"] + report["too_small_images"] + report["duplicates_vs_core"] + report["duplicates_vs_figshare"]
            if report["approved_images"] > 0 or report["mapped_class_counts"]:
                report["status"] = "APPROVED"
            else:
                report["status"] = "REVIEW"
                report.setdefault("errors", []).append("No commercially ready mapped images")
        elif report["commercial_ok"] is False:
            report["status"] = "REJECTED"
            report.setdefault("errors", []).append("Non-commercial license")
        else:
            report["status"] = "REVIEW"
            report.setdefault("errors", []).append("License/commercial status unverified")

    return report


def read_dataset_metadata(dataset_dir: Path) -> Dict:
    metadata = {}
    readme = dataset_dir / "README.md"
    manifest = dataset_dir / "manifest.json"

    if readme.exists():
        metadata["readme_text"] = readme.read_text(encoding="utf-8", errors="ignore")
    if manifest.exists():
        try:
            metadata["manifest_data"] = json.loads(manifest.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            metadata["manifest_data"] = {}

    return metadata


def process_raw_datasets(source_dir: Path = RAW_DIR) -> List[Dict]:
    core_hashes, figshare_hashes = load_existing_hashes()
    ledger = load_ledger()
    reports = []

    if not source_dir.exists():
        print(f"ERROR: Source directory {source_dir} does not exist")
        return reports

    for dataset_dir in sorted(source_dir.iterdir()):
        if not dataset_dir.is_dir():
            continue
        if dataset_dir.name.startswith("."):
            continue
        if dataset_dir.name in (".cache",):
            continue

        metadata = read_dataset_metadata(dataset_dir)
        readme_text = metadata.get("readme_text", "")
        manifest_data = metadata.get("manifest_data", {})

        license_text, license_source, commercial_ok = detect_license(readme_text, manifest_data)
        attribution_required = "attribution" in readme_text.lower() or "cc by" in license_text.lower()
        attribution_text = manifest_data.get("attribution", "") if manifest_data else ""

        dataset_info = {
            "dataset_id": dataset_dir.name,
            "name": manifest_data.get("name", dataset_dir.name),
            "source": manifest_data.get("source", "unknown"),
            "url": manifest_data.get("source_url", manifest_data.get("url", "")),
            "license": license_text,
            "license_evidence": f"{license_source}: {license_text}",
            "commercial_ok": commercial_ok,
            "attribution_required": attribution_required,
            "attribution_text": attribution_text,
            "notes": manifest_data.get("instructions", ""),
        }

        fingerprint = f"{dataset_dir.name}:dir"
        existing = find_ledger_entry(ledger, fingerprint)
        if existing:
            reports.append(dict(existing))
            continue

        report = process_dataset(dataset_dir, dataset_info, core_hashes, figshare_hashes)
        report["fingerprint"] = fingerprint
        report["domain"] = detect_domain(dataset_dir.name, report.get("classes_discovered", []), readme_text)

        reports.append(report)
        save_ledger_entry(report)

    return reports


def generate_phase35d_gap_report(ledger_entries: List[Dict]) -> Dict:
    approved = [e for e in ledger_entries if e.get("status") == "APPROVED"]
    review = [e for e in ledger_entries if e.get("status") == "REVIEW"]
    rejected = [e for e in ledger_entries if e.get("status") == "REJECTED"]
    no_images = [e for e in ledger_entries if e.get("status") == "NO_IMAGES"]

    class_sources = defaultdict(set)
    for entry in approved:
        for cls in entry.get("mapped_class_counts", {}).keys():
            class_sources[cls].add(entry.get("dataset_id"))

    tier1_gaps = []
    for cls in TIER1_CLASSES:
        if cls not in class_sources or len(class_sources[cls]) == 0:
            tier1_gaps.append(cls)

    domain_counts = defaultdict(lambda: {"datasets": 0, "approved_images": 0, "classes": set()})
    for entry in ledger_entries:
        domain = entry.get("domain", "CROP / PLANT ID")
        domain_counts[domain]["datasets"] += 1
        if entry.get("status") == "APPROVED":
            domain_counts[domain]["approved_images"] += entry.get("approved_images", 0)
        for cls in entry.get("mapped_class_counts", {}).keys():
            domain_counts[domain]["classes"].add(cls)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_datasets": len(ledger_entries),
            "approved": len(approved),
            "review": len(review),
            "rejected": len(rejected),
            "no_images": len(no_images),
            "total_approved_images": sum(e.get("approved_images", 0) for e in approved),
            "total_valid_images": sum(e.get("valid_images", 0) for e in ledger_entries),
            "tier1_classes_with_data": len([cls for cls in TIER1_CLASSES if cls in class_sources]),
            "tier1_classes_without_data": len(tier1_gaps),
        },
        "approved_datasets": [{"dataset_id": e.get("dataset_id"), "approved_images": e.get("approved_images", 0), "domain": e.get("domain")} for e in approved],
        "review_datasets": [{"dataset_id": e.get("dataset_id"), "reason": e.get("errors", [""])[0] if e.get("errors") else "unverified"} for e in review],
        "rejected_datasets": [{"dataset_id": e.get("dataset_id"), "reason": e.get("errors", [""])[0] if e.get("errors") else "non-commercial"} for e in rejected],
        "no_images_datasets": [{"dataset_id": e.get("dataset_id"), "notes": e.get("notes", "")} for e in no_images],
        "tier1_gaps": tier1_gaps,
        "domain_coverage": {k: {"datasets": v["datasets"], "approved_images": v["approved_images"], "classes": len(v["classes"])} for k, v in domain_counts.items()},
    }


def generate_phase35d_class_coverage(ledger_entries: List[Dict]) -> Dict:
    class_info: Dict[str, Dict] = defaultdict(lambda: {
        "approved_images": 0,
        "source_dataset_count": 0,
        "sources": [],
        "status": "NO_DATA",
        "domain": "CROP / PLANT ID",
    })

    for entry in ledger_entries:
        if entry.get("status") == "APPROVED":
            for cls, count in entry.get("mapped_class_counts", {}).items():
                class_info[cls]["approved_images"] += count
                if entry.get("dataset_id") not in class_info[cls]["sources"]:
                    class_info[cls]["sources"].append(entry.get("dataset_id"))
                class_info[cls]["source_dataset_count"] = len(class_info[cls]["sources"])
                class_info[cls]["status"] = "APPROVED"

    classes = {}
    for cls in TIER1_CLASSES:
        info = class_info.get(cls, {"approved_images": 0, "source_dataset_count": 0, "status": "NO_DATA", "domain": "CROP / PLANT ID", "sources": []})
        classes[cls] = info

    candidate_classes = []
    for entry in ledger_entries:
        for cand in entry.get("candidate_classes", []):
            candidate_classes.append({
                "source_dataset": entry.get("dataset_id"),
                "source_label": cand.get("source_label"),
                "valid_images": cand.get("count"),
                "domain": cand.get("domain"),
            })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_tier1_classes": len(TIER1_CLASSES),
        "classes_with_data": sum(1 for c in classes.values() if c.get("status") == "APPROVED"),
        "classes": classes,
        "candidate_classes": candidate_classes,
    }


def write_phase35d_acquisition_report(ledger_entries: List[Dict], gap_report: Dict):
    lines = []
    lines.append("# Soil & Supper — Phase 35D Acquisition Report")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"**Phase**: 35D — Comprehensive Dataset Intake")
    lines.append(f"**Status**: OPEN — acquisition ongoing")
    lines.append("")
    lines.append("## 1. Dataset Status")
    lines.append("")
    lines.append("| Dataset ID | Domain | Status | Approved Images | License | Notes |")
    lines.append("|------------|--------|--------|-----------------|---------|-------|")

    for entry in ledger_entries:
        status = entry.get("status", "UNKNOWN")
        ds_id = entry.get("dataset_id", "unknown")
        domain = entry.get("domain", "CROP / PLANT ID")
        approved = entry.get("approved_images", 0)
        license = entry.get("license", "unknown")
        notes = entry.get("notes", "")
        lines.append(f"| {ds_id} | {domain} | {status} | {approved:,} | {license} | {notes} |")

    lines.append("")
    lines.append("## 2. Tier 1 Class Coverage (CROP / PLANT ID)")
    lines.append("")
    lines.append("| Class | Approved Images | Source Datasets | Status |")
    lines.append("|-------|-----------------|-----------------|--------|")

    coverage = generate_phase35d_class_coverage(ledger_entries)
    for cls in TIER1_CLASSES:
        info = coverage["classes"].get(cls, {})
        approved = info.get("approved_images", 0)
        sources = info.get("source_dataset_count", 0)
        status = info.get("status", "NO_DATA")
        lines.append(f"| {cls} | {approved:,} | {sources} | {status} |")

    lines.append("")
    lines.append("## 3. Domain Coverage")
    lines.append("")
    lines.append("| Domain | Datasets | Approved Images | Classes Mapped |")
    lines.append("|--------|----------|-----------------|----------------|")

    domain_data = gap_report.get("domain_coverage", {})
    for domain, info in domain_data.items():
        lines.append(f"| {domain} | {info['datasets']} | {info['approved_images']:,} | {info['classes']} |")

    lines.append("")
    lines.append("## 4. Gap Summary")
    lines.append("")
    summary = gap_report.get("summary", {})
    lines.append(f"- **Total datasets**: {summary.get('total_datasets', 0)}")
    lines.append(f"- **Approved datasets**: {summary.get('approved', 0)}")
    lines.append(f"- **Review datasets**: {summary.get('review', 0)}")
    lines.append(f"- **Rejected datasets**: {summary.get('rejected', 0)}")
    lines.append(f"- **No-image datasets**: {summary.get('no_images', 0)}")
    lines.append(f"- **Total approved images**: {summary.get('total_approved_images', 0):,}")
    lines.append(f"- **Total valid images**: {summary.get('total_valid_images', 0):,}")
    lines.append(f"- **Tier 1 classes with data**: {summary.get('tier1_classes_with_data', 0)} / {len(TIER1_CLASSES)}")
    lines.append(f"- **Tier 1 classes without data**: {summary.get('tier1_classes_without_data', 0)}")
    lines.append("")

    if gap_report.get("tier1_gaps"):
        lines.append("### Classes Without Commercial Data")
        lines.append("")
        for cls in gap_report["tier1_gaps"]:
            lines.append(f"- {cls}")
        lines.append("")

    lines.append("## 5. Candidate Classes (Unmapped)")
    lines.append("")
    candidates = coverage.get("candidate_classes", [])
    if candidates:
        for cand in candidates:
            lines.append(f"- **{cand['source_label']}** ({cand['source_dataset']}) — {cand['valid_images']} images — {cand['domain']}")
        lines.append("")
    else:
        lines.append("No candidate classes discovered.")
        lines.append("")

    lines.append("## 6. Next Steps")
    lines.append("")
    lines.append("1. Review datasets marked as REVIEW for license verification")
    lines.append("2. Download missing Priority 1 datasets if coverage is insufficient")
    lines.append("3. Rerun: `python training/phase35d_intake.py --all --json`")
    lines.append("")
    lines.append("---")
    lines.append("*Phase 35D remains open until acquisition is complete.*")
    lines.append("*Do not train crop model yet.*")

    PHASE35D_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Acquisition report written to: {PHASE35D_REPORT}")


def write_attribution_document(ledger_entries: List[Dict]):
    lines = []
    lines.append("# Soil & Supper — Dataset Attributions")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append("## Approved Datasets Requiring Attribution")
    lines.append("")

    attribution_entries = []
    for entry in ledger_entries:
        if entry.get("status") == "APPROVED" and entry.get("attribution_required"):
            attribution_entries.append(entry)

    if attribution_entries:
        for entry in attribution_entries:
            lines.append(f"### {entry.get('name', entry.get('dataset_id'))}")
            lines.append("")
            lines.append(f"- **Dataset ID**: {entry.get('dataset_id')}")
            lines.append(f"- **License**: {entry.get('license')}")
            lines.append(f"- **Source**: {entry.get('source')}")
            lines.append(f"- **URL**: {entry.get('url')}")
            lines.append(f"- **Attribution**: {entry.get('attribution_text', 'Required — see license')}")
            lines.append(f"- **Domain**: {entry.get('domain', 'CROP / PLANT ID')}")
            lines.append(f"- **Approved Images**: {entry.get('approved_images', 0):,}")
            lines.append("")
    else:
        lines.append("No approved datasets currently require attribution.")
        lines.append("")

    lines.append("## Review Datasets")
    lines.append("")
    review_entries = [e for e in ledger_entries if e.get("status") == "REVIEW"]
    if review_entries:
        for entry in review_entries:
            lines.append(f"- **{entry.get('dataset_id')}**: {entry.get('license', 'unknown')} — {entry.get('notes', 'License verification needed')}")
        lines.append("")
    else:
        lines.append("No datasets in REVIEW status.")
        lines.append("")

    PHASE35D_ATTRIBUTIONS.write_text("\n".join(lines), encoding="utf-8")
    print(f"Attribution document written to: {PHASE35D_ATTRIBUTIONS}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Phase 35D comprehensive dataset intake")
    parser.add_argument("--all", action="store_true", help="Process all datasets in raw/")
    parser.add_argument("--dataset", type=str, help="Process specific dataset path under raw/")
    parser.add_argument("--json", action="store_true", help="Emit JSON reports")
    parser.add_argument("--dry-run", action="store_true", help="Inspect candidates without modifying manifests")
    args = parser.parse_args()

    if not args.all and not args.dataset:
        parser.print_help()
        sys.exit(1)

    if args.dataset:
        candidate = Path(args.dataset)
        if not candidate.exists():
            print(f"ERROR: {candidate} does not exist")
            sys.exit(1)

        core_hashes, figshare_hashes = load_existing_hashes()
        ledger = load_ledger()
        metadata = read_dataset_metadata(candidate)
        readme_text = metadata.get("readme_text", "")
        manifest_data = metadata.get("manifest_data", {})

        license_text, license_source, commercial_ok = detect_license(readme_text, manifest_data)
        attribution_required = "attribution" in readme_text.lower() or "cc by" in license_text.lower()
        attribution_text = manifest_data.get("attribution", "") if manifest_data else ""

        dataset_info = {
            "dataset_id": candidate.name,
            "name": manifest_data.get("name", candidate.name),
            "source": manifest_data.get("source", "unknown"),
            "url": manifest_data.get("source_url", manifest_data.get("url", "")),
            "license": license_text,
            "license_evidence": f"{license_source}: {license_text}",
            "commercial_ok": commercial_ok,
            "attribution_required": attribution_required,
            "attribution_text": attribution_text,
            "notes": manifest_data.get("instructions", ""),
        }

        report = process_dataset(candidate, dataset_info, core_hashes, figshare_hashes)
        report["domain"] = detect_domain(candidate.name, report.get("classes_discovered", []), readme_text)

        print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else str(report))
        if not args.dry_run:
            save_ledger_entry(report)
        return

    if not args.all:
        parser.print_help()
        sys.exit(1)

    reports = process_raw_datasets()

    gap = generate_phase35d_gap_report(reports)
    with open(PHASE35D_GAP_REPORT, "w", encoding="utf-8") as f:
        json.dump(gap, f, indent=2, ensure_ascii=False)

    coverage = generate_phase35d_class_coverage(reports)
    with open(PHASE35D_CLASS_COVERAGE, "w", encoding="utf-8") as f:
        json.dump(coverage, f, indent=2, ensure_ascii=False)

    with open(PHASE35D_CANDIDATE_CLASSES, "w", encoding="utf-8") as f:
        json.dump(coverage.get("candidate_classes", []), f, indent=2, ensure_ascii=False)

    write_phase35d_acquisition_report(reports, gap)
    write_attribution_document(reports)

    print("\n" + "=" * 80)
    print("PHASE 35D INTAKE SUMMARY")
    print("=" * 80)
    print(f"Datasets processed: {len(reports)}")
    print(f"Total images discovered: {sum(r.get('total_images', 0) for r in reports):,}")
    print(f"Total valid images: {sum(r.get('valid_images', 0) for r in reports):,}")
    print(f"Total approved images: {sum(r.get('approved_images', 0) for r in reports):,}")
    print()
    for r in reports:
        print(f"  {r.get('dataset_id', 'unknown'):<30} {r.get('status', 'UNKNOWN'):<15} {r.get('domain', 'N/A'):<20} {r.get('total_images', 0):>8} images  {r.get('approved_images', 0):>8} approved")
    print("=" * 80)


if __name__ == "__main__":
    main()
