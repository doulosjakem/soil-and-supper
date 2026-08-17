import SwiftData

@Model
final class GrowingSpace {
    var id: UUID
    var name: String
    var notes: String?
    var createdAt: Date
    var updatedAt: Date

    @Relationship(deleteRule: .nullify, inverse: \Garden.growingSpaces)
    var garden: Garden?

    @Relationship(deleteRule: .cascade, inverse: \Occupancy.growingSpace)
    var occupancies: [Occupancy] = []

    @Relationship(deleteRule: .cascade, inverse: \PlannedPlanting.growingSpace)
    var plannedPlantings: [PlannedPlanting] = []

    init(name: String, notes: String? = nil) {
        self.id = UUID()
        self.name = name
        self.notes = notes
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}
