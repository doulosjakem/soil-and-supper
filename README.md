# Soil & Supper

An offline-first native iOS garden companion built with SwiftUI.

## Milestone 6 Phase 1 — Plant Identification Architecture

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
   - `Services/` (entire folder)
   - `Models/` (entire folder)
   - `Info.plist`
   - `Assets.xcassets/` (entire folder)
7. In Xcode project settings, set **iOS Deployment Target** to `17.0` or higher.
8. Build and run on the iOS Simulator.

### Project Structure (Milestone 6 Phase 1)

```
SoilAndSupper/
├── SoilAndSupperApp.swift   # App entry point with SwiftData + MockPlantIdentifier
├── ContentView.swift        # Root TabView
├── GardenView.swift         # Plant list with add/delete
├── PlantDetailView.swift    # Edit plant details + photos + journal + harvests
├── AddPlantView.swift       # Add new plant form
├── JournalEntryView.swift   # Add/edit journal entry sheet
├── AddEditHarvestView.swift # Add/edit harvest entry sheet
├── HarvestView.swift        # Harvest inventory view
├── PhotoStore.swift         # Local photo file management
├── IdentifyView.swift       # Plant identification UI with mock pipeline
├── GardenToTableView.swift  # Placeholder
├── Info.plist
├── Assets.xcassets/
│   └── AppIcon.appiconset/
├── Services/
│   ├── PlantIdentifier.swift    # Protocol + result model
│   └── MockPlantIdentifier.swift # Mock implementation for Phase 1
└── Models/
    ├── Garden.swift
    ├── Plant.swift
    ├── PlantPhoto.swift
    ├── JournalEntry.swift
    └── Harvest.swift
```

### What Changed in Milestone 6 Phase 1

- Added `PlantIdentifier` protocol with `identify(image:) async throws -> PlantIdentification`.
- Added `PlantIdentification` result model with `cropName`, `variety`, and `confidence`.
- Added `MockPlantIdentifier` that returns simulated predictions after a short delay.
- Replaced the `IdentifyView` placeholder with a full identification UI:
  - Lists existing plant photos.
  - Runs selected photo through the mock identifier.
  - Displays predicted name, optional variety, and confidence.
  - Allows confirming the result.
  - Allows correcting the result and saving the corrected name.
  - If confirmed/corrected, creates a new Plant or updates an existing linked Plant.

### Next Steps (Phase 2 — NOT YET IMPLEMENTED)

- Determine plant dataset and species classes for MVP.
- Evaluate Create ML training pipeline and base model choice.
- Train, convert, and bundle a real Core ML model.
- Replace `MockPlantIdentifier` with a Core ML + Vision implementation.

### Notes

- No third-party ML dependencies are used in Phase 1.
- No Core ML model is bundled yet.
- The architecture keeps the model behind the `PlantIdentifier` protocol so the real implementation can be swapped in later without changing the UI.
