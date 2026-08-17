import SwiftUI
import SwiftData

struct GardenView: View {
    @Query private var plants: [Plant]
    @Query private var growingSpaces: [GrowingSpace]
    @Query private var seeds: [Seed]
    @Query private var desires: [Desire]
    @Query private var plannedPlantings: [PlannedPlanting]
    @Environment(\.modelContext) private var modelContext

    @State private var showingAddPlant = false
    @State private var showingAddSpace = false
    @State private var showingAddSeed = false
    @State private var showingSettings = false
    @State private var defaultSeedState: SeedState = .own
    @State private var showingAddDesire = false
    @State private var showingAddPlan = false

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

                Section("I Have") {
                    let ownedSeeds = seeds.filter { $0.state == .own }
                    if ownedSeeds.isEmpty {
                        ContentUnavailableView {
                            Label("No seeds yet", systemImage: "leaf")
                        } description: {
                            Text("Add seeds you have to your shelf.")
                        } actions: {
                            Button("Add Seeds") {
                                showingAddSeed = true
                                defaultSeedState = .own
                            }
                        }
                    } else {
                        ForEach(ownedSeeds) { seed in
                            NavigationLink(value: seed) {
                                HStack {
                                    Text(seed.displayName)
                                        .font(.headline)
                                    Spacer()
                                    Image(systemName: seed.state.symbolName)
                                        .foregroundStyle(.green)
                                }
                            }
                        }
                    }
                } header: {
                    HStack {
                        Text("I Have")
                        Spacer()
                        Button {
                            showingAddSeed = true
                            defaultSeedState = .own
                        } label: {
                            Image(systemName: "plus")
                        }
                    }
                }

                Section("I Want") {
                    let wantedSeeds = seeds.filter { $0.state == .want }
                    if wantedSeeds.isEmpty {
                        ContentUnavailableView {
                            Label("Nothing on your list yet", systemImage: "leaf")
                        } description: {
                            Text("Add seeds you want to your list.")
                        } actions: {
                            Button("Add Seeds") {
                                showingAddSeed = true
                                defaultSeedState = .want
                            }
                        }
                    } else {
                        ForEach(wantedSeeds) { seed in
                            NavigationLink(value: seed) {
                                HStack {
                                    Text(seed.displayName)
                                        .font(.headline)
                                    Spacer()
                                    Image(systemName: seed.state.symbolName)
                                        .foregroundStyle(.orange)
                                }
                            }
                        }
                    }
                } header: {
                    HStack {
                        Text("I Want")
                        Spacer()
                        Button {
                            showingAddSeed = true
                            defaultSeedState = .want
                        } label: {
                            Image(systemName: "plus")
                        }
                    }
                }

                Section("Want to Grow") {
                    let activeDesires = desires.filter { !$0.isFulfilled && !$0.isCancelled && !$0.isExpired }
                    if activeDesires.isEmpty {
                        ContentUnavailableView {
                            Label("Nothing on your list yet", systemImage: "leaf")
                        } description: {
                            Text("Add things you want to grow.")
                        } actions: {
                            Button("Add Desire") {
                                showingAddDesire = true
                            }
                        }
                    } else {
                        ForEach(activeDesires) { desire in
                            NavigationLink(value: desire) {
                                HStack {
                                    Text(desire.displayName)
                                        .font(.headline)
                                    Spacer()
                                    Image(systemName: "heart.fill")
                                        .foregroundStyle(.pink)
                                }
                            }
                        }
                    }
                } header: {
                    HStack {
                        Text("Want to Grow")
                        Spacer()
                        Button {
                            showingAddDesire = true
                        } label: {
                            Image(systemName: "plus")
                        }
                    }
                }

                Section("Planned") {
                    let activePlans = plannedPlantings.filter { $0.status == .planned }
                    if activePlans.isEmpty {
                        ContentUnavailableView {
                            Label("No plans yet", systemImage: "leaf")
                        } description: {
                            Text("Add plans for upcoming plantings.")
                        } actions: {
                            Button("Add Plan") {
                                showingAddPlan = true
                            }
                        }
                    } else {
                        ForEach(activePlans) { plan in
                            NavigationLink(value: plan) {
                                HStack {
                                    Text(plan.displayName)
                                        .font(.headline)
                                    Spacer()
                                    Group {
                                        if let space = plan.growingSpace {
                                            Text(space.name)
                                        } else {
                                            Text("Unassigned")
                                        }
                                    }
                                    .foregroundStyle(.secondary)
                                    if let date = plan.plannedDate {
                                        Text(date, format: .dateTime.day().month().year())
                                            .foregroundStyle(.secondary)
                                    }
                                }
                            }
                        }
                    }
                } header: {
                    HStack {
                        Text("Planned")
                        Spacer()
                        Button {
                            showingAddPlan = true
                        } label: {
                            Image(systemName: "plus")
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
            .navigationDestination(for: Desire.self) { desire in
                DesireDetailView(desire: desire)
            }
            .navigationDestination(for: PlannedPlanting.self) { plan in
                PlannedPlantingDetailView(plan: plan)
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
                            defaultSeedState = .own
                        } label: {
                            Label("Add Seed", systemImage: "seedling")
                        }
                        Button {
                            showingAddDesire = true
                        } label: {
                            Label("Add Desire", systemImage: "heart")
                        }
                        Button {
                            showingAddPlan = true
                        } label: {
                            Label("Plan a Planting", systemImage: "calendar")
                        }
                    } label: {
                        Label("Add", systemImage: "plus")
                    }
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        showingSettings = true
                    } label: {
                        Image(systemName: "gearshape")
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
                AddEditSeedView(defaultState: defaultSeedState)
            }
            .sheet(isPresented: $showingAddDesire) {
                AddDesireView()
            }
            .sheet(isPresented: $showingAddPlan) {
                AddPlannedPlantingView()
            }
            .sheet(isPresented: $showingSettings) {
                GardenSettingsView()
            }
        }
    }
}

struct GardenView_Previews: PreviewProvider {
    static var previews: some View {
        GardenView()
            .modelContainer(for: [Garden.self, Plant.self, GrowingSpace.self, Seed.self, Occupancy.self, Desire.self, PlannedPlanting.self], inMemory: true)
    }
}
