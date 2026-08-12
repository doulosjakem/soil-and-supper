# Soil & Supper

An offline-first native iOS garden companion built with SwiftUI.

## Milestone 5 — Harvest Tracking and Inventory

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
   - `JournalEntryView.swift`
   - `AddEditHarvestView.swift`
   - `PhotoStore.swift`
   - `Models/` (entire folder)
   - `Info.plist`
   - `Assets.xcassets/` (entire folder)
7. In Xcode project settings, set **iOS Deployment Target** to `17.0` or higher.
8. Build and run on the iOS Simulator.

### Project Structure (Milestone 5)

```
SoilAndSupper/
├── SoilAndSupperApp.swift   # App entry point with SwiftData ModelContainer
├── ContentView.swift        # Root TabView
├── GardenView.swift         # Plant list with add/delete
├── PlantDetailView.swift    # Edit plant details + photos + journal + harvests
├── AddPlantView.swift       # Add new plant form
├── JournalEntryView.swift   # Add/edit journal entry sheet
├── AddEditHarvestView.swift # Add/edit harvest entry sheet
├── HarvestView.swift        # Harvest inventory view
├── PhotoStore.swift         # Local photo file management
├── IdentifyView.swift       # Placeholder
├── GardenToTableView.swift  # Placeholder
├── Info.plist
├── Assets.xcassets/
│   └── AppIcon.appiconset/
└── Models/
    ├── Garden.swift
    ├── Plant.swift
    ├── PlantPhoto.swift
    ├── JournalEntry.swift
    └── Harvest.swift
```

### What Changed in Milestone 5

- Added `Harvest` SwiftData model with `cropName`, `quantity`, `unit`, `date`, and `notes` fields.
- `PlantDetailView` now shows a Harvests section with entries sorted newest-first.
- Users can add new harvests via a sheet form.
- Users can edit existing harvests by swiping and tapping Edit.
- Users can delete harvests by swiping and tapping Delete.
- `HarvestView` now shows a simple inventory aggregated by crop name and unit.
- Users can tap an inventory item to see the underlying harvest records.
- Harvest data is structured for future Garden-to-Table AI integration.

### Next Steps

- Milestone 6: Local Plant AI identification.
- Milestone 7: Garden-to-table AI.

### Notes

- No third-party dependencies are used.
- Persistence uses SwiftData (iOS 17+), Apple's native framework.
- Photo storage uses the app's local documents directory.
- Journal entries and harvests are plain text only.
