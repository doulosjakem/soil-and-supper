# Soil & Supper — ML Taxonomy

## 1. Overview

This document defines the recommended plant identification taxonomy for the Soil & Supper Android application.

The taxonomy is designed for:

- North American home gardeners
- Visual distinguishability
- Commercially usable training data availability
- Mobile-friendly model size (40–60 classes)
- Future expandability

## 2. Design Principles

1. **Species-level, not variety-level**: Varieties are grouped unless visually distinct.
2. **Commonness first**: Prioritize plants grown by >5% of North American home gardeners.
3. **Visual distinguishability**: Group only when a casual gardener cannot reliably tell them apart.
4. **Commercial data availability**: Only include classes for which we can obtain legally usable training images.
5. **Garden context**: Include vegetables, fruits, herbs, berries, and common garden flowers.

## 3. Final Recommended Taxonomy (v1)

### Tier 1 — Core Vegetables (High Priority)

| # | Class | Scientific Name | Priority | Rationale |
|---|-------|----------------|----------|-----------|
| 1 | Tomato | Solanum lycopersicum | Critical | 86% of gardeners grow; visually distinct |
| 2 | Pepper (sweet) | Capsicum annuum | High | 49% of gardeners; bell/sweet peppers visually distinct from hot peppers |
| 3 | Pepper (hot) | Capsicum annuum | High | Jalapeño, habanero, etc. visually distinct from sweet peppers |
| 4 | Cucumber | Cucumis sativus | High | 43% of gardeners; distinct from squash/melon |
| 5 | Bean | Phaseolus vulgaris | High | 28% of gardeners; green/yellow/wax beans grouped |
| 6 | Carrot | Daucus carota | High | Common; distinct root vegetable |
| 7 | Corn | Zea mays | High | Sweet corn; visually distinct |
| 8 | Onion | Allium cepa | High | Bulb onions; distinct |
| 9 | Potato | Solanum tuberosum | High | 23% of gardeners; distinct |
| 10 | Broccoli | Brassica oleracea var. italica | Medium | 22% of gardeners; distinct |
| 11 | Cabbage | Brassica oleracea var. capitata | Medium | Common; distinct head structure |
| 12 | Lettuce | Lactuca sativa | Medium | 29% of gardeners; leafy greens |
| 13 | Spinach | Spinacia oleracea | Medium | Common leafy green |
| 14 | Pea | Pisum sativum | Medium | Common; distinct pods/vines |
| 15 | Radish | Raphanus sativus | Medium | Common root; fast-growing |

### Tier 2 — Squash, Melons, and Cucurbits (Medium Priority)

| # | Class | Scientific Name | Priority | Rationale |
|---|-------|----------------|----------|-----------|
| 16 | Summer Squash | Cucurbita pepo | Medium | Zucchini, yellow squash; visually similar |
| 17 | Winter Squash | Cucurbita spp. | Medium | Butternut, spaghetti, acorn; distinct from summer squash |
| 18 | Watermelon | Citrullus lanatus | Low | Distinct from other melons |
| 19 | Cantaloupe | Cucumis melo var. cantalupensis | Low | Distinct from watermelon |
| 20 | Pumpkin | Cucurbita pepo | Low | Visually distinct from other squash |

### Tier 3 — Root and Stem Vegetables (Medium Priority)

| # | Class | Scientific Name | Priority | Rationale |
|---|-------|----------------|----------|-----------|
| 21 | Beet | Beta vulgaris | Medium | Distinct root |
| 22 | Turnip | Brassica rapa subsp. rapa | Low | Similar to radish but larger |
| 23 | Sweet Potato | Ipomoea batatas | Low | Distinct from regular potato |

### Tier 4 — Herbs (Medium Priority)

| # | Class | Scientific Name | Priority | Rationale |
|---|-------|----------------|----------|-----------|
| 24 | Basil | Ocimum basilicum | Medium | Common herb; distinct leaves |
| 25 | Cilantro | Coriandrum sativum | Medium | Common herb; distinct |
| 26 | Parsley | Petroselinum crispum | Low | Common herb |
| 27 | Dill | Anethum graveolens | Low | Common herb |
| 28 | Chives | Allium schoenoprasum | Low | Distinct from onion |
| 29 | Rosemary | Salvia rosmarinus | Low | Distinct woody herb |
| 30 | Thyme | Thymus vulgaris | Low | Small leaves, distinct |
| 31 | Oregano | Origanum vulgare | Low | Similar to thyme but distinct |
| 32 | Sage | Salvia officinalis | Low | Distinct leaves |

### Tier 5 — Berries and Small Fruits (Low Priority)

| # | Class | Scientific Name | Priority | Rationale |
|---|-------|----------------|----------|-----------|
| 33 | Strawberry | Fragaria × ananassa | Medium | Common; distinct |
| 34 | Blueberry | Vaccinium corymbosum | Low | Common berry |
| 35 | Grape | Vitis spp. | Low | Common; vines |

### Tier 6 — Common Garden Flowers (Low Priority)

| # | Class | Scientific Name | Priority | Rationale |
|---|-------|----------------|----------|-----------|
| 36 | Marigold | Tagetes spp. | Low | Very common garden flower |
| 37 | Zinnia | Zinnia elegans | Low | Common garden flower |
| 38 | Nasturtium | Tropaeolum majus | Low | Common garden flower |
| 39 | Sunflower | Helianthus annuus | Low | Distinct; common |
| 40 | Cosmos | Cosmos bipinnatus | Low | Common garden flower |
| 41 | Petunia | Petunia spp. | Low | Common bedding plant |
| 42 | Begonia | Begonia spp. | Low | Common shade garden plant |

### Tier 7 — Edge Crops (Lowest Priority)

| # | Class | Scientific Name | Priority | Rationale |
|---|-------|----------------|----------|-----------|
| 43 | Eggplant | Solanum melongena | Low | Distinct; less common |
| 44 | Okra | Abelmoschus esculentus | Low | Southern US; distinct |
| 45 | Asparagus | Asparagus officinalis | Low | Perennial; distinct |
| 46 | Rhubarb | Rheum rhabarbarum | Low | Perennial; distinct |
| 47 | Celery | Apium graveolens | Low | Distinct stalks |
| 48 | Leek | Allium ampeloprasum var. porrum | Low | Similar to onion but distinct |
| 49 | Fennel | Foeniculum vulgare | Low | Distinct herb/vegetable |
| 50 | Artichoke | Cynara cardunculus var. scolymus | Low | Distinct; Mediterranean |

### Deferred to v2

- More specific herb varieties (e.g., Thai basil vs. sweet basil)
- More specific flower varieties
- Tree fruits (apple, pear, peach) — require different model architecture (tree/fruit vs. plant)
- Grains (wheat, oats) — niche for home gardeners
- Mushrooms — not plants, different domain
- Weeds — separate negative-example dataset

## 4. Grouping Decisions and Rationale

### Beans (Phaseolus vulgaris)
**Decision**: Group all common beans into one class.
**Rationale**: Green beans, wax beans, and snap beans are visually similar at the garden stage. Dry beans (pinto, kidney, black) are similar when growing but different when harvested. For MVP, group as "Bean" and potentially split in v2.

### Peppers (Capsicum annuum)
**Decision**: Split into Sweet Pepper and Hot Pepper.
**Rationale**: Sweet peppers (bell, pimento) and hot peppers (jalapeño, habanero) have distinct shapes, sizes, and colors that are visually meaningful. Gardeners care about this distinction.

### Squash/Melons
**Decision**: Summer squash, winter squash, watermelon, cantaloupe, and pumpkin are separate classes.
**Rationale**: These are visually distinct at both plant and fruit stages. However, data availability for melons may be limited.

### Herbs
**Decision**: Individual herbs are separate classes.
**Rationale**: While some herbs look similar (thyme/oregano), they have distinct culinary uses and gardeners want to identify them correctly. However, data availability may be challenging.

## 5. Likely Confusion Pairs

Based on visual similarity:

1. **Summer Squash ↔ Winter Squash**: Both are Cucurbita pepo in some cases.
2. **Cucumber ↔ Summer Squash**: Both are cucurbits with similar leaf shapes.
3. **Watermelon ↔ Cantaloupe**: Both are melons, similar vine growth.
4. **Tomato ↔ Eggplant**: Both are Solanum, similar flower/fruit shapes.
5. **Spinach ↔ Lettuce**: Both are leafy greens.
6. **Cilantro ↔ Parsley**: Similar leaf shapes.
7. **Dill ↔ Fennel**: Similar feathery foliage.
8. **Thyme ↔ Oregano**: Similar small-leaf herbs.
9. **Onion ↔ Leek**: Both are Allium.
10. **Bean ↔ Pea**: Both are legumes with podded fruit.

## 6. Class Aliases and Synonyms

For model training and UI display:

| Model Class | Aliases / Synonyms |
|-------------|-------------------|
| Tomato | tomato, tomatoes |
| Pepper (sweet) | bell pepper, sweet pepper, capsicum |
| Pepper (hot) | chili pepper, chile pepper, jalapeño, habanero |
| Cucumber | cucumber, cukes |
| Bean | bean, green bean, snap bean, wax bean, pole bean, bush bean |
| Carrot | carrot, carrots |
| Corn | corn, sweet corn, maize |
| Onion | onion, onions, bulb onion |
| Potato | potato, potatoes |
| Broccoli | broccoli |
| Cabbage | cabbage, head cabbage |
| Lettuce | lettuce, leafy lettuce |
| Spinach | spinach |
| Pea | pea, peas, garden pea, snap pea, snow pea |
| Radish | radish, radishes |
| Summer Squash | summer squash, zucchini, yellow squash, courgette |
| Winter Squash | winter squash, butternut, spaghetti squash, acorn squash |
| Watermelon | watermelon, water melon |
| Cantaloupe | cantaloupe, muskmelon |
| Pumpkin | pumpkin, pumpkins |
| Beet | beet, beets, beetroot |
| Turnip | turnip, turnips |
| Sweet Potato | sweet potato, yam |
| Basil | basil, sweet basil, Thai basil |
| Cilantro | cilantro, coriander, Chinese parsley |
| Parsley | parsley |
| Dill | dill |
| Chives | chives, garlic chives |
| Rosemary | rosemary |
| Thyme | thyme |
| Oregano | oregano, marjoram |
| Sage | sage, common sage |
| Strawberry | strawberry, strawberries |
| Blueberry | blueberry, blueberries |
| Grape | grape, grapes |
| Marigold | marigold, tagetes |
| Zinnia | zinnia, zinnias |
| Nasturtium | nasturtium |
| Sunflower | sunflower, sunflowers |
| Cosmos | cosmos, cosmos flower |
| Petunia | petunia, petunias |
| Begonia | begonia, begonias |
| Eggplant | eggplant, aubergine, brinjal |
| Okra | okra, gumbo, lady's finger |
| Asparagus | asparagus |
| Rhubarb | rhubarb |
| Celery | celery |
| Leek | leek, leeks |
| Fennel | fennel, common fennel |
| Artichoke | artichoke, globe artichoke |

## 7. Scientific Names Reference

Scientific names are included in the model manifest for:

- Disambiguation in training data
- Cross-referencing with botanical datasets
- Future multilingual support
- Precision in dataset curation

## 8. Priority and Data Requirements

### Critical (must have for MVP)
- Tomato
- Pepper (sweet + hot)
- Cucumber
- Bean
- Carrot
- Corn
- Lettuce/Spinach (grouped as leafy greens)

### High (should have for MVP)
- Onion
- Potato
- Broccoli
- Cabbage
- Strawberry

### Medium (desired for MVP)
- Pea
- Radish
- Summer/Winter Squash
- Basil + common herbs

### Low (acceptable to defer)
- Melons, pumpkins
- Berries (blueberry, grape)
- Flowers
- Edge crops (eggplant, okra, asparagus)

## 9. Data Sufficiency Assessment

Based on preliminary research:

| Class | Estimated Available Images | Status |
|-------|---------------------------|--------|
| Tomato | 5,000+ | Sufficient |
| Pepper | 4,000+ | Sufficient |
| Cucumber | 3,000+ | Sufficient |
| Bean | 3,000+ | Sufficient |
| Carrot | 2,000+ | Marginal |
| Corn | 3,000+ | Sufficient |
| Onion | 2,000+ | Marginal |
| Potato | 2,000+ | Marginal |
| Broccoli | 1,500+ | Marginal |
| Cabbage | 1,500+ | Marginal |
| Lettuce | 1,500+ | Marginal |
| Spinach | 1,000+ | Insufficient |
| Pea | 1,000+ | Insufficient |
| Radish | 1,500+ | Marginal |
| Summer Squash | 2,000+ | Marginal |
| Winter Squash | 1,500+ | Marginal |
| Watermelon | 1,000+ | Insufficient |
| Cantaloupe | 800+ | Insufficient |
| Herbs (each) | 200-800 | Insufficient individually |
| Flowers (each) | 100-500 | Insufficient individually |

**Key finding**: Most vegetables have marginal to insufficient data from current known sources. The training pipeline must support:

1. Automated acquisition from multiple sources
2. Deduplication and quality filtering
3. Data augmentation
4. Targeted acquisition for weak classes

## 10. Unknown / Other Strategy

**Recommendation**: Confidence thresholding, not an explicit "Unknown" class.

Implementation:
- If top-1 confidence < 0.40, display "Uncertain" rather than a specific class name.
- Optionally show top-3 predictions.
- Do not create a catch-all "Unknown" class from random Internet images.

Rationale:
- Unknown classes trained on random images degrade performance on known classes.
- Confidence thresholding is simpler and more honest.
- The UI already allows users to correct identifications.

## 11. Hard Negative Data

**Recommendation**: Add 2–4 classes of common North American weeds and non-target plants.

Candidates:
- Dandelion (Taraxacum officinale)
- Clover (Trifolium spp.)
- Crabgrass (Digitaria spp.)
- Common lambsquarters (Chenopodium album)

Source: Public domain / CC0 weed datasets.

Purpose: Teach the model "this is not a crop" rather than forcing every image into a crop class.

## 12. Revision History

- 2026-08-14: Initial taxonomy v1 — 50 classes across 7 tiers.
