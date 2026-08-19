# Soil & Supper — Kotlin Multiplatform / Compose Multiplatform Migration
## Phase 1–4 Assessment (repository audit)

Status: assessment milestone. Companion docs:
- `PERSISTENCE_DECISION.md`
- `MIGRATION_PLAN.md`

---

## 1. Starting architecture (as-found)

- **Single Android module** `:app` (AGP 8.5.0, Kotlin 1.9.22, Compose 1.5.4/BOM, Gradle 8.7 wrapper).
- **One source set** `app/src/main/java/com/soilandsupper/...`, JVM unit tests in `app/src/test`.
- **Compose Multiplatform**: none (Jetpack Compose / androidx only).
- **Persistence**: Room 2.6.1 (kapt). The Room `@Entity` classes **are** the domain models.
- **Camera / photos**: androidx.camera
- **ML inference (Android)**: TensorFlow Lite — separate workstream, to stay isolated.
- **iOS**: a *legacy SwiftUI* app (root `.swift` files + `Models/`, `Services/`, `Tests/`) is tracked but not migrated into KMP here, and is explicitly **not** being developed in parallel.

## 2. Inventory (relevant components)

| Component | File(s) | Coupling |
|---|---|---|
| Domain models (Room entities) | `domain/model/{Garden,GrowingSpace,Occupancy,Seed,Desire,Plant,PlantPhoto,Harvest,JournalEntry,PlannedPlanting}.kt` | `androidx.room` |
| Pure value types | `Crop.kt`, `PlantingSuggestion.kt`, `SpaceType.kt` (+ enums `SeedState`, `OccupancyStatus`, `PlanStatus`) | none |
| `CropKnowledge` | `service/CropKnowledge.kt` | none (pure) |
| `PlanningEngine` | `service/PlanningEngine.kt` | pure, but references Room-entangled models |
| `GardenService` | `service/GardenService.kt` | pure, references Room-entangled models |
| `GardenTimelineState` | `ui/GardenTimelineState.kt` | pure (models + `java.util.Calendar`) — no UI |
| Garden Compose UI | `ui/{GardenScreen,GrowingSpaceTimelineRow,CropLifecycleIndicator,DateScrubber,Theme}.kt` | androidx Compose |
| Other screens | `ui/{AddPlantScreen,PlantDetailScreen,HarvestScreen,IdentifyScreen,...}.kt` | androidx Compose + Camera + TFLite |
| Persistence | `data/local/SoilAndSupperDatabase.kt`, `data/local/dao/*` | Room |
| Repositories | `GardenRepository.kt`, `PlantRepository.kt` | Room DAOs + `kotlinx.coroutines.Flow` |
| ML/plant id | `domain/model/{PlantIdentifier,MockPlantIdentifier}.kt` | `android.graphics.Bitmap` (Android-only) |
| SwiftiOS legacy | Root `.swift`, `Models/`, `Services/`, `Tests/` | SwiftUI (not to be extended) |

## 3. Classification

- **COMMON (move to `shared/commonMain`)** →
  Pure value types: `Crop`, `Variety`, `PlantingWindow`, `CropCharacteristics`, `PlantingSuggestion` (+ `SeedAvailability`, `SuggestionRank`), `SpaceType`; `CropKnowledge`; and the *logic core*: `PlanningEngine`, `GardenService`, `GardenTimelineState` — **after** the models they reference are freed from Room (see Persistence Decision).
- **COMMON (UI, Compose Multiplatform, deferred to phased migration)** →
  `GardenScreen`, `GrowingSpaceTimelineRow`, `CropLifecycleIndicator`, `DateScrubber`, theme/design system. They are pure Compose (no Android-only APIs) and portable; converted to CMP in the shared-UI phase.
- **ANDROID-SPECIFIC** → `MainActivity`, `SoilAndSupperApplication`, navigation, `add_plant`/`plant_detail`/`harvest`/`identify` screens (Camera, Bitmap, TFLite), Room database + DAOs, repositories that bind Room → domain, `PlantIdentifier`/`MockPlantIdentifier` (Bitmap).
- **NEEDS ABSTRACTION** → persistence (repository interfaces in commonMain, Room impl in `androidMain`/app); `PlantIdentifier` (common interface, Android image impl, future iOS image impl).
- **IOS-SPECIFIC (to be created in shared `iosMain`)** → `MainViewController` Kotlin/Native entry, plus the `iosApp` Xcode shell (not buildable on Windows).
- **OBSOLETE / DO NOT EXTEND** → the legacy SwiftUI app tree (left as-is, not shipped as the iOS impl).

## 4. Key findings

1. **The domain models are Room entities.** This single fact is the biggest migration cost: moving planning/timeline into `commonMain` requires Room-free domain models and an Android persistence adapter.
2. **`PlanningEngine`, `GardenService`, `GardenTimelineState` are pure Kotlin** (only `java.*` + models). They are the ideal first commonMain citizens once models are freed.
3. **Garden Compose UI is pure Compose** (no `Context`/`Activity`), so it is portable to CMP with mechanical import changes.
4. **Android-only couplings** are confined to: Room annotations (models + persistence), `android.graphics.Bitmap` (plant id), Camera, TFLite, and `MainActivity`/navigation.
5. **No version catalog** exists. Migration should introduce `gradle/libs.versions.toml`.
6. **Kotlin 1.9.22 / Compose 1.5.4 are Android-era.** CMP + KMP require Kotlin 2.x and the Compose Multiplatform Gradle plugin.

## 5. Deferred items (see `MIGRATION_PLAN.md` for rationale and sequencing)

Verified-on-Windows assessment only. The following are consciously deferred to phases that require a macOS/Xcode host for honest verification:
- Compile/run of the iOS target.
- Full CMP (UI-in-common) conversion + the accompanying Room unwinding (a destructive, high-regression-risk change to the working Android app that cannot be cross-validated from Windows).
