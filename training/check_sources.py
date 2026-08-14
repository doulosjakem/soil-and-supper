import requests
import re

sites = [
    ('Mendeley Bangladesh', 'https://data.mendeley.com/datasets/rtx9ngb68j'),
    ('Mendeley Smartphone', 'https://data.mendeley.com/datasets/gnc4s3z2mf/3'),
    ('BanglaVeg', 'https://www.sciencedirect.com/science/article/pii/S2352340925001738'),
    ('PlantVillage', 'https://data.mendeley.com/datasets/tywbtsjrjv/1'),
    ('Roboflow', 'https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection'),
    ('Zenodo', 'https://zenodo.org/record/3675446'),
    ('PlantDoc GitHub', 'https://github.com/pratikkayal/PlantDoc-Dataset'),
    ('DeepWeeds GitHub', 'https://github.com/AlexOlsen/DeepWeeds'),
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for name, url in sites:
    try:
        resp = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        print(f'\n{name}:')
        print(f'  Status: {resp.status_code}')
        print(f'  Final URL: {resp.url}')
        print(f'  Length: {len(resp.text)}')
        
        # Look for download links
        links = re.findall(r'href="([^"]*download[^"]*)"', resp.text)
        if links:
            print(f'  Download links: {links[:3]}')
        
        # Look for .zip/.tar.gz
        archives = re.findall(r'href="([^"]*\.(zip|tar\.gz))[^"]*"', resp.text)
        if archives:
            print(f'  Archives: {archives[:3]}')
        
        # Look for Google Drive
        drive = re.findall(r'drive\.google\.com/[^"\']+', resp.text)
        if drive:
            print(f'  Google Drive: {drive[:3]}')
            
    except Exception as e:
        print(f'\n{name}: ERROR - {e}')
