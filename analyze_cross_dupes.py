import json
from collections import defaultdict

with open('D:/soil-and-supper/soil-and-supper/training_data/manifests/phase35i_duplicates.json', 'r') as f:
    data = json.load(f)

# Find cross-dataset duplicates
cross_dataset = []
for dup in data['duplicates']:
    datasets = set(p[0] for p in dup['paths'])
    if len(datasets) > 1:
        cross_dataset.append(dup)

print(f'Cross-dataset duplicate groups: {len(cross_dataset)}')
for dup in cross_dataset[:20]:
    print(f'\nHash: {dup["hash"][:32]}...')
    for dataset, path in dup['paths']:
        print(f'  - {dataset}: {path}')

# Also check within-dataset duplicates for plants_type datasets
print('\n=== Within-dataset duplicates ===')
for dup in data['duplicates']:
    datasets = set(p[0] for p in dup['paths'])
    if len(datasets) == 1:
        dataset = list(datasets)[0]
        if 'plants_type' in dataset:
            print(f'{dataset}: {dup["hash"][:32]}... ({len(dup["paths"])} copies)')
            if len([d for d in data['duplicates'] if set(p[0] for p in d['paths']) == datasets]) > 5:
                print('  ... and more')
                break
