import zipfile
from pathlib import Path

inbox = Path(r'D:\soil-and-supper\soil-and-supper\training_data\inbox')
extracted_dir = Path(r'D:\soil-and-supper\soil-and-supper\training_data\inbox_extracted')
last_batch = inbox / 'last batch'

for archive_path in sorted(last_batch.iterdir()):
    if not archive_path.is_file():
        continue
    if archive_path.suffix.lower() != '.zip':
        continue
    
    print(f"\nProcessing: {archive_path.name}")
    print(f"  Size: {archive_path.stat().st_size / (1024*1024):.1f} MB")
    
    safe_name = archive_path.name.replace('.zip', '').replace(' ', '_')
    safe_name = ''.join(c if c.isalnum() or c in ('-', '_') else '_' for c in safe_name)
    safe_name = safe_name.strip()[:100]
    
    target = extracted_dir / f"last_batch_{safe_name}"
    if target.exists():
        print(f"  Already extracted to {target}")
        continue
    
    try:
        with zipfile.ZipFile(archive_path, 'r') as zf:
            zf.extractall(target)
        print(f"  Extracted to: {target}")
        
        # Check for nested archives
        nested = list(target.rglob('*.zip')) + list(target.rglob('*.tar.gz')) + list(target.rglob('*.tgz'))
        if nested:
            print(f"  Found {len(nested)} nested archives")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\nLast batch extraction complete.")
