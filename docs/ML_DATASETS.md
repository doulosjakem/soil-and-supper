# Soil & Supper — ML Datasets

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
- **Recommendation**: USE / SUPPLEMENT / REJECT

## 2. Dataset Evaluations

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
- Manual curation by authors.
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
| **Recommendation** | **SUPPLEMENT** — Early growth images for Corn and Bean |

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
| **Recommendation** | **SUPPLEMENT** — High-quality public domain images for augmentation |

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
| **Estimated Useful Images** | ~5,000 |
| **Recommendation** | **SUPPLEMENT** — High-quality pepper and tomato images with quality labels |

**Notes**:
- DOI: 10.17632/6nxnjbn9w6.1
- Collected at Vishwakarma University, Pune, India.
- Xiaomi Mi10T smartphone.

---

### DS-06: Kaggle Vegetable Image Dataset (misrakahmed)

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
| **Known Limitations** | CC BY-SA license requires derivative works to be shared under same license; may be incompatible with proprietary app |
| **Estimated Useful Images** | ~15,000 |
| **Recommendation** | **REJECT for primary use** — ShareAlike license incompatible with proprietary Android app |

**Notes**:
- Already split into train (15,000), test (3,000), validation (3,000).
- High quality and convenient, but license is problematic.

---

### DS-07: Oxford 102 Flower Dataset

| Field | Value |
|-------|-------|
| **Name** | 102 Category Flower Dataset |
| **URL** | https://www.robots.ox.ac.uk/~vgg/data/flowers/102/ |
| **License** | Unclear (no explicit license on dataset page) |
| **Commercial Use** | Unknown — verify before use |
| **Attribution Required** | Unknown |
| **Image Count** | 8,189 images |
| **Classes** | 102 flower categories |
| **Relevant Classes** | Various common garden flowers |
| **Image Characteristics** | Various scales, poses, lighting |
| **Growth Stages** | Blooming flowers |
| **Environmental Diversity** | Gardens, nature |
| **Known Limitations** | License unclear; UK-focused flowers |
| **Estimated Useful Images** | Unknown |
| **Recommendation** | **REJECT until license clarified** — Do not use without explicit commercial-use confirmation |

**Notes**:
- HuggingFace dataset shows empty license field.
- Original publication: Nilsback & Zisserman, 2008.
- Contact Oxford VGG for license clarification before use.

---

### DS-08: Pl@ntNet Images

| Field | Value |
|-------|-------|
| **Name** | Pl@ntNet Collaborative Images |
| **URL** | https://plantnet.org |
| **License** | CC BY-SA (images), CC BY (observation data) |
| **Commercial Use** | Yes, but ShareAlike required for images |
| **Attribution Required** | Yes |
| **Image Count** | Millions of images |
| **Classes** | 7806+ plant species (PlantCLEF 2024) |
| **Relevant Classes** | All target classes |
| **Image Characteristics** | User-contributed, variable quality, diverse backgrounds |
| **Growth Stages** | All stages |
| **Environmental Diversity** | Global |
| **Known Limitations** | CC BY-SA requires derivative works to be shared under same license; impractical for proprietary app |
| **Estimated Useful Images** | Very large |
| **Recommendation** | **REJECT for primary use** — ShareAlike license incompatible with proprietary app |

**Notes**:
- PlantCLEF 2024/2025 data is a subset of Pl@ntNet training data.
- Individual image licenses may vary; most are CC BY-SA.
- Do not use for proprietary commercial model.

---

### DS-09: PlantCLEF 2024/2025

| Field | Value |
|-------|-------|
| **Name** | PlantCLEF 2024/2025 Training Data |
| **URL** | https://www.imageclef.org/PlantCLEF2025 |
| **License** | CC BY-NC-SA 4.0 |
| **Commercial Use** | No |
| **Attribution Required** | Yes |
| **Image Count** | ~1.4M images (PlantCLEF 2024) |
| **Classes** | ~7,806 species (southwestern Europe flora) |
| **Relevant Classes** | Many target classes |
| **Image Characteristics** | Individual plant photos, vegetation quadrat images |
| **Growth Stages** | All stages |
| **Environmental Diversity** | Southwestern Europe |
| **Known Limitations** | Non-commercial only; European flora bias |
| **Estimated Useful Images** | Very large but unusable |
| **Recommendation** | **REJECT** — Non-commercial license explicitly prohibits commercial AI training |

**Notes**:
- Kaggle competition rules state: "Competition Use and Non-Commercial & Academic Research only."
- Even though some underlying data may be CC BY, the competition dataset has NC restrictions.
- Do not use.

---

### DS-10: iNaturalist AWS Open Data

| Field | Value |
|-------|-------|
| **Name** | iNaturalist Open Data (AWS) |
| **URL** | https://registry.opendata.aws/inaturalist-open-data/ |
| **License** | Mixed (mostly CC BY-NC) |
| **Commercial Use** | Prohibited by iNaturalist Terms of Service |
| **Attribution Required** | Yes |
| **Image Count** | Millions of observations |
| **Classes** | All species |
| **Relevant Classes** | All target classes |
| **Image Characteristics** | User-contributed, variable quality |
| **Growth Stages** | All stages |
| **Environmental Diversity** | Global |
| **Known Limitations** | Terms of Service explicitly prohibit commercial AI training |
| **Estimated Useful Images** | Very large but unusable |
| **Recommendation** | **REJECT** — Terms of Service prohibit commercial AI training |

**Notes**:
- iNaturalist Terms of Service (Section 7): "Users may not use any iNaturalist data for training artificial intelligence, machine learning models, large language models, or similar networks, algorithms, or systems for commercial purposes."
- Even if individual images are CC0, the platform terms prohibit commercial AI training.

---

### DS-11: VegNet (PMC 9679474)

| Field | Value |
|-------|-------|
| **Name** | VegNet: Dataset of vegetable quality images |
| **URL** | https://data.mendeley.com/datasets/6nxnjbn9w6 |
| **License** | CC BY 4.0 |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | 6,850 images |
| **Classes** | Bell Pepper, Tomato, Chili Pepper, New Mexico Chile |
| **Relevant Classes** | Pepper, Tomato |
| **Image Characteristics** | Mobile phone, white background, 256×256, quality stages |
| **Growth Stages** | Unripe, Ripe, Old, Dried, Damaged |
| **Environmental Diversity** | Indoor lab |
| **Known Limitations** | Only 4 classes; controlled background |
| **Estimated Useful Images** | ~6,000 |
| **Recommendation** | **SUPPLEMENT** — High-quality pepper/tomato images with quality labels |

**Notes**:
- Same dataset as DS-05? Actually different - this is the 6,850 image dataset with 4 classes and quality sub-labels.
- DOI: 10.17632/6nxnjbn9w6.1

---

### DS-12: CommonCanvas CC-BY

| Field | Value |
|-------|-------|
| **Name** | CommonCanvas CC-BY |
| **URL** | https://huggingface.co/datasets/common-canvas/commoncatalog-cc-by |
| **License** | CC BY 2.0 (varies by image) |
| **Commercial Use** | Yes, with attribution |
| **Attribution Required** | Yes |
| **Image Count** | ~14.5M images |
| **Classes** | General web images |
| **Relevant Classes** | Indirect — contains some plant/vegetable images |
| **Image Characteristics** | Web-crawled, variable quality |
| **Growth Stages** | Mixed |
| **Environmental Diversity** | Global web |
| **Known Limitations** | Not plant-specific; requires filtering; very large |
| **Estimated Useful Images** | Unknown |
| **Recommendation** | **LOW PRIORITY** — Not worth the filtering effort for plant-specific model |

---

### DS-13: KoalaAI StockImages-CC0

| Field | Value |
|-------|-------|
| **Name** | StockImages-CC0 |
| **URL** | https://huggingface.co/datasets/KoalaAI/StockImages-CC0 |
| **License** | CC0 (Public Domain) |
| **Commercial Use** | Yes, no restrictions |
| **Attribution Required** | No |
| **Image Count** | ~4,000 images |
| **Classes** | General stock photos |
| **Relevant Classes** | Indirect — contains some plant images |
| **Image Characteristics** | Stock photography, high quality |
| **Growth Stages** | Mixed |
| **Environmental Diversity** | Studio and outdoor |
| **Known Limitations** | Not plant-specific; very small for our needs |
| **Estimated Useful Images** | <100 plant-related |
| **Recommendation** | **REJECT** — Not plant-specific; insufficient scale |

---

### DS-14: BanglaVeg (ScienceDirect 2025)

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

### DS-15: Mendeley Vegetables Image Dataset (j33g3nsm9k)

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
| **Known Limitations** | Limited class list |
| **Estimated Useful Images** | Unknown |
| **Recommendation** | **EVALUATE** — Download and assess image quality and count |

**Notes**:
- Published 2025-05-27.
- DOI: 10.17632/j33g3nsm9k

---

## 3. Summary Recommendations

| Dataset | Recommendation | Target Classes | Est. Images | License Risk |
|---------|---------------|----------------|-------------|--------------|
| Bangladesh Vegetables (Mendeley) | USE | 12+ | ~2,500 | Low (CC BY 4.0) |
| Smartphone Vegetable Detection | USE | 10+ | ~2,000 | Low (CC BY 4.0) |
| USDA ARS Image Gallery | SUPPLEMENT | 15+ | ~500 | None (Public Domain) |
| VegNet (Mendeley) | SUPPLEMENT | 2 | ~6,000 | Low (CC BY 4.0) |
| BanglaVeg | USE | 8+ | ~3,000 | Low (CC BY 4.0) |
| Early-Stage Crops | SUPPLEMENT | 2 | ~1,500 | Low (CC BY 4.0) |
| Kaggle Vegetable (misrakahmed) | REJECT | 15 | ~15,000 | High (CC BY-SA) |
| Pl@ntNet | REJECT | All | Millions | High (CC BY-SA) |
| PlantCLEF 2025 | REJECT | All | ~1.4M | High (CC BY-NC-SA) |
| iNaturalist | REJECT | All | Millions | High (ToS prohibition) |
| Oxford 102 Flowers | REJECT | Flowers | 8,189 | Unknown |
| CommonCanvas CC-BY | LOW | Indirect | 14.5M | Low but not useful |

## 4. Estimated Total Data by Class (Without Personal Photography)

| Class | Estimated Images | Status |
|-------|-----------------|--------|
| Tomato | 8,000+ | Strong |
| Pepper (sweet + hot) | 6,000+ | Strong |
| Cucumber | 4,000+ | Strong |
| Bean | 4,000+ | Strong |
| Corn | 3,000+ | Moderate |
| Carrot | 2,500+ | Moderate |
| Onion | 2,000+ | Moderate |
| Potato | 2,500+ | Moderate |
| Broccoli | 2,000+ | Moderate |
| Cabbage | 1,500+ | Marginal |
| Lettuce | 1,500+ | Marginal |
| Spinach | 1,000+ | Weak |
| Pea | 1,500+ | Marginal |
| Radish | 1,500+ | Marginal |
| Summer Squash | 2,000+ | Moderate |
| Winter Squash | 1,500+ | Marginal |
| Strawberry | 2,000+ | Moderate |
| Watermelon | 1,000+ | Weak |
| Cantaloupe | 800+ | Weak |
| Eggplant | 1,000+ | Weak |
| Herbs (each) | 200-500 | Weak |
| Flowers (each) | 100-300 | Weak |

**Key Finding**: 6–8 classes have strong data. 10+ classes have moderate data. 10+ classes have weak or insufficient data.

**Strategy**: Train baseline with strong + moderate classes. Evaluate. Target weak classes for additional data acquisition or consider merging/removing.

## 5. Data Pipeline Strategy

1. **Download** approved datasets automatically.
2. **Filter** to only relevant classes.
3. **Deduplicate** using perceptual hashing.
4. **Validate** image integrity.
5. **Normalize** filenames and metadata.
6. **Split** stratified train/val/test.
7. **Augment** training data (rotation, flip, color jitter).
8. **Report** class counts, source counts, license attribution.

## 6. Next Steps

1. Finalize taxonomy (this document).
2. Build automated download pipeline.
3. Acquire and curate datasets.
4. Generate manifest and quality report.
5. Train baseline model.
6. Evaluate and iterate.
