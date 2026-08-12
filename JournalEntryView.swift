import SwiftUI
import SwiftData

struct JournalEntryView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let plant: Plant
    let entry: JournalEntry?

    @State private var date: Date
    @State private var text: String

    init(plant: Plant, entry: JournalEntry? = nil) {
        self.plant = plant
        self.entry = entry
        _date = State(initialValue: entry?.date ?? Date())
        _text = State(initialValue: entry?.text ?? "")
    }

    var body: some View {
        Form {
            Section("Entry") {
                DatePicker("Date", selection: $date, displayedComponents: .date)
                TextField("Notes", text: $text, axis: .vertical)
                    .lineLimit(3...10)
            }
        }
        .navigationTitle(entry == nil ? "New Journal Entry" : "Edit Journal Entry")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    saveEntry()
                }
                .disabled(text.trimmingCharacters(in: .whitespaces).isEmpty)
            }
        }
    }

    private func saveEntry() {
        let trimmedText = text.trimmingCharacters(in: .whitespaces)
        guard !trimmedText.isEmpty else { return }

        if let entry {
            entry.date = date
            entry.text = trimmedText
        } else {
            let newEntry = JournalEntry(date: date, text: trimmedText)
            newEntry.plant = plant
            modelContext.insert(newEntry)
        }

        dismiss()
    }
}

struct JournalEntryView_Previews: PreviewProvider {
    static var previews: some View {
        JournalEntryView(plant: Plant(name: "Tomato"))
    }
}
