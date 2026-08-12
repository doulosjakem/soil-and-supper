import SwiftData

@Model
final class PlantPhoto {
    var id: UUID
    var fileName: String
    var createdAt: Date

    @Relationship(deleteRule: .nullify, inverse: \Plant.photos)
    var plant: Plant?

    init(fileName: String) {
        self.id = UUID()
        self.fileName = fileName
        self.createdAt = Date()
    }
}
