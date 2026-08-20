# Garden Timeline — Screenshot Testing Investigation

## Current State

No screenshot testing library is configured. The project has:
- `androidx.compose.ui:ui-test-junit4:1.5.4` (instrumented tests)
- `androidx.compose.ui:ui-tooling:1.5.4` (debug)
- No Paparazzi, Roborazzi, or similar visual regression tool

## Feasible Approaches

### 1. Paparazzi (Recommended for future adoption)
- **What**: Renders Compose UI to PNG bitmaps on JVM without an emulator
- **Pros**: No device needed, fast, integrates with CI, detects visual regressions
- **Cons**: Requires adding a new dependency, setup overhead
- **Effort**: Medium
- **Command to add**: `implementation("app.cash.paparazzi:paparazzi:1.3.1")`

### 2. Compose `captureToImage` (Available now, limited)
- **What**: Captures individual composables to `ImageBitmap`
- **Pros**: No new dependencies, works in tests today
- **Cons**: Only captures individual composables, not full screens, no built-in diffing
- **Effort**: Low
- **Example**: `CropLifecycleIndicator(phase).captureToImage()`

### 3. Instrumented screenshot via `PixelCopy` (Requires device/emulator)
- **What**: Takes screenshots of the running app window
- **Pros**: Full-screen captures, real device rendering
- **Cons**: Requires device/emulator, slower, no built-in diffing
- **Effort**: Medium

## Recommendation

**Do not add a screenshot testing library in this phase.** The project is still in active UI development toward Compose Multiplatform. Adding Paparazzi now would create migration work later.

Instead:
1. Use the existing Compose UI tests to verify semantics and structure
2. Use the Android instrumented tests (when a device is available) for manual screenshot capture
3. Revisit screenshot testing after the Compose Multiplatform migration stabilizes

## Baseline Scenarios for Future Screenshot Testing

When a screenshot tool is adopted, capture baselines for:
- Empty garden (no spaces)
- Single occupied space (producing crop)
- Single occupied space (nearing release)
- Available space with suggestions
- Mixed occupied/open garden
- Unknown maturity occupancy
- Narrow phone width (320dp)

## Commands for Manual Screenshot Capture (Android)

```bash
# Start emulator or connect device
adb devices

# Install debug APK
./gradlew :app:installDebug

# Launch app
adb shell am start -n com.soilandsupper/.ui.MainActivity

# Take screenshot via adb
adb exec-out screencap -p > screenshot_$(date +%Y%m%d_%H%M%S).png
```
