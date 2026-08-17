import SwiftUI
import SwiftData

struct PlannedPlantingDetailView: View {
    @Bindable var plan: PlannedPlanting
    @Environment(\.modelContext) private var modelContext
    @State private var showingEdit = false
    @State private var showingRecordPlanting = false

    var body: some View {
        Form {
            Section("Plan") {
                Text(plan.cropName)
                    .font(.headline)

                if let variety = plan.variety, !variety.isEmpty {
                    Text(variety)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }

                HStack {
                    Text("Status")
                    Spacer()
                    Text(plan.status.displayName)
                        .foregroundStyle(.secondary)
                }

                if let space = plan.growingSpace {
                    HStack {
                        Text("Growing Space")
                        Spacer()
                        Text(space.name)
                            .foregroundStyle(.secondary)
                    }
                }

                if let plannedDate = plan.plannedDate {
                    HStack {
                        Text("Planned")
                        Spacer()
                        Text(plannedDate, format: .dateTime.day().month().year())
                            .foregroundStyle(.secondary)
                    }
                }

                if let actualDate = plan.actualDate {
                    HStack {
                        Text("Planted")
                        Spacer()
                        Text(actualDate, format: .dateTime.day().month().year())
                            .foregroundStyle(.secondary)
                    }
                }

                if let desire = plan.desire {
                    HStack {
                        Text("Desire")
                        Spacer()
                        Text(desire.displayName)
                            .foregroundStyle(.secondary)
                    }
                }

                if let seed = plan.seed {
                    HStack {
                        Text("Seed")
                        Spacer()
                        Text(seed.displayName)
                            .foregroundStyle(.secondary)
                    }
                }

                if let notes = plan.notes, !notes.isEmpty {
                    Text(notes)
                        .font(.body)
                } else {
                    Text("No notes")
                        .font(.body)
                        .foregroundStyle(.secondary)
                }
            }

            if plan.status == .planned {
                Section {
                    Button("Mark planted") {
                        showingRecordPlanting = true
                    }
                    Button("Cancel", role: .destructive) {
                        GardenService.cancelPlannedPlanting(plan)
                    }
                }
            }
        }
        .navigationTitle("Planned")
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button("Edit") {
                    showingEdit = true
                }
            }
            ToolbarItem(placement: .destructiveAction) {
                Button("Delete", role: .destructive) {
                    GardenService.deletePlannedPlanting(plan, in: modelContext)
                }
            }
        }
        .sheet(isPresented: $showingEdit) {
            EditPlannedPlantingView(plan: plan)
        }
        .sheet(isPresented: $showingRecordPlanting) {
            RecordActualPlantingView(plan: plan)
        }
    }
}

struct PlannedPlantingDetailView_Previews: PreviewProvider {
    static var previews: some View {
        PlannedPlantingDetailView(plan: PlannedPlanting(cropName: "Carrots", variety: "Nantes"))
    }
}
