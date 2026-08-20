package com.soilandsupper.ui

import com.soilandsupper.gardentimeline.CropTimelinePhase
import com.soilandsupper.gardentimeline.buildTimelineSpaces
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.ui.fixture.RealisticGardenFixture
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class RealisticGardenTimelineTest {

    @Test
    fun `realistic garden - empty bed produces current suggestions`() {
        val emptyBed = RealisticGardenFixture.spaces.last()
        val selectedDate = RealisticGardenFixture.makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(emptyBed),
            occupancies = emptyList(),
            selectedDate = selectedDate,
            garden = RealisticGardenFixture.garden,
            seeds = RealisticGardenFixture.seeds,
            desires = RealisticGardenFixture.desires
        )

        val model = spaces.first()
        assertTrue(model.isAvailable)
        assertNotNull(model.currentSuggestions)
        assertFalse(model.currentSuggestions?.suggestions?.isEmpty() ?: true)
    }

    @Test
    fun `realistic garden - occupied space shows current crop`() {
        val bed2 = RealisticGardenFixture.spaces.first { it.id == 2L }
        val selectedDate = RealisticGardenFixture.makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(bed2),
            occupancies = RealisticGardenFixture.occupiedSpaces,
            selectedDate = selectedDate,
            garden = RealisticGardenFixture.garden,
            seeds = RealisticGardenFixture.seeds,
            desires = RealisticGardenFixture.desires
        )

        val model = spaces.first { it.space.id == bed2.id }
        assertFalse(model.isAvailable)
        assertNotNull(model.occupancy)
        assertEquals("Potato", model.occupancy!!.occupancy.cropName)
    }

    @Test
    fun `realistic garden - future succession shows suggestions after release`() {
        val bed2 = RealisticGardenFixture.spaces.first { it.id == 2L }
        val selectedDate = RealisticGardenFixture.makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(bed2),
            occupancies = RealisticGardenFixture.occupiedSpaces,
            selectedDate = selectedDate,
            garden = RealisticGardenFixture.garden,
            seeds = RealisticGardenFixture.seeds,
            desires = RealisticGardenFixture.desires
        )

        val model = spaces.first { it.space.id == bed2.id }
        assertNotNull(model.futureSuggestions)
        assertFalse(model.futureSuggestions?.suggestions?.isEmpty() ?: true)
    }

    @Test
    fun `realistic garden - unknown maturity does not fabricate dates`() {
        val mysterySpace = GrowingSpace(id = 1L, name = "Mystery Bed", gardenId = RealisticGardenFixture.garden.id)
        val selectedDate = RealisticGardenFixture.makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(mysterySpace),
            occupancies = listOf(RealisticGardenFixture.occupancyWithUnknownMaturity),
            selectedDate = selectedDate,
            garden = RealisticGardenFixture.garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val model = spaces.first()
        assertFalse(model.isAvailable)
        assertNull(model.occupancy!!.daysUntilHarvest)
        assertNull(model.occupancy!!.daysUntilRelease)
    }

    @Test
    fun `realistic garden - completed occupancy frees space`() {
        val emptyBed = RealisticGardenFixture.spaces.last { it.id == 6L }
        val selectedDate = RealisticGardenFixture.makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(emptyBed),
            occupancies = listOf(RealisticGardenFixture.completedOccupancy),
            selectedDate = selectedDate,
            garden = RealisticGardenFixture.garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val model = spaces.first()
        assertTrue(model.isAvailable)
        assertNull(model.occupancy)
    }

    @Test
    fun `realistic garden - scrubbing does not mutate occupancy`() {
        val bed2 = RealisticGardenFixture.spaces.first { it.id == 2L }
        val today = RealisticGardenFixture.makeDate(2026, 7, 1)
        val future = RealisticGardenFixture.makeDate(2026, 9, 20)

        val todaySpaces = buildTimelineSpaces(
            growingSpaces = listOf(bed2),
            occupancies = RealisticGardenFixture.occupiedSpaces,
            selectedDate = today,
            garden = RealisticGardenFixture.garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val futureSpaces = buildTimelineSpaces(
            growingSpaces = listOf(bed2),
            occupancies = RealisticGardenFixture.occupiedSpaces,
            selectedDate = future,
            garden = RealisticGardenFixture.garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val todayModel = todaySpaces.first { it.space.id == bed2.id }
        val futureModel = futureSpaces.first { it.space.id == bed2.id }

        assertEquals("Potato", todayModel.occupancy!!.occupancy.cropName)
        assertEquals("Potato", futureModel.occupancy!!.occupancy.cropName)
        assertEquals(CropTimelinePhase.GROWING, todayModel.occupancy!!.phase)
        assertEquals(CropTimelinePhase.NEARING_RELEASE, futureModel.occupancy!!.phase)
    }

    @Test
    fun `realistic garden - seeds and desires improve ranking`() {
        val emptyBed = RealisticGardenFixture.spaces.last()
        val selectedDate = RealisticGardenFixture.makeDate(2026, 8, 17)

        val withSeedsAndDesires = buildTimelineSpaces(
            growingSpaces = listOf(emptyBed),
            occupancies = emptyList(),
            selectedDate = selectedDate,
            garden = RealisticGardenFixture.garden,
            seeds = RealisticGardenFixture.seeds,
            desires = RealisticGardenFixture.desires
        )

        val withoutSeedsAndDesires = buildTimelineSpaces(
            growingSpaces = listOf(emptyBed),
            occupancies = emptyList(),
            selectedDate = selectedDate,
            garden = RealisticGardenFixture.garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val withModel = withSeedsAndDesires.first()
        val withoutModel = withoutSeedsAndDesires.first()

        assertNotNull(withModel.currentSuggestions)
        assertNotNull(withoutModel.currentSuggestions)

        val withCarrot = withModel.currentSuggestions!!.suggestions.firstOrNull { it.cropName == "Carrot" }
        val withoutCarrot = withoutModel.currentSuggestions!!.suggestions.firstOrNull { it.cropName == "Carrot" }

        assertNotNull(withCarrot)
        assertNotNull(withoutCarrot)

        assertEquals("Owned seed should improve ranking to BEST_FIT",
            com.soilandsupper.shared.domain.model.SuggestionRank.BEST_FIT,
            withCarrot!!.ranking)
        assertEquals("Untracked crop remains ALSO_GOOD",
            com.soilandsupper.shared.domain.model.SuggestionRank.ALSO_GOOD,
            withoutCarrot!!.ranking)
    }

    @Test
    fun `realistic garden - empty seeds and desires suppress future suggestions`() {
        val bed2 = RealisticGardenFixture.spaces.first { it.id == 2L }
        val selectedDate = RealisticGardenFixture.makeDate(2026, 8, 17)

        val withIntent = buildTimelineSpaces(
            growingSpaces = listOf(bed2),
            occupancies = RealisticGardenFixture.occupiedSpaces,
            selectedDate = selectedDate,
            garden = RealisticGardenFixture.garden,
            seeds = RealisticGardenFixture.seeds,
            desires = RealisticGardenFixture.desires
        )

        val withoutIntent = buildTimelineSpaces(
            growingSpaces = listOf(bed2),
            occupancies = RealisticGardenFixture.occupiedSpaces,
            selectedDate = selectedDate,
            garden = RealisticGardenFixture.garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        assertNotNull(withIntent.first().futureSuggestions)
        assertNull(withoutIntent.first().futureSuggestions)
    }
}
