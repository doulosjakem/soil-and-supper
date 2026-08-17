import SwiftData

@Model
final class Seed {
    var id: UUID
    var cropName: String
    var variety: String?
    var state: SeedState
    var notes: String?
    var createdAt: Date
    var updatedAt: Date

    @Relationship(deleteRule: .nullify, inverse: \Garden.seeds)
    var garden: Garden?

    @Relationship(deleteRule: .nullify, inverse: \PlannedPlanting.seed)
    var plannedPlantings: [PlannedPlanting] = []

    init(cropName: String, variety: String? = nil, state: SeedState = .own, notes: String? = nil) {
        self.id = UUID()
        self.cropName = cropName
        self.variety = variety
        self.state = state
        self.notes = notes
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

enum SeedState: String, CaseIterable {
    case own
    case want

    var displayName: String {
        switch self {
        case .own: return "I Have"
        case .want: return "I Want"
        }
    }

    var symbolName: String {
        switch self {
        case .own: return "checkmark.circle.fill"
        case .want: return "plus.circle.fill"
        }
    }
}
