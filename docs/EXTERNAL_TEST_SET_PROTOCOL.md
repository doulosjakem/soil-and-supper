# External Test Set Protocol

## 1. Purpose

This document defines how Soil & Supper will establish, validate, and use an **external generalization test set** — a collection of plant images drawn from sources completely independent of the commercial training corpus.

The external test set exists to answer one question:

> "How accurately does our model recognize the kinds of photographs an actual Soil & Supper gardener is likely to take?"

It is NOT intended to:
- Replace the existing development validation/test splits
- Become training data
- Be used for hyperparameter tuning
- Be repeatedly evaluated until the numbers look good

## 2. Distinction from Training, Validation, and Test Data

| Data Set | Purpose | Source Overlap Allowed | Used for Tuning |
|----------|---------|------------------------|-----------------|
| **Training** | Model weight updates | No (within split) | Yes |
| **Validation** | Development monitoring, early stopping, checkpoint selection | Yes (within commercial core) | Yes |
| **Test (Strategy A)** | Final model evaluation on held-out commercial data | Yes (within commercial core) | No |
| **External Generalization Test** | Measurement of real-world generalization | **No — must be independent** | **No — immutable** |

The existing Strategy A split (69,040 train / 14,789 val / 14,813 test) remains the primary development split. It is useful for training stability and ordinary validation. However, because its sources overlap with the training set, it cannot provide a trustworthy estimate of generalization to unseen garden photographs.

## 3. Acceptance Criteria for External Test Candidates

A dataset may be promoted to the official external test set only if it satisfies ALL of the following:

### 3.1 License and Commercial Compatibility
- License must explicitly permit:
  - Commercial use
  - Model evaluation / inference
  - Local storage of copies
  - Derived outputs (evaluation metrics, confusion matrices)
- Acceptable licenses: CC0, CC BY 4.0, CC BY-SA 4.0 (with attribution), MIT, Apache 2.0, Public Domain
- Unacceptable licenses: CC BY-NC, CC BY-NC-SA, CC BY-NC-ND, "all rights reserved", unknown
- If license cannot be verified from a primary source: mark REVIEW, do not include

### 3.2 Provenance and Independence
- Must originate from a source NOT in the commercial training core:
  - Not PlantVillage
  - Not Irish Potato (Zenodo 8286529)
  - Not PlantDoc
  - Not Grapevine (Zenodo 17343474)
  - Not Common Beans
  - Not SegPPD-101
- Must not be a re-packaging of any of the above
- Must have clear attribution: authors, institution, publication, DOI or URL

### 3.3 Capture Context
- Prefer real-world field or home-garden photographs
- Must NOT be exclusively lab-controlled images with uniform backgrounds
- Different geographic region from training data preferred
- Different camera/device types preferred
- Different time period preferred

### 3.4 Label Quality
- Expert annotation preferred
- Clear class labels
- Labels must be mappable to the Soil & Supper taxonomy OR explicitly marked as unmappable
- Do not force ambiguous labels into existing classes

### 3.5 Size and Scope
- Minimum viable size: 200 images per class for classes that exist in the taxonomy
- Do not maximize size at the expense of independence
- A 500-image genuinely independent test set is more valuable than 50,000 images from a near-duplicate source

### 3.6 Duplicate Independence
- Must pass exact-duplicate check against the entire commercial training corpus
- Must pass perceptual-hash check against the entire commercial training corpus
- Any image with a near-duplicate in training must be excluded from the test set

## 4. Taxonomy Mapping Rules

The external test set does NOT need to cover all 30 Soil & Supper taxonomy classes.

Mapping rules:
1. Map external labels to Soil & Supper classes ONLY when the mapping is unambiguous
2. If an external label could reasonably map to multiple Soil & Supper classes, mark it UNMAPPABLE
3. If an external label represents a class not in the Soil & Supper taxonomy, mark it OUT-OF-TAXONOMY
4. Do not invent new taxonomy entries to accommodate external labels
5. Document every mapping decision with rationale

Example:
- External: "Tomato leaf disease" → UNMAPPABLE (Soil & Supper distinguishes multiple tomato diseases)
- External: "Apple scab" → maps to `Apple_scab` (exact match)
- External: "Pear leaf spot" → OUT-OF-TAXONOMY (pear not in current taxonomy)

## 5. External Test Set Design

### 5.1 Immutability
Once promoted to official status, the external test set is **immutable**:
- No images added or removed
- No labels changed
- No augmentations applied
- No preprocessing beyond standardization required by the model

### 5.2 Versioning
Each official external test set receives a version tag:
```
external_test_v1_2026-08-18
```

Version tags are date-stamped and never reused.

### 5.3 Manifest Format
Every external test set manifest entry must contain:
```json
{
  "external_test_image_id": "diamos_plant_healthy_00001",
  "local_path": "/absolute/path/to/image.jpg",
  "source_dataset": "diamos_plant",
  "source_image_id": "original_filename.jpg",
  "source_path": "https://doi.org/10.5281/zenodo.5557313",
  "mapped_class": "Healthy",
  "original_class": "Healthy",
  "license": "CC BY 4.0",
  "license_url": "https://creativecommons.org/licenses/by/4.0/",
  "provenance": "Field-collected pear orchard, Italy, 2021",
  "acquisition_date": "2026-08-18",
  "test_set_version": "external_test_v1_2026-08-18",
  "sha256": "<hash>",
  "width": 1024,
  "height": 768,
  "mapping_rationale": "Exact match: healthy pear leaf → Healthy",
  "exclusion_reason": null
}
```

Fields:
- `mapped_class`: Soil & Supper taxonomy class, or `UNMAPPABLE` or `OUT-OF-TAXONOMY`
- `mapping_rationale`: Explanation of mapping decision
- `exclusion_reason`: If image was reviewed but excluded from the final test set, state why

### 5.4 Directory Structure
```
training_data/
  external_test/
    v1_2026-08-18/
      images/
        <source_dataset>/
          <class>/
            <image_id>.jpg
      external_test_manifest.jsonl
      metadata.json
      SHA256SUMS.txt
```

## 6. Overlap Check Procedure

Before any dataset becomes official:

1. **Exact duplicate check**: Compute SHA256 for every external image. Compare against:
   - `training_data/manifests/commercial_manifest.jsonl`
   - `training_data/manifests/commercial_train_manifest.json`
   - `training_data/manifests/commercial_val_manifest.json`
   - `training_data/manifests/commercial_test_manifest.json`

2. **Perceptual hash check**: Compute phash for every external image. Compare against the commercial core.

3. **Near-duplicate threshold**: If phash distance < 10 (Hamming), flag as ambiguous.

4. **Decision**:
   - Exact match: EXCLUDE from external test set
   - Near-duplicate (phash < 10): EXCLUDE unless manually verified as independent capture
   - Ambiguous: Mark REVIEW, do not include in official set

5. **Document decisions**: Every excluded image must have an entry in the manifest with `exclusion_reason`.

## 7. Evaluation Protocol

The external test set is used ONLY after model development is otherwise complete.

### 7.1 Required Metrics
For each evaluation run on the external test set, report:
- Overall accuracy
- Macro F1
- Per-class precision
- Per-class recall
- Confusion matrix
- Coverage / abstention rate (if the model supports "unknown")
- Per-source breakdown (if the external set contains multiple sources)

### 7.2 Evaluation Discipline
- Run external evaluation exactly once per model version
- Do not iterate on the external test set
- Do not tune hyperparameters based on external test results
- Do not add external test images to training after seeing results
- Report results with full transparency, including failures

### 7.3 Interpretation Guidance
External test performance should be interpreted as:
- **Lower bound on real-world performance** if the external set is harder than average user photos
- **Upper bound on real-world performance** if the external set is easier (e.g., still mostly lab-like)
- Not a guarantee of performance on any specific user's garden

## 8. Open-Set / Unknown Class Considerations

The eventual Soil & Supper model will encounter:
- Plants outside the 30-class taxonomy
- Poor-quality photographs
- Multiple diseases in one image
- Insects, nutrient problems, environmental damage
- Weeds and non-plant objects

The external test set should eventually include:
- **Known classes**: Images that map to existing taxonomy classes
- **Unknown/out-of-taxonomy**: Images of plants/diseases not in the taxonomy
- **Ambiguous**: Images where the disease is unclear even to a human
- **Poor quality**: Blurry, dark, occluded images

This allows eventual evaluation of:
- Closed-set accuracy (known classes only)
- Open-set abstention (does the model decline when uncertain?)
- Robustness to poor image quality

Do NOT implement an "unknown" classifier yet. Simply ensure the external test set infrastructure can accommodate these categories when needed.

## 9. Promoting a Candidate to Official Status

A candidate dataset is promoted to official external test set when:
1. All acceptance criteria in Section 3 are satisfied
2. Overlap check (Section 6) is passed
3. Manifest is complete and verified
4. Dataset is copied to immutable versioned directory
5. Manifest is committed to the repository
6. Documentation is updated

Promotion requires explicit review. Do not silently add images to the external test set.

## 10. Criteria for Rejecting a Candidate

Reject a candidate if:
- License is non-commercial or unclear
- Source overlaps with training data
- Labels are too ambiguous to map
- Dataset is a re-packaging of training data
- Provenance cannot be verified
- Image quality is too low to be meaningful

Document the rejection reason in `external_test_candidates.json`.

## 11. Parallel Acquisition Goals

Do not let external-test search replace training-data acquisition.

| Goal | Priority | Current Status |
|------|----------|----------------|
| Anthracnose replacement (training) | P1 | 0 commercial images |
| Rust additional source (training) | P2 | 1,308 images, weak |
| Downy_mildew second source (training) | P2 | 1,002 images, single-source |
| Peach_bacterial_spot second source (training) | P2 | 2,297 images, single-source |
| External generalization test set | P1 (evaluation) | No independent source identified yet |

A dataset can serve as:
- Training data supplement
- External test set
- Both
- Neither

These roles must be evaluated separately.

## 12. Phase 27 Status (2026-08-18)

### Verified Candidates
- **DiaMOS Plant Dataset** (Zenodo 5557313): CC BY 4.0 verified from primary source. 3,505 images (pear orchard, Italy). Only 1 mappable class (Healthy) with high confidence. Acquisition blocked by 13.1 GB file size and Zenodo browser verification.
- **FieldPlant** (Roboflow/IEEE Access 2023): CC BY 4.0 verified from primary source. 5,170 images (Cameroon plantations). 10+ mappable classes with high confidence. Acquisition blocked by Roboflow API authentication requirement and Kaggle JavaScript crash.

### Selected Candidate
FieldPlant was selected as the preferred candidate based on superior taxonomic coverage, field-realistic capture conditions, expert annotation, and geographic diversity.

### Acquisition Status
**FAILED** — No dataset was successfully acquired.
- Roboflow API requires authentication (API key)
- Kaggle page JavaScript crash / authentication required
- Zenodo browser verification required; DiaMOS download timed out at 396MB of 13.1GB

### Current Status
**NO_APPROVED_EXTERNAL_TEST_SET**

Neither candidate passed the REPRODUCIBLE acquisition gate. License verification passed for both, but practical download barriers prevent establishment of the external test set.

### Next Steps
1. Resolve FieldPlant download authentication (obtain Roboflow API key or Kaggle access)
2. Search for FieldPlant mirrors on alternative platforms (Hugging Face Datasets, academic repositories)
3. If FieldPlant remains inaccessible, search for DiaMOS subset or alternative smaller dataset
4. Evaluate PlantCLEF or other plant pathology challenge datasets with CC licensing
5. Contact FieldPlant authors directly for dataset access

### Audit Report
See: `training_data/reports/external_test_audit.json`
