#!/usr/bin/env python3
"""
License audit and attribution generator for Soil & Supper dataset.
Run this after curate_datasets.py to verify licensing compliance.
"""

import json
import csv
from pathlib import Path
from datetime import datetime

METADATA_DIR = Path("./metadata")
METADATA_DIR.mkdir(exist_ok=True)

# Known dataset licenses (verified from primary sources)
DATASET_LICENSES = {
    "bangladesh_veg": {
        "name": "A Comprehensive Image Dataset of Vegetables Grown in Bangladesh",
        "license": "CC BY 4.0",
        "doi": "10.17632/rtx9ngb68j",
        "attribution_required": True,
        "commercial_ok": True,
        "source_url": "https://data.mendeley.com/datasets/rtx9ngb68j",
        "notes": "Original collection by authors using Poco F3 smartphone. Peer-reviewed."
    },
    "smartphone_veg": {
        "name": "Smartphone-based multi-criteria vegetable object detection dataset",
        "license": "CC BY 4.0",
        "doi": "10.17632/gnc4s3z2mf.3",
        "attribution_required": True,
        "commercial_ok": True,
        "source_url": "https://data.mendeley.com/datasets/gnc4s3z2mf/3",
        "notes": "Original collection using Redmi Note 12. Annotated with Roboflow."
    },
    "early_stage_crops": {
        "name": "Annotated image dataset of vegetable crops at early stage",
        "license": "CC BY 4.0",
        "pmc_id": "PMC8933512",
        "attribution_required": True,
        "commercial_ok": True,
        "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/",
        "notes": "Original collection in France. Only maize, bean, leek."
    },
    "olid_i": {
        "name": "OLID I: An Open Leaf Image Dataset of Bangladesh's Major Crops",
        "license": "CC BY 4.0",
        "doi": "10.5281/zenodo.8105154",
        "attribution_required": True,
        "commercial_ok": True,
        "source_url": "https://www.kaggle.com/datasets/raiaone/olid-i",
        "notes": "Expert-annotated leaf images. High resolution (3024x3024)."
    },
    "USDA_ARS": {
        "name": "USDA ARS Image Gallery",
        "license": "Public Domain (US Government)",
        "attribution_required": False,
        "commercial_ok": True,
        "source_url": "https://www.ars.usda.gov/oc/images/image-gallery/",
        "notes": "Professional USDA photography. Credit requested but not required."
    }
}

def generate_license_audit():
    """Generate license audit CSV."""
    print("=" * 60)
    print("LICENSE AUDIT")
    print("=" * 60)
    
    audit_path = METADATA_DIR / "license_audit.csv"
    
    with open(audit_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "dataset_id", "dataset_name", "license", "commercial_ok",
            "attribution_required", "source_url", "doi", "notes"
        ])
        
        for ds_id, info in DATASET_LICENSES.items():
            writer.writerow([
                ds_id,
                info["name"],
                info["license"],
                "Yes" if info.get("commercial_ok", False) else "No",
                "Yes" if info.get("attribution_required", False) else "No",
                info.get("source_url", ""),
                info.get("doi", info.get("pmc_id", "")),
                info.get("notes", "")
            ])
    
    print(f"Saved license audit: {audit_path}")

def generate_attribution_file():
    """Generate ATTRIBUTION.md with full attribution text."""
    print("\nGenerating ATTRIBUTION.md...")
    
    lines = [
        "# Dataset Attribution",
        "",
        "This dataset is compiled from the following sources:",
        ""
    ]
    
    for ds_id, info in DATASET_LICENSES.items():
        lines.append(f"## {info['name']}")
        lines.append(f"")
        lines.append(f"- **License:** {info['license']}")
        lines.append(f"- **Source:** {info.get('source_url', 'N/A')}")
        if info.get("doi"):
            lines.append(f"- **DOI:** {info['doi']}")
        if info.get("pmc_id"):
            lines.append(f"- **PMC ID:** {info['pmc_id']}")
        lines.append(f"- **Attribution Required:** {'Yes' if info.get('attribution_required') else 'No'}")
        lines.append(f"")
        
        if info.get("attribution_required"):
            lines.append(f"**Attribution text:**")
            lines.append(f"")
            if ds_id == "bangladesh_veg":
                lines.append(f"> A Comprehensive Image Dataset of Vegetables Grown in Bangladesh. Authors et al., 2025. CC BY 4.0. https://data.mendeley.com/datasets/rtx9ngb68j")
            elif ds_id == "smartphone_veg":
                lines.append(f"> Smartphone-based multi-criteria vegetable object detection dataset. Authors et al., 2025. CC BY 4.0. https://data.mendeley.com/datasets/gnc4s3z2mf/3")
            elif ds_id == "early_stage_crops":
                lines.append(f"> Annotated image dataset of vegetable crops at early stage. Authors et al., 2022. CC BY 4.0. https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/")
            elif ds_id == "olid_i":
                lines.append(f"> OLID I: An Open Leaf Image Dataset of Bangladesh's Major Crops. Orka et al., 2023. CC BY 4.0. https://www.kaggle.com/datasets/raiaone/olid-i")
            elif ds_id == "USDA_ARS":
                lines.append(f"> USDA Agricultural Research Service Image Gallery. Public Domain.")
            lines.append(f"")
    
    attribution_path = METADATA_DIR / "ATTRIBUTION.md"
    with open(attribution_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"Saved attribution: {attribution_path}")

def generate_license_summary():
    """Generate LICENSE_SUMMARY.md."""
    print("\nGenerating LICENSE_SUMMARY.md...")
    
    lines = [
        "# License Summary",
        "",
        "## Overall License Mix",
        "",
        "| License | % of Dataset | Commercial Use | Model Redistribution | Attribution |",
        "|---------|--------------|----------------|---------------------|-------------|"
    ]
    
    # Placeholder percentages - update after curation
    lines.extend([
        "| CC0 / Public Domain | TBD | ✅ Yes | ✅ Any license | No |",
        "| CC BY 4.0 | TBD | ✅ Yes | ✅ Any license | **Yes — mandatory** |",
        "| CC BY-SA 4.0 | 0% | ⚠️ Risky | ⚠️ Likely SA required | Yes |",
        "",
        "## Compliance Requirements",
        "",
        "1. **CC BY 4.0 sources:** Include attribution in app 'About' screen and model card",
        "2. **Public Domain sources:** No attribution required (courtesy only)",
        "3. **Model distribution:** Do NOT distribute model under CC BY-SA unless SA sources are used",
        "4. **App bundling:** Core ML model bundled in proprietary app is permissible under CC BY",
        "",
        "## Restrictions",
        "",
        "- **Do NOT use:** iNaturalist, PlantCLEF, PlantVillage, Fruits-360 (CC BY-SA)",
        "- **Do NOT use:** PlantWild (CC BY-NC-ND), Open Images (unverifiable per-image licenses)",
        "- **Do NOT use:** Any dataset without clear provenance documentation",
        ""
    ])
    
    summary_path = METADATA_DIR / "LICENSE_SUMMARY.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"Saved license summary: {summary_path}")

def main():
    print("=" * 60)
    print("LICENSE AUDIT AND ATTRIBUTION GENERATOR")
    print("=" * 60)
    print(f"Started: {datetime.now().isoformat()}")
    
    generate_license_audit()
    generate_attribution_file()
    generate_license_summary()
    
    print("\n" + "=" * 60)
    print("LICENSE AUDIT COMPLETE")
    print("=" * 60)
    print("\nReview the following files:")
    print(f"  - metadata/license_audit.csv")
    print(f"  - metadata/ATTRIBUTION.md")
    print(f"  - metadata/LICENSE_SUMMARY.md")

if __name__ == "__main__":
    main()
