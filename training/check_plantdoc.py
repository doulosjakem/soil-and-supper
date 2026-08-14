import requests
import re

url = 'https://github.com/pratikkayal/PlantDoc-Dataset'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
resp = requests.get(url, headers=headers, timeout=30)
print('Status:', resp.status_code)
print('Length:', len(resp.text))

# Look for image links
imgs = re.findall(r'href="([^"]*\.(jpg|jpeg|png))"', resp.text)
print('Image links:', len(imgs))

# Look for download links
dls = re.findall(r'href="([^"]*download[^"]*)"', resp.text)
print('Download links:', dls[:5])

# Look for dataset links
ds = re.findall(r'href="([^"]*dataset[^"]*)"', resp.text)
print('Dataset links:', ds[:5])

# Look for tree/main links (directory listings)
trees = re.findall(r'href="([^"]*/tree/main[^"]*)"', resp.text)
print('Tree links:', trees[:10])

# Look for blob links
blobs = re.findall(r'href="([^"]*/blob/main[^"]*)"', resp.text)
print('Blob links:', blobs[:10])
