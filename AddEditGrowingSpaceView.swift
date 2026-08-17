import SwiftUI
import SwiftData

struct AddEditGrowingSpaceView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let space: GrowingSpace?

    @State private var name: String
    @State private var notes: String

    init(space: GrowingSpace? = nil) {
        self.space = space
        _name = State(initialValue: space?.name ?? "")
        _notes = State(initialValue: space?.notes ?? "")
    }

    var body: some View {
        Form {
            Section("Space Info") {
                TextField("Name", text: $name)
                TextField("Notes", text: $notes, axis: .vertical)
                    .lineLimit(3...6)
            }
        }
        .navigationTitle(space == nil ? "Add Growing Space" : "Edit Growing Space")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    saveSpace()
                }
                .disabled(name.trimmingCharacters(in: .whitespaces).isEmpty)
            }
        }
    }

    private func saveSpace() {
        let trimmedName = name.trimmingCharacters(in: .whitespaces)
        guard !trimmedName.isEmpty else { return }

        if let space {
            space.name = trimmedName
            space.notes = notes.isEmpty ? nil : notes
            space.updatedAt = Date()
        } else {
            let newSpace = GrowingSpace(name: trimmedName, notes: notes.isEmpty ? nil : notes)
            modelContext.insert(newSpace)
        }

        dismiss()
    }
}

struct AddEditGrowingSpaceView_Previews: PreviewProvider {
    static var previews: some View {
        AddEditGrowingSpaceView()
    }
}
