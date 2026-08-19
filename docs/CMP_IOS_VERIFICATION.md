# CMP iOS Verification Checklist

This document contains the exact steps for verifying the Soil & Supper Compose Multiplatform iOS target on macOS.

## Prerequisites

- macOS 13.0+
- Xcode 15.0+
- Kotlin 2.x compatible with the project's Gradle/KMP plugin versions
- Ruby/Bundler for CocoaPods, or Swift Package Manager support

## Step 1: Clone and Open

```bash
git clone <repository-url>
cd soil-and-supper
```

Open the project in Android Studio or IntelliJ IDEA with the Kotlin Multiplatform plugin.

## Step 2: Resolve Dependencies

```bash
./gradlew dependencies --configuration debugCompileClasspath
```

Verify no dependency resolution errors.

## Step 3: Build Shared Framework

```bash
./gradlew :shared:linkDebugFrameworkIosX64
```

Or for a specific simulator/device:

```bash
./gradlew :shared:linkDebugFrameworkIosArm64
./gradlew :shared:linkDebugFrameworkIosSimulatorArm64
```

## Step 4: Build iOS App

1. Open `iosApp/` in Xcode.
2. Ensure the `:shared` framework is linked as a local package or via SPM.
3. Select a simulator target (e.g., iPhone 15 Pro).
4. Build (`Cmd+B`).

## Step 5: Launch Simulator

1. Run (`Cmd+R`) from Xcode.
2. Verify the app launches without crash.
3. The first screen should display the Garden Timeline.

## Expected Garden Timeline Behavior

- A list of growing spaces is shown.
- For each space:
  - Name and optional notes are displayed.
  - "Available" badge appears when the space is unoccupied.
  - Current planting suggestions appear for available spaces.
  - Active occupancy details appear for occupied spaces:
    - Crop display name
    - Lifecycle phase label (Establishing, Growing, Producing, Space opening soon)
    - Lifecycle indicator
    - Harvest timing
    - Space opening timing
  - Future suggestions appear for occupied spaces with a projected release date, ONLY if seeds or desires exist.
- Date scrubber at the top allows changing the selected date.
- "Today" button resets to current date.

## Known Limitations

1. **Date formatting**: iOS uses Foundation `NSDateFormatter`. Month/day formatting may differ slightly from Android `SimpleDateFormat` defaults. Verify locale handling.
2. **Repository**: The iOS repository (`IosGardenRepository`) is an in-memory temporary implementation. Data does not persist between app launches. It exists only to prove the UI architecture.
3. **Navigation**: Only the Garden screen is wired for iOS. Other screens (Harvest, Identify, Garden-to-Table, Add Plant) are not yet available from the iOS entry point.
4. **Plant identification**: Requires platform-specific image handling and ML inference. Not implemented for iOS.
5. **Persistence**: No real iOS persistence layer exists yet. SQLite, Core Data, or another KMP-compatible store must be chosen and implemented.
6. **Kotlin 2.x**: The project currently targets Kotlin 1.9.22 with Compose compiler 1.5.8. A future Kotlin 2.x upgrade may be required for full CMP stability.

## Current iOS Stubs

| Component | Status | Notes |
|-----------|--------|-------|
| `formatDate` | Real Foundation impl | Uses `NSDateFormatter` |
| `epochMillis` | Real Foundation impl | Uses `NSCalendar` + `NSDateComponents` |
| `IosGardenRepository` | Temporary in-memory | Must be replaced before production |
| `MainViewController` | Minimal bootstrap | Launches GardenScreen only |
| `iosApp` Xcode shell | Not created | Developer must create on macOS |

## Where iOS Persistence Still Needs Implementation

The `GardenRepository` interface is defined in `shared/src/commonMain/kotlin/com/soilandsupper/repository/GardenRepository.kt`.

iOS must provide a concrete implementation behind this interface. Options to evaluate on macOS:

- SQLDelight (KMP-compatible)
- Multiplatform Room (experimental)
- Core Data via Kotlin/Native interop
- A simple SQLite wrapper

The Android side continues using Room via `GardenRepository` in the app module.

## Reporting Failures

If iOS build/run fails on macOS:

1. Record the exact Xcode/Gradle error output.
2. Note the macOS version, Xcode version, and device/simulator target.
3. Check `docs/CMP_IOS_VERIFICATION.md` for known limitations.
4. Report back with:
   - Failure point (link framework, build, launch, runtime)
   - Full error message
   - Steps to reproduce

## Git Hygiene Note

The ML workstream (`ml/`, `training/`) is unrelated to this migration. Do not stage, commit, or modify ML files during iOS verification.
