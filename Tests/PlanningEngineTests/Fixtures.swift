import Foundation
@testable import SoilAndSupper

let testCalendar = Calendar(identifier: .gregorian)
let testTimeZone = TimeZone(secondsFromGMT: 0)!

func makeDate(year: Int, month: Int, day: Int) -> Date {
    var components = DateComponents()
    components.calendar = testCalendar
    components.timeZone = testTimeZone
    components.year = year
    components.month = month
    components.day = day
    components.hour = 12
    components.minute = 0
    components.second = 0
    return components.date!
}

func makeGarden(
    name: String = "Test Garden",
    location: String? = nil,
    climateZone: String? = nil,
    lastFrost: Date? = nil,
    firstFrost: Date? = nil,
    growingSpaces: [GrowingSpace] = []
) -> Garden {
    let garden = Garden(name: name, location: location)
    garden.climateZone = climateZone
    garden.averageLastFrostDate = lastFrost
    garden.averageFirstFrostDate = firstFrost
    for space in growingSpaces {
        space.garden = garden
    }
    return garden
}

func makeGrowingSpace(
    name: String,
    notes: String? = nil,
    spaceType: SpaceType? = nil,
    width: Double? = nil,
    length: Double? = nil,
    occupancies: [Occupancy] = [],
    plannedPlantings: [PlannedPlanting] = [],
    garden: Garden? = nil
) -> GrowingSpace {
    let space = GrowingSpace(name: name, notes: notes, spaceType: spaceType, width: width, length: length)
    space.garden = garden
    space.occupancies = occupancies
    for occupancy in occupancies {
        occupancy.growingSpace = space
    }
    space.plannedPlantings = plannedPlantings
    return space
}

func makeOccupancy(
    cropName: String,
    variety: String? = nil,
    startDate: Date,
    endDate: Date? = nil,
    expectedHarvestDate: Date? = nil,
    expectedReleaseDate: Date? = nil,
    status: OccupancyStatus = .active,
    growingSpace: GrowingSpace? = nil,
    plant: Plant? = nil,
    plannedPlanting: PlannedPlanting? = nil
) -> Occupancy {
    let occupancy = Occupancy(
        cropName: cropName,
        variety: variety,
        startDate: startDate,
        endDate: endDate,
        expectedHarvestDate: expectedHarvestDate,
        expectedReleaseDate: expectedReleaseDate,
        status: status,
        growingSpace: growingSpace,
        plant: plant,
        plannedPlanting: plannedPlanting
    )
    return occupancy
}

func makeSeed(
    cropName: String,
    variety: String? = nil,
    state: SeedState = .own,
    garden: Garden? = nil
) -> Seed {
    let seed = Seed(cropName: cropName, variety: variety, state: state)
    seed.garden = garden
    return seed
}

func makeDesire(
    cropName: String,
    variety: String? = nil,
    isFulfilled: Bool = false,
    isExpired: Bool = false,
    isCancelled: Bool = false,
    garden: Garden? = nil
) -> Desire {
    let desire = Desire(cropName: cropName, variety: variety)
    desire.isFulfilled = isFulfilled
    desire.isExpired = isExpired
    desire.isCancelled = isCancelled
    desire.garden = garden
    return desire
}

func makePlannedPlanting(
    cropName: String,
    variety: String? = nil,
    plannedDate: Date? = nil,
    actualDate: Date? = nil,
    status: PlanStatus = .planned,
    growingSpace: GrowingSpace? = nil,
    occupancy: Occupancy? = nil,
    desire: Desire? = nil,
    seed: Seed? = nil,
    garden: Garden? = nil
) -> PlannedPlanting {
    let plan = PlannedPlanting(
        cropName: cropName,
        variety: variety,
        plannedDate: plannedDate,
        actualDate: actualDate,
        status: status,
        growingSpace: growingSpace,
        occupancy: occupancy,
        desire: desire,
        seed: seed
    )
    plan.garden = garden
    return plan
}
