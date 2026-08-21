import json

with open(r'D:\soil-and-supper\soil-and-supper\training_data\manifests\phase35d_dataset_ledger.jsonl') as f:
    for line in f:
        entry = json.loads(line.strip())
        if 'inbox' in entry.get('dataset_id', ''):
            print(f"Dataset: {entry['dataset_id']}")
            print(f"Status: {entry['status']}")
            print(f"License: {entry.get('license', 'unknown')}")
            print(f"Errors: {entry.get('errors', [])}")
            print()
