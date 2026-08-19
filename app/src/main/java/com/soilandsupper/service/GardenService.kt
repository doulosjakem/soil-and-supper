package com.soilandsupper.service

import com.soilandsupper.domain.model.Desire
import com.soilandsupper.domain.model.Garden
import com.soilandsupper.domain.model.GrowingSpace
import com.soilandsupper.domain.model.Occupancy
import com.soilandsupper.domain.model.OccupancyStatus
import com.soilandsupper.domain.model.PlannedPlanting
import com.soilandsupper.domain.model.Plant
import com.soilandsupper.domain.model.Seed
import com.soilandsupper.domain.model.SeedState

object GardenService {

    fun addSeed(
        cropName: String,
        variety: String? = null,
        state: SeedState = SeedState.OWN,
        notes: String? = null,
        garden: Garden? = null
    ): Seed {
        return Seed(
            cropName = cropName,
            variety = variety,
            state = state.name,
            notes = notes,
            gardenId = garden?.id
        )
    }

    fun updateSeed(
        seed: Seed,
        cropName: String,
        variety: String?,
        state: SeedState,
        notes: String?
    ): Seed {
        return seed.copy(
            cropName = cropName,
            variety = variety,
            state = state.name,
            notes = notes,
            updatedAt = System.currentTimeMillis()
        )
    }

    fun addGrowingSpace(
        name: String,
        notes: String? = null,
        spaceType: String? = null,
        width: Double? = null,
        length: Double? = null,
        garden: Garden? = null
    ): GrowingSpace {
        return GrowingSpace(
            name = name,
            notes = notes,
            spaceType = spaceType,
            width = width,
            length = length,
            gardenId = garden?.id
        )
    }

    fun updateGrowingSpace(
        space: GrowingSpace,
        name: String,
        notes: String?,
        spaceType: String?,
        width: Double?,
        length: Double?
    ): GrowingSpace {
        return space.copy(
            name = name,
            notes = notes,
            spaceType = spaceType,
            width = width,
            length = length,
            updatedAt = System.currentTimeMillis()
        )
    }

    fun recordPlanting(
        cropName: String,
        variety: String? = null,
        startDate: Long,
        growingSpace: GrowingSpace? = null,
        plant: Plant? = null,
        expectedHarvestDate: Long? = null,
        expectedReleaseDate: Long? = null,
        notes: String? = null
    ): Occupancy {
        return Occupancy(
            cropName = cropName,
            variety = variety,
            startDate = startDate,
            expectedHarvestDate = expectedHarvestDate,
            expectedReleaseDate = expectedReleaseDate,
            status = OccupancyStatus.ACTIVE.name,
            notes = notes,
            growingSpaceId = growingSpace?.id,
            plantId = plant?.id
        )
    }

    fun completeOccupancy(occupancy: Occupancy, endDate: Long? = null): Occupancy {
        return occupancy.copy(
            endDate = endDate ?: System.currentTimeMillis(),
            status = OccupancyStatus.COMPLETED.name,
            updatedAt = System.currentTimeMillis()
        )
    }

    fun updateOccupancy(
        occupancy: Occupancy,
        cropName: String,
        variety: String?,
        startDate: Long,
        expectedHarvestDate: Long?,
        expectedReleaseDate: Long?,
        notes: String?
    ): Occupancy {
        return occupancy.copy(
            cropName = cropName,
            variety = variety,
            startDate = startDate,
            expectedHarvestDate = expectedHarvestDate,
            expectedReleaseDate = expectedReleaseDate,
            notes = notes,
            updatedAt = System.currentTimeMillis()
        )
    }

    fun createDesire(
        cropName: String,
        variety: String? = null,
        notes: String? = null,
        garden: Garden? = null
    ): Desire {
        return Desire(
            cropName = cropName,
            variety = variety,
            notes = notes,
            gardenId = garden?.id
        )
    }

    fun updateDesire(
        desire: Desire,
        cropName: String,
        variety: String?,
        notes: String?
    ): Desire {
        return desire.copy(
            cropName = cropName,
            variety = variety,
            notes = notes,
            updatedAt = System.currentTimeMillis()
        )
    }

    fun fulfillDesire(desire: Desire): Desire {
        return desire.copy(
            isFulfilled = true,
            isCancelled = false,
            isExpired = false,
            updatedAt = System.currentTimeMillis()
        )
    }

    fun cancelDesire(desire: Desire): Desire {
        return desire.copy(
            isCancelled = true,
            isFulfilled = false,
            isExpired = false,
            updatedAt = System.currentTimeMillis()
        )
    }

    fun expireDesire(desire: Desire): Desire {
        return desire.copy(
            isExpired = true,
            isFulfilled = false,
            isCancelled = false,
            updatedAt = System.currentTimeMillis()
        )
    }

    fun createPlannedPlanting(
        cropName: String,
        variety: String? = null,
        plannedDate: Long? = null,
        growingSpace: GrowingSpace? = null,
        desire: Desire? = null,
        seed: Seed? = null,
        notes: String? = null,
        garden: Garden? = null
    ): PlannedPlanting {
        return PlannedPlanting(
            cropName = cropName,
            variety = variety,
            plannedDate = plannedDate,
            status = com.soilandsupper.domain.model.PlanStatus.PLANNED.name,
            notes = notes,
            gardenId = garden?.id,
            growingSpaceId = growingSpace?.id,
            desireId = desire?.id,
            seedId = seed?.id
        )
    }

    fun updatePlannedPlanting(
        plan: PlannedPlanting,
        cropName: String,
        variety: String?,
        plannedDate: Long?,
        growingSpace: GrowingSpace?,
        desire: Desire?,
        seed: Seed?,
        notes: String?
    ): PlannedPlanting {
        return plan.copy(
            cropName = cropName,
            variety = variety,
            plannedDate = plannedDate,
            notes = notes,
            growingSpaceId = growingSpace?.id,
            desireId = desire?.id,
            seedId = seed?.id,
            updatedAt = System.currentTimeMillis()
        )
    }

    fun cancelPlannedPlanting(plan: PlannedPlanting): PlannedPlanting {
        return plan.copy(
            status = com.soilandsupper.domain.model.PlanStatus.CANCELLED.name,
            updatedAt = System.currentTimeMillis()
        )
    }
}
