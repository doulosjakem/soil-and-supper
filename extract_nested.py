import zipfile
from pathlib import Path

extracted_dir = Path(r'D:\soil-and-supper\soil-and-supper\training_data\inbox_extracted')

# Find all nested zip files
nested_zips = list(extracted_dir.rglob('*.zip'))
print(f"Found {len(nested_zips)} nested zip files")

for zip_path in nested_zips:
    # Skip if it's already at the root level (already processed)
    relative = zip_path.relative_to(extracted_dir)
    parts = relative.parts
    if len(parts) <= 2:
        print(f"Skipping root-level: {zip_path.name}")
        continue
    
    print(f"\nExtracting nested: {zip_path}")
    print(f"  Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")
    
    # Create target directory
    target_name = zip_path.name.replace('.zip', '')
    target = zip_path.parent / target_name
    if target.exists():
        print(f"  Already exists: {target}")
        continue
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(target)
        print(f"  Extracted to: {target}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\nNested extraction complete.")
