from pathlib import Path
import csv

base = Path('D:/soil-and-supper/soil-and-supper/raw/fruits262_101class_subset')
for csv_file in sorted(base.glob('*.csv')):
    print(f'=== {csv_file.name} ===')
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i < 5:
                print(row)
            else:
                break
    print()

for item in sorted(base.iterdir()):
    if item.is_dir():
        print(f'{item.name}: dir')
        files = list(item.glob('*'))
        print(f'  {len(files)} files')
        for f in files[:3]:
            print(f'    {f.name}')
    else:
        print(f'{item.name}: file')
