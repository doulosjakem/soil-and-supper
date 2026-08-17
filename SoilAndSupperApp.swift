import SwiftUI
import SwiftData

@main
struct SoilAndSupperApp: App {
    let modelContainer: ModelContainer

    init() {
        do {
            modelContainer = try ModelContainer(
                for: [Garden.self, Plant.self, PlantPhoto.self, JournalEntry.self, Harvest.self, GrowingSpace.self, Seed.self, Occupancy.self, Desire.self, PlannedPlanting.self]
            )
        } catch {
            fatalError("Failed to initialize ModelContainer: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
                .modelContainer(modelContainer)
                .environmentObject(MockPlantIdentifier())
        }
    }
}
