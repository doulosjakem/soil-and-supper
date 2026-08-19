# Soil & Supper — AI / Vision Architecture

**Status**: Architecture Decision Document  
**Scope**: Cross-cutting — informs CMP migration and ML workstream  
**Audience**: CMP migration agent, ML workstream agent, platform implementers  

---

## 1. Conceptual Architecture

Soil & Supper is intended to support several natural interfaces to the same garden:

- Visual Garden UI
- Text conversation
- Voice conversation
- Camera / plant recognition
- Garden-plan / document import

These are NOT separate garden systems. They are interfaces into the same underlying Garden Domain and GardenRepository.

```
User
  ↓
Voice / Text / Camera / Document
  ↓
AI / Interpretation Layer
  ↓
Domain operations / queries
  ↓
Garden Domain + GardenRepository
  ↓
Garden DB
```

**CURRENT PRODUCT DIRECTION**: The Garden Domain and GardenRepository remain the single source of truth for garden state. AI is an interface layer, not the garden brain.

---

## 2. AI Is Not the Source of Truth

The domain/repository is authoritative.

AI may:
- Interpret user input
- Answer questions
- Identify plants
- Propose changes
- Create structured proposals

AI must NOT:
- Silently mutate garden state
- Perform arbitrary database writes
- Bypass domain validation

Actual state mutation must go through validated domain/repository operations.

**CURRENT**: PlanningEngine remains deterministic and read-only. It must never mutate garden state, never automatically mark spaces open, never auto-create succession plans or fulfill Desires, and never invoke AI or weather APIs. Planning suggestions are derived output, never persisted as authoritative garden facts.

---

## 3. Camera / Vision Architecture — Two-Stage Recognition

**FUTURE IMPLEMENTATION** — intended product direction, not yet built.

### Stage 1 — Live Camera

While the camera is open:
- Run a lightweight local model
- Prioritize very low latency
- Provide rough real-time perception
- Detect/locate plants where possible
- Provide rough classification/confidence
- Potentially identify obvious crops/weeds
- Potentially give framing/quality guidance

The live model does NOT need to provide definitive identification. Its purpose is responsiveness. The experience should feel immediate.

### Stage 2 — Captured Image

When the user takes a photo:
- Freeze the selected image
- Perform more careful analysis
- Use a higher-quality local model/pipeline where available
- Use garden context
- Use known crops, varieties, locations, dates, and season where appropriate
- Evaluate confidence
- Return a more deliberate identification/result

The system should prefer local inference.

---

## 4. Local-First + Online Fallback

**CURRENT PRODUCT DIRECTION**: Soil & Supper is offline-first. Garden functionality must continue to work without network access.

**FUTURE IMPLEMENTATION**: Plant recognition should preferably happen locally. If local recognition is uncertain, the application may optionally use online research/identification.

Conceptual preference options:
- Local only
- Ask when needed
- Allow online identification automatically

**Architectural contract**:
- Local-first
- Optional online fallback
- User-controlled

Online identification should NOT be silently mandatory. The user should have a setting controlling this behavior.

---

## 5. Online Identification Is Not Training Consent

**CURRENT PRODUCT DIRECTION**: These are TWO DIFFERENT permissions/settings. Do not combine them.

A. Online Identification — Permission for a captured image to be sent to an external/online identification service when local recognition is insufficient.

B. Model Improvement Contribution — Permission for eligible user images and confirmed labels to be retained/shared for improving future Soil & Supper recognition models.

A user may permit online identification while refusing model-improvement data sharing. A user may also opt into model improvement while preferring local identification.

---

## 6. User-Contributed Training Data

**FUTURE IMPLEMENTATION** — intended UX, not yet built.

The intended UX is NOT a permission prompt after every photograph. Instead:
- User makes a one-time choice in onboarding/settings
- Contribution preference persists
- Eligible images may be contributed automatically according to that preference
- User can later change the preference
- There should eventually be a way to manage/review contribution settings/history

Conceptual pipeline:
```
user opts in once
    ↓
eligible confirmed observations
    ↓
candidate contribution
    ↓
dataset curation
    ↓
future model development
```

**CRITICAL**: User-contributed images MUST NOT automatically enter production training. They should enter a separate candidate/contribution pipeline.

Future training requires:
- Provenance
- Consent state
- Label information
- Quality filtering
- Duplicate detection
- Appropriate verification
- Commercial/licensing review where applicable
- Dataset curation

The ML workstream remains responsible for determining whether contributed data is actually suitable for training.

---

## 7. Recognition Scope

**CURRENT PRODUCT DIRECTION**: The goal is NOT universal plant identification.

The product should prioritize high-value practical recognition.

Initial recognition priorities should include:
- Common garden crops
- Common garden plants/herbs
- Common weeds
- Grains / common cereal crops
- High-value plant diseases/pests as the ML roadmap develops

The system should eventually support broader recognition through a combination of:
- Local models
- Garden context
- Online fallback
- Future model improvements

The UX should prioritize usefulness over claims of universal recognition.

Unknown/low-confidence results are acceptable. The system must be able to say:
```
"I don't recognize this confidently."
```
rather than fabricating certainty.

---

## 8. Garden Context

**FUTURE IMPLEMENTATION** — intended capability, not yet built.

Plant recognition should eventually be garden-aware. The AI/vision system may use relevant local garden context such as:
- Growing space
- Known crop
- Variety
- Planting date
- Current season
- Previous/current occupancy
- Nearby planned crops
- Prior observations

Example: If the user photographs a plant in a space known to contain Blue Lake beans, that context can inform interpretation.

However: Context should influence ranking/interpretation, not force an incorrect answer. The system must retain the ability to identify:
```
"This doesn't look like what you planted here."
```

---

## 9. Confirmation / Feedback Loop

**FUTURE IMPLEMENTATION** — intended flow, not yet fully built.

```
Local recognition
    ↓
uncertain
    ↓
optional online research
    ↓
candidate identification
    ↓
user confirmation/correction
    ↓
garden observation
    ↓
optional contribution to future dataset
```

User confirmation is valuable training metadata. However, a user-confirmed image should still go through dataset curation before becoming training data.

**CURRENT**: Corrections are stored. The UI must always allow the user to override the model.

---

## 10. Garden-Plan / Document Import

**FUTURE IMPLEMENTATION** — intended capability, not yet built.

AI-assisted garden-plan import is an intended capability. A user should eventually be able to provide something such as:
- A typed garden plan
- Spreadsheet
- PDF
- Image
- Notes
- Handwritten plan

and ask Soil & Supper to populate the garden.

Conceptual pipeline:
```
Document/image
    ↓
AI extraction
    ↓
Structured Import Proposal
    ↓
Domain validation
    ↓
Human confirmation where ambiguity exists
    ↓
GardenRepository
    ↓
Normal Garden Timeline
```

The AI should NOT silently mutate the database from an ambiguous document. It should distinguish:
- Explicit historical events
- Current state
- Planned future events
- Projected timing
- Conditional plans
- Notes/tasks
- Uncertain interpretations

Do not invent dates or facts that the source document does not contain.

The existing 2026 Master Garden Plan is a representative example of the type of document this system should eventually handle.

---

## 11. AI Is an Interface, Not the Garden Brain

**CURRENT PRODUCT DIRECTION**: Voice, text, camera, and document import should all eventually interact with the same Garden Domain.

For example:
- "I planted carrots today."
- "I pulled the beans."
- "What's this plant?"
- "What can I plant after this?"
- "Import my garden plan."

These should ultimately resolve through the same authoritative garden state.

AI should not directly perform arbitrary database mutations.

Prefer explicit domain operations such as:
- Record planting
- Record harvest
- End occupancy
- Add observation
- Update seed inventory
- Create import proposal
- Confirm identification

The exact API names should be determined by the existing domain architecture.

---

## 12. CMP Implications

Do NOT implement these features. Instead, identify architectural boundaries the current CMP migration should avoid making impossible.

### What belongs in commonMain
- Garden domain models (Room-free)
- Repository interfaces
- PlanningEngine (read-only, deterministic)
- GardenService
- CropKnowledge
- GardenTimelineState
- Shared Compose UI (Garden Timeline)
- Platform-agnostic AI orchestration logic
- AI result types (e.g., PlantIdentification)
- Import proposal / structured result types

### What belongs behind platform-specific interfaces
- Camera access (Android CameraX, iOS AVFoundation)
- Microphone / speech (Android SpeechRecognizer, iOS Speech framework)
- Image representation (android.graphics.Bitmap vs. platform-agnostic abstraction)
- Local model inference runtime (platform-specific TFLite / Core ML bindings)
- Platform-specific AI service integrations

### Local model inference abstraction
Local model inference should eventually be abstracted behind a common interface with platform-specific implementations. The common side defines the contract (input image, output identification); the platform side handles the actual model execution.

### GardenRepository / domain operations
GardenRepository and domain operations remain shared. Future AI capabilities must consume garden state through the same repository interfaces used by the UI, without coupling the domain to a particular model or vendor.

### Important boundary
The CMP migration must not make it impossible to:
1. Replace or swap recognition models without domain changes
2. Add camera/speech platforms without rewriting domain logic
3. Introduce AI orchestration in common code while keeping hardware access platform-specific

---

## 13. ML Implications

Do NOT modify ML files. Document only the architectural relationship.

The ML workstream remains responsible for:
- Model development
- Dataset acquisition
- Licensing
- Dataset curation
- Training
- Evaluation
- Commercial-readiness decisions

The future vision architecture should be able to consume versioned local models. It should not assume a particular model architecture.

The ML pipeline should eventually be able to produce models suitable for:
- Live low-latency inference (Stage 1)
- Captured-image higher-quality inference (Stage 2)

These may be different models/pipelines.

**Existing ML strategy alignment**:
- `docs/ML_MODEL_STRATEGY.md` defines the v1 disease classifier baseline (MobileNetV3 Large, flat classifier, 14 classes).
- `docs/ML_TAXONOMY.md` defines the longer-term modular taxonomy (domain router + hierarchical classifiers).
- `docs/dataset-plan.md` defines the crop recognition dataset acquisition plan.

The AI/Vision architecture described here is platform- and model-agnostic. It consumes whatever models the ML workstream produces.

---

## 14. Privacy / Offline-First Principle

**CURRENT PRODUCT DIRECTION**:

> If the user has not enabled a feature that sends data online, the garden and local recognition experience should remain usable offline.

Do not make the user repeatedly approve routine operations.

Permissions/settings should be understandable and persistent.

Do not design the system around repeated per-photo consent prompts.

At the same time, do not imply that contributed data is anonymous, private, or commercial-safe unless the eventual implementation actually guarantees that.

---

## 15. What Not To Do

Do NOT:
- Implement camera recognition
- Implement AI chat
- Implement voice
- Implement online lookup
- Implement dataset contribution
- Implement document import
- Modify the ML pipeline
- Modify CMP source code
- Modify Swift/iOS source code
- Modify PlanningEngine
- Redesign the Garden Timeline
- Add new product modes

This document is documentation/architecture only.

---

## 16. Existing Artifacts and Alignment

### Canonical design document
`DESIGN.md` is the canonical Android product design document. It defines the MVP goals, data model, screens, milestones, and offline-first requirement.

### CMP migration docs
- `docs/architecture/ARCHITECTURE_ASSESSMENT.md` — repository audit and classification
- `docs/architecture/MIGRATION_PLAN.md` — sequencing and target module layout
- `docs/architecture/PERSISTENCE_DECISION.md` — Room-free domain models and repository abstraction

### ML docs
- `docs/ML_MODEL_STRATEGY.md` — v1 model architecture and training strategy
- `docs/ML_TAXONOMY.md` — full recognition taxonomy and classifier architecture
- `docs/ML_ACQUISITION.md` — data acquisition workflow
- `docs/dataset-plan.md` — crop recognition dataset plan

### Shared code
- `shared/src/commonMain/.../domain/model/PlantIdentification.kt` — platform-agnostic identification result type
- `shared/src/commonMain/.../repository/GardenRepository.kt` — authoritative garden operations interface
- `shared/src/commonMain/.../repository/PlantRepository.kt` — plant operations interface

### Current Android coupling
- `app/src/main/java/.../domain/model/PlantIdentifier.kt` — Android-specific interface using `android.graphics.Bitmap`
- `app/src/main/java/.../domain/model/MockPlantIdentifier.kt` — mock implementation
- `app/src/main/java/.../ui/IdentifyScreen.kt` — Android-only identification screen

These Android-specific types will need to be re-evaluated during CMP migration to move image handling and model inference behind platform-abstracted boundaries.

---

*Document generated as part of the Soil & Supper documentation/architecture workstream. Does not modify application source, ML pipeline, or dataset files.*
