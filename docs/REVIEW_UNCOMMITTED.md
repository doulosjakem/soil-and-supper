## Local Review for **uncommitted changes**

### Summary
This review covers 12 modified tracked files, 27+ untracked files, and spans Android app architecture, ML documentation, and training pipelines. The changes include a major Kotlin refactor (Swift-to-Kotlin migration), new domain/repository/DAO layer, planning engine, and ML data-acquisition plan documents. High-confidence issues were found across security, deploy safety, business logic, duplication, and dead code tracks.

### Issues Found
| Severity | File:Line | Issue |
|---|---|---|
| CRITICAL | `app/src/main/java/com/soilandsupper/data/local/SoilAndSupperDatabase.kt:67` | Destructive migration wipes all user data on version bump |
| CRITICAL | `app/src/main/java/com/soilandsupper/ui/HarvestScreen.kt:95` | Hardcoded `plantId = 0` violates FK constraint → runtime crash |
| WARNING | `app/src/main/java/com/soilandsupper/service/PlanningEngine.kt:335-345` | `rankSuggestion` always returns same rank; `NOT_RECOMMENDED` unreachable |
| WARNING | `app/src/main/java/com/soilandsupper/service/PlanningEngine.kt:402-409` | `daysBetween` truncation causes false season-length rejection |
| WARNING | `app/src/main/java/com/soilandsupper/service/PlanningEngine.kt:246-252` | Cross-year planting windows incorrectly rejected for future openings |
| WARNING | `app/src/main/java/com/soilandsupper/service/PlanningEngine.kt:395-400` | `deduplicateAndRank` collapses suggestions across open growing spaces |
| WARNING | `app/src/main/java/com/soilandsupper/ui/GardenScreen.kt:36` | Unused `plants` state causes unnecessary DB queries |
| WARNING | `app/src/main/java/com/soilandsupper/ui/AddPlantScreen.kt:73-76` | Navigation occurs before DB insert completes → silent data loss |
| WARNING | `app/src/main/java/com/soilandsupper/ui/GardenScreen.kt:32-33` | Dead `onPlantClick` callback silently breaks navigation |
| SUGGESTION | `training/download_dataset.py:141` | ZIP slip / path traversal vulnerability in archive extraction |
| SUGGESTION | `app/src/main/java/com/soilandsupper/domain/model/Seed.kt:29` | `displayName` logic copy-pasted across 4 domain models |
| SUGGESTION | `app/src/main/java/com/soilandsupper/service/PlanningEngine.kt:402-409` | `daysBetween` duplicated across 4 files with nullability drift |
| SUGGESTION | `app/src/main/java/com/soilandsupper/ui/DateScrubber.kt:6` | Review artifact `// <--- added` comment in production code |
| SUGGESTION | `app/src/main/java/com/soilandsupper/domain/model/SpaceType.kt:3` | Entire `SpaceType` enum is unused — zero consumers |
| SUGGESTION | `app/src/main/java/com/soilandsupper/ui/GardenScreen.kt:10` | Unused `Card` import from rewritten UI |

### Detailed Findings

#### CRITICAL

**1. Destructive migration wipes all user data on version bump**
- **File:** `app/src/main/java/com/soilandsupper/data/local/SoilAndSupperDatabase.kt:67`
- **Confidence:** HIGH
- **Problem:** Database version incremented from 1 to 2 with `.fallbackToDestructiveMigration()` and zero `Migration` classes. Any existing user upgrading will lose their entire local database (gardens, plants, harvests, journal).
- **Suggestion:** Add an explicit `Migration(1, 2)` that `CREATE TABLE`s the new entities while preserving existing tables. If this is a brand-new app with no production users, reset version to 1 and remove the destructive fallback until the schema is stable.

**2. Hardcoded `plantId = 0` violates FK constraint → runtime crash**
- **File:** `app/src/main/java/com/soilandsupper/ui/HarvestScreen.kt:95`
- **Confidence:** HIGH
- **Problem:** `Harvest.plantId` is a non-nullable `Long` with a `ForeignKey` to `Plant` (`CASCADE`). The UI hardcodes `plantId = 0`, but auto-generated IDs start at 1. Room enforces FK constraints by default, so every save throws `SQLiteConstraintException`.
- **Suggestion:** Add plant selection to `HarvestScreen`, or make `plantId` nullable and change the FK action to `SET_NULL`.

#### WARNING

**3. `rankSuggestion` always returns the same rank; `NOT_RECOMMENDED` unreachable**
- **File:** `app/src/main/java/com/soilandsupper/service/PlanningEngine.kt:335-345`
- **Confidence:** HIGH
- **Problem:** Every branch returns either `BEST_FIT` or `ALSO_GOOD`. The inner `if (desire != null)` checks are dead code (both branches return the same value). The `NOT_RECOMMENDED` enum value is never produced.
- **Suggestion:** Restore intended differentiation (e.g., OWNED+desire → BEST_FIT, WANTED+desire → BEST_FIT, WANTED only → ALSO_GOOD, NOT_TRACKED only → NOT_RECOMMENDED).

**4. `daysBetween` truncation causes false "too little season" blocks**
- **File:** `app/src/main/java/com/soilandsupper/service/PlanningEngine.kt:402-409`
- **Confidence:** HIGH
- **Problem:** `daysBetween` divides millisecond delta by `86400000` and truncates to Int. If `(firstFrost - candidateDate)` equals exactly `daysToMaturity * 86400000 - 1ms`, the function returns `daysToMaturity - 1`, triggering a false rejection at line 290.
- **Suggestion:** Compare millisecond deltas directly: `if ((firstFrost - candidateDate) < daysToMaturity * 86400000L)` or use ceiling division.

**5. Cross-year planting windows incorrectly rejected for future openings**
- **File:** `app/src/main/java/com/soilandsupper/service/PlanningEngine.kt:246-252`
- **Confidence:** HIGH
- **Problem:** For `futureOpening = true`, the validity check for cross-year windows uses `currentMonth >= window.startMonth || currentMonth <= window.endMonth`. When the opening month falls between `endMonth + 1` and `startMonth - 1` (e.g., March for an Oct–Feb garlic window), the window is rejected even though a future occurrence exists.
- **Suggestion:** For `futureOpening = true`, treat all cross-year windows as valid since they recur annually.

**6. `deduplicateAndRank` collapses suggestions across open growing spaces**
- **File:** `app/src/main/java/com/soilandsupper/service/PlanningEngine.kt:395-400`
- **Confidence:** HIGH
- **Problem:** `groupBy { it.cropName }` discards `growingSpaceId`. If multiple spaces are open, only one arbitrary suggestion per crop survives, losing which space should be used.
- **Suggestion:** Group by both `cropName` and `growingSpaceId`, or remove deduplication and let the UI handle uniqueness.

**7. Unused `plants` state causes unnecessary database queries**
- **File:** `app/src/main/java/com/soilandsupper/ui/GardenScreen.kt:36`
- **Confidence:** HIGH
- **Problem:** The UI was rewritten from a plant-list to a Garden Timeline, but the old `plants` collection was left behind. It is collected but never referenced in the composable body.
- **Suggestion:** Remove the unused `plants` state and its associated collection.

**8. Navigation occurs before DB insert completes → silent data loss**
- **File:** `app/src/main/java/com/soilandsupper/ui/AddPlantScreen.kt:73-76`
- **Confidence:** HIGH
- **Problem:** `onPlantSaved()` is called immediately after launching the insert coroutine, not after the insert finishes. If the insert fails, the user is already navigated back with no error feedback.
- **Suggestion:** Move `onPlantSaved()` inside the coroutine after `insertPlant` completes, and add `try/catch` to surface errors.

**9. Dead `onPlantClick` callback silently breaks navigation**
- **File:** `app/src/main/java/com/soilandsupper/ui/GardenScreen.kt:32-33`
- **Confidence:** HIGH
- **Problem:** The composable still accepts `onPlantClick: (Long) -> Unit`, but the new implementation renders `GrowingSpaceTimelineRow` and never invokes the callback. Any navigation caller passing a plant-detail lambda will silently fail.
- **Suggestion:** Either wire `onPlantClick` to an actual navigation action or remove the parameter from the signature.

#### SUGGESTION

**10. ZIP slip / path traversal in training pipeline**
- **File:** `training/download_dataset.py:141`
- **Confidence:** HIGH
- **Problem:** `zipfile.ZipFile.extractall()` is called without validating archive member paths. A malicious or compromised dataset ZIP could contain entries with path traversal sequences and write files outside the intended extraction directory.
- **Suggestion:** Validate all archive member paths before extraction. Reject entries containing `..` or absolute paths.

**11. `displayName` logic copy-pasted across 4 domain models**
- **File:** `app/src/main/java/com/soilandsupper/domain/model/Seed.kt:29` (also `Desire.kt:31`, `Occupancy.kt:47`, `PlannedPlanting.kt:59`)
- **Confidence:** HIGH
- **Problem:** Identical `displayName` getter copy-pasted across 4 entities. Any change to naming convention must be replicated in all 4 files.
- **Suggestion:** Extract to a shared interface or extension (e.g., `interface NamedCrop { val cropName: String; val variety: String? }` with a common `displayName` implementation).

**12. `daysBetween` duplicated across 4 files with nullability drift**
- **File:** `app/src/main/java/com/soilandsupper/service/PlanningEngine.kt:402-409` (also `GardenTimelineState.kt:130-138`, `DefaultPlanningEngineTest.kt:148-155`, `PlanningEngineTest.kt:226-230`)
- **Confidence:** HIGH
- **Problem:** Identical date-calculation logic duplicated in production code and 2 test classes. `GardenTimelineState.kt` already diverges by returning `Int?` (nullable) while the other 3 return non-null `Int`.
- **Suggestion:** Extract to a single shared utility (e.g., `DateUtils.daysBetween(start, end): Int`) and use it from both production and test code.

**13. Review artifact comment in production code**
- **File:** `app/src/main/java/com/soilandsupper/ui/DateScrubber.kt:6`
- **Confidence:** HIGH
- **Problem:** `import androidx.compose.foundation.layout.Column  // <--- added` contains a review marker that was not removed.
- **Suggestion:** Strip the `// <--- added` comment.

**14. Entire `SpaceType` enum is unused**
- **File:** `app/src/main/java/com/soilandsupper/domain/model/SpaceType.kt:3`
- **Confidence:** HIGH
- **Problem:** `SpaceType` is defined but never referenced anywhere in the codebase, and `GrowingSpace.spaceType` remains a `String?` with no integration.
- **Suggestion:** Remove the file or integrate it into `GrowingSpace.spaceType` if intended for future use.

**15. Unused `Card` import from rewritten UI**
- **File:** `app/src/main/java/com/soilandsupper/ui/GardenScreen.kt:10`
- **Confidence:** HIGH
- **Problem:** The old plant-list UI used `Card` for each plant item; the new timeline UI does not.
- **Suggestion:** Remove the unused import.

### Recommendation
**NEEDS CHANGES** — Critical data-loss and crash issues must be fixed before this code is used. The destructive migration (finding 1) and FK constraint crash (finding 2) are production-blocking. The planning engine logic errors (findings 3-6) will cause incorrect crop suggestions. The dead code and duplication (findings 11-15) should be cleaned up to reduce maintenance burden.
