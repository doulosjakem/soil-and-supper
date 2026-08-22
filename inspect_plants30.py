from pathlib import Path

base = Path('D:/soil-and-supper/soil-and-supper/raw/plants_type_30class')
for item in sorted(base.iterdir()):
    print(f'{item.name}: is_dir={item.is_dir()}, is_file={item.is_file()}')
    if item.is_dir():
        for sub in sorted(item.iterdir()):
            print(f'  {sub.name}: is_dir={sub.is_dir()}, is_file={sub.is_file()}')
            if sub.is_dir():
                for sub2 in sorted(sub.iterdir()):
                    if sub2.is_dir():
                        count = len(list(sub2.glob('*')))
                        print(f'    {sub2.name}: dir, {count} items')
                    else:
                        print(f'    {sub2.name}: file')
