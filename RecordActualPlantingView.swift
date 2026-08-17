import SwiftUI
import SwiftData

struct RecordActualPlantingView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let plan: PlannedPlanting

    @Query private var growingSpaces: [GrowingSpace]

    @State private var cropName: String
    @State private var variety: String
    @State private var selectedGrowingSpace: GrowingSpace?
    @State private var plantedDate: Date

    init(plan: PlannedPlanting) {
        self.plan = plan
        _cropName = State(initialValue: plan.cropName)
        _variety = State(initialValue: plan.variety ?? "")
        _selectedGrowingSpace = State(initialValue: plan.growingSpace)
        _plantedDate = State(initialValue: Date())
    }

    var body: some View {
        Form {
            Section("Actual Planting") {
                TextField("Crop", text: $cropName)
                TextField("Variety", text: $variety)
                DatePicker("Planted", selection: $plantedDate, displayedComponents: .date)
            }

            Section("Growing Space") {
                Picker("Space", selection: $selectedGrowingSpace) {
                    Text("None").tag(nil as GrowingSpace?)
                    ForEach(growingSpaces) { space in
                        Text(space.name).tag(space as GrowingSpace?)
                    }
                }
            }
        }
        .navigationTitle("Record Planting")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    savePlanting()
                }
                .disabled(cropName.trimmingCharacters(in: .whitespaces).isEmpty)
            }
        }
    }

    private func savePlanting() {
        let trimmedCropName = cropName.trimmingCharacters(in: .whitespaces)
        guard !trimmedCropName.isEmpty else { return }

        GardenService.completePlannedPlanting(
            plan,
            actualStartDate: plantedDate,
            cropName: trimmedCropName,
            variety: variety.isEmpty ? nil : variety,
            growingSpace: selectedGrowingSpace,
            notes: nil,
            in: modelContext
        )

        dismiss()
    }
}

struct RecordActualPlantingView_Previews: PreviewProvider {
    static var previews: some View {
        RecordActualPlantingView(plan: PlannedPlanting(cropName: "Carrots", variety: "Nantes"))
    }
}
