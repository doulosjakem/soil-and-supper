package com.soilandsupper.ui

import com.soilandsupper.gardentimeline.CropTimelinePhase
import com.soilandsupper.gardentimeline.buildTimelineSpaces
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.Garden
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.OccupancyStatus
import com.soilandsupper.shared.domain.model.PlantingSuggestion
import com.soilandsupper.shared.domain.model.Seed
import com.soilandsupper.shared.domain.model.SeedState
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
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
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
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
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
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
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
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
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
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
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
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
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
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
            garden = garden,
            seeds = listOf(Seed(cropName = "Carrot", variety = "Nantes", state = SeedState.OWN.name))
        )

        val future = spaces.first().futureSuggestions
        assertTrue(future != null)
        assertEquals(expectedRelease, future?.openingDate)
        assertFalse(future?.suggestions?.isEmpty() ?: true)
    }

    @Test
    fun `no future suggestions after expected release`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
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
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
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
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
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

    @Test
    fun `available space produces current suggestions`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val selectedDate = makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = emptyList(),
            selectedDate = selectedDate,
            garden = garden
        )

        val model = spaces.first()
        assertTrue(model.isAvailable)
        assertNotNull(model.currentSuggestions)
        assertFalse(model.currentSuggestions?.suggestions?.isEmpty() ?: true)
    }

    @Test
    fun `seeds and desires flow to suggestions`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val seed = Seed(cropName = "Carrot", variety = "Nantes", state = SeedState.OWN.name)
        val desire = Desire(cropName = "Carrot")
        val selectedDate = makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = emptyList(),
            selectedDate = selectedDate,
            garden = garden,
            seeds = listOf(seed),
            desires = listOf(desire)
        )

        val model = spaces.first()
        val carrot = model.currentSuggestions?.suggestions?.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertTrue(carrot!!.hasActiveDesire)
    }

    @Test
    fun `empty seeds and desires suppress future suggestions`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val expectedRelease = makeDate(2026, 9, 15)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedReleaseDate = expectedRelease,
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        // No gardener intent: the occupied space must NOT produce future suggestions.
        val noSeedsNoDesires = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden,
            seeds = emptyList(),
            desires = emptyList()
        ).first()
        assertNull("No seeds/desires must suppress future suggestions", noSeedsNoDesires.futureSuggestions)

        // Current "what can I plant now" suggestions for an available space remain
        // engine-driven and must NOT depend on tracked seeds/desires.
        val available = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = emptyList(),
            selectedDate = selectedDate,
            garden = garden
        ).first()
        assertTrue(available.isAvailable)
        assertFalse("Available space still shows current suggestions without seeds/desires",
            available.currentSuggestions?.suggestions?.isEmpty() ?: true)
    }

    @Test
    fun `seeds or desires enable future suggestions`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val expectedRelease = makeDate(2026, 9, 15)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedReleaseDate = expectedRelease,
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        val viaSeed = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden,
            seeds = listOf(Seed(cropName = "Carrot", variety = "Nantes", state = SeedState.OWN.name)),
            desires = emptyList()
        ).first()
        assertNotNull("A tracked seed enables future suggestions", viaSeed.futureSuggestions)
        assertFalse(viaSeed.futureSuggestions?.suggestions?.isEmpty() ?: true)

        val viaDesire = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden,
            seeds = emptyList(),
            desires = listOf(Desire(cropName = "Carrot"))
        ).first()
        assertNotNull("A desire enables future suggestions", viaDesire.futureSuggestions)

        // Deterministic: same inputs yield the same ranked suggestion order.
        val firstRun = viaSeed.futureSuggestions!!.suggestions.map { it.cropName }
        val secondRun = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden,
            seeds = listOf(Seed(cropName = "Carrot", variety = "Nantes", state = SeedState.OWN.name)),
            desires = emptyList()
        ).first().futureSuggestions!!.suggestions.map { it.cropName }
        assertEquals("Future suggestions must be deterministic", firstRun, secondRun)
    }

    @Test
    fun `future candidate planting date respects opening date`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val expectedRelease = makeDate(2026, 9, 15)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedReleaseDate = expectedRelease,
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        val future = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden,
            seeds = listOf(Seed(cropName = "Carrot", variety = "Nantes", state = SeedState.OWN.name)),
            desires = emptyList()
        ).first().futureSuggestions!!

        assertTrue(future.suggestions.isNotEmpty())
        assertTrue(
            "Suggested planting must not be earlier than the projected opening",
            future.suggestions.all { it.suggestedPlantingDate >= future.openingDate }
        )
    }

    @Test
    fun `recently planted crop is establishing`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 8, 12),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        assertEquals(
            CropTimelinePhase.ESTABLISHING,
            buildTimelineSpaces(
                growingSpaces = listOf(space),
                occupancies = listOf(occupancy),
                selectedDate = selectedDate,
                garden = garden
            ).first().occupancy?.phase
        )
    }

    @Test
    fun `planting day is establishing`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 8, 17),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )

        assertEquals(
            CropTimelinePhase.ESTABLISHING,
            buildTimelineSpaces(
                growingSpaces = listOf(space),
                occupancies = listOf(occupancy),
                selectedDate = makeDate(2026, 8, 17),
                garden = garden
            ).first().occupancy?.phase
        )
    }

    @Test
    fun `after estimated harvest remains producing until release`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedHarvestDate = makeDate(2026, 8, 1),
            expectedReleaseDate = makeDate(2026, 9, 15),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        // Between harvest and release the crop is still producing - not finished.
        val afterHarvest = makeDate(2026, 8, 20)
        val model = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = afterHarvest,
            garden = garden
        ).first()
        assertEquals(CropTimelinePhase.PRODUCING, model.occupancy?.phase)
        assertFalse(model.isAvailable)
    }

    @Test
    fun `after expected release does not fabricate completion`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val expectedRelease = makeDate(2026, 9, 15)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedReleaseDate = expectedRelease,
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        // A projected release is an estimate the space may open around - it is NOT the
        // gardener removing the crop, and it is not an explicit completion event.
        val afterRelease = makeDate(2026, 9, 20)
        val model = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = afterRelease,
            garden = garden
        ).first()

        assertNotNull("Crop must still be present after projected release", model.occupancy)
        assertEquals(CropTimelinePhase.NEARING_RELEASE, model.occupancy?.phase)
        assertFalse("Projected release must not free the space on its own", model.isAvailable)
    }

    @Test
    fun `explicit end date releases the space`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            endDate = makeDate(2026, 8, 1),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )
        val selectedDate = makeDate(2026, 8, 17)

        val model = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = selectedDate,
            garden = garden
        ).first()

        assertNull("Explicit end date removes the active crop", model.occupancy)
        assertTrue("Explicit end date frees the space", model.isAvailable)
    }

    @Test
    fun `scrubbing the timeline does not mutate domain state`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedHarvestDate = makeDate(2026, 8, 1),
            expectedReleaseDate = makeDate(2026, 9, 15),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )

        val today = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = makeDate(2026, 7, 1),
            garden = garden
        ).first()
        val future = buildTimelineSpaces(
            growingSpaces = listOf(space),
            occupancies = listOf(occupancy),
            selectedDate = makeDate(2026, 9, 20),
            garden = garden
        ).first()

        // Selecting different dates changes only the read view; the underlying occupancy
        // data (planting, harvest, release) is never mutated.
        assertTrue("Same occupancy instance must be reused", today.occupancy?.occupancy === occupancy)
        assertTrue("Same occupancy instance must be reused", future.occupancy?.occupancy === occupancy)
        assertEquals(makeDate(2026, 5, 15), occupancy.startDate)
        assertEquals(makeDate(2026, 8, 1), occupancy.expectedHarvestDate)
        assertEquals(makeDate(2026, 9, 15), occupancy.expectedReleaseDate)
        assertEquals(CropTimelinePhase.GROWING, today.occupancy?.phase)
        assertEquals(CropTimelinePhase.NEARING_RELEASE, future.occupancy?.phase)
    }

    @Test
    fun `lifecycle phase display names are human readable`() {
        // The lifecycle is always accompanied by a textual label (never color-only),
        // so each stage needs a clear, gardener-friendly phrase.
        val expected = mapOf(
            CropTimelinePhase.NOT_PLANTED to "Not planted",
            CropTimelinePhase.ESTABLISHING to "Establishing",
            CropTimelinePhase.GROWING to "Growing",
            CropTimelinePhase.PRODUCING to "Producing",
            CropTimelinePhase.NEARING_RELEASE to "Space opening soon",
            CropTimelinePhase.COMPLETED to "Completed"
        )
        expected.forEach { (phase, label) ->
            assertEquals(label, phase.displayName)
        }
    }
}
