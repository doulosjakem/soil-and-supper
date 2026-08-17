import SwiftData

@Model
final class Desire {
    var id: UUID
    var cropName: String
    var variety: String?
    var isFulfilled: Bool
    var isExpired: Bool
    var isCancelled: Bool
    var notes: String?
    var createdAt: Date
    var updatedAt: Date

    @Relationship(deleteRule: .cascade, inverse: \Garden.desires)
    var garden: Garden?

    @Relationship(deleteRule: .nullify, inverse: \PlannedPlanting.desire)
    var plannedPlantings: [PlannedPlanting] = []

    init(
        cropName: String,
        variety: String? = nil,
        notes: String? = nil,
        garden: Garden? = nil
    ) {
        self.id = UUID()
        self.cropName = cropName
        self.variety = variety
        self.isFulfilled = false
        self.isExpired = false
        self.isCancelled = false
        self.notes = notes
        self.garden = garden
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
