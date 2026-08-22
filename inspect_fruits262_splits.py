from pathlib import Path

base = Path('D:/soil-and-supper/soil-and-supper/raw/fruits262_101class_subset')
for split in ['train', 'test', 'val']:
    split_base = base / split
    items = sorted(split_base.iterdir())
    dirs = [i for i in items if i.is_dir()]
    files = [i for i in items if i.is_file()]
    print(f'=== {split} ===')
    print(f'Total items: {len(items)}')
    print(f'Dirs: {len(dirs)}, Files: {len(files)}')
    if dirs:
        for d in dirs[:5]:
            count = len(list(d.glob('*')))
            print(f'  {d.name}: {count} items')
        if len(dirs) > 5:
            print(f'  ... and {len(dirs) - 5} more dirs')
    if files:
        for f in files[:5]:
            print(f'  {f.name} (file)')
