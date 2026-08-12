# Milestone 1 — Empty App: Plan

## 1. Current State

The repository is effectively empty:
- `MVP-design-doc.md` — the project's design document (source of truth).
- `.kilo/plans/` — empty directory for plan files.
- `.txt` — unknown, likely unrelated.

No Xcode project, Swift files, dependencies, or build configuration exist.

---

## 2. Recommended Milestone 1 Plan

**Goal:** Create an Xcode project structure and a working SwiftUI app shell that launches and builds on the iOS simulator.

**What Milestone 1 means in practice:**
The design doc says: *Create Xcode project, SwiftUI navigation, Basic app shell, Build successfully on simulator.*

For a native SwiftUI iOS app, the smallest reasonable shell consists of:
1. An Xcode project that the user opens in Xcode.
2. An `@main` app entry point (`SoilAndSupperApp.swift`).
3. A root `ContentView` with a `TabView` matching the four core feature areas:
   - **Garden** (home screen — plants list)
   - **Harvest** (inventory + history)
   - **Identify** (plant photo identification)
   - **Garden-to-Table** (AI cooking/preservation)
4. One placeholder `View` per tab so navigation compiles and renders.
5. Standard `Info.plist` and asset catalog placeholders (app icon, display name).

**What we will NOT create yet:**
- No data models (Garden, Plant, Harvest, etc.) — Milestone 2.
- No persistence (Core Data, SwiftData) — Milestone 2.
- No AI service protocols or model integration — Milestone 6/7.
- No camera/photo picker — Milestone 3.
- No third-party dependencies.

---

## 3. Decisions Needed

### A. Minimum iOS Deployment Target
**Recommended: iOS 17.0**

- Rationale: Full `NavigationStack` API, modern SwiftUI features, `@Observable` macro available if desired later, and it will remain supported for years. The app is being built in 2026; targeting iOS 17+ is reasonable.
- If you prefer broader compatibility, iOS 16.0 also works for `NavigationStack`.

### B. How the User Creates the Xcode Project
**Recommended: Create the Xcode project manually in Xcode; we provide the source files.**

- Rationale: A valid `.xcodeproj` is a complex directory bundle with many internal state files that are impractical to generate accurately from text tools. The standard workflow is:
  1. You create a new "iOS App" project in Xcode (SwiftUI interface, Swift language).
  2. You add the source files we generate into the project.
  3. You build and run.

### C. App Display Name
**Recommended: "Soil & Supper"**

- Rationale: Matches the project name from the design doc. We'll set `CFBundleDisplayName` in `Info.plist`.

### D. Bundle Identifier
**Recommended: `com.soilandsupper.app`**

- Rationale: Standard reverse-DNS format. Will be needed for signing in later milestones.

### E. Project File Organization (for now)
**Recommended: Flat structure for Milestone 1.**

- Rationale: Only ~5-6 files exist. Adding folder groups now adds overhead without benefit. We'll introduce folders (`Models/`, `Views/`, `Services/`) once Milestone 2 introduces real models.

---

## 4. Implementation Plan

If you approve, the implementation agent will make these changes in order:

1. **Create `SoilAndSupperApp.swift`** at the repo root — the `@main` struct that creates the app's `WindowGroup` and injects the root `ContentView`.

2. **Create `ContentView.swift`** — a `TabView` with four tabs, each backed by a placeholder view. Each placeholder will display the tab name and a short description.

3. **Create placeholder view files:**
   - `GardenView.swift`
   - `HarvestView.swift`
   - `IdentifyView.swift`
   - `GardenToTableView.swift`

4. **Create `Info.plist`** with the minimum configuration needed to launch (display name, bundle identifier, iOS deployment target).

5. **Create `Assets.xcassets/AppIcon.appiconset/`** with a minimal placeholder icon configuration so the app has a valid icon slot.

6. **Create `README.md`** with explicit instructions for the user to:
   - Open Xcode → Create a new iOS App project named "SoilAndSupper".
   - Delete the auto-generated `ContentView.swift` (or merge).
   - Add the source files from this repo into the Xcode project.
   - Set the deployment target to iOS 17.0.
   - Build and run on the simulator.

7. **Verify build** — the user (or implementation agent if possible) builds on the simulator and reports any compiler errors.

---

## 5. Open Questions

None. The three decisions above (iOS version, project creation method, app name) are the only material choices for Milestone 1. If you approve the recommendations, implementation can proceed without further input.
