import SwiftData

@Model
final class Occupancy {
    var id: UUID
    var cropName: String
    var variety: String?
    var startDate: Date
    var endDate: Date?
    var expectedHarvestDate: Date?
    var expectedReleaseDate: Date?
    var status: OccupancyStatus
    var notes: String?
    var createdAt: Date
    var updatedAt: Date

    @Relationship(deleteRule: .cascade, inverse: \GrowingSpace.occupancies)
    var growingSpace: GrowingSpace?

    @Relationship(deleteRule: .nullify, inverse: \Plant.occupancy)
    var plant: Plant?

    @Relationship(deleteRule: .nullify, inverse: \PlannedPlanting.occupancy)
    var plannedPlanting: PlannedPlanting?

    init(
        cropName: String,
        variety: String? = nil,
        startDate: Date,
        endDate: Date? = nil,
        expectedHarvestDate: Date? = nil,
        expectedReleaseDate: Date? = nil,
        status: OccupancyStatus = .active,
        notes: String? = nil,
        growingSpace: GrowingSpace? = nil,
        plant: Plant? = nil
    ) {
        self.id = UUID()
        self.cropName = cropName
        self.variety = variety
        self.startDate = startDate
        self.endDate = endDate
        self.expectedHarvestDate = expectedHarvestDate
        self.expectedReleaseDate = expectedReleaseDate
        self.status = status
        self.notes = notes
        self.growingSpace = growingSpace
        self.plant = plant
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

enum OccupancyStatus: String, CaseIterable {
    case active
    case completed
    case cancelled

    var displayName: String {
        switch self {
        case .active: return "Active"
        case .completed: return "Completed"
        case .cancelled: return "Cancelled"
        }
    }
}
