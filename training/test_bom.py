import json

s = chr(0xfeff) + '{"test": 1}'
print("String repr:", repr(s[:20]))
try:
    json.loads(s)
    print("OK")
except Exception as e:
    print("Error:", e)

# Test with utf-8-sig encoding
from pathlib import Path
p = Path("D:/soil-and-supper/soil-and-supper/raw/plants_type_30class/manifest.json")
content = p.read_bytes()
print("First bytes:", content[:20])
try:
    data = json.loads(content.decode("utf-8-sig"))
    print("Decoded with utf-8-sig:", data.get("license"))
except Exception as e:
    print("Error with utf-8-sig:", e)
