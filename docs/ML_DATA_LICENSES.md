# Soil & Supper — ML Data Licenses (Revised)

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
| CC BY 3.0 | Yes | No | Yes | Yes |
| CC BY-SA 4.0 | Yes | Yes | Yes | Yes, but model must be shared under same license |
| CC BY-NC 4.0 | No | No | Yes | No |
| CC BY-NC-SA 4.0 | No | Yes | Yes | No |
| Mixed (per-creator) | Varies | Varies | Varies | Only CC BY / CC0 / Public Domain images |
| Custom "Academic Only" | No | Varies | Yes | No |
| Unclear | Unknown | Unknown | Unknown | Do not use until clarified |

## 3. Approved Sources for Commercial Model Training

| Source | License | Commercial OK | Attribution Required | Domain |
|--------|---------|---------------|---------------------|--------|
| PlantVillage | CC0 1.0 | Yes | No | Disease |
| PlantDoc | CC BY 4.0 | Yes | Yes | Disease |
| Crop Disease Image Dataset (HF) | CC BY 4.0 | Yes | Yes | Disease |
| Bangladesh Vegetables | CC BY 4.0 | Yes | Yes | Crops |
| Smartphone Vegetable Detection | CC BY 4.0 | Yes | Yes | Crops |
| BanglaVeg | CC BY 4.0 | Yes | Yes | Crops |
| VegNet | CC BY 4.0 | Yes | Yes | Crops |
| Early-Stage Crops | CC BY 4.0 | Yes | Yes | Crops |
| DeepWeeds | CC BY 4.0 | Yes | Yes | Weeds |
| Weed-crop dataset (NDSU) | CC BY 4.0 | Yes | Yes | Weeds |
| Weed Growth Stage Dataset | CC BY 4.0 | Yes | Yes | Weeds |
| Plant Growth Stage Detection | CC BY 4.0 | Yes | Yes | Growth Stage |
| BDFlower | CC BY 4.0 | Yes | Yes | Growth Stage |
| Sunflower Growth Stage | CC BY 4.0 | Yes | Yes | Growth Stage |
| BIOSCAN-5M | CC BY 3.0 | Yes | Yes | Insects |
| images.cv Vegetables | CC0 | Yes | No | Crops |
| images.cv Insects | CC0 | Yes | No | Insects |
| Roboflow Insect Pest | CC BY 4.0 | Yes | Yes | Insects |
| USDA ARS | Public Domain | Yes | No | Crops |

## 4. Conditional / Rejected Sources

| Source | License | Status | Reason |
|--------|---------|--------|--------|
| CWD30 | Unclear (Elsevier) | REJECT until clarified | No explicit commercial-use license |
| IP102 | Academic only | REJECT until permission obtained | Contact author required for commercial use |
| Bugwood Images | Mixed (per-creator) | SUPPLEMENT with caution | Commercial use requires photographer approval per image |
| iNaturalist | Mixed + ToS | REJECT | Terms of Service prohibit commercial AI training |
| PlantCLEF 2024/2025 | CC BY-NC-SA 4.0 | REJECT | Non-commercial; ShareAlike |
| Pl@ntNet | CC BY-SA | REJECT | ShareAlike incompatible with proprietary app |
| Kaggle Vegetable (misrakahmed) | CC BY-SA 4.0 | REJECT | ShareAlike incompatible |
| Oxford 102 Flowers | Unclear | REJECT | License not confirmed |
| PlantSeg | CC BY-NC 4.0 | REJECT | Non-commercial |
| Plant Seedlings Dataset | CC BY-SA 4.0 | REJECT | ShareAlike incompatible |
| OpenPlant | Unclear | REJECT until verified | License must be confirmed on GitHub |

## 5. Attribution Requirements

### CC BY 4.0 Attribution Format

For each dataset used, include in the app's attribution section:

```
This app uses images from [Dataset Name] by [Authors], available at [URL] under CC BY 4.0 license.
```

### CC0 / Public Domain Attribution Format

No attribution required, but citation is appreciated:

```
Some images courtesy of [Source]. (Public Domain / CC0)
```

### Bugwood Attribution Format

Each image must be attributed to its specific photographer:

```
Photo by [Photographer Name] / [Organization], courtesy of Bugwood.org
```

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
  "quality_status": "passed",
  "download_date": "2026-08-14",
  "preprocessing_status": "normalized"
}
```

## 7. Source-Specific Provenance

### 7.1 PlantVillage

- **Dataset ID**: plantvillage
- **Name**: PlantVillage Dataset
- **Authors**: David P. Hughes, Marcel Salathé, Sharada Mohanty
- **Institution**: Pennsylvania State University
- **URL**: https://data.mendeley.com/datasets/tywbtsjrjv/1
- **DOI**: 10.17632/tywbtsjrjv.1
- **License**: CC0 1.0 (Public Domain)
- **Published**: 2015 (updated 2019)
- **Image Count**: 54,306
- **Classes**: 38 (14 crop species × healthy/disease)
- **Attribution**: "PlantVillage Dataset. CC0 1.0. https://data.mendeley.com/datasets/tywbtsjrjv/1"
- **Acquisition Status**: ACQUIRED — Downloaded from HuggingFace (`mohanty/PlantVillage`), archive `plantvillage_hf.zip` (verified integrity), extracted to `training_data/raw/plantvillage/color/`.
- **Verified On**: 2026-08-15

### 7.2 PlantDoc

- **Dataset ID**: plantdoc
- **Name**: PlantDoc: A Dataset for Visual Plant Disease Detection
- **Authors**: Davinder Singh, Naman Jain, Pranjali Jain, Pratik Kayal, Sudhakar Kumawat, Nipun Batra
- **Institution**: Indian Institute of Technology Gandhinagar
- **URL**: https://github.com/pratikkayal/PlantDoc-Dataset
- **DOI**: 10.1145/3371158.3371196
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Published**: 2020
- **Image Count**: 2,569 (2,572 labeled/ingested, 2,502 after deduplication)
- **Classes**: 28 (real-world field imagery, 13 disease classes + healthy)
- **Attribution**: "Singh et al., 2020. PlantDoc: A Dataset for Visual Plant Disease Detection. CoDS-COMAD 2020. https://doi.org/10.1145/3371158.3371196"
- **License Evidence**: Verified from primary `LICENSE.txt` in GitHub repository.
- **Acquisition Status**: ACQUIRED — Downloaded from GitHub, extracted to `training_data/raw/plantdoc/`.
- **Verified On**: 2026-08-14
  - LICENSE.txt fetched directly from https://raw.githubusercontent.com/pratikkayal/PlantDoc-Dataset/master/LICENSE.txt
  - GitHub repo license field: Creative Commons Attribution 4.0 International
  - Roboflow mirror: CC BY 4.0, commercial use explicitly permitted
  - DatasetNinja: CC BY 4.0
  - No ShareAlike, No NonCommercial restrictions
  - Model training and commercial distribution of weights permitted
  - Attribution must retain creator identification, copyright notice, license notice, and URI
- **Commercial Use**: PERMITTED
- **Modification/Derivative Works**: PERMITTED
- **Redistribution**: PERMITTED
- **Trained Model Distribution**: PERMITTED

### 7.3 Bangladesh Comprehensive Vegetables

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

### 7.4 Smartphone Vegetable Detection

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

### 7.6 VegNet

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

### 7.7 DeepWeeds

- **Dataset ID**: deepweeds
- **Name**: DeepWeeds: A Multiclass Weed Species Image Dataset for Deep Learning
- **Authors**: Alex Olsen, Dmitry A. Konovalov, Bronson Philippa, Peter Ridd, et al.
- **Institution**: James Cook University, Australia
- **URL**: https://github.com/AlexOlsen/DeepWeeds
- **DOI**: 10.1038/s41598-018-38343-3
- **License**: CC BY 4.0
- **Published**: 2019
- **Image Count**: 17,509
- **Attribution**: "Olsen et al., 2019. DeepWeeds: A Multiclass Weed Species Image Dataset for Deep Learning. Scientific Reports. https://doi.org/10.1038/s41598-018-38343-3"

### 7.8 Plant Growth Stage Detection

- **Dataset ID**: plant_growth_stage
- **Name**: Plant Growth Stage Detection Dataset
- **Author**: MendozaJRL
- **URL**: https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection
- **License**: CC BY 4.0
- **Published**: 2025
- **Image Count**: 7,306
- **Classes**: Flowering, Germination, Harvesting, Vegetative
- **Attribution**: "MendozaJRL, 2025. Plant Growth Stage Detection Dataset. Roboflow Universe. https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection"

### 7.9 BDFlower

- **Dataset ID**: bdflower
- **Name**: BDFlower: Growth stage flower image dataset for precision agriculture and floriculture
- **Authors**: Aritra Das, Mohammad Rifat Ahmmad Rashid, Md Rakibul Hasan, Karib Shams, Raihan Ul Islam
- **Institution**: East West University, Dhaka, Bangladesh
- **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/
- **PMC ID**: PMC13123495
- **License**: CC BY 4.0
- **Published**: 2025
- **Image Count**: 23,334 (3,889 original + augmented)
- **Classes**: 8 flowers × 3 growth stages
- **Attribution**: "Das et al., 2025. BDFlower: Growth stage flower image dataset for precision agriculture and floriculture. PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/"

### 7.10 Early-Stage Vegetable Crops

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

### 7.11 USDA ARS Image Gallery

- **Dataset ID**: USDA_ARS
- **Name**: USDA ARS Image Gallery
- **Author**: USDA Agricultural Research Service
- **URL**: https://www.ars.usda.gov/oc/images/image-gallery/
- **Handle**: https://hdl.handle.net/10113/AA130
- **License**: Public Domain (US Government)
- **Published**: 2015 (ongoing)
- **Image Count**: 6,500+
- **Attribution**: "Courtesy of the USDA Agricultural Research Service." (Requested but not required)

### 7.12 BIOSCAN-5M

- **Dataset ID**: bioscan_5m
- **Name**: BIOSCAN-5M Insect Dataset
- **Authors**: BIOSCAN Consortium (Zahra Gharaee, et al.)
- **Institution**: Centre for Biodiversity Genomics, University of Guelph
- **URL**: https://huggingface.co/datasets/bioscan-ml/BIOSCAN-5M
- **DOI**: 10.48550/arxiv.2406.12723 (NeurIPS 2024 Datasets and Benchmarks Track)
- **License**: Creative Commons Attribution 3.0 Unported (CC BY 3.0)
- **Copyright Holder**: CBG Photography Group
- **Copyright Institution**: Centre for Biodiversity Genomics
- **Photographer**: CBG Robotic Imager
- **Copyright Year**: 2021
- **Contact**: collectionsBIO@gmail.com, cbg.collections@uoguelph.ca
- **Published**: 2024
- **Image Count**: 5,150,850 specimens (2.1 GB downloaded: original_256_train split, 289,203 images)
- **Attribution**: "BIOSCAN-5M Insect Dataset. CC BY 3.0. https://huggingface.co/datasets/bioscan-ml/BIOSCAN-5M"
- **License Evidence**:
  - GitHub README explicitly states: "Copyright License: Creative Commons Attribution 3.0 Unported (CC BY 3.0)"
  - Supplementary materials (NeurIPS 2024) Table S1 confirms same license
  - No ShareAlike, No NonCommercial restrictions
  - Model training and commercial distribution of weights permitted
  - Attribution required to CBG Photography Group / Centre for Biodiversity Genomics
- **Commercial Use**: PERMITTED (with attribution)
- **Modification/Derivative Works**: PERMITTED
- **Redistribution**: PERMITTED
- **Trained Model Distribution**: PERMITTED
- **Status**: LICENSE VERIFIED but PRACTICAL SUITABILITY PENDING — see Phase 16 analysis

### 7.13 Weed-crop dataset (NDSU)

- **Dataset ID**: weed_ndsu
- **Name**: Weed-crop dataset (NDSU)
- **Authors**: North Dakota State University
- **URL**: https://data.mendeley.com/datasets/mthv4ppwyw/2
- **License**: CC BY 4.0
- **Published**: 2023
- **Image Count**: 5,000+
- **Attribution**: "NDSU Weed-crop dataset. CC BY 4.0. https://data.mendeley.com/datasets/mthv4ppwyw/2"

### 7.14 Weed Growth Stage Dataset

- **Dataset ID**: weed_growth_stage_zenodo
- **Name**: Weed Growth Stage Dataset
- **Authors**: Various
- **URL**: https://zenodo.org/records/15808623
- **License**: CC BY 4.0
- **Published**: 2025
- **Image Count**: 203,567
- **Attribution**: "Weed Growth Stage Dataset. CC BY 4.0. https://zenodo.org/records/15808623"

## 8. Compliance Checklist

Before training:

- [ ] Verify each dataset's license from primary source
- [ ] Confirm commercial-use compatibility
- [ ] Check for ShareAlike or NonCommercial restrictions
- [ ] Record full provenance in this document
- [ ] Exclude rejected datasets (PlantCLEF, iNaturalist, Pl@ntNet, Kaggle Vegetable, Oxford 102 Flowers, PlantSeg, Plant Seedlings, OpenPlant)
- [ ] Do not use CC BY-SA or CC BY-NC datasets for proprietary model
- [ ] Include attribution in app's "About" or "Licenses" section
- [ ] Track Bugwood images individually for photographer attribution
- [ ] Contact CWD30 and IP102 authors for commercial use clarification
- [ ] Verify OpenPlant license before use
- [ ] Curate BIOSCAN-5M to extract only target insect classes

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
- 2026-08-14: Revised license record — 11 approved sources, 9 rejected sources, expanded to weeds/diseases/insects/growth stages.
