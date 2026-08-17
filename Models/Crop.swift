import Foundation

struct Crop: Identifiable, Equatable {
    let id: String
    let name: String
    let varieties: [Variety]
    let family: String?
    let frostTolerant: Bool
    let killedByFrost: Bool
    let transplantSensitive: Bool

    var defaultVariety: Variety? {
        varieties.first
    }

    func variety(named name: String) -> Variety? {
        varieties.first { $0.name.localizedCaseInsensitiveCompare(name) == .orderedSame }
    }
}

struct Variety: Identifiable, Equatable {
    let id: String
    let name: String
    let cropName: String
    let daysToMaturity: Int?
    let plantingWindows: [PlantingWindow]

    init(name: String, cropName: String, daysToMaturity: Int? = nil, plantingWindows: [PlantingWindow] = []) {
        self.id = "\(cropName)-\(name)"
        self.name = name
        self.cropName = cropName
        self.daysToMaturity = daysToMaturity
        self.plantingWindows = plantingWindows
    }
}

struct PlantingWindow: Equatable {
    let name: String
    let startMonth: Int
    let endMonth: Int
    let frostTolerant: Bool
    let notes: String?

    init(name: String, startMonth: Int, endMonth: Int, frostTolerant: Bool = false, notes: String? = nil) {
        self.name = name
        self.startMonth = startMonth
        self.endMonth = endMonth
        self.frostTolerant = frostTolerant
        self.notes = notes
    }
}

struct CropCharacteristics {
    let frostTolerant: Bool
    let killedByFrost: Bool
    let transplantSensitive: Bool
    let minimumGerminationTempCelsius: Int?
    let preferredTempRangeCelsius: (min: Int, max: Int)?
}
