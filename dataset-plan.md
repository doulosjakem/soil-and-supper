# Soil & Supper: Training Dataset Plan
## Milestone 6 Phase 2 — Garden Plant Image Classification

**Status:** Proposed — Awaiting Approval Before Acquisition  
**Created:** 2026-08-13  
**Constraint:** No self-photography required; build from existing publicly available sources  
**Goal:** Commercially usable training dataset for 12-class garden plant identification  

---

## 1. Objectives

1. Acquire a legally safe, commercially distributable image dataset for 12 garden plant classes
2. Prioritize verified licenses with clear provenance over raw image count
3. Avoid datasets that require model open-sourcing (CC BY-SA) or prohibit commercial AI training (iNaturalist ToS)
4. Deliver a curated, deduplicated, stratified train/val/test split ready for model training
5. Document all sources, licenses, and attribution requirements

---

## 2. Target Classes (v1)

| # | Class | Priority | Notes |
|---|-------|----------|-------|
| 1 | Tomato | High | Abundant external data |
| 2 | Pepper | High | Abundant external data |
| 3 | Eggplant | High | Good external coverage |
| 4 | Cucumber | High | Good external coverage |
| 5 | Zucchini | Medium | Moderate coverage; may need merge with Cucumber |
| 6 | Green Bean | Medium | Seedling dataset available |
| 7 | Corn | High | Good external coverage |
| 8 | Broccoli | Medium | Moderate coverage |
| 9 | Carrot | Medium | Moderate coverage |
| 10 | Potato | Medium | Good external coverage |
| 11 | Onion | Medium | Moderate coverage |
| 12 | Strawberry | Low | Limited external data; lowest priority |

**Deferred to v2:** Pumpkin/Squash, Cabbage, Kale, Lettuce, Pea, Radish

---

## 3. Dataset Sources

### 3.1 Tier 1: Primary Sources (Verified, Download Immediately)

#### DS-01: USDA ARS Image Gallery
- **URL:** https://www.ars.usda.gov/oc/images/image-gallery/
- **License:** Public Domain (US Government work)
- **Provenance:** Original USDA Agricultural Research Service photography
- **Size:** ~6,500 total images across categories; estimate 50–200 relevant per target class
- **Content:** Professional field photos, whole plants, fruit, flowers, seedlings
- **Attribution:** Credit requested but not legally required
- **Risk:** None (US Government public domain)

#### DS-02: Bangladesh Comprehensive Vegetables (Mendeley)
- **URL:** https://data.mendeley.com/datasets/rtx9ngb68j
- **License:** CC BY 4.0
- **Provenance:** Original collection by authors using Poco F3 smartphone; manual review; peer-reviewed publication
- **Size:** 4,730 JPG images, 42 classes
- **Content:** Natural light market/field photos; multiple angles; realistic backgrounds
- **Relevant classes:** Tomato, Capsicum (→ Pepper), Cucumber, Eggplant (Brinjal), Broccoli, Cabbage, Carrot, Onion, Potato, Pumpkin, Radish, Zucchini, Flat Bean (→ Green Bean)
- **Attribution:** Required (authors, publication, Mendeley DOI)
- **Risk:** Low (clear original collection, standard CC BY)

#### DS-03: Smartphone Vegetable Detection (PMC 12686877)
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12686877/
- **License:** CC BY 4.0
- **Provenance:** Original collection using Redmi Note 12; annotated with Roboflow; peer-reviewed
- **Size:** 3,534 images, 22 classes
- **Content:** Ground-level vendor photos; natural backgrounds; multiple angles
- **Relevant classes:** Tomato, Capsicum, Cucumber, Eggplant, Potato, Pumpkin, Radish, Green Bean
- **Attribution:** Required (authors, article DOI)
- **Risk:** Low (original collection, CC BY)

#### DS-04: Early-Stage Vegetable Crops (PMC 8933512)
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/
- **License:** CC BY 4.0
- **Provenance:** Original collection in France using Intel RealSense, Canon EOS, Sony W800; expert annotation
- **Size:** 2,801 images
- **Content:** Seedling/early growth (2–5 weeks); controlled lighting; annotated bounding boxes
- **Relevant classes:** Corn (maize), Green Bean (Phaseolus vulgaris)
- **Attribution:** Required (authors, article DOI)
- **Risk:** Low (original collection, CC BY)

### 3.2 Tier 2: Investigate Further (Conditional Approval Required)

#### DS-05: FloraLebanon (Scientific Data 2026)
- **URL:** https://www.nature.com/articles/s41597-026-07576-7
- **License:** TBD — Read article license section before download
- **Provenance:** University student volunteers; expert validation; field expeditions
- **Size:** 24,944 images, 102 species
- **Content:** Whole plants, leaves, stems, flowers, fruits, habitats; structured capture protocol
- **Potential value:** Could significantly boost coverage for classes missing from Tier 1
- **Action required:** Read article, verify license, then approve/deny

#### DS-06: VegAnn (Zenodo/Hugging Face)
- **URL:** https://zenodo.org/records/7636408
- **License:** CC BY 4.0 (confirmed on GitHub and Zenodo)
- **Provenance:** Multi-institution compilation; clear source documentation
- **Size:** 3,775 images, 26+ crop species
- **Content:** Vegetation/background segmentation masks; outdoor images; diverse conditions
- **Potential value:** Segmentation masks useful for background replacement augmentation
- **Action required:** Verify target class coverage in dataset metadata

### 3.3 Tier 3: Explicitly Excluded

| Dataset | Reason for Exclusion |
|---------|---------------------|
| Fruits-360 | CC BY-SA — ShareAlike likely requires model open-sourcing |
| PlantCLEF / Pl@ntNet-300K | iNaturalist ToS prohibits commercial AI training; CC BY-SA images |
| PlantVillage | CC BY-SA; leaf-disease only |
| PlantWild (Voxel51) | CC BY-NC-ND — NonCommercial + NoDerivatives |
| iNaturalist / GBIF | ToS explicitly prohibits commercial AI training |
| Open Images V7 | Google disclaims license warranty; per-image verification impractical |
| "140 Most Popular Crops" (Kaggle) | Aggregated from unspecified sources; no provenance; unverified CC0 |
| "Fruits and Vegetables" 45k (Kaggle) | Aggregated from unspecified sources; no provenance; unverified CC0 |
| Food-101 | Foodspotting terms restrict to "scientific fair use" |
| Any dataset without clear provenance documentation | Cannot verify commercial license |

---

## 4. Class Coverage Projection

| Class | DS-01 USDA | DS-02 Bangladesh | DS-03 Smartphone | DS-04 Seedling | DS-05 FloraLebanon? | DS-06 VegAnn? | **Projected Verified Total** |
|-------|-----------|------------------|------------------|----------------|---------------------|---------------|------------------------------|
| Tomato | 30–50 | 112 | 160 | — | TBD | — | **300–320 +** |
| Pepper | 30–50 | 112 | 160 | — | TBD | — | **300–320 +** |
| Eggplant | 30–50 | 112 | 160 | — | TBD | — | **300–320 +** |
| Cucumber | 30–50 | 107 | 160 | — | TBD | — | **295–315 +** |
| Zucchini | 20–40 | 107 | — | — | TBD | — | **125–145 +** |
| Green Bean | 20–40 | 137 | — | 200+ | TBD | — | **355–375 +** |
| Corn | 30–50 | — | — | 200+ | TBD | — | **230–250 +** |
| Broccoli | 20–40 | ~50 | — | — | TBD | — | **70–90 +** |
| Carrot | 20–40 | ~50 | — | — | TBD | — | **70–90 +** |
| Potato | 30–50 | 110 | — | — | TBD | — | **140–160 +** |
| Onion | 20–40 | ~50 | — | — | TBD | — | **70–90 +** |
| Strawberry | 30–50 | — | — | — | TBD | — | **30–50 +** |

**Notes:**
- "TBD" columns depend on approval of DS-05 and DS-06 after license verification
- Projected totals are conservative estimates; actual counts may be higher after filtering
- Classes below 200 verified images (Broccoli, Carrot, Onion, Strawberry) are at risk of insufficient coverage
- **Self-collection supplement may still be necessary** for low-coverage classes even with Tier 1 complete

---

## 5. Curation Pipeline

### Phase 1: Acquisition (Week 1)
1. Download DS-01 through DS-04 to `./raw/` directory
2. If approved, download DS-05 and DS-06
3. Preserve original filenames and directory structures in `./raw/{dataset-id}/`

### Phase 2: License Audit (Week 1)
For each image:
1. Read dataset-level license metadata
2. For CC BY datasets: record author, title, source URL, license in `manifest.csv`
3. Flag any image with EXIF copyright notice conflicting with dataset license
4. Output: `CLEAN/` and `REJECTED/` subfolders per dataset

### Phase 3: Class Mapping & Filtering (Week 2)
Create `class_mapping.yaml`:
```yaml
target_classes:
  - name: Tomato
    source_datasets:
      - dataset: DS-02
        source_labels: [Tomato]
      - dataset: DS-03
        source_labels: [Tomato]
  - name: Pepper
    source_datasets:
      - dataset: DS-02
        source_labels: [Capsicum]
      - dataset: DS-03
        source_labels: [Capsicum]
  # ... etc
```

Filtering rules:
1. Copy matching images to `./curated/{class_name}/`
2. Remove images with shortest side < 100 pixels
3. Remove exact duplicates (MD5 hash)
4. Remove near-duplicates (perceptual hash, Hamming distance < 5)
5. Remove images that are clearly mislabeled (e.g., "tomato" label but image is apple)

### Phase 4: Quality Control (Week 2–3)
1. Blur detection: reject images with Laplacian variance < 100
2. Exposure check: reject images with > 99% pixels at 0 or 255
3. Duplicate detection: phash across all classes
4. Mislabel audit: train a quick MobileNetV3 for 5 epochs, review top-20 confused image pairs
5. Expert review: if available, spot-check 100 random images per class

### Phase 5: Splitting (Week 3)
- Stratified random split: 70% train, 15% val, 15% test
- If photographer/source metadata exists, ensure no photographer leakage between splits
- Output: `./splits/{class_name}/train/`, `./splits/{class_name}/val/`, `./splits/{class_name}/test/`

### Phase 6: Documentation (Week 3)
Create:
1. `dataset_manifest.jsonl` — one record per image with source, license, split, attribution
2. `DATA_SOURCES.md` — human-readable attribution for all sources
3. `CURATION_LOG.md` — decisions made during filtering (what was removed and why)
4. `LICENSE_SUMMARY.md` — table of all licenses used, percentages, obligations

---

## 6. Augmentation Strategy (Post-Acquisition, Pre-Training)

Since external data lacks garden/field context, use augmentation to simulate realism:

| Augmentation | Purpose | Implementation |
|--------------|---------|----------------|
| **Background replacement** | Simulate garden soil, pots, raised beds | Segment subject (RMBG or similar), composite onto CC0 garden backgrounds |
| **Lighting variation** | Simulate morning/afternoon/shade | Albumentations: RandomBrightnessContrast, RandomShadow, RandomFog |
| **Scale/pose** | Simulate in-hand vs. on-plant | Rotate, flip, perspective transform, RandomResizedCrop |
| **Blur/noise** | Simulate shaky hands, low light | MotionBlur, GaussianBlur, ISONoise |
| **Weather** | Simulate rain, dew, dust | RandomRain, RandomSunFlare, JPEG compression |

**Important:** Any composite backgrounds must be CC0 or CC BY with attribution. Do not use all-rights-reserved stock imagery.

---

## 7. Licensing Compliance Matrix

| Dataset | License | Commercial Model OK? | Model Redistribution | Attribution Required? |
|---------|---------|----------------------|----------------------|----------------------|
| DS-01 USDA ARS | Public Domain | ✅ Yes | ✅ Any license | No (courtesy: yes) |
| DS-02 Bangladesh | CC BY 4.0 | ✅ Yes | ✅ Any license | **Yes — mandatory** |
| DS-03 Smartphone Veg | CC BY 4.0 | ✅ Yes | ✅ Any license | **Yes — mandatory** |
| DS-04 Early-Stage | CC BY 4.0 | ✅ Yes | ✅ Any license | **Yes — mandatory** |
| DS-05 FloraLebanon | TBD | TBD | TBD | TBD |
| DS-06 VegAnn | CC BY 4.0 | ✅ Yes | ✅ Any license | **Yes — mandatory** |

**Obligations:**
1. Maintain `DATA_SOURCES.md` with full attribution for all CC BY sources
2. Include "Data Sources" screen in app with attribution links
3. Do NOT distribute model under CC BY-SA unless SA sources are used
4. Do NOT use iNaturalist, PlantCLEF, PlantVillage, Fruits-360, or any SA/NC dataset

---

## 8. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Tier 1 datasets yield < 200 images/class for some targets | Medium | High | Identify self-collection supplement targets early |
| DS-05/DS-06 licenses prove unacceptable | Low | Medium | Proceed without them; they are bonuses |
| Copyright claim on CC BY dataset images | Low | High | Verify provenance; use only datasets with clear original collection |
| Model accuracy insufficient for v1 release | Medium | High | Set accuracy gate at 80% before shipping; plan v2 iteration |
| Attribution missing in app | Low | Medium | Automated check: build attribution into model card + app credits screen |

---

## 9. Timeline

| Week | Activity | Deliverable |
|------|----------|-------------|
| 1 | Acquire DS-01 through DS-04; begin DS-05/DS-06 review | `./raw/` populated |
| 1 | License audit | `CLEAN/` and `REJECTED/` folders |
| 2 | Class mapping, filtering, deduplication | `./curated/{class}/` populated |
| 2–3 | Quality control (blur, exposure, duplicates, mislabels) | QC report |
| 3 | Train/val/test split; documentation | `./splits/`, `DATA_SOURCES.md`, `dataset_manifest.jsonl` |
| 3 | **STOP — Present dataset for approval before training** | Dataset plan sign-off |

---

## 10. Approval Gates

1. **Gate A (Now):** Approve dataset plan and source list
2. **Gate B (After DS-05/DS-06 review):** Approve conditional sources
3. **Gate C (After curation):** Approve final train/val/test splits before training begins
4. **Gate D (After initial training):** Approve model accuracy before Core ML conversion

---

## 11. Open Questions

1. Should DS-05 (FloraLebanon) and DS-06 (VegAnn) be pursued? Depends on license verification.
2. Are there additional verified CC BY/CC0 datasets we have not identified?
3. What is the minimum acceptable accuracy for v1 release? (Recommend: 80% top-1 on held-out test)
4. Should we merge Zucchini/Pumpkin into a single "Squash" class to increase coverage?
5. Do we have access to a botanist or Master Gardener for expert validation of a sample set?

---

*This plan is a proposal. Do not download data or begin curation until Gate A is approved.*
