import SwiftUI
import SwiftData

struct AddDesireView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    @State private var cropName: String = ""
    @State private var variety: String = ""
    @State private var notes: String = ""

    var body: some View {
        Form {
            Section("Desire") {
                TextField("What do you want to grow?", text: $cropName)
                TextField("Variety", text: $variety)
                TextField("Notes", text: $notes, axis: .vertical)
                    .lineLimit(3...6)
            }
        }
        .navigationTitle("New Desire")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Add") {
                    saveDesire()
                }
                .disabled(cropName.trimmingCharacters(in: .whitespaces).isEmpty)
            }
        }
    }

    private func saveDesire() {
        let trimmedCropName = cropName.trimmingCharacters(in: .whitespaces)
        guard !trimmedCropName.isEmpty else { return }

        GardenService.createDesire(
            cropName: trimmedCropName,
            variety: variety.isEmpty ? nil : variety,
            notes: notes.isEmpty ? nil : notes,
            garden: nil,
            in: modelContext
        )

        dismiss()
    }
}

struct AddDesireView_Previews: PreviewProvider {
    static var previews: some View {
        AddDesireView()
    }
}
