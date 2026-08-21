import zipfile
import tarfile
import os
from pathlib import Path

inbox = Path(r'D:\soil-and-supper\soil-and-supper\training_data\inbox')

for archive_path in sorted(inbox.rglob('*')):
    if archive_path.is_file() and archive_path.suffix.lower() in ('.zip', '.tar', '.gz', '.tgz', '.bz2', '.7z', '.rar'):
        print(f"\n{'='*80}")
        print(f"ARCHIVE: {archive_path.name}")
        print(f"SIZE: {archive_path.stat().st_size / (1024*1024):.1f} MB")
        print(f"TYPE: {archive_path.suffix.lower()}")
        
        try:
            if archive_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    namelist = zf.namelist()
                    print(f"TOTAL ITEMS: {len(namelist)}")
                    images = [n for n in namelist if any(n.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tif', '.tiff'])]
                    print(f"IMAGES: {len(images)}")
                    print(f"SAMPLE FILES (first 10):")
                    for n in namelist[:10]:
                        print(f"  {n}")
                    if len(namelist) > 10:
                        print(f"  ... and {len(namelist)-10} more")
                    
                    # Check for README/LICENSE
                    readmes = [n for n in namelist if 'readme' in n.lower() or 'license' in n.lower()]
                    if readmes:
                        print(f"README/LICENSE FILES:")
                        for r in readmes[:5]:
                            print(f"  {r}")
            
            elif archive_path.suffix.lower() in ('.tar', '.gz', '.tgz', '.bz2'):
                mode = 'r:gz' if archive_path.suffix.lower() in ('.gz', '.tgz') else 'r:bz2' if archive_path.suffix.lower() == '.bz2' else 'r'
                with tarfile.open(archive_path, mode) as tf:
                    namelist = tf.getnames()
                    print(f"TOTAL ITEMS: {len(namelist)}")
                    images = [n for n in namelist if any(n.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tif', '.tiff'])]
                    print(f"IMAGES: {len(images)}")
                    print(f"SAMPLE FILES (first 10):")
                    for n in namelist[:10]:
                        print(f"  {n}")
                    if len(namelist) > 10:
                        print(f"  ... and {len(namelist)-10} more")
                    
                    readmes = [n for n in namelist if 'readme' in n.lower() or 'license' in n.lower()]
                    if readmes:
                        print(f"README/LICENSE FILES:")
                        for r in readmes[:5]:
                            print(f"  {r}")
        except Exception as e:
            print(f"ERROR: {e}")
