import SwiftUI
import SwiftData

struct AddEditHarvestView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let plant: Plant
    let harvest: Harvest?

    @State private var cropName: String
    @State private var quantity: Double
    @State private var unit: String
    @State private var date: Date
    @State private var notes: String

    init(plant: Plant, harvest: Harvest? = nil) {
        self.plant = plant
        self.harvest = harvest
        _cropName = State(initialValue: harvest?.cropName ?? "")
        _quantity = State(initialValue: harvest?.quantity ?? 0)
        _unit = State(initialValue: harvest?.unit ?? "")
        _date = State(initialValue: harvest?.date ?? Date())
        _notes = State(initialValue: harvest?.notes ?? "")
    }

    var body: some View {
        Form {
            Section("Harvest") {
                TextField("Crop Name", text: $cropName)
                TextField("Quantity", value: $quantity, format: .number)
                TextField("Unit", text: $unit)
                DatePicker("Date", selection: $date, displayedComponents: .date)
            }

            Section("Notes") {
                TextField("Notes", text: $notes, axis: .vertical)
                    .lineLimit(3...10)
            }
        }
        .navigationTitle(harvest == nil ? "Add Harvest" : "Edit Harvest")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    saveHarvest()
                }
                .disabled(cropName.trimmingCharacters(in: .whitespaces).isEmpty || unit.trimmingCharacters(in: .whitespaces).isEmpty)
            }
        }
    }

    private func saveHarvest() {
        let trimmedCropName = cropName.trimmingCharacters(in: .whitespaces)
        let trimmedUnit = unit.trimmingCharacters(in: .whitespaces)
        guard !trimmedCropName.isEmpty, !trimmedUnit.isEmpty else { return }

        if let harvest {
            harvest.cropName = trimmedCropName
            harvest.quantity = quantity
            harvest.unit = trimmedUnit
            harvest.date = date
            harvest.notes = notes.isEmpty ? nil : notes
        } else {
            let newHarvest = Harvest(
                cropName: trimmedCropName,
                quantity: quantity,
                unit: trimmedUnit,
                date: date,
                notes: notes.isEmpty ? nil : notes,
                plant: plant
            )
            modelContext.insert(newHarvest)
        }

        dismiss()
    }
}

struct AddEditHarvestView_Previews: PreviewProvider {
    static var previews: some View {
        AddEditHarvestView(plant: Plant(name: "Tomato"))
    }
}
