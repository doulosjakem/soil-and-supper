# Soil & Supper — ML Datasets (Revised)

## 1. Evaluation Criteria

Each dataset is evaluated against:

- **License**: Commercial-use compatibility
- **Attribution**: Required or not
- **Image Count**: Total and per-class estimates
- **Classes**: Overlap with target taxonomy
- **Image Characteristics**: Background, lighting, angle, resolution
- **Growth Stages**: Seedling, mature, fruit, flower
- **Environmental Diversity**: Indoor, outdoor, greenhouse, market
- **Known Limitations**: Background removal, low resolution, geographic bias
- **Estimated Useful Images**: After filtering for target classes
- **Recommendation**: USE / SUPPLEMENT / REJECT / CONTACT_REQUIRED

## 2. Crop Datasets

### DS-01: Bangladesh Comprehensive Vegetables (Mendeley)

| Field | Value |
|-------|-------|
| **Name** | A Comprehensive Image Dataset of Vegetables Grown in Bangladesh |
| **URL** | https://data.mendeley.com/datasets/rtx9ngb68j |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 4,730 JPG images |
| **Classes** | 42 vegetable classes |
| **Relevant Classes** | Tomato, Capsicum (→ Pepper), Cucumber, Eggplant (Brinjal), Broccoli, Cabbage, Carrot, Onion, Potato, Pumpkin, Radish, Zucchini, Flat Bean (→ Bean) |
| **Image Characteristics** | Natural light, market/field photos, multiple angles, realistic backgrounds |
| **Growth Stages** | Mostly mature/ripe vegetables |
| **Environmental Diversity** | Outdoor market and field |
| **Known Limitations** | Bangladesh-specific varieties; some classes may have different appearance than North American varieties |
| **Estimated Useful Images** | ~2,500 after filtering for target classes |
| **Recommendation** | **USE** — Primary source for 12+ target classes |

**Notes**:
- Original collection using Poco F3 smartphone.
- Peer-reviewed publication.
- Clear CC BY 4.0 license.
- DOI: 10.17632/rtx9ngb68j

---

### DS-02: Smartphone Vegetable Detection (PMC 12686877)

| Field | Value |
|-------|-------|
| **Name** | Smartphone-based multi-criteria vegetable object detection dataset |
| **URL** | https://data.mendeley.com/datasets/gnc4s3z2mf/3 |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 3,534 high-resolution images |
| **Classes** | 22 vegetable classes |
| **Relevant Classes** | Tomato, Capsicum, Cucumber, Eggplant, Potato, Pumpkin, Radish, Green Bean, Carrot, Onion |
| **Image Characteristics** | Ground-level vendor photos, natural backgrounds, multiple angles, Redmi Note 12 |
| **Growth Stages** | Mature vegetables for sale |
| **Environmental Diversity** | Outdoor roadside vendor stalls |
| **Known Limitations** | Object detection format (Pascal VOC); requires conversion to classification format |
| **Estimated Useful Images** | ~2,000 after filtering |
| **Recommendation** | **USE** — Supplement for 10+ target classes |

**Notes**:
- Peer-reviewed open access article.
- Annotated with Roboflow.
- DOI: 10.17632/gnc4s3z2mf.3
- Article: https://pmc.ncbi.nlm.nih.gov/articles/PMC12686877/

---

### DS-03: Early-Stage Vegetable Crops (PMC 8933512)

| Field | Value |
|-------|-------|
| **Name** | Annotated image dataset of vegetable crops at early stage |
| **URL** | https://pmc.ncbi.nlm.nih.gov/articles/PMC8933512/ |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 2,801 images |
| **Classes** | Maize, Bean, Leek (3 classes) |
| **Relevant Classes** | Maize (→ Corn), Bean |
| **Image Characteristics** | Seedling/early growth (2–5 weeks), controlled lighting, annotated bounding boxes |
| **Growth Stages** | Seedling stage only |
| **Environmental Diversity** | Greenhouse/controlled |
| **Known Limitations** | Only 3 classes; early growth stage only |
| **Estimated Useful Images** | ~1,500 |
| **Recommendation** | **USE** — Supplement for Corn and Bean seedling images |

**Notes**:
- Collected in France using Intel RealSense, Canon EOS, Sony W800.
- Expert annotation.
- PMC ID: 8933512

---

### DS-04: USDA ARS Image Gallery

| Field | Value |
|-------|-------|
| **Name** | USDA ARS Image Gallery |
| **URL** | https://www.ars.usda.gov/oc/images/image-gallery/ |
| **License** | Public Domain (US Government) |
| **Commercial Use** | Yes |
| **Attribution Required** | No (credit requested but not required) |
| **Image Count** | 6,500+ searchable images |
| **Classes** | Crops, fruits, vegetables, plants, insects |
| **Relevant Classes** | Tomato, Pepper, Cucumber, Corn, Potato, Onion, Strawberry, Grape, etc. |
| **Image Characteristics** | Professional field photos, high resolution, whole plants, fruit, flowers |
| **Growth Stages** | All stages |
| **Environmental Diversity** | Field research, agricultural settings |
| **Known Limitations** | Must manually search and download per class; no pre-labeled classification dataset |
| **Estimated Useful Images** | 200–500 per target class after manual curation |
| **Recommendation** | **SUPPLEMENT** — High-quality public domain images for augmentation AND external test set |

**Notes**:
- Copyright-free unless otherwise indicated.
- Ag Data Commons record: https://agdatacommons.nal.usda.gov/articles/dataset/USDA_ARS_Image_Gallery/24659814
- Requires manual download; no bulk dataset.

---

### DS-05: VegNet (Mendeley)

| Field | Value |
|-------|-------|
| **Name** | VegNet: Dataset of vegetable quality images |
| **URL** | https://data.mendeley.com/datasets/6nxnjbn9w6 |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 6,850 images |
| **Classes** | Bell Pepper, Tomato, Chili Pepper, New Mexico Chile (4 classes) |
| **Relevant Classes** | Pepper (sweet + hot), Tomato |
| **Image Characteristics** | Mobile phone camera, various lighting, white background, 256×256 |
| **Growth Stages** | Unripe, Ripe, Old, Dried, Damaged |
| **Environmental Diversity** | Indoor lab and outdoor |
| **Known Limitations** | Only 4 classes; white background (not realistic garden settings) |
| **Estimated Useful Images** | ~6,000 |
| **Recommendation** | **USE** — Supplement for pepper and tomato images with quality labels |

**Notes**:
- DOI: 10.17632/6nxnjbn9w6.1
- Collected at Vishwakarma University, Pune, India.
- Xiaomi Mi10T smartphone.

---

### DS-06: BanglaVeg (ScienceDirect 2025)

| Field | Value |
|-------|-------|
| **Name** | BanglaVeg: A curated vegetable image dataset |
| **URL** | https://www.sciencedirect.com/science/article/pii/S2352340925001738 |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 4,319 images |
| **Classes** | 12 vegetable classes |
| **Relevant Classes** | Tomato, Capsicum, Cucumber, Eggplant, Potato, Onion, Radish, Bean |
| **Image Characteristics** | High resolution, market/field photos, Bangladesh |
| **Growth Stages** | Mature vegetables |
| **Environmental Diversity** | Outdoor markets and fields |
| **Known Limitations** | Bangladesh-specific; backgrounds removed in some versions |
| **Estimated Useful Images** | ~3,000 |
| **Recommendation** | **USE** — Good supplement for 8+ target classes |

**Notes**:
- Published 2025 in Data in Brief.
- DOI: 10.1016/j.dib.2025.???
- Clear CC BY 4.0 license.

---

### DS-07: Kaggle Vegetable Image Dataset (misrakahmed)

| Field | Value |
|-------|-------|
| **Name** | Vegetable Image Dataset |
| **URL** | https://www.kaggle.com/datasets/misrakahmed/vegetable-image-dataset |
| **License** | CC BY-SA 4.0 |
| **Commercial Use** | Yes, but ShareAlike required |
| **Attribution Required** | Yes |
| **Image Count** | 21,000 images |
| **Classes** | 15 classes |
| **Relevant Classes** | Bean, Bitter Gourd, Bottle Gourd, Brinjal (Eggplant), Broccoli, Cabbage, Capsicum (Pepper), Carrot, Cauliflower, Cucumber, Papaya, Potato, Pumpkin, Radish, Tomato |
| **Image Characteristics** | 224×224, JPG, clean backgrounds |
| **Growth Stages** | Mature vegetables |
| **Environmental Diversity** | Studio/controlled |
| **Known Limitations** | CC BY-SA license requires derivative works to be shared under same license; incompatible with proprietary app |
| **Estimated Useful Images** | ~15,000 |
| **Recommendation** | **REJECT for primary use** — ShareAlike license incompatible with proprietary Android app |

---

### DS-08: Mendeley Vegetables Image Dataset (j33g3nsm9k)

| Field | Value |
|-------|-------|
| **Name** | Vegetables Image Dataset for Machine Applications |
| **URL** | https://data.mendeley.com/datasets/j33g3nsm9k |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | Unknown (6 vegetable types) |
| **Classes** | Potato, Chili, Tomato, Cucumber, Beans, Okra |
| **Relevant Classes** | Potato, Chili (→ Pepper), Tomato, Cucumber, Bean, Okra |
| **Image Characteristics** | Unknown |
| **Growth Stages** | Unknown |
| **Environmental Diversity** | Unknown |
| **Known Limitations** | Limited class list; metadata not yet reviewed |
| **Estimated Useful Images** | Unknown |
| **Recommendation** | **EVALUATE** — Download and assess image quality and count |

**Notes**:
- Published 2025-05-27.
- DOI: 10.17632/j33g3nsm9k

---

## 3. Weed Datasets

### DS-09: DeepWeeds

| Field | Value |
|-------|-------|
| **Name** | DeepWeeds: A Multiclass Weed Species Image Dataset for Deep Learning |
| **URL** | https://github.com/AlexOlsen/DeepWeeds |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 17,509 images |
| **Classes** | 8 weed species + 1 negative class |
| **Relevant Classes** | Lantana, Prickly acacia, Parkinsonia, Rubber vine (some overlap with warm US climates). **NOT** common Northern American garden weeds. |
| **Image Characteristics** | In-situ rangeland photos, 256×256, various lighting |
| **Growth Stages** | Mature weeds |
| **Environmental Diversity** | Northern Australia rangelands |
| **Known Limitations** | Australian species; not representative of North American garden weeds |
| **Estimated Useful Images** | ~2,000 usable for North American context (after filtering) |
| **Recommendation** | **SUPPLEMENT** — Use only as supplementary weed data; prioritize CWD30 and Bugwood for North American weeds |

**Notes**:
- Published in Scientific Reports, 2019.
- DOI: 10.1038/s41598-018-38343-3

---

### DS-10: CWD30

| Field | Value |
|-------|-------|
| **Name** | CWD30: A new benchmark dataset for crop weed recognition in precision agriculture |
| **URL** | https://cwd-30.github.io/cwd-30/ |
| **License** | **UNCLEAR — no explicit license on GitHub or project website** |
| **Commercial Use** | Unknown — published in Elsevier journal (Computers and Electronics in Agriculture) |
| **Attribution Required** | Unknown |
| **Image Count** | 219,770 images |
| **Classes** | 10 crop + 20 weed species |
| **Relevant Classes** | 20 weed species including: Amaranthus sp., Digitaria sp., Portulaca oleracea, Chenopodium album, Stellaria media, Cyperus sp., Ambrosia artemisiifolia, Calystegia sepium, Setaria sp., Cirsium sp., Polygonum sp., Oxalis corniculata, Sorghum halepense, Elymus repens, and others |
| **Image Characteristics** | High resolution, multiple viewing angles, diverse growth stages, indoor/outdoor |
| **Growth Stages** | Multiple growth stages documented |
| **Environmental Diversity** | Agricultural fields, lab-grown |
| **Known Limitations** | **License unclear for commercial use**; some species are Korean/Australian; dataset is large (219K images) |
| **Estimated Useful Images** | ~50,000+ after filtering for 21 target weed classes |
| **Recommendation** | **REJECT until license clarified** — Do not use for commercial model without explicit permission from authors |

**Notes**:
- Published 2025 in Computers and Electronics in Agriculture.
- DOI: 10.1016/j.compag.2024.109737
- Contact authors before use.

---

## 4. Insect / Pest Datasets

### DS-11: IP102

| Field | Value |
|-------|-------|
| **Name** | IP102: A Large-Scale Benchmark Dataset for Insect Pest Recognition |
| **URL** | https://github.com/xpwu95/IP102 |
| **License** | **Academic use only — contact author for commercial use** |
| **Commercial Use** | **Prohibited without explicit permission** |
| **Attribution Required** | Yes |
| **Image Count** | 75,222 images |
| **Classes** | 102 pest species |
| **Relevant Classes** | Aphids, Japanese beetle, Colorado potato beetle, Cucumber beetles, Cabbage worms, Tomato hornworm, Squash bugs, Whiteflies, Thrips, Spider mites, Leaf miners, Cutworms, Stink bugs, Flea beetles, and more |
| **Image Characteristics** | Field photos, variable quality, long-tailed distribution |
| **Growth Stages** | Mixed (egg, larva, pupa, adult) |
| **Environmental Diversity** | Agricultural fields, China |
| **Known Limitations** | **License prohibits commercial use without contacting author**; long-tailed distribution; some classes have very few images |
| **Estimated Useful Images** | Very large but currently unusable |
| **Recommendation** | **REJECT for now** — Contact Xiaoping Wu (xpwu95@163.com) for commercial use permission before using |

**Notes**:
- Accepted at CVPR 2019.
- Hierarchical taxonomy (pests grouped by crop).
- 19,000 images have bounding box annotations.

---

### DS-12: Bugwood Images

| Field | Value |
|-------|-------|
| **Name** | Bugwood Images (WeedImages, InsectImages, Invasive.org) |
| **URL** | https://images.bugwood.org/ |
| **License** | **Mixed — per-photographer Creative Commons licenses** |
| **Commercial Use** | **Requires photographer approval for commercial use** |
| **Attribution Required** | Yes (per photographer) |
| **Image Count** | Unknown (hundreds of thousands across all sub-sites) |
| **Classes** | Weeds, insects, diseases, invasive species |
| **Relevant Classes** | All target weed, insect, and disease classes |
| **Image Characteristics** | Professional identification photos, high quality, various angles |
| **Growth Stages** | All stages |
| **Environmental Diversity** | North American field and garden settings |
| **Known Limitations** | **Individual photographers retain rights; commercial use requires approval per image**; no bulk download; time-consuming provenance tracking |
| **Estimated Useful Images** | Unknown — requires manual search and download |
| **Recommendation** | **SUPPLEMENT with caution** — Excellent quality and relevance, but requires approval workflow for commercial use. Use only CC BY-licensed images for MVP. |

**Notes**:
- Run by University of Georgia Center for Invasive Species and Ecosystem Health.
- Sub-sites: WeedImages.org, InsectImages.org, Invasive.org, ForestryImages.org, IPMImages.org.
- Automated image request system: https://forestryimages.org/about/image-usage

---

## 5. Disease Datasets

### DS-13: PlantVillage

| Field | Value |
|-------|-------|
| **Name** | PlantVillage Dataset |
| **URL** | https://data.mendeley.com/datasets/tywbtsjrjv/1 |
| **License** | CC0 1.0 (Public Domain) |
| **Commercial Use** | Yes, no restrictions |
| **Attribution Required** | No (but citation appreciated) |
| **Image Count** | 54,306 images |
| **Classes** | 38 classes (14 crop species × healthy/disease) |
| **Relevant Classes** | Apple (scab, rust, healthy), Blueberry (healthy), Cherry (powdery mildew, healthy), Corn (rust, healthy), Grape (black rot, healthy), Orange (huanglongbing), Peach (healthy, bacterial spot), Pepper (bacterial spot, healthy), Potato (early/late blight, healthy), Raspberry (healthy), Soybean (healthy), Squash (powdery mildew), Strawberry (healthy), Tomato (bacterial spot, early/late blight, leaf mold, Septoria, spider mites, target spot, mosaic virus, yellow leaf curl, healthy) |
| **Image Characteristics** | 256×256, controlled background (gray/black), lab lighting, leaf close-ups |
| **Growth Stages** | Mature leaves |
| **Environmental Diversity** | Controlled/lab |
| **Known Limitations** | Controlled backgrounds; not real-world garden photos; some classes have few images |
| **Estimated Useful Images** | ~54,000 (entire dataset usable) |
| **Recommendation** | **USE** — Primary disease dataset. CC0 makes it legally risk-free. |

**Notes**:
- Original paper: Hughes & Salathé, 2015. arXiv:1511.08060
- Available via TensorFlow Datasets: `plant_village`
- Meta-Album confirms CC0 1.0 license.

---

### DS-14: PlantDoc

| Field | Value |
|-------|-------|
| **Name** | PlantDoc: A Dataset for Visual Plant Disease Detection |
| **URL** | https://github.com/pratikkayal/PlantDoc-Dataset |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 2,569 images |
| **Classes** | 29 classes (13 plant species, 17 disease types) |
| **Relevant Classes** | Corn leaf blight, Tomato Septoria, Squash powdery mildew, Potato early/late blight, Tomato early blight, Tomato mold, Tomato bacterial spot, Tomato yellow virus, Tomato mosaic virus, Tomato two-spotted spider mites, Apple scab, Apple rust, Grape black rot, Peach leaf, Strawberry leaf, Blueberry leaf, Raspberry leaf, Soybean leaf, Bell pepper leaf spot, Cherry leaf, and more |
| **Image Characteristics** | Real-world field photos, natural backgrounds, variable lighting, variable resolution |
| **Growth Stages** | Mature leaves |
| **Environmental Diversity** | Field/garden |
| **Known Limitations** | Small dataset; some classes have few images; object detection format (can be converted to classification) |
| **Estimated Useful Images** | ~2,500 |
| **Recommendation** | **USE** — Supplement for real-world disease images with natural backgrounds. Complements PlantVillage perfectly. |

**Notes**:
- Published at CoDS-COMAD 2020.
- DOI: 10.1145/3371158.3371196
- Authors: Singh et al., IIT Gandhinagar.

---

## 6. Growth Stage Datasets

### DS-15: Plant Growth Stage Detection (Roboflow)

| Field | Value |
|-------|-------|
| **Name** | Plant Growth Stage Detection Dataset |
| **URL** | https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 7,306 images |
| **Classes** | Flowering, Germination, Harvesting, Vegetative |
| **Relevant Classes** | Flowering (→ Flowering), Vegetative (→ Vegetative), Germination (→ Seedling), Harvesting (→ Mature/Harvest) |
| **Image Characteristics** | Various crops, overhead/side views, natural lighting |
| **Growth Stages** | All 4 stages represented |
| **Environmental Diversity** | Field/garden |
| **Known Limitations** | Only 4 stages (no Senescing); object detection format |
| **Estimated Useful Images** | ~7,000 |
| **Recommendation** | **USE** — Supplement for growth stage training. Add "Senescing" from other sources. |

**Notes**:
- Published 2025.
- CC BY 4.0 license confirmed on Roboflow.

---

### DS-16: BDFlower

| Field | Value |
|-------|-------|
| **Name** | BDFlower: Growth stage flower image dataset for precision agriculture and floriculture |
| **URL** | https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/ |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 23,334 images (3,889 original + augmented) |
| **Classes** | 8 flowers × 3 growth stages (Early, Mid, Full) |
| **Relevant Classes** | General growth stage patterns applicable to all flowering plants |
| **Image Characteristics** | Flower close-ups, controlled and natural backgrounds |
| **Growth Stages** | Early, Mid, Full |
| **Environmental Diversity** | Field and controlled |
| **Known Limitations** | Only flowers; 3 stages (not 6); Bangladesh-specific flower species |
| **Estimated Useful Images** | ~7,000 original-equivalent |
| **Recommendation** | **USE** — Supplement for flowering stage recognition. Generalizable to other plants. |

**Notes**:
- Published 2025.
- PMCID: PMC13123495
- Authors: Das et al.

---

### DS-17: Sunflower Growth Stage Dataset

| Field | Value |
|-------|-------|
| **Name** | Sunflower Growth Stage Image Dataset for Phenological Classification |
| **URL** | https://data.mendeley.com/datasets/byftmdzg4g |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 1,255 images |
| **Classes** | 5 growth stages |
| **Relevant Classes** | General growth stage patterns |
| **Image Characteristics** | High resolution (12,288×16,320), field photos, Redmi Note 11 |
| **Growth Stages** | 5 stages |
| **Environmental Diversity** | Outdoor field, Bangladesh |
| **Known Limitations** | Single crop (sunflower); very high resolution (needs downsampling) |
| **Estimated Useful Images** | ~1,000 |
| **Recommendation** | **SUPPLEMENT** — Useful for growth stage model but single-crop limitation |

**Notes**:
- Published 2025.
- DOI: 10.17632/byftmdzg4g.2

---

## 7. Rejected or High-Risk Datasets

| Dataset | Reason for Rejection |
|---------|----------------------|
| iNaturalist | Terms of Service explicitly prohibit commercial AI training |
| PlantCLEF 2024/2025 | CC BY-NC-SA 4.0 — non-commercial |
| Pl@ntNet | CC BY-SA — ShareAlike incompatible with proprietary app |
| Kaggle Vegetable (misrakahmed) | CC BY-SA 4.0 — ShareAlike incompatible |
| Oxford 102 Flowers | License unclear — no explicit commercial-use confirmation |
| IP102 | Academic use only — commercial requires contacting author |
| CWD30 | License unclear — published in Elsevier journal, no explicit license |
| PlantSeg | CC BY-NC 4.0 — non-commercial |

---

## 8. Dataset Acquisition Priority

### Immediate (No License Risk)
1. PlantVillage — CC0 1.0, 54K images, diseases
2. PlantDoc — CC BY 4.0, 2.5K images, diseases
3. Bangladesh Vegetables — CC BY 4.0, 4.7K images, crops
4. Smartphone Vegetable Detection — CC BY 4.0, 3.5K images, crops
5. BanglaVeg — CC BY 4.0, 4.3K images, crops
6. VegNet — CC BY 4.0, 6.8K images, crops
7. DeepWeeds — CC BY 4.0, 17.5K images, weeds
8. Plant Growth Stage Detection — CC BY 4.0, 7.3K images, growth stages
9. BDFlower — CC BY 4.0, 23K images, growth stages

### Conditional (License Clarification Needed)
10. CWD30 — Contact authors for commercial use permission
11. IP102 — Contact Xiaoping Wu for commercial use permission

### Supplemental (Manual/Automated with Caution)
12. Bugwood Images — Use only CC BY-licensed images; track photographer attribution per image
13. USDA ARS — Manual download; public domain but no bulk access

---

## 9. Estimated Total Data by Domain

| Domain | Estimated Images | Status |
|--------|-----------------|--------|
| Crops | 25,000–30,000 | Strong |
| Weeds | 15,000–20,000 | Moderate (CWD30 gap if license unresolved) |
| Diseases | 25,000–30,000 | Strong (PlantVillage CC0 is excellent) |
| Growth Stages | 10,000–15,000 | Moderate |
| Insects/Pests | 2,000–5,000 | Weak (IP102 license unresolved; Bugwood requires approval) |
| Beneficial Insects | 500–1,000 | Weak |

**Key Finding**: Crops and diseases have strong data. Weeds have moderate data if CWD30 license is resolved. Insects are the weakest domain due to IP102 licensing and Bugwood's per-photographer approval requirements.

---

## 10. Next Steps for Data Acquisition

1. **Download immediately**: PlantVillage, PlantDoc, Bangladesh Vegetables, Smartphone Veg, BanglaVeg, VegNet, DeepWeeds, Plant Growth Stage Detection, BDFlower
2. **Contact authors**: CWD30 (Talha Ilyas), IP102 (Xiaoping Wu)
3. **Manual curation**: USDA ARS for external test set
4. **Supplement with caution**: Bugwood CC BY images only
5. **Generate manifest**: Every image must have provenance metadata
6. **Run pipeline**: prepare → validate → deduplicate → split → report
