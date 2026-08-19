package com.soilandsupper.ui

import com.soilandsupper.domain.model.Desire
import com.soilandsupper.domain.model.Garden
import com.soilandsupper.domain.model.GrowingSpace
import com.soilandsupper.domain.model.Occupancy
import com.soilandsupper.domain.model.OccupancyStatus
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.Calendar

class GardenTimelineStateTest {

    private fun makeDate(year: Int, month: Int, day: Int): Long {
        val calendar = Calendar.getInstance()
        calendar.set(year, month - 1, day, 12, 0, 0)
        calendar.set(Calendar.MILLISECOND, 0)
        return calendar.timeInMillis
    }

    @Test
    fun `occupancy before start date does not appear as active`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 9, 1),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden
        )

        val spaceModel = spaces.first()
        assertNull(spaceModel.occupancy)
        assertTrue(spaceModel.isAvailable)
    }

    @Test
    fun `occupancy after start date appears as active`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden
        )

        val spaceModel = spaces.first()
        assertTrue(spaceModel.occupancy != null)
        assertFalse(spaceModel.isAvailable)
    }

    @Test
    fun `phase transitions with known dates`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val expectedHarvest = makeDate(2026, 8, 1)
        val expectedRelease = makeDate(2026, 9, 15)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedHarvestDate = expectedHarvest,
            expectedReleaseDate = expectedRelease,
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )

        val beforeHarvest = makeDate(2026, 7, 15)
        val stateBeforeHarvest = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = beforeHarvest,
            garden = garden
        ).first()
        assertEquals(CropTimelinePhase.GROWING, stateBeforeHarvest.occupancy?.phase)

        val atHarvest = makeDate(2026, 8, 1)
        val stateAtHarvest = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = atHarvest,
            garden = garden
        ).first()
        assertEquals(CropTimelinePhase.PRODUCING, stateAtHarvest.occupancy?.phase)

        val atRelease = makeDate(2026, 9, 15)
        val stateAtRelease = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = atRelease,
            garden = garden
        ).first()
        assertEquals(CropTimelinePhase.NEARING_RELEASE, stateAtRelease.occupancy?.phase)
    }

    @Test
    fun `no dates defaults to growing`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden
        )

        assertEquals(CropTimelinePhase.GROWING, spaces.first().occupancy?.phase)
    }

    @Test
    fun `completed occupancy does not appear active`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            endDate = makeDate(2026, 8, 1),
            status = OccupancyStatus.COMPLETED.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden
        )

        assertNull(spaces.first().occupancy)
        assertTrue(spaces.first().isAvailable)
    }

    @Test
    fun `future suggestions use expected release date`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val expectedRelease = makeDate(2026, 9, 15)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedReleaseDate = expectedRelease,
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden
        )

        val future = spaces.first().futureSuggestions
        assertTrue(future != null)
        assertEquals(expectedRelease, future?.openingDate)
        assertFalse(future?.suggestions?.isEmpty() ?: true)
    }

    @Test
    fun `no future suggestions after expected release`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val expectedRelease = makeDate(2026, 9, 15)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedReleaseDate = expectedRelease,
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 9, 20)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden
        )

        assertNull(spaces.first().futureSuggestions)
    }

    @Test
    fun `no release date suppresses future suggestions`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden
        )

        assertNull(spaces.first().futureSuggestions)
    }

    @Test
    fun `days calculations are correct`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val selectedDate = makeDate(2026, 8, 1)
        val expectedHarvest = makeDate(2026, 8, 16)
        val expectedRelease = makeDate(2026, 9, 1)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedHarvestDate = expectedHarvest,
            expectedReleaseDate = expectedRelease,
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden
        )

        val occupancyModel = spaces.first().occupancy!!
        assertEquals(15, occupancyModel.daysUntilHarvest)
        assertEquals(31, occupancyModel.daysUntilRelease)
    }

    @Test
    fun `multiple spaces handled independently`() {
        val garden = Garden(name = "Test Garden")
        val space1 = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val space2 = GrowingSpace(id = 2L, name = "Bed 2", gardenId = garden.id)
        val occupancy1 = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space1.id
        )
        val occupancy2 = Occupancy(
            cropName = "Carrot",
            startDate = makeDate(2026, 4, 1),
            endDate = makeDate(2026, 7, 1),
            status = OccupancyStatus.COMPLETED.name,
            growingSpaceId = space2.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space1, space2),
            occupancies = listOf(occupancy1, occupancy2),
            selectedDate = selectedDate,
            garden = garden
        )

        val model1 = spaces.first { it.space.id == space1.id }
        val model2 = spaces.first { it.space.id == space2.id }

        assertTrue(model1.occupancy != null)
        assertEquals(CropTimelinePhase.GROWING, model1.occupancy?.phase)
        assertNull(model2.occupancy)
        assertTrue(model2.isAvailable)
    }
}
