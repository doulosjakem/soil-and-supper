import Foundation
import UIKit
import SwiftUI

final class MockPlantIdentifier: ObservableObject, PlantIdentifier {
    let samplePredictions: [PlantIdentification] = [
        PlantIdentification(cropName: "Tomato", variety: "Roma", confidence: 0.92),
        PlantIdentification(cropName: "Basil", variety: nil, confidence: 0.87),
        PlantIdentification(cropName: "Zucchini", variety: "Black Beauty", confidence: 0.78),
        PlantIdentification(cropName: "Bell Pepper", variety: "California Wonder", confidence: 0.65),
        PlantIdentification(cropName: "Unknown", variety: nil, confidence: 0.41)
    ]

    func identify(image: UIImage) async throws -> PlantIdentification {
        try await Task.sleep(nanoseconds: 500_000_000)
        return samplePredictions.randomElement() ?? samplePredictions.last!
    }
}
