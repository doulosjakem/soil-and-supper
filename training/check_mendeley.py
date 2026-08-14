import requests
import re

url = 'https://data.mendeley.com/datasets/rtx9ngb68j'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
resp = requests.get(url, headers=headers, timeout=30)
print('Status:', resp.status_code)
print('Length:', len(resp.text))

# Look for download links
links = re.findall(r'href="([^"]*download[^"]*)"', resp.text)
print('Download links:', links[:5])

# Look for file IDs
file_ids = re.findall(r'files/([a-f0-9-]+)', resp.text)
print('File IDs:', list(set(file_ids))[:5])

# Look for API endpoints
api_links = re.findall(r'/api/datasets/([^"\']+)', resp.text)
print('API links:', api_links[:5])
