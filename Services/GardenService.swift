import Foundation
import SwiftData

struct GardenService {

    // MARK: - Seed Operations
    // These deterministic operations are the target for future voice interaction.
    // The GardenAssistant layer will invoke these rather than simulating UI taps.

    static func addSeed(
        cropName: String,
        variety: String? = nil,
        state: SeedState = .own,
        notes: String? = nil,
        garden: Garden? = nil,
        in context: ModelContext
    ) -> Seed {
        let seed = Seed(cropName: cropName, variety: variety, state: state, notes: notes)
        seed.garden = garden
        context.insert(seed)
        return seed
    }

    static func updateSeed(
        _ seed: Seed,
        cropName: String,
        variety: String?,
        state: SeedState,
        notes: String?
    ) {
        seed.cropName = cropName
        seed.variety = variety
        seed.state = state
        seed.notes = notes
        seed.updatedAt = Date()
    }

    static func deleteSeed(_ seed: Seed, in context: ModelContext) {
        context.delete(seed)
    }

    static func changeSeedState(_ seed: Seed, to newState: SeedState) {
        seed.state = newState
        seed.updatedAt = Date()
    }

    // MARK: - Growing Space Operations

    static func addGrowingSpace(
        name: String,
        notes: String? = nil,
        garden: Garden? = nil,
        in context: ModelContext
    ) -> GrowingSpace {
        let space = GrowingSpace(name: name, notes: notes)
        space.garden = garden
        context.insert(space)
        return space
    }

    static func updateGrowingSpace(
        _ space: GrowingSpace,
        name: String,
        notes: String?
    ) {
        space.name = name
        space.notes = notes
        space.updatedAt = Date()
    }

    static func deleteGrowingSpace(_ space: GrowingSpace, in context: ModelContext) {
        context.delete(space)
    }

    // MARK: - Occupancy Operations

    static func recordPlanting(
        cropName: String,
        variety: String? = nil,
        startDate: Date,
        growingSpace: GrowingSpace? = nil,
        plant: Plant? = nil,
        expectedHarvestDate: Date? = nil,
        expectedReleaseDate: Date? = nil,
        notes: String? = nil,
        in context: ModelContext
    ) -> Occupancy {
        let occupancy = Occupancy(
            cropName: cropName,
            variety: variety,
            startDate: startDate,
            expectedHarvestDate: expectedHarvestDate,
            expectedReleaseDate: expectedReleaseDate,
            status: .active,
            notes: notes,
            growingSpace: growingSpace,
            plant: plant
        )
        if let plant {
            plant.occupancy = occupancy
        }
        context.insert(occupancy)
        return occupancy
    }

    static func completeOccupancy(_ occupancy: Occupancy, endDate: Date? = nil) {
        occupancy.endDate = endDate ?? Date()
        occupancy.status = .completed
        occupancy.updatedAt = Date()
    }

    static func updateOccupancy(
        _ occupancy: Occupancy,
        cropName: String,
        variety: String?,
        startDate: Date,
        expectedHarvestDate: Date?,
        expectedReleaseDate: Date?,
        notes: String?
    ) {
        occupancy.cropName = cropName
        occupancy.variety = variety
        occupancy.startDate = startDate
        occupancy.expectedHarvestDate = expectedHarvestDate
        occupancy.expectedReleaseDate = expectedReleaseDate
        occupancy.notes = notes
        occupancy.updatedAt = Date()
    }

    static func deleteOccupancy(_ occupancy: Occupancy, in context: ModelContext) {
        context.delete(occupancy)
    }

    // MARK: - Desire Operations

    static func createDesire(
        cropName: String,
        variety: String? = nil,
        notes: String? = nil,
        garden: Garden? = nil,
        in context: ModelContext
    ) -> Desire {
        let desire = Desire(cropName: cropName, variety: variety, notes: notes, garden: garden)
        context.insert(desire)
        return desire
    }

    static func updateDesire(
        _ desire: Desire,
        cropName: String,
        variety: String?,
        notes: String?
    ) {
        desire.cropName = cropName
        desire.variety = variety
        desire.notes = notes
        desire.updatedAt = Date()
    }

    static func fulfillDesire(_ desire: Desire) {
        desire.isFulfilled = true
        desire.isCancelled = false
        desire.isExpired = false
        desire.updatedAt = Date()
    }

    static func cancelDesire(_ desire: Desire) {
        desire.isCancelled = true
        desire.isFulfilled = false
        desire.isExpired = false
        desire.updatedAt = Date()
    }

    static func expireDesire(_ desire: Desire) {
        desire.isExpired = true
        desire.isFulfilled = false
        desire.isCancelled = false
        desire.updatedAt = Date()
    }

    static func deleteDesire(_ desire: Desire, in context: ModelContext) {
        context.delete(desire)
    }

    // MARK: - Planned Planting Operations

    static func createPlannedPlanting(
        cropName: String,
        variety: String? = nil,
        plannedDate: Date? = nil,
        growingSpace: GrowingSpace? = nil,
        desire: Desire? = nil,
        seed: Seed? = nil,
        notes: String? = nil,
        garden: Garden? = nil,
        in context: ModelContext
    ) -> PlannedPlanting {
        let plan = PlannedPlanting(
            cropName: cropName,
            variety: variety,
            plannedDate: plannedDate,
            status: .planned,
            notes: notes,
            garden: garden,
            growingSpace: growingSpace,
            desire: desire,
            seed: seed
        )
        context.insert(plan)
        return plan
    }

    static func updatePlannedPlanting(
        _ plan: PlannedPlanting,
        cropName: String,
        variety: String?,
        plannedDate: Date?,
        growingSpace: GrowingSpace?,
        desire: Desire?,
        seed: Seed?,
        notes: String?
    ) {
        plan.cropName = cropName
        plan.variety = variety
        plan.plannedDate = plannedDate
        plan.growingSpace = growingSpace
        plan.desire = desire
        plan.seed = seed
        plan.notes = notes
        plan.updatedAt = Date()
    }

    static func cancelPlannedPlanting(_ plan: PlannedPlanting) {
        plan.status = .cancelled
        plan.updatedAt = Date()
    }

    static func completePlannedPlanting(
        _ plan: PlannedPlanting,
        actualStartDate: Date? = nil,
        cropName: String? = nil,
        variety: String? = nil,
        growingSpace: GrowingSpace? = nil,
        notes: String? = nil,
        in context: ModelContext
    ) -> Occupancy {
        let actualDate = actualStartDate ?? Date()
        let actualCropName = cropName ?? plan.cropName
        let actualVariety = variety ?? plan.variety
        let actualSpace = growingSpace ?? plan.growingSpace

        let occupancy = Occupancy(
            cropName: actualCropName,
            variety: actualVariety,
            startDate: actualDate,
            status: .active,
            notes: notes,
            growingSpace: actualSpace
        )

        plan.occupancy = occupancy
        plan.status = .planted
        plan.actualDate = actualDate
        plan.updatedAt = Date()

        context.insert(occupancy)
        return occupancy
    }

    static func deletePlannedPlanting(_ plan: PlannedPlanting, in context: ModelContext) {
        context.delete(plan)
    }
}
