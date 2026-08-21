import zipfile
import tarfile
import os
import shutil
from pathlib import Path

inbox = Path(r'D:\soil-and-supper\soil-and-supper\training_data\inbox')
extracted_dir = Path(r'D:\soil-and-supper\soil-and-supper\training_data\inbox_extracted')
extracted_dir.mkdir(exist_ok=True)

def extract_archive(archive_path, target_dir):
    target_dir.mkdir(parents=True, exist_ok=True)
    
    if archive_path.suffix.lower() == '.zip':
        with zipfile.ZipFile(archive_path, 'r') as zf:
            # Check for nested archives
            nested = [n for n in zf.namelist() if n.endswith('.zip') or n.endswith('.tar.gz') or n.endswith('.tgz')]
            if nested:
                print(f"  Nested archives found: {nested[:3]}...")
            
            zf.extractall(target_dir)
            return True
    elif archive_path.suffix.lower() in ('.tar', '.gz', '.tgz', '.bz2'):
        mode = 'r:gz' if archive_path.suffix.lower() in ('.gz', '.tgz') else 'r:bz2' if archive_path.suffix.lower() == '.bz2' else 'r'
        with tarfile.open(archive_path, mode) as tf:
            tf.extractall(target_dir)
            return True
    else:
        return False

# Process each archive
for archive_path in sorted(inbox.rglob('*')):
    if not archive_path.is_file():
        continue
    if archive_path.suffix.lower() not in ('.zip', '.tar', '.gz', '.tgz', '.bz2', '.7z', '.rar'):
        continue
    
    print(f"\nProcessing: {archive_path.name}")
    print(f"  Size: {archive_path.stat().st_size / (1024*1024):.1f} MB")
    
    # Create extraction directory based on archive name
    safe_name = archive_path.name.replace('.zip', '').replace('.tar', '').replace('.gz', '').replace('.tgz', '')
    safe_name = ''.join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in safe_name)
    safe_name = safe_name.strip()[:100]
    
    target = extracted_dir / safe_name
    if target.exists():
        print(f"  Already extracted to {target}")
        continue
    
    try:
        success = extract_archive(archive_path, target)
        if success:
            print(f"  Extracted to: {target}")
            
            # Check for nested archives in extracted content
            nested = list(target.rglob('*.zip')) + list(target.rglob('*.tar.gz')) + list(target.rglob('*.tgz'))
            if nested:
                print(f"  Found {len(nested)} nested archives")
                for n in nested[:3]:
                    print(f"    - {n.relative_to(target)}")
        else:
            print(f"  SKIPPED: unsupported format")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n\nExtraction complete.")
