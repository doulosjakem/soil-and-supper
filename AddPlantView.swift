import SwiftUI
import SwiftData

struct AddPlantView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    @State private var name: String = ""
    @State private var variety: String = ""
    @State private var plantingDate: Date = Date()
    @State private var location: String = ""

    var body: some View {
        Form {
            Section("Plant Info") {
                TextField("Name", text: $name)
                TextField("Variety", text: $variety)
                DatePicker("Planting Date", selection: $plantingDate, displayedComponents: .date)
                TextField("Location", text: $location)
            }
        }
        .navigationTitle("Add Plant")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    savePlant()
                }
                .disabled(name.trimmingCharacters(in: .whitespaces).isEmpty)
            }
        }
    }

    private func savePlant() {
        let trimmedName = name.trimmingCharacters(in: .whitespaces)
        guard !trimmedName.isEmpty else { return }

        let plant = Plant(
            name: trimmedName,
            variety: variety.isEmpty ? nil : variety,
            plantingDate: plantingDate,
            location: location.isEmpty ? nil : location
        )

        modelContext.insert(plant)
        dismiss()
    }
}

struct AddPlantView_Previews: PreviewProvider {
    static var previews: some View {
        AddPlantView()
    }
}
