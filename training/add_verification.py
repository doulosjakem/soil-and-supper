#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

manifest_path = Path('training_data/manifests/license_verification.jsonl')

records = [
    {
        'dataset_id': 'diamos_plant',
        'name': 'DiaMOS Plant Dataset',
        'url': 'https://zenodo.org/records/5557313',
        'license_type': 'CC BY 4.0',
        'license_url': 'https://creativecommons.org/licenses/by/4.0/',
        'commercial_use': True,
        'ml_training_permitted': True,
        'attribution_required': True,
        'share_alike': False,
        'non_commercial': False,
        'no_derivatives': False,
        'tos_restrictions': '',
        'verification_source': 'Zenodo dataset page + OpenAIRE + peer-reviewed paper (Agronomy 2021, 11, 2107)',
        'verification_notes': 'Zenodo record explicitly lists CC BY 4.0 license. OpenAIRE confirms CC BY. Paper states dataset is freely available. DOI: 10.5281/zenodo.5557313. Authors: Gianni Fenu, Francesca Maridina Malloci (University of Cagliari). 3,505 images (3,006 leaf + 499 fruit). Field-collected pear orchard, Sardegna, Italy. Honor 6x smartphone + Canon EOS 60D DSLR. Published October 2021.',
        'status': 'APPROVED',
        'issues': []
    },
    {
        'dataset_id': 'fieldplant',
        'name': 'FieldPlant',
        'url': 'https://universe.roboflow.com/plant-disease-detection/fieldplant',
        'license_type': 'CC BY 4.0',
        'license_url': 'https://creativecommons.org/licenses/by/4.0/',
        'commercial_use': True,
        'ml_training_permitted': True,
        'attribution_required': True,
        'share_alike': False,
        'non_commercial': False,
        'no_derivatives': False,
        'tos_restrictions': '',
        'verification_source': 'Roboflow Universe dataset page + IEEE Access paper (2023) + Kaggle dataset page',
        'verification_notes': 'Roboflow Universe explicitly lists CC BY 4.0 license. data.yaml confirms license: CC BY 4.0. IEEE Access paper (DOI: 10.1109/ACCESS.2023.3263042) is open access under CC BY 4.0. Authors: Emmanuel Moupojou et al. 5,170 images collected from Cameroon plantations. Smartphone cameras (4608x3456). Expert annotation by plant pathologists. Published March 2023.',
        'status': 'APPROVED',
        'issues': []
    }
]

for record in records:
    record['verification_date'] = datetime.now().isoformat()
    with open(manifest_path, 'a') as f:
        f.write(json.dumps(record) + '\n')
    print(f"Added {record['dataset_id']} license verification record")
