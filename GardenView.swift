import SwiftUI
import SwiftData

struct GardenView: View {
    @Query private var plants: [Plant]
    @Environment(\.modelContext) private var modelContext

    @State private var showingAddPlant = false

    var body: some View {
        NavigationStack {
            List {
                if plants.isEmpty {
                    ContentUnavailableView(
                        "No Plants",
                        systemImage: "leaf",
                        description: Text("Tap + to add your first plant.")
                    )
                } else {
                    ForEach(plants) { plant in
                        NavigationLink(value: plant) {
                            VStack(alignment: .leading) {
                                Text(plant.name)
                                    .font(.headline)
                                if let variety = plant.variety, !variety.isEmpty {
                                    Text(variety)
                                        .font(.subheadline)
                                        .foregroundStyle(.secondary)
                                }
                            }
                        }
                    }
                }
            }
            .navigationTitle("Garden")
            .navigationDestination(for: Plant.self) { plant in
                PlantDetailView(plant: plant)
            }
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button {
                        showingAddPlant = true
                    } label: {
                        Label("Add Plant", systemImage: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingAddPlant) {
                AddPlantView()
            }
        }
    }
}

struct GardenView_Previews: PreviewProvider {
    static var previews: some View {
        GardenView()
    }
}
