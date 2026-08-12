# Soil & Supper

An offline-first native iOS garden companion built with SwiftUI.

## Milestone 1 — Empty App

### Prerequisites

- Xcode 15+ (for iOS 17+)
- macOS with Xcode installed

### Setup

1. Open Xcode.
2. Choose **Create New Project** → **iOS** → **App**.
3. Configure:
   - **Product Name:** `SoilAndSupper`
   - **Interface:** `SwiftUI`
   - **Language:** `Swift`
   - **Bundle Identifier:** `com.soilandsupper.app`
   - **User Interface:** `Storyboard` is not applicable; use SwiftUI.
4. Save the project in this repository directory: `D:\soil-and-supper\soil-and-supper\SoilAndSupper.xcodeproj`
5. **Important:** After creating the project, delete the auto-generated `ContentView.swift` that Xcode creates. The `ContentView.swift` in this repository is the one you want.
6. Drag the following files from this repository into your Xcode project (choose **Copy items if needed**):
   - `SoilAndSupperApp.swift`
   - `ContentView.swift`
   - `GardenView.swift`
   - `HarvestView.swift`
   - `IdentifyView.swift`
   - `GardenToTableView.swift`
   - `Info.plist`
   - `Assets.xcassets/` (the entire folder)
7. In Xcode project settings, set **iOS Deployment Target** to `17.0` or higher.
8. Build and run on the iOS Simulator.

### Project Structure (Milestone 1)

```
SoilAndSupper/
├── SoilAndSupperApp.swift   # App entry point (@main)
├── ContentView.swift        # Root TabView
├── GardenView.swift         # Placeholder for Garden tab
├── HarvestView.swift        # Placeholder for Harvest tab
├── IdentifyView.swift       # Placeholder for Identify tab
├── GardenToTableView.swift  # Placeholder for Garden-to-Table tab
├── Info.plist
└── Assets.xcassets/
    └── AppIcon.appiconset/
```

### Next Steps

- Milestone 2: Garden CRUD with local persistence.
- Milestone 3: Photos.
- Milestone 4: Journal entries.
- Milestone 5: Harvest records.
- Milestone 6: Plant identification AI.
- Milestone 7: Garden-to-table AI.

### Notes

- No third-party dependencies are used in Milestone 1.
- The app is structured to add AI service protocols later without major refactoring.
