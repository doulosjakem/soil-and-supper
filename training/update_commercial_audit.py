#!/usr/bin/env python3
"""
Update commercial class audit with figshare dataset incorporation.
"""

import json
from collections import defaultdict
from datetime import datetime, timezone

# Original commercial counts from Phase 22
ORIGINAL_COUNTS = {
    "Apple_scab": 723,
    "Bacterial_spot": 3305,
    "Cedar_apple_rust": 362,
    "Downy_mildew": 1002,
    "Early_blight": 8421,
    "Grape_black_rot": 1244,
    "Healthy": 36342,
    "Late_blight": 16141,
    "Leaf_spot": 13897,
    "Peach_bacterial_spot": 2297,
    "Powdery_mildew": 2178,
    "Rust": 1308,
    "Septoria_leaf_spot": 1920,
    "Spider_mite": 1678,
    "Squash_powdery_mildew": 1965,
    "Tomato_mosaic_virus": 427,
    "Tomato_yellow_leaf_curl": 5432,
}

# Figshare contributions (from manifest analysis)
FIGSHARE_CONTRIBUTIONS = {
    "Anthracnose": 383,
    "Early_blight": 493,
    "Leaf_spot": 4366,
    "Powdery_mildew": 2423,
    "Rust": 2332,
    "Spider_mite": 488,
}

# Source counts for each class
ORIGINAL_SOURCES = {
    "Apple_scab": {"plantdoc": 93, "plantvillage": 630},
    "Bacterial_spot": {"plantdoc": 181, "plantvillage": 3124},
    "Cedar_apple_rust": {"plantdoc": 87, "plantvillage": 275},
    "Downy_mildew": {"grapevine": 1002},
    "Early_blight": {"irish_potato": 6217, "plantdoc": 204, "plantvillage": 2000},
    "Grape_black_rot": {"plantdoc": 64, "plantvillage": 1180},
    "Healthy": {"grapevine": 1117, "irish_potato": 19308, "plantdoc": 846, "plantvillage": 15071},
    "Late_blight": {"irish_potato": 13029, "plantdoc": 211, "plantvillage": 2901},
    "Leaf_spot": {"plantdoc": 347, "plantvillage": 13550},
    "Peach_bacterial_spot": {"plantvillage": 2297},
    "Powdery_mildew": {"grapevine": 1126, "plantvillage": 1052},
    "Rust": {"plantdoc": 116, "plantvillage": 1192},
    "Septoria_leaf_spot": {"plantdoc": 149, "plantvillage": 1771},
    "Spider_mite": {"plantdoc": 2, "plantvillage": 1676},
    "Squash_powdery_mildew": {"plantdoc": 130, "plantvillage": 1835},
    "Tomato_mosaic_virus": {"plantdoc": 54, "plantvillage": 373},
    "Tomato_yellow_leaf_curl": {"plantdoc": 75, "plantvillage": 5357},
}

# Add figshare sources
FIGSHARE_SOURCES = {
    "Anthracnose": {"figshare_disease": 383},
    "Early_blight": {"figshare_disease": 493},
    "Leaf_spot": {"figshare_disease": 4366},
    "Powdery_mildew": {"figshare_disease": 2423},
    "Rust": {"figshare_disease": 2332},
    "Spider_mite": {"figshare_disease": 488},
}

# Combine sources
ALL_SOURCES = defaultdict(dict)
for cls, sources in ORIGINAL_SOURCES.items():
    ALL_SOURCES[cls].update(sources)
for cls, sources in FIGSHARE_SOURCES.items():
    if cls in ALL_SOURCES:
        ALL_SOURCES[cls].update(sources)
    else:
        ALL_SOURCES[cls] = sources

# Calculate new totals
NEW_COUNTS = {}
for cls in ORIGINAL_COUNTS:
    NEW_COUNTS[cls] = ORIGINAL_COUNTS[cls]
for cls in FIGSHARE_CONTRIBUTIONS:
    if cls in NEW_COUNTS:
        NEW_COUNTS[cls] += FIGSHARE_CONTRIBUTIONS[cls]
    else:
        NEW_COUNTS[cls] = FIGSHARE_CONTRIBUTIONS[cls]

total_original = sum(ORIGINAL_COUNTS.values())
total_new = sum(NEW_COUNTS.values())

print("=== COMMERCIAL CLASS AUDIT UPDATE ===")
print(f"Original total: {total_original}")
print(f"New total: {total_new}")
print(f"Added: {total_new - total_original}")
print()

print("=== BEFORE/AFTER BY CLASS ===")
for cls in sorted(NEW_COUNTS.keys(), key=lambda x: -NEW_COUNTS[x]):
    orig = ORIGINAL_COUNTS.get(cls, 0)
    new = NEW_COUNTS[cls]
    change = new - orig
    pct_change = (change / orig * 100) if orig > 0 else float('inf')
    sources = ALL_SOURCES.get(cls, {})
    num_sources = len(sources)
    dominant = max(sources.items(), key=lambda x: x[1]) if sources else ("none", 0)
    dominant_pct = (dominant[1] / new * 100) if new > 0 else 0
    
    print(f"{cls}:")
    print(f"  Before: {orig}")
    print(f"  After: {new}")
    print(f"  Change: +{change} ({pct_change:+.1f}%)")
    print(f"  Sources: {num_sources}")
    print(f"  Dominant: {dominant[0]} ({dominant_pct:.1f}%)")
    print()

# Write updated audit
audit = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "total_commercial_images": total_new,
    "total_original_images": total_original,
    "added_from_figshare": total_new - total_original,
    "classes": {}
}

for cls in sorted(NEW_COUNTS.keys(), key=lambda x: -NEW_COUNTS[x]):
    sources = ALL_SOURCES.get(cls, {})
    total = NEW_COUNTS[cls]
    dominant_source = max(sources.items(), key=lambda x: x[1])[0] if sources else "none"
    dominant_pct = (max(sources.values()) / total * 100) if total > 0 else 0
    
    audit["classes"][cls] = {
        "count": total,
        "percentage": round(total / total_new * 100, 2),
        "num_sources": len(sources),
        "sources": dict(sources),
        "dominant_source": dominant_source,
        "dominant_source_percentage": round(dominant_pct, 2),
        "disproportionately_dependent": dominant_pct > 80
    }

with open("training_data/reports/commercial_class_audit_updated.json", "w", encoding="utf-8") as f:
    json.dump(audit, f, indent=2, ensure_ascii=False)

print(f"\nWrote updated audit to training_data/reports/commercial_class_audit_updated.json")
