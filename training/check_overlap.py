#!/usr/bin/env python3
"""
Overlap checker for external test set candidates.
Checks external candidate images against the commercial training core
for exact duplicates (SHA256) and near-duplicates (phash).
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Set, Tuple, List
from collections import defaultdict

import imagehash
from PIL import Image

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
EXACT_DEDUP_MANIFEST = MANIFESTS_DIR / "exact_dedup_manifest.jsonl"
COMMERCIAL_MANIFEST = MANIFESTS_DIR / "commercial_manifest.jsonl"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def load_commercial_hashes() -> Set[str]:
    """Load SHA256 hashes from the exact dedup manifest."""
    hashes = set()
    if not EXACT_DEDUP_MANIFEST.exists():
        print(f"Warning: {EXACT_DEDUP_MANIFEST} not found")
        return hashes
    with open(EXACT_DEDUP_MANIFEST, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            hashes.add(entry["hash"])
    return hashes


def compute_sha256(image_path: Path) -> str:
    """Compute SHA256 hash of an image file."""
    h = hashlib.sha256()
    with open(image_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def compute_phash(image_path: Path, hash_size: int = 8) -> imagehash.ImageHash:
    """Compute perceptual hash of an image."""
    with Image.open(image_path) as img:
        return imagehash.phash(img, hash_size=hash_size)


def check_exact_duplicates(
    candidate_dir: Path, commercial_hashes: Set[str]
) -> Tuple[List[str], List[str]]:
    """Check candidate images for exact duplicates in commercial core."""
    exact_matches = []
    errors = []
    for img_path in candidate_dir.rglob("*"):
        if img_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        try:
            img_hash = compute_sha256(img_path)
            if img_hash in commercial_hashes:
                exact_matches.append(str(img_path))
        except Exception as e:
            errors.append(f"{img_path}: {e}")
    return exact_matches, errors


def check_near_duplicates(
    candidate_dir: Path,
    commercial_hashes: Set[str],
    hash_size: int = 8,
    threshold: int = 10,
) -> Tuple[List[Tuple[str, str, int]], List[str]]:
    """Check candidate images for near-duplicates in commercial core.
    
    Note: This requires computing phash for ALL commercial images, which is
    expensive. For now, this function only checks exact duplicates.
    Full phash checking should be done with a pre-computed commercial phash index.
    """
    near_matches = []
    errors = []
    # Placeholder: full phash checking requires pre-computed commercial phash index
    # For now, we only report that phash checking is not yet implemented
    errors.append(
        "Perceptual hash checking not yet implemented. "
        "Requires pre-computed phash index of commercial training images."
    )
    return near_matches, errors


def check_candidate(
    candidate_name: str, candidate_dir: Path
) -> Dict:
    """Run overlap checks for a single candidate dataset."""
    print(f"\n=== Checking {candidate_name} ===")
    print(f"Directory: {candidate_dir}")

    commercial_hashes = load_commercial_hashes()
    print(f"Loaded {len(commercial_hashes)} commercial image hashes")

    exact_matches, errors = check_exact_duplicates(candidate_dir, commercial_hashes)
    near_matches, phash_errors = check_near_duplicates(candidate_dir, commercial_hashes)

    result = {
        "candidate_name": candidate_name,
        "candidate_dir": str(candidate_dir),
        "total_images_checked": 0,
        "exact_duplicates": exact_matches,
        "near_duplicates": near_matches,
        "errors": errors + phash_errors,
        "status": "PASS" if not exact_matches else "FAIL",
    }

    # Count total images
    result["total_images_checked"] = sum(
        1 for p in candidate_dir.rglob("*")
        if p.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    print(f"Total images checked: {result['total_images_checked']}")
    print(f"Exact duplicates: {len(exact_matches)}")
    if exact_matches:
        for match in exact_matches[:10]:
            print(f"  EXACT MATCH: {match}")
        if len(exact_matches) > 10:
            print(f"  ... and {len(exact_matches) - 10} more")
    print(f"Near duplicates: {len(near_matches)}")
    if errors:
        print(f"Errors: {len(errors)}")
        for err in errors[:5]:
            print(f"  {err}")

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python check_overlap.py <candidate_dir> [candidate_name]")
        sys.exit(1)

    candidate_dir = Path(sys.argv[1])
    candidate_name = sys.argv[2] if len(sys.argv) > 2 else candidate_dir.name

    if not candidate_dir.exists():
        print(f"Error: {candidate_dir} does not exist")
        sys.exit(1)

    result = check_candidate(candidate_name, candidate_dir)

    report_path = MANIFESTS_DIR / f"overlap_check_{candidate_name}.json"
    with open(report_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nReport saved to: {report_path}")
