from pathlib import Path

extracted_dir = Path(r'D:\soil-and-supper\soil-and-supper\training_data\inbox_extracted')
sep = "=" * 80

last_batch_dirs = [d for d in extracted_dir.iterdir() if d.is_dir() and d.name.startswith('last_batch_')]
for d in sorted(last_batch_dirs):
    print(f"\n{sep}")
    print(f"DATASET: {d.name}")
    print(sep)
    
    top_items = list(d.iterdir())
    print(f"Top-level items: {len(top_items)}")
    
    for item in top_items[:5]:
        if item.is_dir():
            sub_items = list(item.iterdir())
            print(f"  {item.name}/ ({len(sub_items)} items)")
            if len(sub_items) > 5:
                print(f"    ... and {len(sub_items)-5} more")
        else:
            print(f"  {item.name} ({item.stat().st_size/1024:.1f} KB)")
    
    if len(top_items) > 5:
        print(f"  ... and {len(top_items)-5} more top-level items")
    
    exts = {}
    for f in d.rglob('*'):
        if f.is_file():
            ext = f.suffix.lower()
            exts[ext] = exts.get(ext, 0) + 1
    
    print(f"\nFile extensions:")
    for ext, count in sorted(exts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {ext}: {count:,}")
    
    class_dirs = []
    for item in d.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            img_count = sum(1 for f in item.rglob('*') if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif'))
            if img_count > 0:
                class_dirs.append((item.name, img_count))
    
    if class_dirs:
        print(f"\nClass directories ({len(class_dirs)}):")
        for name, count in sorted(class_dirs, key=lambda x: -x[1])[:15]:
            try:
                print(f"  {name}: {count} images")
            except UnicodeEncodeError:
                safe_name = name.encode('ascii', 'replace').decode('ascii')
                print(f"  {safe_name}: {count} images")
        if len(class_dirs) > 15:
            print(f"  ... and {len(class_dirs)-15} more")
