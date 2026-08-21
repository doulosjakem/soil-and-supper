from pathlib import Path

extracted_dir = Path(r'D:\soil-and-supper\soil-and-supper\training_data\inbox_extracted')

# Key datasets to identify
key_datasets = [
    'A Comprehensive Image Dataset of  Vegetables Grown in Bangladesh',
    'archive',
    'archive _10_',
    'archive _11_',
    'archive _13_',
    'archive _1_',
    'archive _2_',
    'archive _3_',
    'archive _4_',
    'archive _5_',
    'archive _8_',
    'archive _9_',
    'd7kbzjr83k-1',
    'Vegetable Image Dataset for Classification Models A Bangladeshi Perspective',
    'Vegetable Object Detection Dataset from Bangladesh',
    'VegNet Vegetable Dataset with quality _Unripe_ Ripe_ Old_ Dried and Damaged_',
    'last_batch_archive',
    'last_batch_archive__1_',
    'last_batch_archive__2_',
    'last_batch_archive__4_',
    'last_batch_archive__5_',
    'last_batch_archive__7_',
]

for name in key_datasets:
    d = extracted_dir / name
    if not d.exists():
        continue
    
    print(f"\n{'='*80}")
    print(f"DATASET: {name}")
    print(f"{'='*80}")
    
    # Find README files
    readmes = list(d.rglob('README*')) + list(d.rglob('readme*'))
    if readmes:
        print(f"\nREADME files:")
        for r in readmes[:3]:
            print(f"  {r.relative_to(d)}")
            try:
                content = r.read_text(encoding='utf-8', errors='ignore')[:500]
                print(f"  Content preview:")
                for line in content.split('\n')[:10]:
                    print(f"    {line}")
            except:
                pass
    
    # Find LICENSE files
    licenses = list(d.rglob('LICENSE*')) + list(d.rglob('license*'))
    if licenses:
        print(f"\nLICENSE files:")
        for l in licenses[:3]:
            print(f"  {l.relative_to(d)}")
            try:
                content = l.read_text(encoding='utf-8', errors='ignore')[:300]
                print(f"  Content: {content[:200]}")
            except:
                pass
    
    # Find classname.txt
    classnames = list(d.rglob('classname.txt'))
    if classnames:
        print(f"\nClass names:")
        for cn in classnames[:2]:
            print(f"  {cn.relative_to(d)}")
            try:
                content = cn.read_text(encoding='utf-8', errors='ignore')
                lines = content.strip().split('\n')[:20]
                for line in lines:
                    print(f"    {line}")
            except:
                pass
    
    # Find top-level class directories
    class_dirs = []
    for item in d.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in ('extracted', '.cache', 'splits', 'images', 'leaf_grouping', 'data', 'train', 'val', 'test', 'valid', 'annotations'):
            img_count = sum(1 for f in item.rglob('*') if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif'))
            if img_count > 0:
                class_dirs.append((item.name, img_count))
    
    if class_dirs:
        print(f"\nTop-level class directories ({len(class_dirs)}):")
        for name, count in sorted(class_dirs, key=lambda x: -x[1])[:20]:
            try:
                print(f"  {name}: {count} images")
            except UnicodeEncodeError:
                print(f"  [{name.encode('ascii', 'replace').decode()}]: {count} images")
