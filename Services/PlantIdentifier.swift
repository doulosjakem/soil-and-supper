import Foundation

struct PlantIdentification: Identifiable, Equatable {
    let id = UUID()
    let cropName: String
    let variety: String?
    let confidence: Double
}

protocol PlantIdentifier {
    func identify(image: UIImage) async throws -> PlantIdentification
}
