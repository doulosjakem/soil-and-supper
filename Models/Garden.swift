import SwiftData

@Model
final class Garden {
    var id: UUID
    var name: String
    var location: String?
    var climateZone: String?
    var averageLastFrostDate: Date?
    var averageFirstFrostDate: Date?
    var createdAt: Date
    var updatedAt: Date

    @Relationship(deleteRule: .cascade, inverse: \Plant.garden)
    var plants: [Plant] = []

    @Relationship(deleteRule: .cascade, inverse: \GrowingSpace.garden)
    var growingSpaces: [GrowingSpace] = []

    @Relationship(deleteRule: .cascade, inverse: \Seed.garden)
    var seeds: [Seed] = []

    init(name: String, location: String? = nil) {
        self.id = UUID()
        self.name = name
        self.location = location
        self.climateZone = nil
        self.averageLastFrostDate = nil
        self.averageFirstFrostDate = nil
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}
