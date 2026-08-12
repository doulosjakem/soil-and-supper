# Soil & Supper

An offline-first native iOS garden companion built with SwiftUI.

## Milestone 3 — Plant Photos

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
   - `PhotoStore.swift`
   - `Models/` (entire folder)
   - `Info.plist`
   - `Assets.xcassets/` (entire folder)
7. In Xcode project settings, set **iOS Deployment Target** to `17.0` or higher.
8. Build and run on the iOS Simulator.

### Project Structure (Milestone 3)

```
SoilAndSupper/
├── SoilAndSupperApp.swift   # App entry point with SwiftData ModelContainer
├── ContentView.swift        # Root TabView
├── GardenView.swift         # Plant list with add/delete
├── PlantDetailView.swift    # Edit plant details + photos
├── AddPlantView.swift       # Add new plant form
├── PhotoStore.swift         # Local photo file management
├── HarvestView.swift        # Placeholder
├── IdentifyView.swift       # Placeholder
├── GardenToTableView.swift  # Placeholder
├── Info.plist
├── Assets.xcassets/
│   └── AppIcon.appiconset/
└── Models/
    ├── Garden.swift
    ├── Plant.swift
    └── PlantPhoto.swift
```

### What Changed in Milestone 3

- Added `PlantPhoto` SwiftData model with local file storage.
- `PlantDetailView` now shows a horizontal scroll of plant photos.
- Users can add photos via the system photo picker.
- Users can delete photos from the context menu.
- Photos are stored locally in the app's documents directory, not in iCloud or third-party services.

### Next Steps

- Milestone 4: Journal entries.
- Milestone 5: Harvest records.
- Milestone 6: Plant identification AI.
- Milestone 7: Garden-to-table AI.

### Notes

- No third-party dependencies are used.
- Persistence uses SwiftData (iOS 17+), Apple's native framework.
- Photo storage uses the app's local documents directory.
- Camera capture is deferred to a later milestone; photo library selection is available now.
