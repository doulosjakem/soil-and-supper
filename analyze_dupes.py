import json
from collections import Counter

with open('D:/soil-and-supper/soil-and-supper/training_data/manifests/phase35i_duplicates.json', 'r') as f:
    data = json.load(f)

print(f'Total duplicate groups: {data["duplicate_groups"]}')
print(f'Total hashes: {data["total_hashes"]}')

dataset_counts = Counter()
for dup in data['duplicates']:
    for path in dup['paths']:
        dataset = path[0]
        dataset_counts[dataset] += 1

for ds, count in dataset_counts.most_common():
    print(f'  {ds}: {count} duplicate occurrences')

# Count unique duplicate images per dataset
unique_dupes = Counter()
for dup in data['duplicates']:
    datasets_involved = set(p[0] for p in dup['paths'])
    for ds in datasets_involved:
        unique_dupes[ds] += 1

print()
print('Unique duplicate images per dataset:')
for ds, count in unique_dupes.most_common():
    print(f'  {ds}: {count}')
