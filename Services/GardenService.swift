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
}
