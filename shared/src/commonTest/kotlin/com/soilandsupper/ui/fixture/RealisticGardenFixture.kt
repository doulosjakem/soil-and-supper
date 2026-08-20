package com.soilandsupper.ui.fixture

import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.Garden
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.OccupancyStatus
import com.soilandsupper.shared.domain.model.Seed
import com.soilandsupper.shared.domain.model.SeedState
import com.soilandsupper.util.epochMillis

object RealisticGardenFixture {
    internal fun makeDate(year: Int, month: Int, day: Int): Long =
        epochMillis(year, month, day, 12, 0, 0)

    val garden: Garden
        get() = Garden(
            name = "Test Garden",
            averageLastFrostDate = makeDate(2026, 5, 15),
            averageFirstFrostDate = makeDate(2026, 10, 15)
        )

    val spaces: List<GrowingSpace>
        get() = listOf(
            GrowingSpace(id = 1L, name = "Bed 1 - Garlic", gardenId = garden.id, notes = "Garlic succession"),
            GrowingSpace(id = 2L, name = "Bed 2 - Potatoes", gardenId = garden.id, notes = "Potatoes / Onions"),
            GrowingSpace(id = 3L, name = "Bed 3 - Corn", gardenId = garden.id, notes = "Flour corn"),
            GrowingSpace(id = 4L, name = "Fabric Pot 1", gardenId = garden.id, notes = "Tomatoes"),
            GrowingSpace(id = 5L, name = "Fabric Pot 2", gardenId = garden.id, notes = "Dry Beans"),
            GrowingSpace(id = 6L, name = "Empty Bed", gardenId = garden.id, notes = "Available for planting")
        )

    val seeds: List<Seed>
        get() = listOf(
            Seed(cropName = "Carrot", variety = "Nantes", state = SeedState.OWN.name),
            Seed(cropName = "Bean", variety = "Blue Lake", state = SeedState.OWN.name),
            Seed(cropName = "Garlic", variety = "German Extra Early", state = SeedState.OWN.name),
            Seed(cropName = "Corn", variety = "Flour", state = SeedState.OWN.name),
            Seed(cropName = "Fava", variety = "Broad Windsor", state = SeedState.WANT.name)
        )

    val desires: List<Desire>
        get() = listOf(
            Desire(cropName = "Bean"),
            Desire(cropName = "Radish"),
            Desire(cropName = "Kale")
        )

    val occupiedSpaces: List<Occupancy>
        get() = listOf(
            Occupancy(
                id = 1L,
                cropName = "Garlic",
                variety = "German Extra Early",
                startDate = makeDate(2026, 10, 15),
                expectedHarvestDate = makeDate(2027, 6, 20),
                expectedReleaseDate = makeDate(2027, 7, 10),
                status = OccupancyStatus.ACTIVE.name,
                growingSpaceId = 1L
            ),
            Occupancy(
                id = 2L,
                cropName = "Potato",
                variety = "Yukon Gold",
                startDate = makeDate(2026, 3, 20),
                expectedHarvestDate = makeDate(2026, 8, 1),
                expectedReleaseDate = makeDate(2026, 9, 15),
                status = OccupancyStatus.ACTIVE.name,
                growingSpaceId = 2L
            ),
            Occupancy(
                id = 3L,
                cropName = "Onion",
                variety = "Walla Walla",
                startDate = makeDate(2026, 3, 25),
                expectedHarvestDate = makeDate(2026, 8, 10),
                expectedReleaseDate = makeDate(2026, 9, 20),
                status = OccupancyStatus.ACTIVE.name,
                growingSpaceId = 2L
            ),
            Occupancy(
                id = 4L,
                cropName = "Corn",
                variety = "Flour",
                startDate = makeDate(2026, 5, 20),
                expectedHarvestDate = makeDate(2026, 9, 15),
                expectedReleaseDate = makeDate(2026, 10, 5),
                status = OccupancyStatus.ACTIVE.name,
                growingSpaceId = 3L
            ),
            Occupancy(
                id = 5L,
                cropName = "Tomato",
                variety = "San Marzano",
                startDate = makeDate(2026, 5, 10),
                expectedHarvestDate = makeDate(2026, 8, 1),
                expectedReleaseDate = makeDate(2026, 9, 30),
                status = OccupancyStatus.ACTIVE.name,
                growingSpaceId = 4L
            ),
            Occupancy(
                id = 6L,
                cropName = "Bean",
                variety = "Dry",
                startDate = makeDate(2026, 6, 1),
                expectedHarvestDate = makeDate(2026, 9, 20),
                expectedReleaseDate = makeDate(2026, 10, 20),
                status = OccupancyStatus.ACTIVE.name,
                growingSpaceId = 5L
            )
        )

    val completedOccupancy: Occupancy
        get() = Occupancy(
            id = 7L,
            cropName = "Pea",
            variety = "Sugar Snap",
            startDate = makeDate(2026, 3, 1),
            endDate = makeDate(2026, 6, 15),
            status = OccupancyStatus.COMPLETED.name,
            growingSpaceId = 6L
        )

    val occupancyWithUnknownMaturity: Occupancy
        get() = Occupancy(
            id = 8L,
            cropName = "Mystery Crop",
            variety = "Unknown",
            startDate = makeDate(2026, 7, 1),
            expectedHarvestDate = null,
            expectedReleaseDate = null,
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = 1L
        )
}
