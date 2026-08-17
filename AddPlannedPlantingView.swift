import SwiftUI
import SwiftData

struct AddPlannedPlantingView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    @Query private var growingSpaces: [GrowingSpace]
    @Query private var desires: [Desire]
    @Query private var seeds: [Seed]

    @State private var cropName: String = ""
    @State private var variety: String = ""
    @State private var plannedDate: Date = Calendar.current.date(byAdding: .day, value: 14, to: Date()) ?? Date()
    @State private var selectedGrowingSpace: GrowingSpace? = nil
    @State private var selectedDesire: Desire? = nil
    @State private var selectedSeed: Seed? = nil
    @State private var notes: String = ""

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
        .navigationTitle("New Plan")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Add") {
                    savePlan()
                }
                .disabled(cropName.trimmingCharacters(in: .whitespaces).isEmpty)
            }
        }
    }

    private func savePlan() {
        let trimmedCropName = cropName.trimmingCharacters(in: .whitespaces)
        guard !trimmedCropName.isEmpty else { return }

        GardenService.createPlannedPlanting(
            cropName: trimmedCropName,
            variety: variety.isEmpty ? nil : variety,
            plannedDate: plannedDate,
            growingSpace: selectedGrowingSpace,
            desire: selectedDesire,
            seed: selectedSeed,
            notes: notes.isEmpty ? nil : notes,
            garden: nil,
            in: modelContext
        )

        dismiss()
    }
}

struct AddPlannedPlantingView_Previews: PreviewProvider {
    static var previews: some View {
        AddPlannedPlantingView()
    }
}
