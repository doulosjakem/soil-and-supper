import SwiftData

@Model
final class Harvest {
    var id: UUID
    var cropName: String
    var quantity: Double
    var unit: String
    var date: Date
    var notes: String?

    @Relationship(deleteRule: .cascade, inverse: \Plant.harvests)
    var plant: Plant?

    init(
        cropName: String,
        quantity: Double,
        unit: String,
        date: Date = Date(),
        notes: String? = nil,
        plant: Plant? = nil
    ) {
        self.id = UUID()
        self.cropName = cropName
        self.quantity = quantity
        self.unit = unit
        self.date = date
        self.notes = notes
        self.plant = plant
    }
}
