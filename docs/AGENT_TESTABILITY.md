# Garden Timeline — Agent Testability Guide

## Overview

This document explains how an automated coding agent can build, test, and verify the Soil & Supper Garden Timeline on this Windows development machine.

## Environment Summary

| Component | Status |
|-----------|--------|
| OS | Windows (win32) |
| JDK | 17 |
| Android SDK | `C:\Users\keath\AppData\Local\Android\Sdk` |
| Gradle | Included via `gradlew.bat` |
| Emulator | `Pixel_5_API_30` AVD available |
| Physical device | None detected |
| iOS/macOS | Not available |

---

## 1. Build the App

### Debug APK
```bash
cd D:\soil-and-supper\soil-and-supper
.\gradlew.bat :app:assembleDebug --no-daemon
```
Output: `app/build/outputs/apk/debug/app-debug.apk`

### Install on Emulator/Device
```bash
.\gradlew.bat :app:installDebug --no-daemon
```

### Build Test APKs
```bash
# Shared (common) tests
.\gradlew.bat :shared:test --no-daemon

# App local unit tests
.\gradlew.bat :app:test --no-daemon

# Android instrumented tests (requires device/emulator)
.\gradlew.bat :app:assembleAndroidTest --no-daemon
.\gradlew.bat :app:installDebugAndroidTest --no-daemon
```

---

## 2. Launch Test Environment

### Start Emulator
```bash
emulator -avd Pixel_5_API_30 -no-audio -no-boot-anim -gpu swiftshader_indirect
```

**Wait for boot:**
```bash
adb wait-for-device
adb shell getprop sys.boot_completed
# Repeat until output is "1"
```

### Connect Physical Device
```bash
adb devices
# Enable USB debugging on device if not listed
```

---

## 3. Execute Tests

### Shared/Common Tests (JVM)
```bash
cd D:\soil-and-supper\soil-and-supper
.\gradlew.bat :shared:test --no-daemon
```
- **Runs on:** JVM (no device needed)
- **Duration:** ~1-2 minutes
- **Tests:** 77 unit tests covering timeline logic, planning engine, and realistic garden fixtures
- **Reports:** `shared/build/reports/tests/testDebugUnitTest/index.html`

### App Local Unit Tests (JVM)
```bash
cd D:\soil-and-supper\soil-and-supper
.\gradlew.bat :app:test --no-daemon
```
- **Runs on:** JVM (no device needed)
- **Duration:** ~1-2 minutes
- **Tests:** JVM-based tests (currently no Compose UI tests due to emulator constraints)
- **Reports:** `app/build/reports/tests/testDebugUnitTest/index.html`

### Android Instrumented Tests (Device/Emulator)
```bash
cd D:\soil-and-supper\soil-and-supper
.\gradlew.bat :connectedAndroidTest --no-daemon
```
- **Runs on:** Connected device or running emulator
- **Duration:** ~3-5 minutes
- **Tests:** Compose UI tests for Garden Timeline
- **Reports:** `app/build/reports/androidTests/connected/index.html`

---

## 4. Collect Failures

### Test Result Files
- Shared tests: `shared/build/test-results/testDebugUnitTest/*.xml`
- App tests: `app/build/test-results/testDebugUnitTest/*.xml`
- Instrumented tests: `app/build/outputs/androidTest-results/connected/*.xml`

### View HTML Reports
```bash
# Shared
start shared\build\reports\tests\testDebugUnitTest\index.html

# App
start app\build\reports\tests\testDebugUnitTest\index.html

# Instrumented
start app\build\reports\androidTests\connected\index.html
```

---

## 5. Collect Screenshots

### Manual Screenshot via ADB
```bash
adb exec-out screencap -p > screenshot_$(Get-Date -Format "yyyyMMdd_HHmmss").png
```

### Via Compose Testing (Instrumented only)
```kotlin
composeTestRule.onNodeWithText("Growing")
    .captureToImage()
    .asAndroidBitmap()
    // Save to file via Android context
```

---

## 6. Inspect Logs

### Gradle Build Logs
```bash
# Recent build output
Get-Content .gradle\console.log -Tail 100

# Specific task logs
Get-Content shared\build\reports\tests\testDebugUnitTest\output.txt
```

### Device Logs
```bash
adb logcat -s SoilAndSupper:D *:S
```

### Filter for Test Failures
```bash
adb logcat -d | Select-String -Pattern "FAIL|ERROR|Exception" | Select-Object -First 50
```

---

## 7. Report Regressions

### Regression Report Template
```
REGRESSION REPORT
=================
Date: [timestamp]
Commit: [git rev-parse HEAD]
Tests Run: [X]
Tests Passed: [Y]
Tests Failed: [Z]

FAILED TESTS:
1. [Test name] - [Failure message]

SCREENSHOTS:
[Attach relevant screenshots]

STEPS TO REPRODUCE:
1. [Step 1]
2. [Step 2]

EXPECTED: [Expected behavior]
ACTUAL: [Actual behavior]
```

---

## 8. Verification Matrix

| Capability | Verified Automatically | Requires Device | Requires iOS/macOS |
|------------|----------------------|-----------------|-------------------|
| Build app | YES | - | - |
| Run shared unit tests | YES | - | - |
| Run app unit tests | YES | - | - |
| Run Compose UI tests | NO | YES | - |
| Capture screenshots | NO | YES | - |
| Accessibility testing | PARTIAL | YES (full) | - |
| Font scaling test | NO | YES | - |
| iOS testing | NO | - | YES |

---

## 9. Commands Cheat Sheet

```bash
# Full test suite (shared + app)
cd D:\soil-and-supper\soil-and-supper
.\gradlew.bat :shared:test :app:test --no-daemon

# Clean build
.\gradlew.bat clean --no-daemon

# Build debug APK
.\gradlew.bat :app:assembleDebug --no-daemon

# Install and run on device
.\gradlew.bat :app:installDebug --no-daemon
adb shell am start -n com.soilandsupper/.ui.MainActivity

# Run instrumented tests (requires device)
.\gradlew.bat :connectedAndroidTest --no-daemon

# Uninstall test APK
.\gradlew.bat :app:uninstallDebugAndroidTest --no-daemon
```

---

## 10. Known Limitations on This Windows Machine

1. **Emulator CPU engine missing**: The `Pixel_5_API_30` AVD requires an x86 CPU engine that is not installed. Instrumented tests cannot run without:
   - Installing Intel HAXM (for Intel CPUs) or AMD Hypervisor (for AMD CPUs)
   - OR using a physical Android device connected via USB

2. **Compose UI tests on JVM**: `createComposeRule` requires Android runtime and cannot run in local JVM unit tests with the current Compose 1.5.x setup.

3. **iOS/macOS testing**: Not available on this Windows machine. iOS tests would require a macOS host with Xcode and an iOS simulator.

4. **Screenshot testing**: No automated screenshot diff tool is configured. Manual screenshots via ADB are the current option.
