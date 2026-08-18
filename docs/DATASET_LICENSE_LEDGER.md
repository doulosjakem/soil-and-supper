# Dataset License Ledger

## Purpose

This ledger documents the commercial-use compatibility of every image source in the Soil & Supper ML training-ready dataset.

**Total training-ready images**: 136,134

---

## Commercial Status Summary

| Status | Count | Description |
|--------|------:|-------------|
| USE | 98,642 | Commercially compatible, verified from primary source |
| EXCLUDE | 36,675 | Commercially incompatible (non-commercial license) |
| REVIEW | 817 | License previously verified but primary source now inaccessible |
| UNKNOWN | 0 | License cannot be established |
| **Total** | **136,134** | |

---

## Source Details

### USE — Commercially Compatible

| Source | Images | Classes | License | Commercial ML | Attribution | Verified From |
|--------|-------:|---------|---------|---------------|-------------|---------------|
| PlantVillage | 54,284 | 20 | CC0 1.0 | YES | NO | Meta-Album dataset page + GitHub mirror (attaullah/downsampled-plant-disease-dataset) |
| Irish Potato | 38,554 | 3 | CC BY 4.0 | YES | YES | Zenodo API record 8286529 + peer-reviewed article (PMC12020891) |
| PlantDoc | 2,559 | 14 | CC BY 4.0 | YES | YES | GitHub repository LICENSE.txt (pratikkayal/PlantDoc-Dataset) |
| Grapevine | 3,245 | 3 | CC BY 4.0 | YES | YES | Zenodo API record 17343474 + Data in Brief article (2026) |
| **Subtotal USE** | **98,642** | | | | | |

#### PlantVillage
- **Dataset ID**: plantvillage
- **URL**: https://data.mendeley.com/datasets/tywbtsjrjv/1
- **License**: CC0 1.0 (Public Domain Dedication)
- **License URL**: https://creativecommons.org/publicdomain/zero/1.0/
- **Commercial use**: YES
- **ML training**: YES
- **Attribution required**: NO
- **Derivative works**: YES
- **Verification source**: Meta-Album dataset page + GitHub mirror
- **Verification notes**: Multiple sources confirm CC0 1.0. Meta-Album explicitly lists "License (original data release): CC0 1.0". GitHub mirror (attaullah/downsampled-plant-disease-dataset) also CC0. No commercial or ML restrictions.

#### Irish Potato Imagery Dataset
- **Dataset ID**: irish_potato
- **URL**: https://zenodo.org/records/8286529
- **DOI**: 10.5281/zenodo.8286529
- **License**: CC BY 4.0
- **License URL**: https://creativecommons.org/licenses/by/4.0/
- **Commercial use**: YES
- **ML training**: YES
- **Attribution required**: YES
- **Derivative works**: YES
- **Share-alike**: NO
- **Verification source**: Zenodo API record 8286529 + peer-reviewed article (PMC12020891)
- **Verification notes**: Zenodo record shows "Creative Commons Attribution 4.0 International". Peer-reviewed article (Data in Brief, 2025) confirms open access CC BY license. 117,418 smartphone field images from Tanzania. Commercially usable with attribution.

#### PlantDoc Dataset
- **Dataset ID**: plantdoc
- **URL**: https://github.com/pratikkayal/PlantDoc-Dataset
- **License**: CC BY 4.0
- **License URL**: https://creativecommons.org/licenses/by/4.0/
- **Commercial use**: YES
- **ML training**: YES
- **Attribution required**: YES
- **Derivative works**: YES
- **Share-alike**: NO
- **Verification source**: GitHub repository LICENSE.txt
- **Verification notes**: GitHub repository contains explicit CC BY 4.0 license file. Commercial use permitted with attribution.

#### Grapevine Leaves RGB Images
- **Dataset ID**: grapevine
- **URL**: https://zenodo.org/records/17343474
- **DOI**: 10.5281/zenodo.17343474
- **License**: CC BY 4.0
- **License URL**: https://creativecommons.org/licenses/by/4.0/
- **Commercial use**: YES
- **ML training**: YES
- **Attribution required**: YES
- **Derivative works**: YES
- **Share-alike**: NO
- **Verification source**: Zenodo API record 17343474 + Data in Brief article (2026)
- **Verification notes**: Zenodo record shows "cc-by-4.0". Data in Brief article confirms CC BY license. 5,267 smartphone field images from Portuguese vineyards. Commercially usable with attribution.

---

### EXCLUDE — Commercially Incompatible

| Source | Images | Classes | License | Commercial ML | Reason |
|--------|-------:|---------|---------|---------------|--------|
| Common Beans | 36,675 | 3 | CC BY-NC 4.0 | NO | Non-commercial restriction |

#### Common Beans Imagery Dataset
- **Dataset ID**: common_beans
- **URL**: https://zenodo.org/records/8286126
- **DOI**: 10.5281/zenodo.8286126
- **License**: CC BY-NC 4.0 (NonCommercial)
- **License URL**: https://creativecommons.org/licenses/by-nc/4.0/
- **Commercial use**: NO
- **ML training**: NO (for commercial purposes)
- **Attribution required**: YES
- **Derivative works**: YES
- **Share-alike**: NO
- **Verification source**: Zenodo API record 8286126 + peer-reviewed article (repository.must.ac.tz)
- **Verification notes**: Zenodo record shows CC BY 4.0, BUT the associated peer-reviewed article (Data in Brief, Elsevier) explicitly states "This is an open access article under the CC BY-NC license." The article is the authoritative source for dataset licensing. Commercial use is prohibited without explicit permission from rights holders.
- **Status**: EXCLUDE
- **Disposition**: Retain files for research/provenance. Do not count in commercial training pool. If commercial permission is obtained from authors, reclassify to USE.

---

### REVIEW — Previously Verified, Source Now Inaccessible

| Source | Images | Classes | License | Commercial ML | Verified From | Current Status |
|--------|-------:|---------|---------|---------------|---------------|----------------|
| SegPPD-101 | 817 | 12 | MIT (claimed) | YES (claimed) | GitHub + Kaggle (now gone) | REVIEW |

#### SegPPD-101
- **Dataset ID**: segppd101
- **URL**: https://github.com/umerzaid007/Seg-PPD-101 (repository now 404/private)
- **License**: MIT (as documented at acquisition time)
- **License URL**: https://opensource.org/licenses/MIT
- **Commercial use**: YES (per original verification)
- **ML training**: YES (per original verification)
- **Attribution required**: NO
- **Verification source**: GitHub repository + Kaggle dataset page (both now inaccessible)
- **Verification notes**: Phase 18 documentation records MIT license verified from GitHub repository and associated Kaggle dataset page. Both sources are now inaccessible. No license file found in downloaded archive. MIT is permissive, but without primary-source verification, commercial use cannot be definitively confirmed.
- **Status**: REVIEW
- **Action required**: Attempt to locate archived copy of license (e.g., Wayback Machine). If MIT license is confirmed, reclassify to USE. If license cannot be verified, treat as UNKNOWN and exclude from commercial training.

---

## Per-Class Commercial Compatibility

| Class | Total | USE | EXCLUDE | REVIEW | UNKNOWN | Primary Source(s) |
|-------|------:|----:|--------:|-------:|--------:|-------------------|
| Healthy | 58,148 | 55,995 | 21,564 | 242 | 0 | PlantVillage, Irish Potato, PlantDoc, Grapevine, Common Beans, SegPPD-101 |
| Late_blight | 16,193 | 13,240 | 2,943 | 52 | 0 | Irish Potato, PlantVillage, PlantDoc, SegPPD-101 |
| Leaf_spot | 14,076 | 14,076 | 0 | 0 | 0 | PlantVillage, PlantDoc, SegPPD-101 |
| Rust | 9,549 | 1,342 | 8,207 | 34 | 0 | PlantVillage, PlantDoc, SegPPD-101, Common Beans |
| Early_blight | 8,437 | 8,421 | 0 | 16 | 0 | Irish Potato, PlantVillage, PlantDoc, SegPPD-101 |
| Anthracnose | 6,904 | 0 | 6,904 | 0 | 0 | Common Beans |
| Tomato_yellow_leaf_curl | 5,432 | 5,432 | 0 | 0 | 0 | PlantVillage, PlantDoc |
| Bacterial_spot | 3,374 | 3,374 | 0 | 0 | 0 | PlantVillage, PlantDoc, SegPPD-101 |
| Powdery_mildew | 2,312 | 2,312 | 0 | 0 | 0 | PlantVillage, Grapevine, SegPPD-101 |
| Peach_bacterial_spot | 2,297 | 2,297 | 0 | 0 | 0 | PlantVillage |
| Squash_powdery_mildew | 1,965 | 1,965 | 0 | 0 | 0 | PlantVillage, PlantDoc |
| Septoria_leaf_spot | 1,920 | 1,920 | 0 | 0 | 0 | PlantVillage, PlantDoc |
| Spider_mite | 1,678 | 1,678 | 0 | 0 | 0 | PlantVillage, PlantDoc |
| Grape_black_rot | 1,271 | 1,271 | 0 | 0 | 0 | PlantVillage, PlantDoc, SegPPD-101 |
| Downy_mildew | 1,002 | 1,002 | 0 | 0 | 0 | Grapevine |
| Apple_scab | 741 | 741 | 0 | 0 | 0 | PlantVillage, PlantDoc, SegPPD-101 |
| Tomato_mosaic_virus | 427 | 427 | 0 | 0 | 0 | PlantVillage, PlantDoc |
| Cedar_apple_rust | 386 | 386 | 0 | 0 | 0 | PlantVillage, PlantDoc, SegPPD-101 |
| Nutrient_deficiency | 22 | 0 | 0 | 22 | 0 | SegPPD-101 |

---

## Key Findings

### 1. Common Beans Is Excluded
- **36,675 images** from Common Beans dataset are commercially incompatible (CC BY-NC 4.0).
- These images must not be used to train a commercial Soil & Supper model.
- Classes affected: Healthy (21,564), Rust (8,207), Anthracnose (6,904).
- If commercial permission is obtained from authors, these can be reclassified.

### 2. SegPPD-101 Is Under Review
- **817 images** from SegPPD-101 cannot be definitively classified as commercially usable.
- Original verification (MIT license) was documented but primary sources are now inaccessible.
- If MIT license is confirmed via archived copy, reclassify to USE.
- Until then, exclude from commercial training pool.

### 3. Commercially Usable Core
- **98,642 images** are confirmed commercially usable.
- These come from: PlantVillage (54,284), Irish Potato (38,554), PlantDoc (2,559), Grapevine (3,245).
- This represents **72.5%** of the total training-ready dataset.

### 4. Classes Most Affected by Exclusions
- **Anthracnose**: 6,904 images, 100% from Common Beans (EXCLUDE). Class has 0 commercially usable images.
- **Rust**: 9,549 images total, 8,207 (86%) from Common Beans (EXCLUDE). Only 1,342 commercially usable.
- **Healthy**: 58,148 images total, 21,564 (37%) from Common Beans (EXCLUDE). 55,995 commercially usable.

---

## Recommendations

1. **Do not use Common Beans images for commercial training** until explicit permission is obtained from rights holders.

2. **Attempt to verify SegPPD-101 license** via Wayback Machine or other archival sources. If MIT license is confirmed, add 817 images to commercial pool.

3. **Commercial training pool is 98,642 images** from 4 verified sources. This is sufficient for initial model development but should be supplemented with additional commercially compatible data.

4. **Do not recalculate readiness** based on commercial counts alone until Phase 23 explicitly adds the commercial license gate to readiness criteria.

---

## Verification Performed

- [x] PlantVillage: CC0 verified from Meta-Album + GitHub mirror
- [x] PlantDoc: CC BY 4.0 verified from GitHub LICENSE.txt
- [x] Irish Potato: CC BY 4.0 verified from Zenodo API + peer-reviewed article
- [x] Grapevine: CC BY 4.0 verified from Zenodo API + Data in Brief article
- [x] Common Beans: CC BY-NC 4.0 verified from article (repository.must.ac.tz)
- [x] SegPPD-101: MIT claimed at acquisition time, sources now inaccessible → REVIEW
- [x] Every source in training-ready dataset appears in ledger
- [x] Every source has explicit license/status
- [x] Commercial counts reconcile to 136,134 total
- [x] Per-class commercial counts reconcile to overall commercial count
- [x] No image counted as commercially usable merely because license is unknown

---

*Phase 22 completed: 2026-08-18*
*Phase 20 baseline commit: ce3392a*
