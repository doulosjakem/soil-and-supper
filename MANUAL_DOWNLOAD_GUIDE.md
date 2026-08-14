# Soil & Supper: Manual Dataset Acquisition Guide
## Milestone 6 Phase 2 — Verified Commercially Usable Sources

**Status:** Ready for manual download  
**Date:** 2026-08-13  
**Constraint:** No self-photography; use existing publicly available sources only  

---

## Important Notice

Automated bulk downloads are **blocked by Zenodo, Mendeley, and PMC** (HTTP 403).  
You must download these datasets manually through your browser.  
All sources below have been verified for commercial license compatibility.

---

## Tier 1: Primary Sources (Download First)

### DS-01: USDA ARS Image Gallery
- **URL:** https://www.ars.usda.gov/oc/images/image-gallery/
- **License:** Public Domain (US Government)
- **Size:** ~6,500 searchable images
- **How to download:**
  1. Open the URL in your browser
  2. Use the search box to search for each target class: "tomato", "pepper", "eggplant", "cucumber", "zucchini", "green bean", "corn", "broccoli", "carrot", "potato", "onion", "strawberry"
  3. Click each relevant image to open the detail page
  4. Click "Download" to get the high-resolution version
  5. Save to: `./raw/USDA_ARS/{class_name}/`
- **Target:** 50–200 images per class
- **Attribution:** Credit requested but not required

### DS-02: Bangladesh Comprehensive Vegetables (Mendeley)
- **URL:** https://data.mendeley.com/datasets/rtx9ngb68j
- **License:** CC BY 4.0
- **Size:** 4,730 JPG images, 42 classes
- **How to download:**
  1. Open the Mendeley page in your browser
  2. Click the "Download" button (usually top-right)
  3. Select "Download as ZIP"
  4. Extract the ZIP to: `./raw/bangladesh_veg/`
- **Relevant classes:** Tomato, Capsicum (→ Pepper), Cucumber, Eggplant (Brinjal), Broccoli, Cabbage, Carrot, Onion, Potato, Pumpkin, Radish, Zucchini, Flat Bean (→ Green Bean)
- **Attribution:** Required — see Mendeley page for citation

### DS-03: Smartphone Vegetable Detection (PMC 12686877)
- **Article:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12686877/
- **Data Repository:** https://data.mendeley.com/datasets/gnc4s3z2mf/3
- **License:** CC BY 4.0
- **Size:** 3,534 images, 22 classes
- **How to download:**
  1. Open the Mendeley data page: https://data.mendeley.com/datasets/gnc4s3z2mf/3
  2. Click "Download" → "Download all files"
  3. Extract to: `./raw/smartphone_veg/`
- **Relevant classes:** Tomato, Capsicum, Cucumber, Eggplant, Potato, Pumpkin, Radish, Green Bean
- **Attribution:** Required — see article for citation

### DS-04: Early-Stage Vegetable Crops (PMC 8933512)
- **Article:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/
- **License:** CC BY 4.0
- **Size:** 2,801 images
- **How to download:**
  1. Open the article page
  2. Look for "Supplementary Materials" or "Data Availability" section
  3. Download the dataset ZIP
  4. Extract to: `./raw/early_stage_crops/`
- **Relevant classes:** Corn (maize), Green Bean (Phaseolus vulgaris)
- **Note:** Only 3 classes but unique seedling perspective

### DS-05: OLID I — Open Leaf Image Dataset (Kaggle)
- **URL:** https://www.kaggle.com/datasets/raiaone/olid-i
- **License:** CC BY 4.0 (confirmed via article and Hugging Face)
- **Size:** 4,749 images, 57 classes, 8 crops
- **How to download:**
  1. Open Kaggle page in browser
  2. Click "Download" (requires free Kaggle account)
  3. Extract to: `./raw/olid_i/`
- **Relevant classes:** Tomato, Eggplant, Cucumber (leaf images)
- **Note:** High-resolution (3024×3024), expert-annotated, natural field conditions
- **Attribution:** Required

### DS-06: VegAnn — Vegetation Annotation Dataset (Zenodo)
- **URL:** https://zenodo.org/records/7636408
- **License:** CC BY 4.0
- **Size:** 3,775 images, 26+ crop species
- **How to download:**
  1. Open Zenodo page in browser
  2. Click "Download all files"
  3. Extract to: `./raw/vegann/`
- **Note:** Includes segmentation masks; can use images for classification
- **Attribution:** Required

---

## Tier 2: Conditional Sources (Investigate Further)

### DS-07: FloraLebanon (Scientific Data 2026)
- **URL:** https://www.nature.com/articles/s41597-026-07576-7
- **License:** TBD — must read article before use
- **Size:** 24,944 images, 102 species
- **Action:** Read article license section; download only if CC BY or CC0

### DS-08: Agri-Vision Bangladesh (Mendeley)
- **URL:** https://data.mendeley.com/datasets/8t6k37ztxc/2
- **License:** TBD — check Mendeley page
- **Size:** 28,000 images (5,266 original + augmented), 4 crops, 28 classes
- **Relevant classes:** Tomato, Zucchini, Bottle Gourd
- **Action:** Verify license on Mendeley page

---

## Directory Structure

```
soil-and-supper/
├── raw/
│   ├── USDA_ARS/              # DS-01: Manual download
│   │   ├── Tomato/
│   │   ├── Pepper/
│   │   └── ...
│   ├── bangladesh_veg/        # DS-02: Mendeley ZIP
│   ├── smartphone_veg/        # DS-03: Mendeley ZIP
│   ├── early_stage_crops/     # DS-04: PMC supplementary
│   ├── olid_i/                # DS-05: Kaggle download
│   ├── vegann/                # DS-06: Zenodo download
│   └── manifests/             # Per-dataset JSON manifests
├── curated/                   # After filtering and dedup
├── splits/                    # Train/val/test splits
├── metadata/                  # Attribution, licenses, manifests
├── dataset-plan.md            # The master plan
└── acquire_datasets_v2.py     # Download automation (limited)
```

---

## Step-by-Step Instructions

### Step 1: Create Directories
```bash
mkdir -p raw/USDA_ARS raw/bangladesh_veg raw/smartphone_veg raw/early_stage_crops raw/olid_i raw/vegann raw/manifests
mkdir -p curated splits metadata
```

### Step 2: Manual Download Priority

**Priority 1 (This Week):**
1. DS-02: Bangladesh Comprehensive Vegetables — largest single verified source (4,730 images)
2. DS-05: OLID I — 4,749 high-quality leaf images, CC BY 4.0
3. DS-03: Smartphone Vegetable Detection — 3,534 images, realistic backgrounds

**Priority 2 (Next Week):**
4. DS-06: VegAnn — 3,775 images with masks
5. DS-04: Early-Stage Crops — 2,801 seedling images
6. DS-01: USDA ARS — manual search and download

### Step 3: Verify Downloads
After downloading each dataset:
1. Check file counts match reported sizes
2. Verify directory structure
3. Open a few random images to confirm they match the class labels
4. Record any discrepancies in `metadata/acquisition_log.json`

### Step 4: License Audit
For each dataset, verify:
1. The license stated on the download page matches the dataset plan
2. No additional restrictions (NC, SA, ND) are present
3. Attribution requirements are documented

Create `metadata/license_audit.csv`:
```csv
dataset_id,dataset_name,license,attribution_required,commercial_ok,notes
DS-02,Bangladesh Comprehensive Vegetables,CC BY 4.0,Yes,Yes,Verified on Mendeley page
DS-05,OLID I,CC BY 4.0,Yes,Yes,Verified via article + Kaggle
...
```

---

## Automation Status

| Dataset | Automated Download | Reason |
|---------|-------------------|--------|
| DS-01 USDA ARS | ❌ Manual only | Requires web search and individual image download |
| DS-02 Bangladesh | ❌ Blocked | Mendeley returns 403 to programmatic requests |
| DS-03 Smartphone Veg | ❌ Blocked | Mendeley returns 403 to programmatic requests |
| DS-04 Early-Stage | ❌ Blocked | PMC supplementary not in scrapable HTML |
| DS-05 OLID I (Zenodo) | ❌ Blocked | Zenodo API returns 403 |
| DS-05 OLID I (Kaggle) | ❌ No API key | Kaggle API not configured |
| DS-06 VegAnn (Zenodo) | ❌ Blocked | Zenodo API returns 403 |

**All Tier 1 datasets require manual browser download.** The scripts in this repository provide structure and documentation only.

---

## Next Steps After Download

1. Run `python curate_datasets.py` (to be created) to:
   - Map source class names to target classes
   - Remove duplicates (perceptual hash)
   - Filter by image quality (blur, exposure)
   - Generate train/val/test splits

2. Review `curated/` directory for class balance

3. Approve dataset before training (Gate C)

---

## Questions?

If you encounter issues downloading any dataset:
1. Check the dataset's official page for updated URLs
2. Verify the license has not changed
3. Document the issue in `metadata/acquisition_log.json`

**Do not proceed to training until all Tier 1 datasets are downloaded and verified.**
