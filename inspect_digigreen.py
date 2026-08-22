from pathlib import Path

base = Path('D:/soil-and-supper/soil-and-supper/raw/hf_digigreen')
for f in sorted(base.rglob('*')):
    if f.is_file() and f.suffix.lower() in ['.csv', '.json', '.txt', '.md', '.yaml', '.yml']:
        print(f.relative_to(base))
        if f.suffix == '.csv':
            with open(f, 'r', encoding='utf-8') as fh:
                lines = fh.readlines()[:5]
                for line in lines:
                    print(f'  {line.strip()}')
        elif f.suffix == '.json':
            with open(f, 'r', encoding='utf-8') as fh:
                import json
                data = json.load(fh)
                print(f'  keys: {list(data.keys())[:10]}')
        elif f.suffix == '.md':
            with open(f, 'r', encoding='utf-8') as fh:
                lines = fh.readlines()[:10]
                for line in lines:
                    print(f'  {line.strip()}')
