# Soil & Supper — Phase 35E Acquisition Backlog

## v1 Acquisition (Complete Before Model Training)

| Priority | Dataset | Classes | Est. Images | License | Size | Status |
|----------|---------|---------|-------------|---------|------|--------|
| 1 | Pisum sativum Image Dataset | Pea | 12,096 | CC BY 4.0 | ~500 MB | Pending download |
| 2 | Radish Plant Leaf Disease Detection | Radish | 2,300 | CC BY 4.0 | ~200 MB | Pending download |
| 3 | Agri-Vision Bangladesh | Zucchini | 5,266+ | CC BY 4.0 | ~2 GB | Pending download |
| 4 | Pumpkin Leaf Diseases | Pumpkin | 2,000 | CC BY 4.0 | ~500 MB | Pending download |
| 5 | GrapeSet | Grape | ~500+ | CC BY 4.0 | ~878 MB | Pending download |
| 6 | ViViD-5K | Grape | 5,000 | CC BY 4.0 | TBD | Pending download |
| 7 | GrapesNet | Grape | 11,000+ | CC BY 4.0 | TBD | Pending download |
| 8 | RaspberrySet | Raspberry | 2,039 | CC BY 4.0 | ~2 GB | Pending download |
| 9 | BlueberryDCM | Blueberry | 140 | CC BY 4.0 | ~107 MB | Pending download |
| 10 | Fruit ImageNet | Apple, Cherry, Peach, Plum, Apricot, Nectarine | Large | CC BY 4.0 | ~8.4 GB | Pending download |
| 11 | YEESI Dataset | Lettuce, Kale, Leek, Sunflower | 7,992 | CC0? | ~19 GB | License verification needed |

## v2 Acquisition (After v1 Model Release)

| Class | Target | Notes |
|-------|--------|-------|
| Basil | 500+ images | Culinary herb, high gardener value |
| Cilantro | 500+ images | Culinary herb, high gardener value |
| Parsley | 500+ images | Culinary herb, high gardener value |
| Dill | 500+ images | Culinary herb, high gardener value |
| Chives | 500+ images | Culinary herb, high gardener value |
| Mint | 500+ images | Culinary herb, high gardener value |
| Rosemary | 500+ images | Culinary herb, high gardener value |
| Thyme | 500+ images | Culinary herb, high gardener value |
| Kale | 500+ images | Leafy green, high gardener value |
| Lettuce | 1,000+ images | Leafy green, very high gardener value |
| Spinach | 1,000+ images | Leafy green, high gardener value |
| Swiss Chard | 500+ images | Leafy green, moderate gardener value |
| Brussels Sprouts | 500+ images | Brassica, seasonal interest |
| Sweet Potato | 1,000+ images | High-calorie staple, warm climates |
| Watermelon | 1,000+ images | Popular fruit, warm climates |
| Cantaloupe | 500+ images | Popular fruit, warm climates |
| Pear | 500+ images | Fruit tree, common in gardens |
| Peach | 500+ images | Fruit tree, common in gardens |
| Cherry | 500+ images | Fruit tree, common in gardens |
| Plum | 500+ images | Fruit tree, common in gardens |
| Apricot | 500+ images | Fruit tree, moderate gardener value |
| Nectarine | 500+ images | Fruit tree, moderate gardener value |
| Blackberry | 1,000+ images | Berry, common in gardens |
| Grape | 1,000+ images | Vine, common in gardens |
| Asparagus | 500+ images | Perennial vegetable, high gardener value |
| Rhubarb | 500+ images | Perennial vegetable, moderate gardener value |

## v3 Acquisition (Long-term / Specialized)

| Domain | Target | Notes |
|--------|--------|-------|
| DISEASE / DISORDER | Expand to 20+ classes | Current: 8 classes, 414 images |
| INSECT / PEST | Beneficial + harmful insects | New recognition domain |
| WEED | Common garden weeds | New recognition domain |
| GROWTH STAGE | Seedling → mature stages | New recognition domain |
| PLANT PART | Leaves, stems, flowers, fruit | Improve part-specific recognition |

## Acquisition Budget Constraints

- Target datasets with CC BY, CC0, MIT, Apache-2.0 licenses
- Avoid datasets requiring commercial purchase unless uniquely valuable
- Prefer datasets with real-world field photography over lab/synthetic
- Prefer datasets with multiple growth stages and diverse backgrounds
- Minimum threshold: 200 usable images per class for v1
- Preferred threshold: 500+ usable images per class for v2

## Dataset Quality Checklist

For each candidate dataset:
- [ ] License verified from primary source
- [ ] Commercial use confirmed
- [ ] Attribution requirements documented
- [ ] Image count verified
- [ ] Class labels reviewed for taxonomy match
- [ ] Sample images inspected for quality
- [ ] Real-world vs synthetic assessment completed
- [ ] Duplicate check against existing corpus
- [ ] Provenance documented
