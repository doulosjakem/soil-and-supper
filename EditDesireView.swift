import SwiftUI
import SwiftData

struct EditDesireView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let desire: Desire

    @State private var cropName: String
    @State private var variety: String
    @State private var notes: String

    init(desire: Desire) {
        self.desire = desire
        _cropName = State(initialValue: desire.cropName)
        _variety = State(initialValue: desire.variety ?? "")
        _notes = State(initialValue: desire.notes ?? "")
    }

    var body: some View {
        Form {
            Section("Desire") {
                TextField("What do you want to grow?", text: $cropName)
                TextField("Variety", text: $variety)
                TextField("Notes", text: $notes, axis: .vertical)
                    .lineLimit(3...6)
            }
        }
        .navigationTitle("Edit Desire")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    saveDesire()
                }
                .disabled(cropName.trimmingCharacters(in: .whitespaces).isEmpty)
            }
        }
    }

    private func saveDesire() {
        let trimmedCropName = cropName.trimmingCharacters(in: .whitespaces)
        guard !trimmedCropName.isEmpty else { return }

        GardenService.updateDesire(
            desire,
            cropName: trimmedCropName,
            variety: variety.isEmpty ? nil : variety,
            notes: notes.isEmpty ? nil : notes
        )

        dismiss()
    }
}

struct EditDesireView_Previews: PreviewProvider {
    static var previews: some View {
        EditDesireView(desire: Desire(cropName: "Carrots", variety: "Nantes"))
    }
}
