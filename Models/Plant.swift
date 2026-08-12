import SwiftData

@Model
final class Plant {
    var id: UUID
    var name: String
    var variety: String?
    var plantingDate: Date?
    var location: String?
    var notes: String?
    var createdAt: Date
    var updatedAt: Date

    @Relationship(deleteRule: .nullify, inverse: \Garden.plants)
    var garden: Garden?

    @Relationship(deleteRule: .cascade, inverse: \PlantPhoto.plant)
    var photos: [PlantPhoto] = []

    @Relationship(deleteRule: .cascade, inverse: \JournalEntry.plant)
    var journalEntries: [JournalEntry] = []

    init(
        name: String,
        variety: String? = nil,
        plantingDate: Date? = nil,
        location: String? = nil,
        notes: String? = nil,
        garden: Garden? = nil
    ) {
        self.id = UUID()
        self.name = name
        self.variety = variety
        self.plantingDate = plantingDate
        self.location = location
        self.notes = notes
        self.garden = garden
        self.photos = []
        self.journalEntries = []
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}
