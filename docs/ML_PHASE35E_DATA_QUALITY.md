# Soil & Supper — Phase 35E Data Quality Report

## 1. Corpus Composition

| Domain | Datasets | Approved Images | % of Total |
|--------|----------|-----------------|------------|
| CROP / PLANT ID | 5 | 8,147 | 90.8% |
| DISEASE / DISORDER | 2 | 821 | 9.2% |
| **Total** | **7** | **8,968** | **100%** |

## 2. Image Quality Metrics

| Metric | Value |
|--------|-------|
| Total images discovered | 35,790 |
| Valid images (pass quality checks) | 35,770 (99.9%) |
| Corrupt images | 20 (0.06%) |
| Too small (<64px) | 0 (0%) |
| Extreme aspect ratio (>10:1) | 0 (0%) |
| Blank images | 0 (0%) |
| Approved images | 8,968 (25.1% of valid) |
| Duplicates vs existing corpus | ~27,000 (included in valid count) |

## 3. Source Diversity

### CROP / PLANT ID Sources

| Dataset | Images | Domain | Classes | Source Type |
|---------|--------|--------|---------|-------------|
| hf_100crops | 3,489 | CROP | 100 | Object detection, real photos |
| hf_veg_bangladesh | 3,066 | CROP | 12 | Field photos, Bangladesh |
| hf_food_veg | 1,099 | CROP | 15 | Food photography, varied |
| hf_food_ingredients_v2 | 493 | CROP | 8 | Food photography, studio |
| hf_digigreen | 414 | DISEASE | 74 | Farmer-submitted field photos |

### Source Quality Assessment

**hf_100crops (MIT, 3,489 images)**
- Strengths: 100 crop classes, real-world photos, object detection annotations
- Weaknesses: Some classes are not garden-relevant (cotton, jute, rubber plant)
- Quality: HIGH

**hf_veg_bangladesh (CC BY 4.0, 3,066 images)**
- Strengths: Field photos from Bangladesh, 12 vegetable classes, mobile phone capture
- Weaknesses: Limited geographic diversity
- Quality: HIGH

**hf_food_veg (Apache-2.0, 1,099 images)**
- Strengths: Clean food photography, consistent lighting
- Weaknesses: Studio/controlled environment, limited to 15 classes
- Quality: MEDIUM-HIGH

**hf_food_ingredients_v2 (CC BY 4.0, 493 images)**
- Strengths: Food photography, some garden-relevant classes
- Weaknesses: Small dataset, food-focused not garden-focused
- Quality: MEDIUM

**hf_digigreen (CC BY 4.0, 414 images)**
- Strengths: Expert-annotated, farmer-submitted field photos, India
- Weaknesses: Disease/disorder domain, not plant ID
- Quality: HIGH (for disease domain)

## 4. Class Balance Analysis

### Well-Balanced (>500 images, multiple sources)
- Pepper (1,106, 5 sources)
- Bean (1,010, 3 sources)
- Onion (1,204, 3 sources)
- Tomato (579, 2 sources) — slightly below 500 but acceptable
- Potato (690, 3 sources)
- Eggplant (708, 3 sources)
- Cucumber (685, 3 sources)
- Corn (593, 3 sources)

### Moderate (100–500 images, 1–2 sources)
- Strawberry (503, 2 sources)
- Broccoli (251, 2 sources)
- Carrot (332, 2 sources)
- Beet (174, 2 sources)
- Apple (132, 2 sources)
- Garlic (89, 1 source)
- Cabbage (92, 1 source)
- Cauliflower (79, 1 source)
- Blueberry (40, 1 source)

### Weak (<100 images)
- None currently approved with <100 except Blueberry (40)

### Missing (0 images)
- 34 Tier 1 classes

## 5. Duplicate Analysis

| Check | Result |
|-------|--------|
| Duplicates vs commercial_manifest.jsonl | Included in counts |
| Duplicates vs exact_dedup_manifest.jsonl | Included in counts |
| Duplicates vs figshare_disease_manifest.jsonl | Included in counts |
| Inter-dataset duplicates | Not yet computed (requires cross-dataset hash comparison) |

**Note:** The current pipeline checks duplicates against existing corpora but does not deduplicate across incoming Phase 35D datasets. This should be addressed in future processing.

## 6. Label Quality

- All Phase 35D approved datasets use directory-based class labels
- Class mappings are applied via synonym dictionary
- Unmapped classes are recorded as candidate classes
- No automatic relabeling of unmapped classes
- Human review required for all candidate classes

## 7. Real-World vs Synthetic Assessment

| Dataset | Real-World % | Synthetic % | Notes |
|---------|-------------|-------------|-------|
| hf_100crops | ~95% | ~5% | Mostly field/garden photos |
| hf_veg_bangladesh | ~100% | 0% | Mobile phone field capture |
| hf_food_veg | ~80% | ~20% | Food photography, some studio |
| hf_food_ingredients_v2 | ~90% | ~10% | Food photography |
| hf_digigreen | ~100% | 0% | Farmer-submitted field photos |

## 8. Geographic Diversity

| Region | Datasets | Approx. Coverage |
|--------|----------|------------------|
| South Asia (Bangladesh, India) | 3 | hf_veg_bangladesh, hf_digigreen, hf_100crops |
| North America | 1 | hf_food_veg |
| Global (mixed) | 2 | hf_100crops, hf_food_ingredients_v2 |

**Gap:** Limited European, African, South American representation.

## 9. Data Quality Recommendations

1. **Add geographic diversity** — prioritize datasets from Europe, Africa, South America
2. **Add seasonal diversity** — current datasets are mostly summer/annual crops
3. **Add growth stage diversity** — include seedling, vegetative, flowering, fruiting stages
4. **Reduce studio images** — prioritize field/garden photography for v1
5. **Increase multi-source classes** — classes with only 1 source are fragile
6. **Address duplicate detection** — implement cross-dataset deduplication
7. **Verify YEESI license** — high potential for multiple gap classes
8. **Consider Herbs & Plants Dataset** — if budget allows, closes all herb gaps at once

## 10. Model Readiness Assessment

### Current State: NO-GO for 51-class model

| Criterion | Requirement | Current | Status |
|-----------|-------------|---------|--------|
| Classes with ≥200 images | 25+ | 8 | ❌ FAIL |
| Classes with ≥500 images | 20+ | 8 | ❌ FAIL |
| Multi-source classes | 15+ | 8 | ❌ FAIL |
| Geographic diversity | 3+ regions | 2 | ⚠️ WEAK |
| Real-world photos | >80% | ~95% | ✅ PASS |
| Commercial license | 100% | 100% | ✅ PASS |
| Duplicate rate | <10% | ~75% | ⚠️ HIGH |

### After Recommended Acquisitions: GO for 16-class model

With the 11 recommended acquisitions:
- Pea, Radish, Zucchini, Pumpkin, Grape, Raspberry, Blueberry, Lettuce, Kale, Leek, Apple, Cherry, Peach, Plum, Apricot, Nectarine would all have ≥200 images
- 16-class focused model becomes viable
- Geographic diversity improves
- Multi-source classes increase

---

**Recommendation:** Proceed with v1 acquisitions, then train focused 16-class model. Defer remaining 35 classes to v2/v3.
