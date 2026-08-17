import SwiftUI
import SwiftData

struct AddEditGrowingSpaceView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let space: GrowingSpace?

    @State private var name: String
    @State private var notes: String
    @State private var spaceType: SpaceType?
    @State private var width: String
    @State private var length: String

    init(space: GrowingSpace? = nil) {
        self.space = space
        _name = State(initialValue: space?.name ?? "")
        _notes = State(initialValue: space?.notes ?? "")
        _spaceType = State(initialValue: space?.spaceType)
        _width = State(initialValue: space?.width.map { String($0) } ?? "")
        _length = State(initialValue: space?.length.map { String($0) } ?? "")
    }

    var body: some View {
        Form {
            Section("Space Info") {
                TextField("Name", text: $name)
                Picker("Type", selection: $spaceType) {
                    Text("None").tag(nil as SpaceType?)
                    ForEach(SpaceType.allCases, id: \.self) { type in
                        Text(type.displayName).tag(type as SpaceType?)
                    }
                }
                TextField("Width (ft)", text: $width)
                    .keyboardType(.decimalPad)
                TextField("Length (ft)", text: $length)
                    .keyboardType(.decimalPad)
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

        let widthValue = Double(width.replacingOccurrences(of: ",", with: "."))
        let lengthValue = Double(length.replacingOccurrences(of: ",", with: "."))

        if let space {
            GardenService.updateGrowingSpace(
                space,
                name: trimmedName,
                notes: notes.isEmpty ? nil : notes,
                spaceType: spaceType,
                width: widthValue,
                length: lengthValue
            )
        } else {
            GardenService.addGrowingSpace(
                name: trimmedName,
                notes: notes.isEmpty ? nil : notes,
                spaceType: spaceType,
                width: widthValue,
                length: lengthValue,
                garden: nil,
                in: modelContext
            )
        }

        dismiss()
    }
}

struct AddEditGrowingSpaceView_Previews: PreviewProvider {
    static var previews: some View {
        AddEditGrowingSpaceView()
    }
}
