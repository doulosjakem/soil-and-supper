# Soil & Supper — KMP / CMP Migration Plan

## Target module layout

```
soil-and-supper
├── shared/                     # Kotlin Multiplatform library (Compose Multiplatform)
│   ├── src/commonMain/kotlin/com/soilandsupper/
│   │   ├── domain/             # Room-free domain models + value types
│   │   ├── planning/           # PlanningEngine (read-only reasoning)
│   │   ├── gardentimeline/     # GardenTimelineState (read projection)
│   │   ├── repositories/       # repository interfaces (common)
│   │   ├── services/           # CropKnowledge, GardenService
│   │   └── ui/                 # shared Compose Garden Timeline UI
│   ├── src/androidMain/        # Android bootstrap + persistence impl
│   ├── src/iosMain/            # MainViewController (Kotlin/Native)
│   └── src/commonTest/         # shared unit tests (planning + timeline)
├── androidApp/                 # thin Android application (AGP) -> MainActivity
└── iosApp/                     # Xcode shell hosting ComposeUIViewController
```

## Sequencing (commits are intentionally reversible)

1. **CMP architecture/bootstrap** — Gradle/Kotlin 2.x + CMP plugin + version catalog;
   add `:shared`, keep `:app`. *(Deferred build wiring: see constraints.)*
2. **Shared domain/planning migration** — Room-free models + `PlanningEngine`,
   `GardenService`, `CropKnowledge`, `GardenTimelineState` into `commonMain`;
   repository interfaces; Android Room adapter mapping rows → shared models.
3. **Shared persistence/repository** — repository interfaces consumed by Android
   (Room impl behind them) and iOS behind the same interfaces.
4. **Shared Compose UI migration** — Garden Timeline UI (GardenScreen,
   GrowingSpaceTimelineRow, CropLifecycleIndicator, DateScrubber) to
   `commonMain` under Compose Multiplatform; thin `AndroidActivity`/`MainView`.
5. **iOS target** — `shared/iosMain` `MainViewController`; `iosApp` Xcode project.
   Requires macOS/Xcode to build.
6. **cleanup/documentation** — remove duplicate Android copies; finalize docs.

## Constraints that bound what can be verified in THIS environment

- Host is **Windows**; no macOS/Xcode. Kotlin/Native Apple targets **cannot** be
  compiled here. **No iOS build/run success will be claimed.**
- The Android app **must keep building and passing tests** at each committed state.
- The domain models are currently Room `@Entity` classes; freeing them for
  `commonMain` is a destructive change to persistence. It is sequenced after the
  bootstrap and must be done with an Android adapter so behavior is preserved.

## Acceptance gates (per phase)

- Phase 2: `:app` (or new equivalent) still compiles + all planning/timeline tests
  pass after models move.
- Phase 4: Android still builds + `assembleDebug` succeeds; timeline UI compiles.
- Phase 5: prepare iOS target correctly; **do not** claim compile success from Windows.

## Do NOT (scope boundary)

Voice/LLM, weather, notifications, crop rotation, interplanting, automatic
succession, new Garden modes, ML training/data acquisition, separate Timeline mode,
planning redesign, agronomic data fabrication, false iOS results.
