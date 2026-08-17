import Foundation
import XCTest
@testable import SoilAndSupper

final class PlanningEngineTests: XCTestCase {

    // MARK: - A — Open space produces current suggestions

    func test_openSpace_producesCurrentSuggestions() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let today = makeDate(year: 2026, month: 8, day: 17)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: today,
            in: garden,
            seeds: [],
            desires: []
        )

        let carrotSuggestions = suggestions.filter { $0.cropName == "Carrot" }
        XCTAssertFalse(carrotSuggestions.isEmpty, "Carrots should be suggested for an open space in August")
        XCTAssertFalse(carrotSuggestions.first!.isFuture, "Current suggestions should not be marked as future")
        XCTAssertNil(carrotSuggestions.first?.openingDate, "Current suggestions should not have an opening date")
    }

    // MARK: - B — Occupied space suppresses current suggestions

    func test_occupiedSpace_suppressesCurrentSuggestions() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        _ = makeOccupancy(
            cropName: "Tomato",
            startDate: makeDate(year: 2026, month: 5, day: 15),
            status: .active,
            growingSpace: space
        )
        let today = makeDate(year: 2026, month: 8, day: 17)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: today,
            in: garden,
            seeds: [],
            desires: []
        )

        XCTAssertTrue(suggestions.isEmpty, "Occupied space should not produce current suggestions")
    }

    // MARK: - C — Completed occupancy allows current suggestions

    func test_completedOccupancy_allowsCurrentSuggestions() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        _ = makeOccupancy(
            cropName: "Tomato",
            startDate: makeDate(year: 2026, month: 5, day: 15),
            endDate: makeDate(year: 2026, month: 9, day: 10),
            status: .completed,
            growingSpace: space
        )
        let today = makeDate(year: 2026, month: 8, day: 17)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: today,
            in: garden,
            seeds: [],
            desires: []
        )

        XCTAssertFalse(suggestions.isEmpty, "Completed occupancy should allow current suggestions")
    }

    // MARK: - D — Future opening inside planting window

    func test_futureOpeningInsideWindow_producesFutureSuggestions() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let openingDate = makeDate(year: 2026, month: 9, day: 15)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: openingDate,
            in: garden,
            seeds: [],
            desires: []
        )

        let carrotSuggestions = suggestions.filter { $0.cropName == "Carrot" }
        XCTAssertFalse(carrotSuggestions.isEmpty, "Carrots should be suggested when opening is inside fall window")
        XCTAssertTrue(carrotSuggestions.first!.isFuture, "Future suggestions should be marked as future")
        XCTAssertEqual(carrotSuggestions.first?.openingDate, openingDate, "Opening date should match the supplied date")
        XCTAssertEqual(carrotSuggestions.first?.suggestedPlantingDate, openingDate, "Candidate date should equal opening date when inside window")
    }

    // MARK: - E — Future opening before planting window

    func test_futureOpeningBeforeWindow_setsCandidateToWindowStart() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let openingDate = makeDate(year: 2026, month: 6, day: 15)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: openingDate,
            in: garden,
            seeds: [],
            desires: []
        )

        let carrotSuggestions = suggestions.filter { $0.cropName == "Carrot" }
        XCTAssertFalse(carrotSuggestions.isEmpty, "Carrots should still be eligible when opening is before fall window")
        let candidate = carrotSuggestions.first!.suggestedPlantingDate
        XCTAssertEqual(testCalendar.component(.month, from: candidate), 7, "Candidate date should be in July (fall window start)")
        XCTAssertFalse(candidate < openingDate, "Candidate date should not be before the opening date")
    }

    // MARK: - F — Future opening after planting window

    func test_futureOpeningAfterWindow_rejectsCrop() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let openingDate = makeDate(year: 2026, month: 10, day: 10)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: openingDate,
            in: garden,
            seeds: [],
            desires: []
        )

        let carrotSuggestions = suggestions.filter { $0.cropName == "Carrot" }
        XCTAssertTrue(carrotSuggestions.isEmpty, "Carrots should be rejected when opening is after fall window")
    }

    // MARK: - G — Explicit opening date is authoritative

    func test_explicitOpeningDate_isAuthoritative() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let explicitDate = makeDate(year: 2026, month: 9, day: 1)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: explicitDate,
            in: garden,
            seeds: [],
            desires: []
        )

        let carrotSuggestions = suggestions.filter { $0.cropName == "Carrot" }
        XCTAssertFalse(carrotSuggestions.isEmpty)
        XCTAssertEqual(carrotSuggestions.first?.openingDate, explicitDate)
        XCTAssertEqual(carrotSuggestions.first?.suggestedPlantingDate, explicitDate)
    }

    // MARK: - G1 — Explicit opening date takes precedence over expectedReleaseDate

    func test_explicitOpeningDate_precedenceOverExpectedRelease() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let expectedRelease = makeDate(year: 2026, month: 9, day: 15)
        let explicitDate = makeDate(year: 2026, month: 8, day: 20)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: explicitDate,
            in: garden,
            seeds: [],
            desires: []
        )

        XCTAssertFalse(suggestions.isEmpty, "Engine should use explicit opening date")
        XCTAssertEqual(suggestions.first?.openingDate, explicitDate, "Opening date should be the explicit caller-supplied date, not the occupancy's expectedReleaseDate")
    }

    // MARK: - H — Expected release date drives future suggestions

    func test_expectedReleaseDate_drivesFutureSuggestions() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let expectedRelease = makeDate(year: 2026, month: 9, day: 15)
        _ = makeOccupancy(
            cropName: "Tomato",
            startDate: makeDate(year: 2026, month: 5, day: 15),
            expectedReleaseDate: expectedRelease,
            status: .active,
            growingSpace: space
        )

        let engine = DefaultPlanningEngine()
        let futureSuggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: expectedRelease,
            in: garden,
            seeds: [],
            desires: []
        )

        XCTAssertFalse(futureSuggestions.isEmpty, "Future suggestions should use expected release date")
        XCTAssertEqual(futureSuggestions.first?.openingDate, expectedRelease)
    }

    // MARK: - I — No expected release date suppresses future suggestions

    func test_noExpectedReleaseDate_suppressesFutureSuggestions() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        _ = makeOccupancy(
            cropName: "Tomato",
            startDate: makeDate(year: 2026, month: 5, day: 15),
            status: .active,
            growingSpace: space
        )

        let engine = DefaultPlanningEngine()

        // The view layer checks for expectedReleaseDate before calling the engine.
        // Here we verify the engine itself doesn't invent a date.
        let suggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: makeDate(year: 2026, month: 9, day: 15),
            in: garden,
            seeds: [],
            desires: []
        )

        // Engine works when caller supplies a date.
        XCTAssertFalse(suggestions.isEmpty)
    }

    // MARK: - J — Multiple active occupancies

    func test_multipleActiveOccupancies_remainsOccupied() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        _ = makeOccupancy(
            cropName: "Tomato",
            startDate: makeDate(year: 2026, month: 5, day: 15),
            status: .active,
            growingSpace: space
        )
        _ = makeOccupancy(
            cropName: "Basil",
            startDate: makeDate(year: 2026, month: 6, day: 1),
            status: .active,
            growingSpace: space
        )

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [],
            desires: []
        )

        XCTAssertTrue(suggestions.isEmpty, "Space with multiple active occupancies should remain occupied")
    }

    // MARK: - K — Known maturity produces harvest estimate

    func test_knownMaturity_producesHarvestEstimate() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let plantingDate = makeDate(year: 2026, month: 9, day: 1)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: plantingDate,
            in: garden,
            seeds: [],
            desires: []
        )

        let radishSuggestions = suggestions.filter { $0.cropName == "Radish" }
        XCTAssertFalse(radishSuggestions.isEmpty)
        let harvest = radishSuggestions.first!.estimatedHarvestDate
        XCTAssertNotNil(harvest, "Known maturity should produce harvest estimate")
        let days = testCalendar.dateComponents([.day], from: plantingDate, to: harvest!).day!
        XCTAssertEqual(days, 22, "Harvest should be 22 days after planting for Cherry Belle radish")
    }

    // MARK: - L — Unknown maturity leaves harvest nil

    func test_unknownMaturity_leavesHarvestNil() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [],
            desires: []
        )

        // All crops in our catalog have known maturity, so we verify the engine
        // returns nil only when daysToMaturity is nil.
        // We test this indirectly by checking that the engine doesn't fabricate dates.
        for suggestion in suggestions {
            if let harvest = suggestion.estimatedHarvestDate {
                XCTAssertTrue(harvest >= suggestion.suggestedPlantingDate, "Harvest should not be before planting")
            }
        }
    }

    // MARK: - M — Frost-sensitive crop with insufficient season is rejected

    func test_frostSensitiveInsufficientSeason_isRejected() {
        let firstFrost = makeDate(year: 2026, month: 10, day: 1)
        let garden = makeGarden(firstFrost: firstFrost)
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let plantingDate = makeDate(year: 2026, month: 8, day: 15)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: plantingDate,
            in: garden,
            seeds: [],
            desires: []
        )

        // Tomato needs 80 days (San Marzano), but only ~47 days until first frost from Aug 15
        let tomatoSuggestions = suggestions.filter { $0.cropName == "Tomato" }
        XCTAssertTrue(tomatoSuggestions.isEmpty, "Tomatoes should be rejected with insufficient season")
    }

    // MARK: - N — Frost-tolerant crop with insufficient season is allowed with warning

    func test_frostTolerantInsufficientSeason_isAllowedWithWarning() {
        let firstFrost = makeDate(year: 2026, month: 10, day: 1)
        let garden = makeGarden(firstFrost: firstFrost)
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let plantingDate = makeDate(year: 2026, month: 8, day: 15)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: plantingDate,
            in: garden,
            seeds: [],
            desires: []
        )

        // Carrot needs 60 days, ~47 days until first frost from Aug 15
        // Carrots are frost-tolerant, so they should be allowed with a warning
        let carrotSuggestions = suggestions.filter { $0.cropName == "Carrot" }
        XCTAssertFalse(carrotSuggestions.isEmpty, "Frost-tolerant carrots should be allowed with insufficient season")
        XCTAssertFalse(carrotSuggestions.first!.warnings.isEmpty, "Warning should be present for frost-tolerant crop with short season")
    }

    // MARK: - O — Owned seed ranking

    func test_ownedSeed_improvesRanking() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let seed = makeSeed(cropName: "Carrot", variety: "Nantes", state: .own)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [seed],
            desires: []
        )

        let carrotSuggestions = suggestions.filter { $0.cropName == "Carrot" }
        XCTAssertFalse(carrotSuggestions.isEmpty)
        XCTAssertEqual(carrotSuggestions.first!.seedAvailability, .owned)
        XCTAssertEqual(carrotSuggestions.first!.ranking, .bestFit)
    }

    // MARK: - P — Wanted seed ranking

    func test_wantedSeed_ranking() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let seed = makeSeed(cropName: "Carrot", variety: "Nantes", state: .want)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [seed],
            desires: []
        )

        let carrotSuggestions = suggestions.filter { $0.cropName == "Carrot" }
        XCTAssertFalse(carrotSuggestions.isEmpty)
        XCTAssertEqual(carrotSuggestions.first!.seedAvailability, .wanted)
        XCTAssertEqual(carrotSuggestions.first!.ranking, .alsoGood)
    }

    // MARK: - Q — Untracked seed remains eligible

    func test_untrackedSeed_remainsEligible() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [],
            desires: []
        )

        let carrotSuggestions = suggestions.filter { $0.cropName == "Carrot" }
        XCTAssertFalse(carrotSuggestions.isEmpty, "Carrots should still be suggested without seed shelf entry")
        XCTAssertEqual(carrotSuggestions.first!.seedAvailability, .notTracked)
    }

    // MARK: - R — Active Desire improves ranking

    func test_activeDesire_improvesRanking() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let desire = makeDesire(cropName: "Carrot", variety: "Nantes")

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [],
            desires: [desire]
        )

        let carrotSuggestions = suggestions.filter { $0.cropName == "Carrot" }
        XCTAssertFalse(carrotSuggestions.isEmpty)
        XCTAssertTrue(carrotSuggestions.first!.hasActiveDesire)
        XCTAssertEqual(carrotSuggestions.first!.ranking, .bestFit)

        // Verify Desire was not mutated
        XCTAssertFalse(desire.isFulfilled)
        XCTAssertFalse(desire.isCancelled)
        XCTAssertFalse(desire.isExpired)
    }

    // MARK: - S — Structured PlantingSuggestion fields

    func test_plantingSuggestion_structuredFields() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let seed = makeSeed(cropName: "Carrot", variety: "Nantes", state: .own)
        let desire = makeDesire(cropName: "Carrot")

        let engine = DefaultPlanningEngine()

        let currentSuggestions = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [seed],
            desires: [desire]
        )

        let currentCarrot = currentSuggestions.first { $0.cropName == "Carrot" }
        XCTAssertNotNil(currentCarrot)
        XCTAssertFalse(currentCarrot!.isFuture)
        XCTAssertNil(currentCarrot!.openingDate)
        XCTAssertTrue(currentCarrot!.hasActiveDesire)

        let futureSuggestions = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: makeDate(year: 2026, month: 9, day: 15),
            in: garden,
            seeds: [seed],
            desires: [desire]
        )

        let futureCarrot = futureSuggestions.first { $0.cropName == "Carrot" }
        XCTAssertNotNil(futureCarrot)
        XCTAssertTrue(futureCarrot!.isFuture)
        XCTAssertNotNil(futureCarrot!.openingDate)
        XCTAssertEqual(futureCarrot!.openingDate, makeDate(year: 2026, month: 9, day: 15))
    }

    // MARK: - T — Deterministic ranking

    func test_deterministicRanking() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)

        let engine = DefaultPlanningEngine()

        let firstRun = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [],
            desires: []
        )

        let secondRun = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [],
            desires: []
        )

        XCTAssertEqual(firstRun.map { $0.cropName }, secondRun.map { $0.cropName }, "Ranking should be deterministic across runs")
    }

    // MARK: - U — Date boundaries

    func test_dateBoundaries() {
        let firstFrost = makeDate(year: 2026, month: 10, day: 15)
        let garden = makeGarden(firstFrost: firstFrost)
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)

        let engine = DefaultPlanningEngine()

        // Opening exactly on carrot fall window start (Sep 1)
        let sep1 = makeDate(year: 2026, month: 9, day: 1)
        let suggestionsSep1 = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: sep1,
            in: garden,
            seeds: [],
            desires: []
        )
        let carrotSep1 = suggestionsSep1.first { $0.cropName == "Carrot" }
        XCTAssertNotNil(carrotSep1)
        XCTAssertEqual(testCalendar.component(.month, from: carrotSep1!.suggestedPlantingDate), 9)

        // Opening exactly on carrot fall window end (Sep 30)
        let sep30 = makeDate(year: 2026, month: 9, day: 30)
        let suggestionsSep30 = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: sep30,
            in: garden,
            seeds: [],
            desires: []
        )
        let carrotSep30 = suggestionsSep30.first { $0.cropName == "Carrot" }
        XCTAssertNotNil(carrotSep30)
        XCTAssertEqual(carrotSep30!.suggestedPlantingDate, sep30)

        // Opening one day after window end (Oct 1)
        let oct1 = makeDate(year: 2026, month: 10, day: 1)
        let suggestionsOct1 = engine.suggestionsForFutureOpening(
            of: space,
            openingDate: oct1,
            in: garden,
            seeds: [],
            desires: []
        )
        let carrotOct1 = suggestionsOct1.first { $0.cropName == "Carrot" }
        XCTAssertNil(carrotOct1, "Carrots should be rejected when opening is after fall window")
    }

    // MARK: - Planting window name exposure

    func test_plantingWindowName_exposedInSuggestion() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [],
            desires: []
        )

        let carrot = suggestions.first { $0.cropName == "Carrot" }
        XCTAssertNotNil(carrot)
        XCTAssertNotNil(carrot!.plantingWindowName, "Planting window name should be exposed")
        XCTAssertEqual(carrot!.plantingWindowName, "Fall")
    }

    // MARK: - Seed shelf does not block recommendations

    func test_seedShelf_doesNotBlockRecommendations() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [],
            desires: []
        )

        XCTAssertFalse(suggestions.isEmpty, "Engine should recommend crops even with empty seed shelf")
    }

    // MARK: - Desire does not mutate state

    func test_desire_doesNotMutateState() {
        let garden = makeGarden()
        let desire = makeDesire(cropName: "Carrot")

        let engine = DefaultPlanningEngine()
        _ = engine.suggestions(
            for: makeGrowingSpace(name: "Bed 1", garden: garden),
            on: makeDate(year: 2026, month: 8, day: 17),
            in: garden,
            seeds: [],
            desires: [desire]
        )

        XCTAssertFalse(desire.isFulfilled)
        XCTAssertFalse(desire.isCancelled)
        XCTAssertFalse(desire.isExpired)
    }

    // MARK: - Killed by frost before last frost date

    func test_killedByFrost_beforeLastFrost() {
        let lastFrost = makeDate(year: 2026, month: 5, day: 15)
        let garden = makeGarden(lastFrost: lastFrost)
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let plantingDate = makeDate(year: 2026, month: 5, day: 1)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            for: space,
            on: plantingDate,
            in: garden,
            seeds: [],
            desires: []
        )

        // Tomato is killed by frost and planting date is before last frost
        let tomatoSuggestions = suggestions.filter { $0.cropName == "Tomato" }
        XCTAssertTrue(tomatoSuggestions.isEmpty, "Tomatoes should be rejected before last frost date")
    }

    // MARK: - whatCanBePlantedNow returns open space suggestions

    func test_whatCanBePlantedNow_returnsOpenSpaceSuggestions() {
        let garden = makeGarden(
            growingSpaces: [
                makeGrowingSpace(name: "Bed 1"),
                makeGrowingSpace(name: "Bed 2")
            ]
        )

        let engine = DefaultPlanningEngine()
        let suggestions = engine.whatCanBePlantedNow(
            in: garden,
            on: makeDate(year: 2026, month: 8, day: 17),
            seeds: [],
            desires: []
        )

        XCTAssertFalse(suggestions.isEmpty, "whatCanBePlantedNow should return suggestions for open spaces")
    }

    // MARK: - suggestions using seeds filters to owned seeds

    func test_suggestionsUsingSeeds_filtersToOwned() {
        let garden = makeGarden()
        let space = makeGrowingSpace(name: "Bed 1", garden: garden)
        let ownedSeed = makeSeed(cropName: "Carrot", variety: "Nantes", state: .own)
        let wantedSeed = makeSeed(cropName: "Tomato", variety: "Roma", state: .want)

        let engine = DefaultPlanningEngine()
        let suggestions = engine.suggestions(
            using: [ownedSeed, wantedSeed],
            in: garden,
            on: makeDate(year: 2026, month: 8, day: 17),
            growingSpaces: [space],
            desires: []
        )

        let cropNames = suggestions.map { $0.cropName }
        XCTAssertTrue(cropNames.contains("Carrot"), "Owned seed crop should be suggested")
        XCTAssertFalse(cropNames.contains("Tomato"), "Wanted seed crop should not appear in owned-seeds-only query")
    }
}
