import Foundation

enum CropKnowledge {

    // MARK: - Lookup

    static func crop(named name: String) -> Crop? {
        catalog.first { $0.name.localizedCaseInsensitiveCompare(name) == .orderedSame }
    }

    static func varieties(for cropName: String) -> [Variety] {
        guard let crop = catalog.first(where: { $0.name.localizedCaseInsensitiveCompare(cropName) == .orderedSame }) else {
            return []
        }
        return crop.varieties
    }

    static func variety(named varietyName: String, for cropName: String) -> Variety? {
        guard let crop = catalog.first(where: { $0.name.localizedCaseInsensitiveCompare(cropName) == .orderedSame }) else {
            return nil
        }
        return crop.variety(named: varietyName)
    }

    static func plantingWindows(for cropName: String, variety: String? = nil) -> [PlantingWindow] {
        guard let crop = catalog.first(where: { $0.name.localizedCaseInsensitiveCompare(cropName) == .orderedSame }) else {
            return []
        }
        if let varietyName = variety, let matched = crop.variety(named: varietyName) {
            return matched.plantingWindows
        }
        let allWindows = crop.varieties.flatMap { $0.plantingWindows }
        return Array(Set(allWindows)).sorted { $0.startMonth < $1.startMonth }
    }

    static func maturityDays(for cropName: String, variety: String? = nil) -> Int? {
        guard let crop = catalog.first(where: { $0.name.localizedCaseInsensitiveCompare(cropName) == .orderedSame }) else {
            return nil
        }
        if let varietyName = variety, let matched = crop.variety(named: varietyName) {
            return matched.daysToMaturity
        }
        return crop.defaultVariety?.daysToMaturity
    }

    static func characteristics(for cropName: String) -> CropCharacteristics? {
        guard let crop = catalog.first(where: { $0.name.localizedCaseInsensitiveCompare(cropName) == .orderedSame }) else {
            return nil
        }
        return CropCharacteristics(
            frostTolerant: crop.frostTolerant,
            killedByFrost: crop.killedByFrost,
            transplantSensitive: crop.transplantSensitive,
            minimumGerminationTempCelsius: nil,
            preferredTempRangeCelsius: nil
        )
    }

    static func allCrops() -> [Crop] {
        catalog
    }

    // MARK: - Catalog

    private static let catalog: [Crop] = [
        Crop(
            id: "carrot",
            name: "Carrot",
            varieties: [
                Variety(name: "Nantes", cropName: "Carrot", daysToMaturity: 60, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 5, frostTolerant: true, notes: "Can be sown as soon as soil can be worked"),
                    PlantingWindow(name: "Fall", startMonth: 7, endMonth: 9, frostTolerant: true, notes: "Sow 8-10 weeks before first frost")
                ]),
                Variety(name: "Napoli", cropName: "Carrot", daysToMaturity: 70, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 5, frostTolerant: true),
                    PlantingWindow(name: "Fall", startMonth: 7, endMonth: 9, frostTolerant: true)
                ]),
                Variety(name: "Danvers", cropName: "Carrot", daysToMaturity: 75, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 5, frostTolerant: true),
                    PlantingWindow(name: "Fall", startMonth: 7, endMonth: 9, frostTolerant: true)
                ])
            ],
            family: "Apiaceae",
            frostTolerant: true,
            killedByFrost: false,
            transplantSensitive: true
        ),
        Crop(
            id: "radish",
            name: "Radish",
            varieties: [
                Variety(name: "Cherry Belle", cropName: "Radish", daysToMaturity: 22, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 5, frostTolerant: true),
                    PlantingWindow(name: "Fall", startMonth: 8, endMonth: 9, frostTolerant: true)
                ]),
                Variety(name: "French Breakfast", cropName: "Radish", daysToMaturity: 25, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 5, frostTolerant: true),
                    PlantingWindow(name: "Fall", startMonth: 8, endMonth: 9, frostTolerant: true)
                ])
            ],
            family: "Brassicaceae",
            frostTolerant: true,
            killedByFrost: false,
            transplantSensitive: true
        ),
        Crop(
            id: "lettuce",
            name: "Lettuce",
            varieties: [
                Variety(name: "Romaine", cropName: "Lettuce", daysToMaturity: 70, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 5, frostTolerant: true),
                    PlantingWindow(name: "Summer", startMonth: 6, endMonth: 8, frostTolerant: false, notes: "Heat-sensitive; provide afternoon shade"),
                    PlantingWindow(name: "Fall", startMonth: 8, endMonth: 10, frostTolerant: true)
                ]),
                Variety(name: "Butterhead", cropName: "Lettuce", daysToMaturity: 60, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 5, frostTolerant: true),
                    PlantingWindow(name: "Fall", startMonth: 8, endMonth: 10, frostTolerant: true)
                ]),
                Variety(name: "Salanova", cropName: "Lettuce", daysToMaturity: 45, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 5, frostTolerant: true),
                    PlantingWindow(name: "Fall", startMonth: 8, endMonth: 10, frostTolerant: true)
                ])
            ],
            family: "Asteraceae",
            frostTolerant: true,
            killedByFrost: false,
            transplantSensitive: false
        ),
        Crop(
            id: "spinach",
            name: "Spinach",
            varieties: [
                Variety(name: "Bloomsdale", cropName: "Spinach", daysToMaturity: 40, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 5, frostTolerant: true),
                    PlantingWindow(name: "Fall", startMonth: 8, endMonth: 10, frostTolerant: true),
                    PlantingWindow(name: "Overwinter", startMonth: 9, endMonth: 11, frostTolerant: true, notes: "Sow late for early spring harvest")
                ]),
                Variety(name: "Space", cropName: "Spinach", daysToMaturity: 45, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 5, frostTolerant: true),
                    PlantingWindow(name: "Fall", startMonth: 8, endMonth: 10, frostTolerant: true)
                ])
            ],
            family: "Amaranthaceae",
            frostTolerant: true,
            killedByFrost: false,
            transplantSensitive: true
        ),
        Crop(
            id: "bush-bean",
            name: "Bush Bean",
            varieties: [
                Variety(name: "Blue Lake 274", cropName: "Bush Bean", daysToMaturity: 55, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 5, endMonth: 6, frostTolerant: false, notes: "Sow after last frost"),
                    PlantingWindow(name: "Summer", startMonth: 7, endMonth: 8, frostTolerant: false)
                ]),
                Variety(name: "Provider", cropName: "Bush Bean", daysToMaturity: 50, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 5, endMonth: 6, frostTolerant: false, notes: "Sow after last frost"),
                    PlantingWindow(name: "Summer", startMonth: 7, endMonth: 8, frostTolerant: false)
                ])
            ],
            family: "Fabaceae",
            frostTolerant: false,
            killedByFrost: true,
            transplantSensitive: true
        ),
        Crop(
            id: "broccoli",
            name: "Broccoli",
            varieties: [
                Variety(name: "Waltham 26", cropName: "Broccoli", daysToMaturity: 70, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 4, frostTolerant: true, notes: "Transplant after last frost"),
                    PlantingWindow(name: "Fall", startMonth: 7, endMonth: 8, frostTolerant: true, notes: "Sow midsummer for fall harvest")
                ]),
                Variety(name: "Di Cicco", cropName: "Broccoli", daysToMaturity: 60, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 4, frostTolerant: true),
                    PlantingWindow(name: "Fall", startMonth: 7, endMonth: 8, frostTolerant: true)
                ])
            ],
            family: "Brassicaceae",
            frostTolerant: true,
            killedByFrost: false,
            transplantSensitive: false
        ),
        Crop(
            id: "tomato",
            name: "Tomato",
            varieties: [
                Variety(name: "San Marzano", cropName: "Tomato", daysToMaturity: 80, plantingWindows: [
                    PlantingWindow(name: "Summer", startMonth: 5, endMonth: 6, frostTolerant: false, notes: "Transplant after last frost")
                ]),
                Variety(name: "Roma", cropName: "Tomato", daysToMaturity: 75, plantingWindows: [
                    PlantingWindow(name: "Summer", startMonth: 5, endMonth: 6, frostTolerant: false, notes: "Transplant after last frost")
                ]),
                Variety(name: "Cherry", cropName: "Tomato", daysToMaturity: 65, plantingWindows: [
                    PlantingWindow(name: "Summer", startMonth: 5, endMonth: 6, frostTolerant: false, notes: "Transplant after last frost")
                ])
            ],
            family: "Solanaceae",
            frostTolerant: false,
            killedByFrost: true,
            transplantSensitive: false
        ),
        Crop(
            id: "cucumber",
            name: "Cucumber",
            varieties: [
                Variety(name: "Marketmore 76", cropName: "Cucumber", daysToMaturity: 60, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 5, endMonth: 6, frostTolerant: false, notes: "Sow after last frost"),
                    PlantingWindow(name: "Summer", startMonth: 7, endMonth: 7, frostTolerant: false)
                ]),
                Variety(name: "Straight Eight", cropName: "Cucumber", daysToMaturity: 58, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 5, endMonth: 6, frostTolerant: false, notes: "Sow after last frost"),
                    PlantingWindow(name: "Summer", startMonth: 7, endMonth: 7, frostTolerant: false)
                ])
            ],
            family: "Cucurbitaceae",
            frostTolerant: false,
            killedByFrost: true,
            transplantSensitive: true
        ),
        Crop(
            id: "potato",
            name: "Potato",
            varieties: [
                Variety(name: "Yukon Gold", cropName: "Potato", daysToMaturity: 70, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 4, frostTolerant: false, notes: "Plant seed potatoes as soon as soil can be worked")
                ]),
                Variety(name: "Russet", cropName: "Potato", daysToMaturity: 90, plantingWindows: [
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 4, frostTolerant: false, notes: "Plant seed potatoes as soon as soil can be worked")
                ])
            ],
            family: "Solanaceae",
            frostTolerant: false,
            killedByFrost: false,
            transplantSensitive: false
        ),
        Crop(
            id: "garlic",
            name: "Garlic",
            varieties: [
                Variety(name: "Hardneck", cropName: "Garlic", daysToMaturity: 240, plantingWindows: [
                    PlantingWindow(name: "Fall", startMonth: 10, endMonth: 11, frostTolerant: true, notes: "Plant cloves 4-6 weeks before first frost")
                ]),
                Variety(name: "Softneck", cropName: "Garlic", daysToMaturity: 180, plantingWindows: [
                    PlantingWindow(name: "Fall", startMonth: 10, endMonth: 11, frostTolerant: true, notes: "Plant cloves 4-6 weeks before first frost"),
                    PlantingWindow(name: "Spring", startMonth: 3, endMonth: 4, frostTolerant: true, notes: "Plant as soon as soil thaws")
                ])
            ],
            family: "Amaryllidaceae",
            frostTolerant: true,
            killedByFrost: false,
            transplantSensitive: false
        )
    ]
}
