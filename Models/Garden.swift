import SwiftData

@Model
final class Garden {
    var id: UUID
    var name: String
    var location: String?
    var createdAt: Date
    var updatedAt: Date

    @Relationship(deleteRule: .cascade, inverse: \Plant.garden)
    var plants: [Plant] = []

    init(name: String, location: String? = nil) {
        self.id = UUID()
        self.name = name
        self.location = location
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}
