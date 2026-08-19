# iOS App

This directory contains the iOS application shell that hosts the shared Compose Multiplatform UI.

## Prerequisites (macOS only)

- Xcode 15+
- CocoaPods or Swift Package Manager
- Kotlin 2.x / Compose Multiplatform plugin compatible with host toolchain

## Setup steps (to be completed on macOS)

1. Open Xcode and create a new iOS App project named `iosApp`.
2. Add the `:shared` KMP framework as a local package or via SPM.
3. In `iosApp/ContentView.swift` (or equivalent), replace the root view with:

```swift
import SwiftUI
import shared

@main
struct iosAppApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .ignoresSafeArea()
                .onAppear {
                    let controller = MainViewController()
                    // Present the Compose UIViewController
                }
        }
    }
}
```

4. Verify that `shared` compiles for iOS targets (`iosX64`, `iosArm64`, `iosSimulatorArm64`).
5. Verify that the Garden Timeline renders in the iOS simulator.

## Known gaps (Windows environment)

- iOS targets are not compiled or tested on Windows.
- `DateScrubber` and `GrowingSpaceTimelineRow` use `java.text.SimpleDateFormat` / `java.util.Calendar` in `commonMain`. These require `expect`/`actual` date utilities before iOS compilation will succeed.
- The `repository` parameter in `MainViewController` is a stub. A real iOS `GardenRepository` implementation is required.
- Navigation between screens (Garden, Harvest, Identify, Garden-to-Table) is not yet implemented for iOS.

## What must be verified on macOS

1. `./gradlew :shared:linkDebugFrameworkIosX64` (or equivalent) succeeds.
2. iOS app launches in simulator.
3. Garden Timeline renders correctly.
4. No missing symbols from Compose Multiplatform runtime.
