import SwiftUI
import SwiftData

struct AddEditSeedView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let seed: Seed?
    let defaultState: SeedState

    @State private var cropName: String
    @State private var variety: String
    @State private var state: SeedState
    @State private var notes: String

    init(seed: Seed? = nil, defaultState: SeedState = .own) {
        self.seed = seed
        self.defaultState = defaultState
        _cropName = State(initialValue: seed?.cropName ?? "")
        _variety = State(initialValue: seed?.variety ?? "")
        _state = State(initialValue: seed?.state ?? defaultState)
        _notes = State(initialValue: seed?.notes ?? "")
    }

    var body: some View {
        Form {
            Section("Seed Info") {
                TextField("Crop Name", text: $cropName)
                TextField("Variety", text: $variety)
                Picker("State", selection: $state) {
                    ForEach(SeedState.allCases, id: \.self) { state in
                        Text(state.displayName).tag(state)
                    }
                }
                TextField("Notes", text: $notes, axis: .vertical)
                    .lineLimit(3...6)
            }
        }
        .navigationTitle(seed == nil ? "Add Seed" : "Edit Seed")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    saveSeed()
                }
                .disabled(cropName.trimmingCharacters(in: .whitespaces).isEmpty)
            }
        }
    }

    private func saveSeed() {
        let trimmedCropName = cropName.trimmingCharacters(in: .whitespaces)
        guard !trimmedCropName.isEmpty else { return }

        if let seed {
            GardenService.updateSeed(
                seed,
                cropName: trimmedCropName,
                variety: variety.isEmpty ? nil : variety,
                state: state,
                notes: notes.isEmpty ? nil : notes
            )
        } else {
            GardenService.addSeed(
                cropName: trimmedCropName,
                variety: variety.isEmpty ? nil : variety,
                state: state,
                notes: notes.isEmpty ? nil : notes,
                garden: nil,
                in: modelContext
            )
        }

        dismiss()
    }
}

struct AddEditSeedView_Previews: PreviewProvider {
    static var previews: some View {
        AddEditSeedView()
    }
}
