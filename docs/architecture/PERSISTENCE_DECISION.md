# Soil & Supper — Persistence Decision (KMP migration)

## Decision

**Keep Room as the Android persistence implementation. Do NOT move Room into
`commonMain` in this migration.**

Adopt a **repository abstraction with platform-specific implementations**:

- Define repository **interfaces over plain (Room-free) domain models** in
  `shared/commonMain`.
- Keep the Room database + DAOs **Android-specific** (`androidApp`, `androidMain`),
  mapping Room row types → common domain models.
- The iOS side gets a platform persistence implementation behind the same
  repository interfaces (fresh; Room is Android-only). No existing Android data is
  touched/migrated cross-platform in this phase.

## Options considered

| Approach | Verdict | Rationale |
|---|---|---|
| Room in common (Room 2.7 KMP, KSP) | Rejected for this phase | iOS Room support is premature/experimental; requires Kotlin 2 + KSP and a compiler/toolchain overhaul that cannot be iOS-verified from Windows. |
| SQLDelight | Considered, deferred | Solid KMP choice, but migrating the existing Room schema/queries is a full data-layer rewrite with regression risk to a working app, and cannot be cross-validated here. |
| Repository abstraction + platform persistence | **Chosen** | Smallest risk; preserves existing Android data + domain semantics exactly; keeps the shared core Room-free; clean seam for any future KMP persistence. |

## Impact

- Domain models gain Room-free twins in `shared/commonMain` (same fields; `id`
  preserved; persistence-only annotations removed).
- Android Room `@Entity`/DAO types stay in the Android layer; `GardenRepository`
  /`PlantRepository` map DAO rows → shared models.
- Common logic (`PlanningEngine`, `GardenService`, `GardenTimelineState`, UI)
  depends only on the shared models + repository interfaces.

## Preserved guarantees (unchanged)

- Deterministic `PlanningEngine` (read-only reasoning layer).
- Seeds/Desires = gardener intent; no future suggestions when both empty.
- Unknown seed ownership does not make a crop ineligible for current planting.
- Unknown maturity stays unknown.
- Projected release ≠ actual completion; only an explicit end date releases a space.
- Timeline is a read projection; scrubbing never mutates data.
