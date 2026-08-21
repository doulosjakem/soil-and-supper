from pathlib import Path

extracted_dir = Path(r'D:\soil-and-supper\soil-and-supper\training_data\inbox_extracted')
sep = "=" * 80

for name in ['last batch']:
    d = extracted_dir / name
    if not d.exists():
        continue
    for sub in sorted(d.iterdir()):
        if not sub.is_dir():
            continue
        print(f"\n{sep}")
        print(f"DATASET: {sub.name}")
        print(sep)
        
        all_files = list(sub.rglob('*'))
        total_files = len([f for f in all_files if f.is_file()])
        images = [f for f in all_files if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tif', '.tiff')]
        other_files = [f for f in all_files if f.is_file() and f.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tif', '.tiff')]
        
        print(f"Total files: {total_files:,}")
        print(f"Images: {len(images):,}")
        print(f"Other files: {len(other_files):,}")
        
        readmes = [f for f in other_files if 'readme' in f.name.lower()]
        licenses = [f for f in other_files if 'license' in f.name.lower()]
        metadata = [f for f in other_files if f.suffix.lower() in ('.json', '.yaml', '.yml', '.csv', '.txt', '.md')]
        
        if readmes:
            print(f"README files:")
            for r in readmes[:3]:
                print(f"  {r.relative_to(sub)}")
        
        if licenses:
            print(f"LICENSE files:")
            for l in licenses[:3]:
                print(f"  {l.relative_to(sub)}")
        
        if metadata:
            print(f"Metadata files (first 10):")
            for m in metadata[:10]:
                print(f"  {m.relative_to(sub)}")
        
        class_dirs = []
        for item in sub.iterdir():
            if item.is_dir() and not item.name.startswith('.') and item.name not in ('extracted', '.cache', 'splits', 'images', 'leaf_grouping', 'data', 'train', 'val', 'test', 'valid', 'annotations', 'test', 'train', 'val'):
                imgs = [f for f in item.rglob('*') if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')]
                if imgs:
                    class_dirs.append(item.name)
        
        if class_dirs:
            print(f"Class directories ({len(class_dirs)}):")
            for c in class_dirs[:15]:
                count = len([f for f in (sub / c).rglob('*') if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')])
                print(f"  {c}: {count} images")
            if len(class_dirs) > 15:
                print(f"  ... and {len(class_dirs)-15} more")
