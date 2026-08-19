# Phase 34C — Human Dataset Acquisition Instructions

## Priority 1 Datasets (Manual Download Required)

All five Priority 1 datasets require manual download because direct automated access is blocked (Mendeley returns 403; PMC requires account/supplementary file navigation).

---

### 1. Bangladesh Comprehensive Vegetables

**DATASET NAME:** Bangladesh Comprehensive Vegetables  
**PRIMARY SOURCE:** Mendeley Data  
**DOWNLOAD PAGE:** https://data.mendeley.com/datasets/rtx9ngb68j  
**LICENSE:** CC BY 4.0  
**CLASSES NEEDED:** Tomato, Capsicum (→ Pepper), Cucumber, Brinjal (→ Eggplant), Broccoli, Cabbage, Carrot, Onion, Potato, Pumpkin (→ Winter Squash/Pumpkin), Radish, Zucchini (→ Summer Squash), Flat Bean (→ Bean)  
**EXPECTED IMAGE COUNT:** ~4,730  
**FILE FORMAT:** ZIP archive containing image folders  
**EXPECTED DOWNLOAD SIZE:** ~200-500 MB  
**WHY IT IS NEEDED:** Fills 13 Tier 1 class gaps with the single largest manual-download dataset.  

**ACQUISITION INSTRUCTIONS:**
1. Open https://data.mendeley.com/datasets/rtx9ngb68j in a browser
2. Sign in to Mendeley (free account) or create one
3. Click the "Download" button
4. Save the ZIP file to `D:\soil-and-supper\soil-and-supper\training_data\raw\bangladesh_veg\`
5. Extract the archive
6. Notify Kilo when complete for processing

---

### 2. Smartphone Vegetable Detection

**DATASET NAME:** Smartphone Vegetable Detection  
**PRIMARY SOURCE:** Mendeley Data  
**DOWNLOAD PAGE:** https://data.mendeley.com/datasets/gnc4s3z2mf/3  
**LICENSE:** CC BY 4.0  
**CLASSES NEEDED:** Tomato, Capsicum (→ Pepper), Cucumber, Eggplant, Potato, Pumpkin (→ Winter Squash/Pumpkin), Radish, Green Bean (→ Bean), Carrot, Onion  
**EXPECTED IMAGE COUNT:** ~3,534  
**FILE FORMAT:** ZIP archive  
**EXPECTED DOWNLOAD SIZE:** ~150-400 MB  
**WHY IT IS NEEDED:** Smartphone-captured images from real field conditions. Critical for domain diversity.  

**ACQUISITION INSTRUCTIONS:**
1. Open https://data.mendeley.com/datasets/gnc4s3z2mf/3 in a browser
2. Sign in to Mendeley (free account) or create one
3. Click the "Download" button
4. Save the ZIP file to `D:\soil-and-supper\soil-and-supper\training_data\raw\smartphone_veg\`
5. Extract the archive
6. Notify Kilo when complete for processing

---

### 3. VegNet Vegetable Quality Dataset

**DATASET NAME:** VegNet Vegetable Quality Dataset  
**PRIMARY SOURCE:** Mendeley Data  
**DOWNLOAD PAGE:** https://data.mendeley.com/datasets/6nxnjbn9w6  
**LICENSE:** CC BY 4.0  
**CLASSES NEEDED:** Bell Pepper (→ Pepper), Tomato, Chili Pepper (→ Pepper), New Mexico Chile (→ Pepper)  
**EXPECTED IMAGE COUNT:** ~6,850  
**FILE FORMAT:** ZIP archive  
**EXPECTED DOWNLOAD SIZE:** ~300-800 MB  
**WHY IT IS NEEDED:** Large pepper-focused dataset. Critical for Pepper class which has high data needs.  

**ACQUISITION INSTRUCTIONS:**
1. Open https://data.mendeley.com/datasets/6nxnjbn9w6 in a browser
2. Sign in to Mendeley (free account) or create one
3. Click the "Download" button
4. Save the ZIP file to `D:\soil-and-supper\soil-and-supper\training_data\raw\vegnet\`
5. Extract the archive
6. Notify Kilo when complete for processing

---

### 4. BanglaVeg

**DATASET NAME:** BanglaVeg  
**PRIMARY SOURCE:** Mendeley Data / ScienceDirect  
**DOWNLOAD PAGE:** https://www.sciencedirect.com/science/article/pii/S2352340925001738  
**LICENSE:** CC BY 4.0  
**CLASSES NEEDED:** Tomato, Capsicum (→ Pepper), Cucumber, Eggplant, Potato, Onion, Radish, Bean, Chilli (→ Pepper)  
**EXPECTED IMAGE COUNT:** ~4,319  
**FILE FORMAT:** ZIP archive or supplementary files  
**EXPECTED DOWNLOAD SIZE:** ~200-500 MB  
**WHY IT IS NEEDED:** Bengali vegetable dataset with smartphone-captured images. Good field-image diversity.  

**ACQUISITION INSTRUCTIONS:**
1. Open https://www.sciencedirect.com/science/article/pii/S2352340925001738 in a browser
2. Look for "Download supplementary files" or "Data availability" section
3. Sign in if required (institutional access may be needed; the dataset itself is CC BY 4.0)
4. Download the dataset ZIP
5. Save to `D:\soil-and-supper\soil-and-supper\training_data\raw\banglaveg\`
6. Extract the archive
7. Notify Kilo when complete for processing

**NOTE:** If institutional access is required and unavailable, skip this dataset and rely on the other 4 Priority 1 sources.

---

### 5. Early-Stage Vegetable Crops

**DATASET NAME:** Early-Stage Vegetable Crops  
**PRIMARY SOURCE:** PMC / PubMed Central  
**DOWNLOAD PAGE:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/  
**LICENSE:** CC BY 4.0  
**CLASSES NEEDED:** Maize (→ Corn), Bean, Leek  
**EXPECTED IMAGE COUNT:** ~2,801  
**FILE FORMAT:** ZIP archive (supplementary materials)  
**EXPECTED DOWNLOAD SIZE:** ~100-300 MB  
**WHY IT IS NEEDED:** Provides Bean and Leek images which have no other verified commercial source.  

**ACQUISITION INSTRUCTIONS:**
1. Open https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/ in a browser
2. Scroll to the "Supplementary Materials" or "Data Availability" section
3. Look for a ZIP file link (typically named like "supplementary_files.zip" or similar)
4. Download the ZIP file
5. Save to `D:\soil-and-supper\soil-and-supper\training_data\raw\early_stage_crops\`
6. Extract the archive
7. Notify Kilo when complete for processing

**NOTE:** If supplementary files are not visible on the article page, try:
- Clicking "PMC Article" link to view the full article
- Looking for a direct download link in the article text
- Searching PMC for "PMC8933512 supplementary"

---

## Summary for Human

**Total datasets to download:** 5  
**Total expected images:** ~22,000  
**Total expected download size:** ~1-2 GB  
**Storage location:** `D:\soil-and-supper\soil-and-supper\training_data\raw\`  

**Accounts needed:**
- Mendeley Data (free) — for datasets 1, 2, 3
- ScienceDirect / institutional access — for dataset 4 (may require university/library login)
- PMC (free) — for dataset 5

**After downloading all 5 datasets:**
1. Place each extracted folder in the corresponding `raw/` subdirectory
2. Notify Kilo
3. Kilo will process, validate, deduplicate, and integrate into commercial manifests

**Do not download any datasets with unclear licenses (images.cv, Kaggle) until CC0 claims are verified.**
