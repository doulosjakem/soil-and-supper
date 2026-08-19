# Garden AI — MVP Design Document

## 1. Project Overview

Build a native Android app that acts as an offline-first personal garden assistant.

The long-term vision is:

> Plan → Grow → Identify → Harvest → Preserve → Eat

The MVP should focus on the middle of that loop:

> **Track plants → identify plants locally with AI → record harvests → get AI-powered cooking/preservation suggestions.**

The app should be designed so specialized local AI models can be added/swapped later without requiring major architectural changes.

This is an indie project and an AI-assisted development/learning project. Keep the implementation simple, maintainable, and intentionally small.

The primary development target is Android. The iOS version is a future target if the product is validated on Android first.

Development workflow:

WINDOWS PC
    ↓
Android development
    ↓
Local ML training on GTX 1060
    ↓
Android offline plant identification
    ↓
Google Play Store MVP
    ↓
Validate the product
    ↓
iOS version later if worthwhile

---

# 2. Primary Goals

The MVP must allow a user to:

1. Create and manage plants in their garden.
2. Add photos to plants.
3. Record notes/journal entries.
4. Record harvested produce.
5. View current harvest inventory.
6. Take/import a plant photo and have an on-device AI model identify it.
7. Confirm or correct the AI's identification.
8. Ask a local AI model what to cook or how to preserve available harvests.
9. Work primarily offline.

The MVP should be usable on a real Android device before additional features are added.

---

# 3. Explicit Non-Goals

DO NOT implement these in the MVP:

* User accounts
* Cloud synchronization
* Social features
* Backend server
* Weather API
* Push notifications
* Subscription system
* Advertising
* In-app purchases
* Full garden mapping
* Automated succession planting
* Complex disease diagnosis
* Canning/preservation safety database
* Multiple model download system
* User-generated community database
* Livestock management
* Shopping lists
* Desktop/web application
* iOS application (future target only)

These may be considered after the MVP is shipped.

---

# 4. Target Platform

Platform:

* Android
* Native Kotlin
* Jetpack Compose
* Android Studio
* Gradle

Prioritize modern Android APIs and simple native solutions.

Avoid unnecessary third-party dependencies.

The application should be structured so that it can eventually support on-device AI models using Google's supported on-device ML/model frameworks.

Do not prematurely commit the entire application to one particular AI model or inference runtime.

---

# 5. Core User Experience

The primary user flow should be:

## Add a plant

Home/Garden
→ Add Plant
→ Take/select photo
→ Enter plant name/variety
→ Enter planting date
→ Optionally enter garden location/bed
→ Save

## View a plant

Garden
→ Plant
→ See:

* Name
* Variety
* Photos
* Planting date
* Location
* Journal entries
* Harvest history

## Identify a plant

Garden
→ Identify Plant
→ Take/select photo
→ Run local vision model
→ Display likely identification and confidence
→ User confirms or corrects result
→ Optionally save as a plant

## Record a harvest

Plant
→ Add Harvest
→ Enter quantity
→ Enter unit
→ Enter date
→ Save

Example:

> Tomatoes — 8 lb — August 12

## Use the harvest

Harvest
→ Garden-to-Table AI
→ Show current available harvest
→ User asks:

> "What can I make with this?"

or:

> "What should I do with all these tomatoes?"

The local language model generates suggestions using the user's available harvest.

---

# 6. MVP Screens

Keep the navigation simple.

## Home / Garden

Display:

* Garden name
* Plants
* Quick action: Add Plant
* Quick action: Identify Plant
* Quick action: View Harvest

## Plant Detail

Display:

* Plant photo
* Plant name
* Variety
* Planting date
* Garden location
* Journal
* Harvests
* Add photo
* Add journal entry
* Add harvest

## Add/Edit Plant

Fields:

* Name
* Variety
* Planting date
* Location/bed
* Notes
* Photos

## Plant Identification

Display:

* Photo picker
* Identification result
* Confidence
* Confirm button
* Correct button

The user must always be able to override the model.

## Harvest

Display:

* Current inventory
* Harvest history
* Add harvest

## Garden-to-Table

Display:

* Available harvest
* Text input
* Suggested prompts

Examples:

* "What can I make tonight?"
* "How can I preserve these?"
* "What should I freeze?"
* "Give me three dinner ideas."

---

# 7. Data Model

Use a local persistent data store.

Prefer Android's native persistence technology where practical.

Core entities:

## Garden

Fields:

* id
* name
* location
* optional frost dates

## Plant

Fields:

* id
* name
* variety
* plantingDate
* location
* notes
* createdAt
* updatedAt

Relationships:

* Garden → Plants
* Plant → Photos
* Plant → JournalEntries
* Plant → Harvests

## PlantPhoto

Fields:

* id
* plantId
* local image reference
* createdAt

Images should be stored locally rather than embedding large image blobs directly in ordinary model records unless there is a strong reason to do otherwise.

## JournalEntry

Fields:

* id
* plantId
* date
* text

## Harvest

Fields:

* id
* plantId
* cropName
* quantity
* unit
* date
* notes

The model should be extensible but should NOT include speculative fields for future features.

---

# 8. AI Architecture

AI should be treated as a replaceable service layer.

Do not tightly couple Compose UI directly to a specific AI model.

Use interfaces similar to:

```kotlin
interface PlantIdentifier {
    suspend fun identify(image: Bitmap): PlantIdentification
}

interface HarvestAssistant {
    suspend fun generateResponse(
        prompt: String,
        harvest: List<Harvest>
    ): String
}
```

The exact implementation is up to the developer/agent, but preserve this separation.

The UI should not need to know which model is being used.

**Cross-cutting AI/Vision architecture** (camera, voice, text, document import, online fallback, contributions, garden context) is documented in `docs/architecture/AI_VISION_ARCHITECTURE.md`. That document defines the contract the CMP migration and ML workstream must honor.

---

# 9. Plant Identification AI

The MVP should support multiple local/on-device vision models organized by domain.

## Recognition Architecture

Use **specialized single-classifier models per domain** rather than one enormous flat classifier:

1. **CropClassifier** — 50 crop classes + Unknown
2. **WeedClassifier** — 21 weed classes + Unknown
3. **DiseaseClassifier** — 30 disease/problem classes + Unknown
4. **GrowthStageClassifier** — 6 growth stages (separate attribute, not per-crop)
5. **InsectClassifier** — 18 pest + 7 beneficial classes + Unknown

Each model is trained independently using TensorFlow Lite Model Maker with transfer learning (EfficientNet-Lite0 or MobileNetV3-Small backbone).

## Why specialized models

- Each model stays small and trainable on GTX 1060 6GB
- Poor data in one domain does not degrade another
- Easy to update one domain without retraining everything
- Matches how gardeners think: "Is this a weed? Is this a pest?"
- Each model can be optimized independently
- TFLite Model Maker supports this workflow natively

## Unknown / OOD handling

Primary mechanism: **confidence thresholding**, not a catch-all Unknown class.

- If top-1 confidence < 0.40, display "Uncertain — try a clearer photo"
- Optionally show top-3 predictions with confidence bars
- Do NOT train a catch-all "Unknown" class from random Internet images
- Include 2–4 explicit negative classes per domain where licensing permits
- UI should encourage multiple photos (leaf + fruit + whole plant) when confidence is low

## Growth stage strategy

Growth stage is a **separate model**, not embedded in crop/disease/weed models.

- GrowthStageClassifier predicts: Seedling, Vegetative, Flowering, Fruiting, Mature/Harvest, Senescing
- This model is crop-agnostic: it predicts stage regardless of plant type
- The Android app runs it alongside other classifiers when user selects "Check growth stage"

## Initial implementation goal

> Image → domain classifier → likely identification + confidence

The model does NOT need to diagnose diseases in the MVP.

It should return structured information where possible:

* Plant/crop/weed/insect/disease name
* Confidence
* Domain (which model made the prediction)

Example:

```text
Domain: Crop
Plant: Tomato
Confidence: 0.87
```

The user must be able to correct the result.

Corrections should be stored because they may eventually become useful training data.

Do not build model training into the app.

---

# 10. Garden-to-Table AI

The MVP should support one local language model.

The model receives structured context rather than simply dumping the entire database into a prompt.

Example context:

```text
Available harvest:
- Tomatoes: 8 lb
- Zucchini: 3
- Basil: 1 bunch
- Peppers: 4
```

The user can ask natural-language questions.

The model may provide:

* Recipe ideas
* Meal ideas
* Preservation ideas
* Freezing suggestions
* Dehydrating suggestions
* General storage ideas

IMPORTANT:

The AI must not be treated as the authoritative source for food-safety instructions.

For potentially safety-critical preservation questions, the app should eventually use a curated/authoritative food-preservation data source.

That safety database is OUT OF SCOPE for the MVP.

---

# 11. Offline-First Requirement

Core garden functionality must work without an internet connection.

This includes:

* Viewing plants
* Adding plants
* Editing plants
* Photos
* Journal entries
* Harvest records

AI functionality should also be designed around local inference.

If a required model is unavailable, the application should clearly explain that AI functionality is unavailable rather than silently sending user data to a cloud service.

Do not add a cloud AI fallback in the MVP unless explicitly requested later.

---

# 12. Model Abstraction

The long-term application may eventually have multiple specialized models:

1. Plant vision model (crops)
2. Weed identification model
3. Insect/pest identification model
4. Disease identification model
5. Growth stage model
6. Garden planning model
7. Cooking/preservation model

The MVP only needs:

1. Crop vision model (50 classes)
2. Disease vision model (30 classes)
3. Weed vision model (21 classes)
4. Growth stage model (6 stages)
5. Garden-to-table language model

Do not build the garden-planning, insect, or beneficial-insect models yet.

The architecture should allow them to be added later without redesigning the application.

Potential future interface:

```kotlin
interface GardenPlanner {
    suspend fun generatePlan(
        context: GardenContext
    ): GardenPlan
}
```

Do not implement this yet.

---

# 13. Succession Planting

Succession planting is a major future feature but is NOT part of the MVP.

Eventually the app should contain a deterministic garden planning engine based on:

* Crop
* Planting window
* Days to maturity
* Frost tolerance
* Harvest window
* Succession interval
* Available garden space

The eventual AI model should explain and interact with the results of this engine rather than being responsible for the underlying calculations.

Do not implement this during the MVP unless explicitly instructed.

---

# 14. Design Principles

## Keep it small

When choosing between two implementations, prefer the simpler one.

Do not build infrastructure for hypothetical future requirements.

## Local first

Garden data and photos should remain on the device in the MVP.

## AI is a tool, not the architecture

Do not make the entire application dependent on a particular model.

## Deterministic code for deterministic problems

Use normal application logic for:

* Dates
* Quantities
* Harvest inventory
* Plant records
* Calculations
* Planning rules

Use AI for:

* Image interpretation
* Natural-language interaction
* Recommendations
* Summarization

## User remains in control

AI suggestions should never silently modify garden data.

Require explicit user confirmation for important changes.

---

# 15. Development Strategy

This project will be built using an agentic coding tool.

The developer is experienced with software development but is relatively inexperienced with Kotlin/Jetpack Compose.

The coding agent should therefore:

1. Make small, reviewable changes.
2. Explain important Kotlin/Compose concepts when introducing them.
3. Avoid unnecessary abstractions.
4. Build and test after meaningful changes.
5. Report compiler errors rather than guessing around them.
6. Keep changes focused on the current task.
7. Avoid modifying unrelated files.
8. Do not introduce dependencies without justification.
9. Do not implement future features without explicit instruction.

The human developer makes product and architectural decisions.

The coding agent implements them.

---

# 16. Development Milestones

Build in this order.

## Milestone 1 — Empty App

* Create Android Studio project
* Jetpack Compose navigation
* Basic app shell
* Build successfully on emulator

## Milestone 2 — Garden CRUD

* Garden
* Plants
* Add/edit/delete plant
* Plant detail
* Local persistence with Room

Success condition:

> I can create a plant and see it after restarting the app.

## Milestone 3 — Photos

* Android Photo Picker
* Attach photos to plants
* View photos
* Local storage

Success condition:

> I can photograph a plant and see the photo attached to it.

## Milestone 4 — Journal

* Add journal entries
* View chronological entries
* Edit/delete entries

## Milestone 5 — Harvests

* Record harvest
* Quantity/unit
* Harvest history
* Current inventory

Success condition:

> I can walk through my garden, record what I harvested, and see what I currently have.

## Milestone 6 — Plant AI

* Integrate first local vision model
* Image → identification
* Display result
* Confirm/correct
* Save correction

Success condition:

> I can take a picture of a plant and receive a useful local AI identification.

## Milestone 7 — Garden-to-Table AI

* Integrate local language model
* Provide harvest inventory as context
* Natural-language prompts
* Recipe/preservation suggestions

Success condition:

> I can tell the app what I harvested and ask what I should do with it.

## Milestone 8 — Polish

* Error handling
* Empty states
* Loading states
* Accessibility
* Basic onboarding
* App icon
* App name
* Privacy information
* Remove obvious bugs

## Milestone 9 — Real Device Testing

Test on a physical Android device.

Test:

* Fresh installation
* App restart
* Photos
* Offline functionality
* AI inference
* Large number of plants
* Large number of photos
* Low-memory conditions
* Error states

## Milestone 10 — Google Play Release

Before publishing:

* Google Play Console
* Bundle identifier
* Signing
* App icon
* Screenshots
* Description
* Privacy information
* Age rating
* Internal testing
* Final release build

---

# 17. Definition of Done for MVP

The MVP is complete when a real user can:

1. Install the app on an Android device.
2. Create a garden.
3. Add plants.
4. Photograph plants.
5. Journal plant observations.
6. Record harvests.
7. View current harvest inventory.
8. Identify a plant using the local vision model.
9. Correct the model when it is wrong.
10. Ask the local AI what to cook or how to use/preserve available harvests.
11. Use all normal garden-record functionality without internet access.
12. Close and reopen the app without losing data.

At this point:

**SHIP IT.**

Do not add succession planning, custom model training, cloud sync, subscriptions, ads, or additional AI models before the MVP has been successfully built and tested.

---

# 18. Future Roadmap

After MVP:

### V1.1

* Better plant identification
* More plant metadata
* Search/filter
* Better harvest management

### V1.2

* Succession planting engine
* Frost dates
* Planting calendar
* Garden-space planning

### V1.3

* Preservation knowledge base
* Freezing/canning/dehydrating workflows
* Pantry/freezer inventory

### V2

* Multiple specialized local AI models
* Garden planner AI
* Better vision model
* Model selection/configuration

### V3

* Collect anonymized/opt-in labeled corrections
* Fine-tune/train a specialized garden vision model
* Improved on-device inference

### V4

* Monetization
* Optional Pro features
* Optional cloud backup/sync
* iOS version
* Other advanced features based on actual user demand

---

# 19. Android Technology Stack

## Core

* Kotlin
* Jetpack Compose
* Material 3
* AndroidX
* Navigation Compose
* Room for persistence
* Kotlin coroutines
* StateFlow / appropriate Android state architecture

## Camera / Photos

* Android Photo Picker for existing photos
* CameraX where camera capture is needed

## Machine Learning

* TensorFlow Lite or LiteRT for on-device inference
* Hardware acceleration where available
* Model bundled in app assets or downloaded offline-first
* Replaceable without app redesign

## Build

* Gradle
* Android Studio

---

# 20. ML Training Strategy

## Hardware

* NVIDIA GTX 1060 6 GB VRAM
* 24 GB system RAM
* AMD FX-6300 CPU
* Windows 10

## Approach

* Transfer learning rather than training from scratch
* Small, fast, offline-capable models
* Convertible to Android-supported inference format (TFLite)
* Replaceable as models improve
* Specialized classifiers per domain (crops, weeds, diseases, insects, growth stages)
* Confidence thresholding for unknown/OOD detection
* External validation with source-separated test sets

## Model Stack (MVP)

| Model | Domain | Classes | Backbone | Est. Size |
|-------|--------|---------|----------|-----------|
| CropClassifier | Crops | 50 + Unknown | EfficientNet-Lite0 | ~4 MB |
| DiseaseClassifier | Diseases | 30 + Unknown | EfficientNet-Lite0 | ~4 MB |
| WeedClassifier | Weeds | 21 + Unknown | MobileNetV3-Small | ~3 MB |
| GrowthStageClassifier | Growth Stages | 6 | MobileNetV3-Small | ~2 MB |

Total model bundle: ~13 MB

## Dataset Strategy

* Primary: Commercially usable datasets with clear licensing (CC0, CC BY 4.0, Public Domain)
* Avoid: CC BY-NC, CC BY-SA, academic-only, ambiguous commercial licensing
* Do not download huge datasets into Git
* Dataset preparation tooling separate from Android app
* Provenance manifest for every image (source, license, attribution)
* Automated pipeline: discover → download → prepare → validate → deduplicate → split → report

## Approved Dataset Sources

### Crops
* Bangladesh Comprehensive Vegetables (CC BY 4.0, 4,730 images)
* Smartphone Vegetable Detection (CC BY 4.0, 3,534 images)
* BanglaVeg (CC BY 4.0, 4,319 images)
* VegNet (CC BY 4.0, 6,850 images)
* USDA ARS Image Gallery (Public Domain, supplement)

### Diseases
* PlantVillage (CC0 1.0, 54,306 images) — PRIMARY
* PlantDoc (CC BY 4.0, 2,569 images) — SUPPLEMENT

### Weeds
* DeepWeeds (CC BY 4.0, 17,509 images) — SUPPLEMENT (Australia-specific)
* CWD30 (219,770 images) — PENDING LICENSE CLARIFICATION
* Bugwood Images (Mixed) — SUPPLEMENT with caution

### Growth Stages
* Plant Growth Stage Detection (CC BY 4.0, 7,306 images)
* BDFlower (CC BY 4.0, 23,334 images)

## Data Pipeline

```bash
python training/prepare_dataset.py --domain crops
python training/prepare_dataset.py --domain diseases
python training/prepare_dataset.py --domain weeds
python training/prepare_dataset.py --domain growth_stages
python training/train.py --domain crops
python training/train.py --domain diseases
python training/train.py --domain weeds
python training/train.py --domain growth_stages
python training/export.py --all
```

## Validation Strategy

* Train: Dataset A (primary) + Dataset B (supplement)
* Validation: Held-out 15% of Dataset A
* External Test: Dataset C never used in training (e.g., USDA ARS for crops, PlantDoc for diseases)
* Report domain shift explicitly: "Model performs 94% same-source, 82% external"

## Compute Feasibility (GTX 1060 6GB)

| Model | Training Time | VRAM Required |
|-------|--------------|---------------|
| CropClassifier | 2–4 hours | ~4 GB |
| DiseaseClassifier | 2–3 hours | ~4 GB |
| WeedClassifier | 1–2 hours | ~3 GB |
| GrowthStageClassifier | 30–60 min | ~2 GB |

All models trainable on GTX 1060 6GB with 24GB system RAM.

---

# 21. Agent Rules

For every task:

1. Read this document before making architectural decisions.
2. Implement only the requested milestone/task.
3. Do not expand scope.
4. Do not implement future roadmap features unless explicitly requested.
5. Prefer native Android frameworks.
6. Keep the code understandable to a developer who is learning Kotlin/Compose.
7. Explain unfamiliar Kotlin/Compose concepts briefly when they matter.
8. Build/test frequently.
9. Fix compiler errors before moving on.
10. Never claim something works without actually verifying it.
11. If a requirement is ambiguous, ask before making a major architectural decision.
12. Keep commits/changes logically grouped where possible.

The goal is not to create the most sophisticated garden application possible.

The goal is to **ship a small, useful Android app and use the project to learn AI-assisted Android development and on-device AI.**
