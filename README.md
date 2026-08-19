# Soil & Supper

An offline-first Android garden companion built with **Kotlin** and **Jetpack Compose**.

> **Canonical application stack:** Android · Kotlin · Jetpack Compose · Room (offline persistence) · Gradle.
> The original iOS/SwiftUI prototype has been superseded and is retained only as a historical/migration reference (see [Migration status](#migration-status)). See `DESIGN.md` for the current product design.

## Product Direction

> "The gardener should not have to manage the complexity. The app should reason about the garden and surface simple decisions."

The primary UI direction is the **Garden Timeline**:

- Garden beds/growing spaces are the primary visual object.
- A lightweight date scrubber lets the gardener move through time; the garden visualization changes with the selected date.
- Plant lifecycle is communicated visually (not as arbitrary percentages).
- Expected production and projected space availability are visible.
- Future succession suggestions appear naturally (no separate Planning / Succession / Timeline modes).

## Architecture

```
Garden data (Room)
    ↓
GardenRepository / GardenService
    ↓
Read-only PlanningEngine
    ↓
ViewModel / derived UI state
    ↓
Jetpack Compose UI
```

`PlanningEngine` is **read-only and deterministic**. It must never mutate garden state, never automatically mark spaces open, never auto-create succession plans or fulfill Desires, and never invoke AI or weather APIs. Planning suggestions are **derived** output, never persisted as authoritative garden facts.

## Project Layout

```
app/                              # Canonical Android application
  src/main/java/com/soilandsupper/
    data/local/                   # Room database + DAOs
    data/repository/              # GardenRepository, PlantRepository
    domain/model/                 # Garden, GrowingSpace, Occupancy, Crop, Plant,
                                  # Harvest, PlantPhoto, JournalEntry, Seed, Desire,
                                  # PlannedPlanting, PlantingSuggestion, ...
    service/                      # GardenService, CropKnowledge, PlanningEngine
    ui/                           # Compose screens (Garden, Garden Timeline, Harvest,
                                  # Identify, Garden-to-Table) + theme + navigation
training/ training_data/ docs/    # Python ML/data pipeline + documentation (independent
                                  # of the Android app)
```

## ML Boundary

The ML recognition/data-acquisition workstream is **Python-based and independent** of the Android application. It lives under `training/`, `training_data/`, `raw/`, `curated/`, `data/`, `metadata/`, and `splits/`, and is documented under `docs/` (`ML_*`, `PHASE*`). Do not modify ML dataset manifests, license records, or acquisition data as part of Android app work.

## Building

Prerequisites: Android SDK, JDK 17+, Gradle 8.7+ (the AGP version in `build.gradle.kts` requires Gradle 8.7 or newer).

```bash
gradle :app:assembleDebug
gradle :app:testDebugUnitTest
```

Open the repository root in Android Studio and the `app` module is the runnable application.

## Migration Status

An earlier Swift/SwiftUI/iOS prototype lives at the repository root (`Package.swift`, `Models/`, `Services/`, `*.swift`, `Tests/`). It is **obsolete** and is retained only as a reference while the Kotlin port is completed and verified. The Kotlin equivalents are largely in place; the remaining work is to finish and verify the Kotlin planning layer (see the architecture inventory in the phase notes) and then retire the Swift implementation. `MVP-design-doc.md` is the historical iOS design document; `DESIGN.md` is the current, Android-canonical design.
