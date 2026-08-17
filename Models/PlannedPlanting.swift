import SwiftData

@Model
final class PlannedPlanting {
    var id: UUID
    var cropName: String
    var variety: String?
    var plannedDate: Date?
    var actualDate: Date?
    var status: PlanStatus
    var notes: String?
    var createdAt: Date
    var updatedAt: Date

    @Relationship(deleteRule: .nullify, inverse: \Garden.plannedPlantings)
    var garden: Garden?

    @Relationship(deleteRule: .nullify, inverse: \GrowingSpace.plannedPlantings)
    var growingSpace: GrowingSpace?

    @Relationship(deleteRule: .nullify, inverse: \Occupancy.plannedPlanting)
    var occupancy: Occupancy?

    @Relationship(deleteRule: .nullify, inverse: \Desire.plannedPlantings)
    var desire: Desire?

    @Relationship(deleteRule: .nullify, inverse: \Seed.plannedPlantings)
    var seed: Seed?

    init(
        cropName: String,
        variety: String? = nil,
        plannedDate: Date? = nil,
        actualDate: Date? = nil,
        status: PlanStatus = .planned,
        notes: String? = nil,
        garden: Garden? = nil,
        growingSpace: GrowingSpace? = nil,
        occupancy: Occupancy? = nil,
        desire: Desire? = nil,
        seed: Seed? = nil
    ) {
        self.id = UUID()
        self.cropName = cropName
        self.variety = variety
        self.plannedDate = plannedDate
        self.actualDate = actualDate
        self.status = status
        self.notes = notes
        self.garden = garden
        self.growingSpace = growingSpace
        self.occupancy = occupancy
        self.desire = desire
        self.seed = seed
        self.createdAt = Date()
        self.updatedAt = Date()
    }

    var displayName: String {
        if let variety = variety, !variety.isEmpty {
            return "\(variety) \(cropName)"
        }
        return cropName
    }
}

enum PlanStatus: String, CaseIterable {
    case planned
    case planted
    case cancelled

    var displayName: String {
        switch self {
        case .planned: return "Planned"
        case .planted: return "Planted"
        case .cancelled: return "Cancelled"
        }
    }
}
