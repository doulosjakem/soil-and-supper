#!/usr/bin/env python3
"""
Quality control for Soil & Supper dataset.
Run after curate_datasets.py to verify image quality.
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image
    import numpy as np
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("[WARNING] Pillow not installed. Quality checks will be limited.")
    print("Install with: pip install Pillow numpy")

SPLITS_DIR = Path("./splits")
METADATA_DIR = Path("./metadata")
REPORTS_DIR = METADATA_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

TARGET_CLASSES = [
    "Tomato", "Pepper", "Eggplant", "Cucumber", "Zucchini",
    "Green Bean", "Corn", "Broccoli", "Carrot", "Potato",
    "Onion", "Strawberry"
]

def check_blur(image_path, threshold=100):
    """Check if image is blurry using Laplacian variance."""
    if not PIL_AVAILABLE:
        return None
    
    try:
        img = Image.open(image_path).convert("L")
        img_array = np.array(img)
        
        # Calculate Laplacian variance
        laplacian = np.var(np.gradient(np.gradient(img_array)[0])[0])
        return laplacian
    except Exception as e:
        print(f"  Error processing {image_path.name}: {e}")
        return None

def check_exposure(image_path):
    """Check if image has extreme exposure issues."""
    if not PIL_AVAILABLE:
        return None
    
    try:
        img = Image.open(image_path).convert("L")
        histogram = img.histogram()
        pixels = sum(histogram)
        if pixels == 0:
            return None
        
        mean_brightness = sum(i * count for i, count in enumerate(histogram)) / pixels
        return mean_brightness
    except Exception as e:
        return None

def run_quality_checks():
    """Run quality checks on all curated images."""
    print("=" * 60)
    print("QUALITY CONTROL CHECKS")
    print("=" * 60)
    
    if not PIL_AVAILABLE:
        print("[SKIP] Pillow not available. Install with: pip install Pillow numpy")
        return
    
    report = []
    stats = {
        "total_images": 0,
        "blurry_images": 0,
        "overexposed_images": 0,
        "underexposed_images": 0,
        "too_small_images": 0,
        "errors": 0
    }
    
    for cls in TARGET_CLASSES:
        class_dir = SPLITS_DIR / "train" / cls
        if not class_dir.exists():
            continue
        
        images = list(class_dir.iterdir())
        print(f"\n{cls}: {len(images)} images")
        
        for img_path in images:
            if not img_path.is_file():
                continue
            
            stats["total_images"] += 1
            
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    
                    # Check size
                    if min(width, height) < 100:
                        stats["too_small_images"] += 1
                        report.append({
                            "filename": img_path.name,
                            "class": cls,
                            "issue": "too_small",
                            "detail": f"{width}x{height}"
                        })
                        continue
                    
                    # Check blur
                    laplacian = check_blur(img_path)
                    if laplacian is not None and laplacian < 100:
                        stats["blurry_images"] += 1
                        report.append({
                            "filename": img_path.name,
                            "class": cls,
                            "issue": "blurry",
                            "detail": f"laplacian={laplacian:.1f}"
                        })
                    
                    # Check exposure
                    brightness = check_exposure(img_path)
                    if brightness is not None:
                        if brightness < 10:
                            stats["underexposed_images"] += 1
                            report.append({
                                "filename": img_path.name,
                                "class": cls,
                                "issue": "underexposed",
                                "detail": f"brightness={brightness:.1f}"
                            })
                        elif brightness > 245:
                            stats["overexposed_images"] += 1
                            report.append({
                                "filename": img_path.name,
                                "class": cls,
                                "issue": "overexposed",
                                "detail": f"brightness={brightness:.1f}"
                            })
            
            except Exception as e:
                stats["errors"] += 1
                report.append({
                    "filename": img_path.name,
                    "class": cls,
                    "issue": "error",
                    "detail": str(e)
                })
    
    # Print summary
    print("\n" + "=" * 60)
    print("QUALITY SUMMARY")
    print("=" * 60)
    print(f"Total images checked: {stats['total_images']}")
    print(f"Blurry images: {stats['blurry_images']}")
    print(f"Overexposed images: {stats['overexposed_images']}")
    print(f"Underexposed images: {stats['underexposed_images']}")
    print(f"Too small images: {stats['too_small_images']}")
    print(f"Errors: {stats['errors']}")
    
    # Save report
    report_path = REPORTS_DIR / "quality_report.json"
    with open(report_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "stats": stats,
            "issues": report
        }, f, indent=2)
    
    print(f"\nDetailed report saved: {report_path}")
    
    # Save CSV
    csv_path = REPORTS_DIR / "quality_issues.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "class", "issue", "detail"])
        writer.writeheader()
        writer.writerows(report)
    
    print(f"Issues CSV saved: {csv_path}")

def check_class_balance():
    """Check class distribution in splits."""
    print("\n" + "=" * 60)
    print("CLASS BALANCE CHECK")
    print("=" * 60)
    
    balance_report = []
    
    for split in ["train", "val", "test"]:
        split_dir = SPLITS_DIR / split
        if not split_dir.exists():
            continue
        
        print(f"\n{split.upper()}:")
        split_counts = {}
        
        for cls in TARGET_CLASSES:
            class_dir = split_dir / cls
            if class_dir.exists():
                count = len([f for f in class_dir.iterdir() if f.is_file()])
                split_counts[cls] = count
                print(f"  {cls}: {count}")
            else:
                split_counts[cls] = 0
        
        balance_report.append({
            "split": split,
            "counts": split_counts,
            "total": sum(split_counts.values())
        })
    
    # Save balance report
    report_path = REPORTS_DIR / "class_balance.json"
    with open(report_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "splits": balance_report
        }, f, indent=2)
    
    print(f"\nClass balance report saved: {report_path}")

def main():
    print("=" * 60)
    print("SOIL & SUPPER QUALITY CONTROL")
    print("=" * 60)
    print(f"Started: {datetime.now().isoformat()}")
    
    run_quality_checks()
    check_class_balance()
    
    print("\n" + "=" * 60)
    print("QUALITY CONTROL COMPLETE")
    print("=" * 60)
    print(f"\nReview reports in: {REPORTS_DIR}")
    print(f"\nNext steps:")
    print(f"1. Review quality_issues.csv for problematic images")
    print(f"2. Remove or replace images marked as issues")
    print(f"3. Re-run curate_datasets.py if major changes are needed")
    print(f"4. Proceed to model training when quality is acceptable")

if __name__ == "__main__":
    main()
