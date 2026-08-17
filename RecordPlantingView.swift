import SwiftUI
import SwiftData

struct RecordPlantingView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let growingSpace: GrowingSpace

    @State private var cropName: String = ""
    @State private var variety: String = ""
    @State private var plantedDate: Date = Date()

    var body: some View {
        Form {
            Section("Planting") {
                TextField("Crop", text: $cropName)
                TextField("Variety", text: $variety)
                DatePicker("Planted", selection: $plantedDate, displayedComponents: .date)
            }
        }
        .navigationTitle("Plant Something")
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

        GardenService.recordPlanting(
            cropName: trimmedCropName,
            variety: variety.isEmpty ? nil : variety,
            startDate: plantedDate,
            growingSpace: growingSpace,
            in: modelContext
        )

        dismiss()
    }
}

struct RecordPlantingView_Previews: PreviewProvider {
    static var previews: some View {
        RecordPlantingView(growingSpace: GrowingSpace(name: "Bed 1"))
    }
}
