import SwiftData

@Model
final class JournalEntry {
    var id: UUID
    var date: Date
    var text: String

    @Relationship(deleteRule: .cascade, inverse: \Plant.journalEntries)
    var plant: Plant?

    init(date: Date = Date(), text: String) {
        self.id = UUID()
        self.date = date
        self.text = text
    }
}
