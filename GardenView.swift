import SwiftUI
import SwiftData

struct GardenView: View {
    @Query private var plants: [Plant]
    @Query private var growingSpaces: [GrowingSpace]
    @Query private var seeds: [Seed]
    @Environment(\.modelContext) private var modelContext

    @State private var showingAddPlant = false
    @State private var showingAddSpace = false
    @State private var showingAddSeed = false

    var body: some View {
        NavigationStack {
            List {
                Section("Growing Spaces") {
                    if growingSpaces.isEmpty {
                        ContentUnavailableView(
                            "No Growing Spaces",
                            systemImage: "square.grid.3x3",
                            description: Text("Add a bed, pot, row, or other growing space.")
                        )
                    } else {
                        ForEach(growingSpaces) { space in
                            NavigationLink(value: space) {
                                VStack(alignment: .leading) {
                                    Text(space.name)
                                        .font(.headline)
                                    if let notes = space.notes, !notes.isEmpty {
                                        Text(notes)
                                            .font(.subheadline)
                                            .foregroundStyle(.secondary)
                                    }
                                }
                            }
                        }
                    }
                }

                Section("Seed Shelf") {
                    if seeds.isEmpty {
                        ContentUnavailableView(
                            "No Seeds",
                            systemImage: "leaf",
                            description: Text("Add seeds to track what you have and what you want.")
                        )
                    } else {
                        ForEach(seeds) { seed in
                            NavigationLink(value: seed) {
                                HStack {
                                    Text(seed.displayName)
                                        .font(.headline)
                                    Spacer()
                                    Image(systemName: seed.state == .own ? "checkmark.circle.fill" : "plus.circle.fill")
                                        .foregroundStyle(seed.state == .own ? .green : .orange)
                                }
                            }
                        }
                    }
                }

                Section("Plants") {
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
            }
            .navigationTitle("Garden")
            .navigationDestination(for: GrowingSpace.self) { space in
                GrowingSpaceDetailView(space: space)
            }
            .navigationDestination(for: Seed.self) { seed in
                SeedDetailView(seed: seed)
            }
            .navigationDestination(for: Plant.self) { plant in
                PlantDetailView(plant: plant)
            }
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Menu {
                        Button {
                            showingAddPlant = true
                        } label: {
                            Label("Add Plant", systemImage: "leaf")
                        }
                        Button {
                            showingAddSpace = true
                        } label: {
                            Label("Add Growing Space", systemImage: "square.grid.3x3")
                        }
                        Button {
                            showingAddSeed = true
                        } label: {
                            Label("Add Seed", systemImage: "seedling")
                        }
                    } label: {
                        Label("Add", systemImage: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingAddPlant) {
                AddPlantView()
            }
            .sheet(isPresented: $showingAddSpace) {
                AddEditGrowingSpaceView()
            }
            .sheet(isPresented: $showingAddSeed) {
                AddEditSeedView()
            }
        }
    }
}

struct GardenView_Previews: PreviewProvider {
    static var previews: some View {
        GardenView()
            .modelContainer(for: [Garden.self, Plant.self, GrowingSpace.self, Seed.self], inMemory: true)
    }
}
