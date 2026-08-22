import json
from pathlib import Path

ledger_path = Path('training_data/manifests/phase35d_dataset_ledger.jsonl')
for line in ledger_path.read_text().splitlines():
    entry = json.loads(line)
    if entry.get('dataset_id') in ('plants_type_30class', 'plants_type_30class_alt'):
        unmapped = entry.get('unmapped_classes', [])
        mapped = entry.get('mapped_class_counts', {})
        print(f"{entry['dataset_id']}: {len(unmapped)} unmapped, {len(mapped)} mapped")
        print(f"  Mapped: {mapped}")
        print(f"  Unmapped: {sorted(set(unmapped))}")
