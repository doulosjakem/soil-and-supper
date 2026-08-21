import os
import json
from pathlib import Path

extracted_dir = Path(r'D:\soil-and-supper\soil-and-supper\training_data\inbox_extracted')

# Scan each top-level directory
for dataset_dir in sorted(extracted_dir.iterdir()):
    if not dataset_dir.is_dir():
        continue
    
    print(f"\n{'='*80}")
    print(f"DATASET: {dataset_dir.name}")
    print(f"{'='*80}")
    
    # Count files and images
    all_files = list(dataset_dir.rglob('*'))
    total_files = len([f for f in all_files if f.is_file()])
    images = [f for f in all_files if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tif', '.tiff')]
    other_files = [f for f in all_files if f.is_file() and f.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tif', '.tiff')]
    
    print(f"Total files: {total_files:,}")
    print(f"Images: {len(images):,}")
    print(f"Other files: {len(other_files):,}")
    
    # Check for README/LICENSE
    readmes = [f for f in other_files if 'readme' in f.name.lower()]
    licenses = [f for f in other_files if 'license' in f.name.lower()]
    metadata = [f for f in other_files if f.suffix.lower() in ('.json', '.yaml', '.yml', '.csv', '.txt', '.md')]
    
    if readmes:
        print(f"\nREADME files:")
        for r in readmes[:3]:
            print(f"  {r.relative_to(dataset_dir)}")
    
    if licenses:
        print(f"\nLICENSE files:")
        for l in licenses[:3]:
            print(f"  {l.relative_to(dataset_dir)}")
    
    if metadata:
        print(f"\nMetadata files (first 10):")
        for m in metadata[:10]:
            print(f"  {m.relative_to(dataset_dir)}")
    
    # Check directory structure
    top_dirs = [d.name for d in dataset_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    if top_dirs:
        print(f"\nTop-level directories ({len(top_dirs)}):")
        for d in top_dirs[:10]:
            print(f"  {d}")
        if len(top_dirs) > 10:
            print(f"  ... and {len(top_dirs)-10} more")
    
    # Check for class directories
    class_dirs = []
    for item in dataset_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in ('extracted', '.cache', 'splits', 'images', 'leaf_grouping', 'data', 'train', 'val', 'test', 'valid', 'annotations'):
            imgs = [f for f in item.rglob('*') if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')]
            if imgs:
                class_dirs.append(item.name)
    
    if class_dirs:
        print(f"\nClass directories ({len(class_dirs)}):")
        for d in class_dirs[:15]:
            count = len([f for f in (dataset_dir / d).rglob('*') if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')])
            print(f"  {d}: {count} images")
        if len(class_dirs) > 15:
            print(f"  ... and {len(class_dirs)-15} more")
