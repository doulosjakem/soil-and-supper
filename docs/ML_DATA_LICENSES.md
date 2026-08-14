# Soil & Supper — ML Data Licenses

## 1. Purpose

This document maintains a provenance record for all training data used in the Soil & Supper plant identification model.

Every training image must be traceable to its source, license, and attribution requirements.

## 2. License Summary

| License | Commercial Use | ShareAlike | Attribution | Model Training OK |
|---------|---------------|------------|-------------|-------------------|
| CC0 | Yes | No | No | Yes |
| Public Domain (US Gov) | Yes | No | No | Yes |
| CC BY 4.0 | Yes | No | Yes | Yes |
| CC BY 2.0 | Yes | No | Yes | Yes |
| CC BY-SA 4.0 | Yes | Yes | Yes | Yes, but model must be shared under same license |
| CC BY-NC 4.0 | No | No | Yes | No |
| CC BY-NC-SA 4.0 | No | Yes | Yes | No |
| Custom ToS Prohibition | Varies | Varies | Varies | Only if explicitly permitted |

## 3. Approved Sources for Commercial Model Training

| Source | License | Commercial OK | Attribution Required |
|--------|---------|---------------|---------------------|
| Bangladesh Vegetables (Mendeley) | CC BY 4.0 | Yes | Yes |
| Smartphone Vegetable Detection (PMC) | CC BY 4.0 | Yes | Yes |
| USDA ARS Image Gallery | Public Domain | Yes | No |
| VegNet (Mendeley) | CC BY 4.0 | Yes | Yes |
| BanglaVeg | CC BY 4.0 | Yes | Yes |
| Early-Stage Crops (PMC) | CC BY 4.0 | Yes | Yes |

## 4. Rejected Sources

| Source | License | Reason for Rejection |
|--------|---------|---------------------|
| iNaturalist | Mixed CC BY-NC + ToS | Terms of Service explicitly prohibit commercial AI training |
| PlantCLEF 2024/2025 | CC BY-NC-SA 4.0 | Non-commercial; ShareAlike |
| Pl@ntNet | CC BY-SA | ShareAlike incompatible with proprietary app |
| Kaggle Vegetable Dataset (misrakahmed) | CC BY-SA 4.0 | ShareAlike incompatible with proprietary app |
| Oxford 102 Flowers | Unclear | License not confirmed for commercial use |

## 5. Attribution Requirements

### CC BY 4.0 Attribution Format

For each dataset used, include in the app's attribution section:

```
This app uses images from [Dataset Name] by [Authors], available at [URL] under CC BY 4.0 license.
```

### USDA ARS Attribution Format

```
Some images courtesy of the USDA Agricultural Research Service.
```

### Multiple Dataset Attribution

If multiple datasets are used, list each separately with its specific attribution.

## 6. Dataset Manifest Format

Every processed image must have a manifest entry:

```json
{
  "image_path": "data/processed/train/Tomato/DS-BD_tomato_img_0001.jpg",
  "class_name": "Tomato",
  "scientific_name": "Solanum lycopersicum",
  "source_dataset": "bangladesh_veg",
  "source_url": "https://data.mendeley.com/datasets/rtx9ngb68j",
  "license": "CC BY 4.0",
  "license_url": "https://creativecommons.org/licenses/by/4.0/",
  "attribution_required": true,
  "attribution_text": "Md JobayerAhmed et al., 2024. A Comprehensive Image Dataset of Vegetables Grown in Bangladesh. Mendeley Data. https://data.mendeley.com/datasets/rtx9ngb68j",
  "plant_part": "fruit",
  "growth_stage": "mature",
  "source_split": "train",
  "quality_status": "passed"
}
```

## 7. Source-Specific Provenance

### 7.1 Bangladesh Comprehensive Vegetables

- **Dataset ID**: bangladesh_veg
- **Name**: A Comprehensive Image Dataset of Vegetables Grown in Bangladesh
- **Authors**: Md JobayerAhmed, RatuSaha, Arpon Kishore Dutta, Mayen Uddin Mojumdar
- **Institution**: Daffodil International University
- **URL**: https://data.mendeley.com/datasets/rtx9ngb68j
- **DOI**: 10.17632/rtx9ngb68j
- **License**: CC BY 4.0
- **Published**: 2024
- **Image Count**: 4,730
- **Device**: Poco F3 smartphone
- **Attribution**: "Md JobayerAhmed et al., 2024. A Comprehensive Image Dataset of Vegetables Grown in Bangladesh. Mendeley Data. https://data.mendeley.com/datasets/rtx9ngb68j"

### 7.2 Smartphone Vegetable Detection

- **Dataset ID**: smartphone_veg
- **Name**: Smartphone-based multi-criteria vegetable object detection dataset
- **Authors**: Sabrina Jahan, Mohammad Rifat AhmmadRashid, B M ShahriaAlam, Ishraque Manzur, Tawhidur Rahman, Raiyan Gani, Karib Shams, Md MiskatHossain, MahamudulHasan
- **Institution**: East West University, Dhaka, Bangladesh
- **URL**: https://data.mendeley.com/datasets/gnc4s3z2mf/3
- **DOI**: 10.17632/gnc4s3z2mf.3
- **License**: CC BY 4.0
- **Published**: 2025
- **Article**: https://pmc.ncbi.nlm.nih.gov/articles/PMC12686877/
- **Image Count**: 3,534
- **Device**: Redmi Note 12 smartphone
- **Attribution**: "Sabrina Jahan et al., 2025. Smartphone-based multi-criteria vegetable object detection dataset. Mendeley Data. https://data.mendeley.com/datasets/gnc4s3z2mf/3"

### 7.3 USDA ARS Image Gallery

- **Dataset ID**: USDA_ARS
- **Name**: USDA ARS Image Gallery
- **Author**: USDA Agricultural Research Service
- **URL**: https://www.ars.usda.gov/oc/images/image-gallery/
- **Handle**: https://hdl.handle.net/10113/AA130
- **License**: Public Domain (US Government)
- **Published**: 2015 (ongoing)
- **Image Count**: 6,500+
- **Attribution**: "Courtesy of the USDA Agricultural Research Service." (Requested but not required)

### 7.4 VegNet

- **Dataset ID**: vegnet
- **Name**: VegNet: Dataset of vegetable quality images for machine learning applications
- **Authors**: Yogesh Suryawanshi, Kailas Patil, Prawit Chumchu
- **Institution**: Vishwakarma University, Pune, India
- **URL**: https://data.mendeley.com/datasets/6nxnjbn9w6
- **DOI**: 10.17632/6nxnjbn9w6.1
- **License**: CC BY 4.0
- **Published**: 2022
- **Article**: https://pmc.ncbi.nlm.nih.gov/articles/PMC9679474/
- **Image Count**: 6,850
- **Device**: Xiaomi Mi10T smartphone
- **Attribution**: "Yogesh Suryawanshi et al., 2022. VegNet: Dataset of vegetable quality images for machine learning applications. Mendeley Data. https://data.mendeley.com/datasets/6nxnjbn9w6"

### 7.5 BanglaVeg

- **Dataset ID**: banglaveg
- **Name**: BanglaVeg: A curated vegetable image dataset
- **Authors**: Md JobayerAhmed et al.
- **URL**: https://www.sciencedirect.com/science/article/pii/S2352340925001738
- **License**: CC BY 4.0
- **Published**: 2025
- **Article**: Data in Brief
- **Image Count**: 4,319
- **Attribution**: "Md JobayerAhmed et al., 2025. BanglaVeg: A curated vegetable image dataset. Data in Brief. https://doi.org/10.1016/j.dib.2025.xxx"

### 7.6 Early-Stage Vegetable Crops

- **Dataset ID**: early_stage_crops
- **Name**: Annotated image dataset of vegetable crops at early stage
- **Authors**: Unknown (PMC article)
- **Institution**: France
- **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/
- **PMC ID**: PMC8933512
- **License**: CC BY 4.0
- **Published**: 2022
- **Image Count**: 2,801
- **Classes**: Maize, Bean, Leek
- **Attribution**: "[Authors], 2022. Annotated image dataset of vegetable crops at early stage. PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/"

## 8. Compliance Checklist

Before training:

- [ ] Verify each dataset's license from primary source
- [ ] Confirm commercial-use compatibility
- [ ] Record attribution requirements
- [ ] Generate manifest with provenance for every image
- [ ] Exclude rejected datasets (PlantCLEF, iNaturalist, Pl@ntNet)
- [ ] Do not use CC BY-SA or CC BY-NC datasets for proprietary model
- [ ] Include attribution in app's "About" or "Licenses" section

## 9. Future Dataset Acquisition

When acquiring new datasets:

1. Verify license from primary source (dataset page, not third-party summaries).
2. Confirm commercial-use rights.
3. Check for ShareAlike or NonCommercial restrictions.
4. Record full provenance in this document.
5. Update manifest format if new metadata fields are needed.
6. Never assume a Kaggle or Mendeley license is CC0.

## 10. Revision History

- 2026-08-14: Initial license record — 6 approved sources, 5 rejected sources.
