# Soil & Supper

An offline-first native iOS garden companion built with SwiftUI.

## Milestone 2 — Garden CRUD

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
4. Save the project in this repository directory: `D:\soil-and-supper\soil-and-supper\SoilAndSupper.xcodeproj`
5. **Important:** After creating the project, delete the auto-generated `ContentView.swift` that Xcode creates. The `ContentView.swift` in this repository is the one you want.
6. Drag the following files/folders from this repository into your Xcode project (choose **Copy items if needed**):
   - `SoilAndSupperApp.swift`
   - `ContentView.swift`
   - `GardenView.swift`
   - `HarvestView.swift`
   - `IdentifyView.swift`
   - `GardenToTableView.swift`
   - `AddPlantView.swift`
   - `PlantDetailView.swift`
   - `Models/` (entire folder)
   - `Info.plist`
   - `Assets.xcassets/` (entire folder)
7. In Xcode project settings, set **iOS Deployment Target** to `17.0` or higher.
8. Build and run on the iOS Simulator.

### Project Structure (Milestone 2)

```
SoilAndSupper/
├── SoilAndSupperApp.swift   # App entry point with SwiftData ModelContainer
├── ContentView.swift        # Root TabView
├── GardenView.swift         # Plant list with add/delete
├── PlantDetailView.swift    # Edit plant details
├── AddPlantView.swift       # Add new plant form
├── HarvestView.swift        # Placeholder
├── IdentifyView.swift       # Placeholder
├── GardenToTableView.swift  # Placeholder
├── Info.plist
├── Assets.xcassets/
│   └── AppIcon.appiconset/
└── Models/
    ├── Garden.swift
    └── Plant.swift
```

### What Changed in Milestone 2

- Added SwiftData persistence layer with `Garden` and `Plant` models.
- `GardenView` now shows a list of plants with navigation to detail.
- `AddPlantView` provides a form to create new plants.
- `PlantDetailView` allows editing and deleting plants.
- All data persists across app launches.

### Next Steps

- Milestone 3: Photos.
- Milestone 4: Journal entries.
- Milestone 5: Harvest records.
- Milestone 6: Plant identification AI.
- Milestone 7: Garden-to-table AI.

### Notes

- No third-party dependencies are used.
- Persistence uses SwiftData (iOS 17+), Apple's native framework.
- The app is structured to add AI service protocols later without major refactoring.
