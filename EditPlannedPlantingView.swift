import SwiftUI
import SwiftData

struct EditPlannedPlantingView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let plan: PlannedPlanting

    @Query private var growingSpaces: [GrowingSpace]
    @Query private var desires: [Desire]
    @Query private var seeds: [Seed]

    @State private var cropName: String
    @State private var variety: String
    @State private var plannedDate: Date
    @State private var selectedGrowingSpace: GrowingSpace?
    @State private var selectedDesire: Desire?
    @State private var selectedSeed: Seed?
    @State private var notes: String

    init(plan: PlannedPlanting) {
        self.plan = plan
        _cropName = State(initialValue: plan.cropName)
        _variety = State(initialValue: plan.variety ?? "")
        _plannedDate = State(initialValue: plan.plannedDate ?? Date())
        _selectedGrowingSpace = State(initialValue: plan.growingSpace)
        _selectedDesire = State(initialValue: plan.desire)
        _selectedSeed = State(initialValue: plan.seed)
        _notes = State(initialValue: plan.notes ?? "")
    }

    var body: some View {
        Form {
            Section("Plan") {
                TextField("Crop", text: $cropName)
                TextField("Variety", text: $variety)
                DatePicker("Planned", selection: $plannedDate, displayedComponents: .date)
            }

            Section("Details") {
                Picker("Growing Space", selection: $selectedGrowingSpace) {
                    Text("None").tag(nil as GrowingSpace?)
                    ForEach(growingSpaces) { space in
                        Text(space.name).tag(space as GrowingSpace?)
                    }
                }

                Picker("Desire", selection: $selectedDesire) {
                    Text("None").tag(nil as Desire?)
                    ForEach(desires) { desire in
                        Text(desire.displayName).tag(desire as Desire?)
                    }
                }

                Picker("Seed", selection: $selectedSeed) {
                    Text("None").tag(nil as Seed?)
                    ForEach(seeds) { seed in
                        Text(seed.displayName).tag(seed as Seed?)
                    }
                }
            }

            Section("Notes") {
                TextField("Notes", text: $notes, axis: .vertical)
                    .lineLimit(3...6)
            }
        }
        .navigationTitle("Edit Plan")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    savePlan()
                }
                .disabled(cropName.trimmingCharacters(in: .whitespaces).isEmpty)
            }
        }
    }

    private func savePlan() {
        let trimmedCropName = cropName.trimmingCharacters(in: .whitespaces)
        guard !trimmedCropName.isEmpty else { return }

        GardenService.updatePlannedPlanting(
            plan,
            cropName: trimmedCropName,
            variety: variety.isEmpty ? nil : variety,
            plannedDate: plannedDate,
            growingSpace: selectedGrowingSpace,
            desire: selectedDesire,
            seed: selectedSeed,
            notes: notes.isEmpty ? nil : notes
        )

        dismiss()
    }
}

struct EditPlannedPlantingView_Previews: PreviewProvider {
    static var previews: some View {
        EditPlannedPlantingView(plan: PlannedPlanting(cropName: "Carrots", variety: "Nantes"))
    }
}
