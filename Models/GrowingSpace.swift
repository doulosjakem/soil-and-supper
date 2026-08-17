import SwiftData

enum SpaceType: String, CaseIterable {
    case bed
    case container
    case row
    case other

    var displayName: String {
        switch self {
        case .bed: return "Bed"
        case .container: return "Container"
        case .row: return "Row"
        case .other: return "Other"
        }
    }
}

@Model
final class GrowingSpace {
    var id: UUID
    var name: String
    var notes: String?
    var spaceType: SpaceType?
    var width: Double?
    var length: Double?
    var createdAt: Date
    var updatedAt: Date

    @Relationship(deleteRule: .nullify, inverse: \Garden.growingSpaces)
    var garden: Garden?

    @Relationship(deleteRule: .cascade, inverse: \Occupancy.growingSpace)
    var occupancies: [Occupancy] = []

    @Relationship(deleteRule: .cascade, inverse: \PlannedPlanting.growingSpace)
    var plannedPlantings: [PlannedPlanting] = []

    init(name: String, notes: String? = nil, spaceType: SpaceType? = nil, width: Double? = nil, length: Double? = nil) {
        self.id = UUID()
        self.name = name
        self.notes = notes
        self.spaceType = spaceType
        self.width = width
        self.length = length
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}
