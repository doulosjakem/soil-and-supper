import Foundation

enum SeedAvailability {
    case owned
    case wanted
    case notTracked

    var label: String {
        switch self {
        case .owned: return "You have seeds"
        case .wanted: return "You want seeds"
        case .notTracked: return "Not on your Seed Shelf"
        }
    }
}

enum SuggestionRank: Int, Comparable {
    case bestFit = 0
    case alsoGood = 1
    case notRecommended = 2

    var label: String {
        switch self {
        case .bestFit: return "Best fit"
        case .alsoGood: return "Also good"
        case .notRecommended: return "Not recommended"
        }
    }

    static func < (lhs: SuggestionRank, rhs: SuggestionRank) -> Bool {
        lhs.rawValue < rhs.rawValue
    }
}

struct PlantingSuggestion: Identifiable, Equatable {
    let id: UUID
    let cropName: String
    let varietyName: String?
    let suggestedPlantingDate: Date
    let estimatedHarvestDate: Date?
    let estimatedReleaseDate: Date?
    let growingSpace: GrowingSpace?
    let seedAvailability: SeedAvailability
    let ranking: SuggestionRank
    let warnings: [String]
    let reason: String

    init(
        id: UUID = UUID(),
        cropName: String,
        varietyName: String? = nil,
        suggestedPlantingDate: Date,
        estimatedHarvestDate: Date? = nil,
        estimatedReleaseDate: Date? = nil,
        growingSpace: GrowingSpace? = nil,
        seedAvailability: SeedAvailability = .notTracked,
        ranking: SuggestionRank = .alsoGood,
        warnings: [String] = [],
        reason: String = ""
    ) {
        self.id = id
        self.cropName = cropName
        self.varietyName = varietyName
        self.suggestedPlantingDate = suggestedPlantingDate
        self.estimatedHarvestDate = estimatedHarvestDate
        self.estimatedReleaseDate = estimatedReleaseDate
        self.growingSpace = growingSpace
        self.seedAvailability = seedAvailability
        self.ranking = ranking
        self.warnings = warnings
        self.reason = reason
    }
}

protocol PlanningEngineProtocol {
    func suggestions(
        for growingSpace: GrowingSpace,
        on date: Date,
        in garden: Garden,
        seeds: [Seed],
        desires: [Desire]
    ) -> [PlantingSuggestion]

    func whatCanBePlantedNow(
        in garden: Garden,
        on date: Date,
        seeds: [Seed],
        desires: [Desire]
    ) -> [PlantingSuggestion]

    func suggestions(
        using seeds: [Seed],
        in garden: Garden,
        on date: Date,
        growingSpaces: [GrowingSpace],
        desires: [Desire]
    ) -> [PlantingSuggestion]
}

struct DefaultPlanningEngine: PlanningEngineProtocol {

    func suggestions(
        for growingSpace: GrowingSpace,
        on date: Date,
        in garden: Garden,
        seeds: [Seed],
        desires: [Desire]
    ) -> [PlantingSuggestion] {
        guard isSpaceAvailable(growingSpace) else {
            return []
        }

        return evaluateCrops(for: growingSpace, on: date, in: garden, seeds: seeds, desires: desires)
    }

    func whatCanBePlantedNow(
        in garden: Garden,
        on date: Date,
        seeds: [Seed],
        desires: [Desire]
    ) -> [PlantingSuggestion] {
        let openSpaces = garden.growingSpaces.filter { isSpaceAvailable($0) }
        guard !openSpaces.isEmpty else { return [] }

        var allSuggestions: [PlantingSuggestion] = []
        for space in openSpaces {
            let suggestions = evaluateCrops(for: space, on: date, in: garden, seeds: seeds, desires: desires)
            allSuggestions.append(contentsOf: suggestions)
        }

        return deduplicateAndRank(allSuggestions)
    }

    func suggestions(
        using seeds: [Seed],
        in garden: Garden,
        on date: Date,
        growingSpaces: [GrowingSpace],
        desires: [Desire]
    ) -> [PlantingSuggestion] {
        let ownedSeeds = seeds.filter { $0.state == .own }
        guard !ownedSeeds.isEmpty else { return [] }

        let openSpaces = growingSpaces.filter { isSpaceAvailable($0) }
        guard !openSpaces.isEmpty else { return [] }

        var allSuggestions: [PlantingSuggestion] = []

        for space in openSpaces {
            for seed in ownedSeeds {
                guard let crop = CropKnowledge.crop(named: seed.cropName) else { continue }

                let variety = seed.variety.flatMap { crop.variety(named: $0) }
                let (allowed, warnings) = canPlantNow(crop: crop, variety: variety, on: date, in: garden)
                guard allowed else { continue }

                let matchingDesire = desires.first { desire in
                    desire.cropName.localizedCaseInsensitiveCompare(seed.cropName) == .orderedSame
                    && !desire.isFulfilled && !desire.isCancelled && !desire.isExpired
                }

                let rank: SuggestionRank
                if let _ = matchingDesire {
                    rank = .bestFit
                } else {
                    rank = .bestFit
                }

                let estimatedHarvest = estimatedHarvest(from: date, variety: variety, crop: crop)
                let reason = reasonText(for: seed.cropName, seedAvailability: .owned, desire: matchingDesire)

                allSuggestions.append(PlantingSuggestion(
                    cropName: crop.name,
                    varietyName: seed.variety,
                    suggestedPlantingDate: date,
                    estimatedHarvestDate: estimatedHarvest,
                    growingSpace: space,
                    seedAvailability: .owned,
                    ranking: rank,
                    warnings: warnings,
                    reason: reason
                ))
            }
        }

        return allSuggestions.sorted { $0.ranking < $1.ranking }
    }

    // MARK: - Private

    private func isSpaceAvailable(_ space: GrowingSpace) -> Bool {
        let activeOccupancies = space.occupancies.filter { $0.status == .active }
        return activeOccupancies.isEmpty
    }

    private func evaluateCrops(
        for space: GrowingSpace,
        on date: Date,
        in garden: Garden,
        seeds: [Seed],
        desires: [Desire]
    ) -> [PlantingSuggestion] {
        var suggestions: [PlantingSuggestion] = []

        for crop in CropKnowledge.allCrops() {
            let (allowed, warnings) = canPlantNow(crop: crop, variety: nil, on: date, in: garden)
            guard allowed else { continue }

            let seedAvailability = seedAvailability(for: crop.name, in: seeds)
            let matchingDesire = desires.first { desire in
                desire.cropName.localizedCaseInsensitiveCompare(crop.name) == .orderedSame
                && !desire.isFulfilled && !desire.isCancelled && !desire.isExpired
            }
            let rank = rankSuggestion(seedAvailability: seedAvailability, desire: matchingDesire)

            let estimatedHarvest = estimatedHarvest(from: date, variety: nil, crop: crop)
            let reason = reasonText(for: crop.name, seedAvailability: seedAvailability, desire: matchingDesire)

            suggestions.append(PlantingSuggestion(
                cropName: crop.name,
                varietyName: nil,
                suggestedPlantingDate: date,
                estimatedHarvestDate: estimatedHarvest,
                growingSpace: space,
                seedAvailability: seedAvailability,
                ranking: rank,
                warnings: warnings,
                reason: reason
            ))
        }

        return suggestions.sorted { $0.ranking < $1.ranking }
    }

    private func canPlantNow(crop: Crop, variety: Variety?, on date: Date, in garden: Garden) -> (allowed: Bool, warnings: [String]) {
        var warnings: [String] = []

        let currentMonth = Calendar.current.component(.month, from: date)
        let windows = variety?.plantingWindows ?? crop.varieties.flatMap { $0.plantingWindows }

        let inWindow = windows.contains { window in
            if window.startMonth <= window.endMonth {
                return currentMonth >= window.startMonth && currentMonth <= window.endMonth
            } else {
                return currentMonth >= window.startMonth || currentMonth <= window.endMonth
            }
        }

        if !inWindow {
            return (false, ["Planting window has closed for this crop."])
        }

        if crop.killedByFrost, let lastFrost = garden.averageLastFrostDate, date < lastFrost {
            return (false, ["This crop is killed by frost. Wait until after the average last frost."])
        }

        if let firstFrost = garden.averageFirstFrostDate,
           let daysToMaturity = variety?.daysToMaturity ?? crop.defaultVariety?.daysToMaturity {
            let daysRemaining = Calendar.current.dateComponents([.day], from: date, to: firstFrost).day ?? 0
            if daysRemaining < daysToMaturity {
                return (false, ["Too little season remaining. Needs \(daysToMaturity) days but only \(daysRemaining) days until first frost."])
            }
        }

        return (true, warnings)
    }

    private func seedAvailability(for cropName: String, in seeds: [Seed]) -> SeedAvailability {
        let owned = seeds.contains { $0.state == .own && $0.cropName.localizedCaseInsensitiveCompare(cropName) == .orderedSame }
        if owned { return .owned }

        let wanted = seeds.contains { $0.state == .want && $0.cropName.localizedCaseInsensitiveCompare(cropName) == .orderedSame }
        if wanted { return .wanted }

        return .notTracked
    }

    private func rankSuggestion(seedAvailability: SeedAvailability, desire: Desire?) -> SuggestionRank {
        if seedAvailability == .owned {
            return desire != nil ? .bestFit : .bestFit
        }
        if seedAvailability == .wanted {
            return desire != nil ? .alsoGood : .alsoGood
        }
        if let _ = desire {
            return .alsoGood
        }
        return .alsoGood
    }

    private func estimatedHarvest(from date: Date, variety: Variety?, crop: Crop) -> Date? {
        guard let daysToMaturity = variety?.daysToMaturity ?? crop.defaultVariety?.daysToMaturity else { return nil }
        return Calendar.current.date(byAdding: .day, value: daysToMaturity, to: date)
    }

    private func reasonText(for cropName: String, seedAvailability: SeedAvailability, desire: Desire?) -> String {
        if seedAvailability == .owned {
            return "You have seeds for this."
        }
        if seedAvailability == .wanted {
            return "You want these seeds."
        }
        if desire != nil {
            return "This matches a desire."
        }
        return "Fits the current season."
    }

    private func deduplicateAndRank(_ suggestions: [PlantingSuggestion]) -> [PlantingSuggestion] {
        let grouped = Dictionary(grouping: suggestions) { $0.cropName }
        return grouped.compactMap { _, group in
            group.min { lhs, rhs in
                lhs.ranking < rhs.ranking
            }
        }.sorted { $0.ranking < $1.ranking }
    }
}
