package com.soilandsupper.service

import com.soilandsupper.domain.model.Crop
import com.soilandsupper.domain.model.Desire
import com.soilandsupper.domain.model.Garden
import com.soilandsupper.domain.model.GrowingSpace
import com.soilandsupper.domain.model.Occupancy
import com.soilandsupper.domain.model.OccupancyStatus
import com.soilandsupper.domain.model.PlantingSuggestion
import com.soilandsupper.domain.model.Seed
import com.soilandsupper.domain.model.SeedAvailability
import com.soilandsupper.domain.model.SeedState
import com.soilandsupper.domain.model.SuggestionRank
import com.soilandsupper.domain.model.Variety
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.Calendar
import java.util.Locale
import java.util.TimeZone

class PlanningEngineTest {

    companion object {
        init {
            TimeZone.setDefault(TimeZone.getTimeZone("UTC"))
            Locale.setDefault(Locale.US)
        }
    }

    private fun makeDate(year: Int, month: Int, day: Int): Long {
        val c = Calendar.getInstance(TimeZone.getTimeZone("UTC")).apply {
            clear()
            set(year, month - 1, day, 12, 0, 0)
        }
        return c.timeInMillis
    }

    private fun makeGarden(lastFrost: Long? = null, firstFrost: Long? = null): Garden =
        Garden(
            name = "Test Garden",
            averageLastFrostDate = lastFrost,
            averageFirstFrostDate = firstFrost
        )

    private fun makeGrowingSpace(name: String): GrowingSpace = GrowingSpace(name = name)

    private fun makeOccupancy(
        cropName: String,
        startDate: Long,
        endDate: Long? = null,
        expectedHarvestDate: Long? = null,
        expectedReleaseDate: Long? = null,
        status: OccupancyStatus = OccupancyStatus.ACTIVE,
        growingSpace: GrowingSpace? = null
    ): Occupancy = Occupancy(
        cropName = cropName,
        startDate = startDate,
        endDate = endDate,
        expectedHarvestDate = expectedHarvestDate,
        expectedReleaseDate = expectedReleaseDate,
        status = status.name,
        growingSpaceId = growingSpace?.id
    )

    private fun makeSeed(cropName: String, variety: String? = null, state: SeedState = SeedState.OWN): Seed =
        Seed(cropName = cropName, variety = variety, state = state.name)

    private fun makeDesire(cropName: String): Desire = Desire(cropName = cropName)

    private fun monthOf(millis: Long): Int {
        val c = Calendar.getInstance()
        c.timeInMillis = millis
        return c.get(Calendar.MONTH) + 1
    }

    private fun daysBetween(start: Long, end: Long): Int {
        val c1 = Calendar.getInstance().apply { timeInMillis = start }
        val c2 = Calendar.getInstance().apply { timeInMillis = end }
        return ((c2.timeInMillis - c1.timeInMillis) / (1000L * 60 * 60 * 24)).toInt()
    }

    @Test
    fun openSpace_producesCurrentSuggestions() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val today = makeDate(2026, 8, 17)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = today,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull("Carrots should be suggested for an open space in August", carrot)
        assertFalse("Current suggestions should not be marked as future", carrot!!.isFuture)
        assertNull("Current suggestions should not have an opening date", carrot.openingDate)
    }

    @Test
    fun occupiedSpace_suppressesCurrentSuggestions() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val occupancy = makeOccupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            status = OccupancyStatus.ACTIVE,
            growingSpace = space
        )
        val today = makeDate(2026, 8, 17)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = listOf(occupancy),
            onDate = today,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        assertTrue("Occupied space should not produce current suggestions", suggestions.isEmpty())
    }

    @Test
    fun completedOccupancy_allowsCurrentSuggestions() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        makeOccupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            endDate = makeDate(2026, 9, 10),
            status = OccupancyStatus.COMPLETED,
            growingSpace = space
        )
        val today = makeDate(2026, 8, 17)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = today,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        assertFalse("Completed occupancy should allow current suggestions", suggestions.isEmpty())
    }

    @Test
    fun futureOpeningInsideWindow_producesFutureSuggestions() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val openingDate = makeDate(2026, 9, 15)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = openingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull("Carrots should be suggested for a future opening in September", carrot)
    }

    @Test
    fun futureOpeningBeforeWindow_usesCandidateDate() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val openingDate = makeDate(2026, 6, 15)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = openingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull("Carrots should still be eligible when opening is before fall window", carrot)
        assertEquals("Candidate date should be in July (fall window start)", 7, monthOf(carrot!!.suggestedPlantingDate))
        assertFalse("Candidate date should not be before the opening date", carrot.suggestedPlantingDate < openingDate)
    }

    @Test
    fun futureOpeningAfterWindow_rejectsCrop() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val openingDate = makeDate(2026, 10, 10)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = openingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNull("Carrots should be rejected when opening is after fall window", carrot)
    }

    @Test
    fun explicitOpeningDate_isAuthoritative() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val explicitDate = makeDate(2026, 9, 1)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = explicitDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertEquals(explicitDate, carrot!!.openingDate)
        assertEquals(explicitDate, carrot.suggestedPlantingDate)
    }

    @Test
    fun explicitOpeningDate_precedenceOverExpectedRelease() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val explicitDate = makeDate(2026, 8, 20)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = explicitDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        assertFalse("Engine should use explicit opening date", suggestions.isEmpty())
        assertEquals("Opening date should be the explicit caller-supplied date, not any expected release",
            explicitDate, suggestions.first().openingDate)
    }

    @Test
    fun expectedReleaseDate_drivesFutureSuggestions() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val expectedRelease = makeDate(2026, 9, 15)

        val engine = DefaultPlanningEngine()
        val futureSuggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = expectedRelease,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        assertFalse("Future suggestions should use expected release date", futureSuggestions.isEmpty())
        assertEquals(expectedRelease, futureSuggestions.first().openingDate)
    }

    @Test
    fun noExpectedReleaseDate_doesNotInventDate() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        makeOccupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            status = OccupancyStatus.ACTIVE,
            growingSpace = space
        )

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = makeDate(2026, 9, 15),
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        assertFalse("Engine should work when caller supplies an explicit date", suggestions.isEmpty())
    }

    @Test
    fun multipleActiveOccupancies_remainsOccupied() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val occ1 = makeOccupancy("Tomato", makeDate(2026, 5, 15), status = OccupancyStatus.ACTIVE, growingSpace = space)
        val occ2 = makeOccupancy("Basil", makeDate(2026, 6, 1), status = OccupancyStatus.ACTIVE, growingSpace = space)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = listOf(occ1, occ2),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        assertTrue("Space with multiple active occupancies should remain occupied", suggestions.isEmpty())
    }

    @Test
    fun knownMaturity_producesHarvestEstimate() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val plantingDate = makeDate(2026, 9, 1)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = plantingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val radish = suggestions.firstOrNull { it.cropName == "Radish" }
        assertNotNull(radish)
        val harvest = radish!!.estimatedHarvestDate
        assertNotNull("Known maturity should produce harvest estimate", harvest)
        assertEquals("Harvest should be 22 days after planting for Cherry Belle radish", 22, daysBetween(plantingDate, harvest!!))
    }

    @Test
    fun unknownMaturity_neverFabricatesDates() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        for (suggestion in suggestions) {
            val harvest = suggestion.estimatedHarvestDate
            if (harvest != null) {
                assertTrue("Harvest should not be before planting", harvest >= suggestion.suggestedPlantingDate)
            }
        }
    }

    @Test
    fun frostSensitiveInsufficientSeason_isRejected() {
        val firstFrost = makeDate(2026, 10, 1)
        val garden = makeGarden(firstFrost = firstFrost)
        val space = makeGrowingSpace("Bed 1")
        val plantingDate = makeDate(2026, 8, 15)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = plantingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val tomato = suggestions.firstOrNull { it.cropName == "Tomato" }
        assertNull("Tomatoes should be rejected with insufficient season", tomato)
    }

    @Test
    fun frostTolerantInsufficientSeason_isAllowedWithWarning() {
        val firstFrost = makeDate(2026, 10, 1)
        val garden = makeGarden(firstFrost = firstFrost)
        val space = makeGrowingSpace("Bed 1")
        val plantingDate = makeDate(2026, 8, 15)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = plantingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull("Frost-tolerant carrots should be allowed with insufficient season", carrot)
        assertFalse("Warning should be present for frost-tolerant crop with short season", carrot!!.warnings.isEmpty())
    }

    @Test
    fun harvestBeforeFrost_producesNoWarning() {
        val firstFrost = makeDate(2026, 10, 15)
        val garden = makeGarden(firstFrost = firstFrost)
        val space = makeGrowingSpace("Bed 1")
        val plantingDate = makeDate(2026, 8, 15)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = plantingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val radish = suggestions.firstOrNull { it.cropName == "Radish" }
        assertNotNull("Radishes should be suggested when harvest is before frost", radish)
        assertTrue("No frost warning when harvest is before first frost", radish!!.warnings.isEmpty())
    }

    @Test
    fun exactFrostBoundary_isAllowed() {
        val firstFrost = makeDate(2026, 10, 14)
        val garden = makeGarden(firstFrost = firstFrost)
        val space = makeGrowingSpace("Bed 1")
        val plantingDate = makeDate(2026, 8, 15)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = plantingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull("Carrots should be allowed when harvest equals first frost", carrot)
    }

    @Test
    fun futureOpeningBeforeWindow_seasonFromCandidateDate() {
        val firstFrost = makeDate(2026, 9, 20)
        val garden = makeGarden(firstFrost = firstFrost)
        val space = makeGrowingSpace("Bed 1")
        val openingDate = makeDate(2026, 8, 20)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = openingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull("Carrots should still be eligible when opening is before window", carrot)
        assertFalse("Warning should reflect season from candidate date, not opening date", carrot!!.warnings.isEmpty())
    }

    @Test
    fun ownedSeed_improvesRanking() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val seed = makeSeed("Carrot", "Nantes", SeedState.OWN)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = listOf(seed),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertEquals(SeedAvailability.OWNED, carrot!!.seedAvailability)
        assertEquals(SuggestionRank.BEST_FIT, carrot.ranking)
    }

    @Test
    fun wantedSeed_ranking() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val seed = makeSeed("Carrot", "Nantes", SeedState.WANT)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = listOf(seed),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertEquals(SeedAvailability.WANTED, carrot!!.seedAvailability)
        assertEquals(SuggestionRank.ALSO_GOOD, carrot.ranking)
    }

    @Test
    fun untrackedSeed_remainsEligible() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull("Carrots should still be suggested without seed shelf entry", carrot)
        assertEquals(SeedAvailability.NOT_TRACKED, carrot!!.seedAvailability)
    }

    @Test
    fun activeDesire_improvesRanking() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val desire = makeDesire("Carrot")

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = emptyList(),
            desires = listOf(desire)
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertTrue(carrot!!.hasActiveDesire)

        assertEquals(SuggestionRank.ALSO_GOOD, carrot.ranking)

        assertFalse(desire.isFulfilled)
        assertFalse(desire.isCancelled)
        assertFalse(desire.isExpired)
    }

    @Test
    fun plantingSuggestion_structuredFields() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val seed = makeSeed("Carrot", "Nantes", SeedState.OWN)
        val desire = makeDesire("Carrot")

        val engine = DefaultPlanningEngine()
        val current = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = listOf(seed),
            desires = listOf(desire)
        )
        val currentCarrot = current.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(currentCarrot)
        assertFalse(currentCarrot!!.isFuture)
        assertNull(currentCarrot.openingDate)
        assertTrue(currentCarrot.hasActiveDesire)

        val future = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = makeDate(2026, 9, 15),
            inGarden = garden,
            seeds = listOf(seed),
            desires = listOf(desire)
        )
        val futureCarrot = future.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(futureCarrot)
        assertTrue(futureCarrot!!.isFuture)
        assertNotNull(futureCarrot.openingDate)
        assertEquals(makeDate(2026, 9, 15), futureCarrot.openingDate)
    }

    @Test
    fun deterministicRanking() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val engine = DefaultPlanningEngine()

        val firstRun = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )
        val secondRun = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        assertEquals("Ranking should be deterministic across runs",
            firstRun.map { it.cropName }, secondRun.map { it.cropName })
    }

    @Test
    fun dateBoundaries() {
        val firstFrost = makeDate(2026, 10, 15)
        val garden = makeGarden(firstFrost = firstFrost)
        val space = makeGrowingSpace("Bed 1")
        val engine = DefaultPlanningEngine()

        val sep1 = makeDate(2026, 9, 1)
        val s1 = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space, openingDate = sep1, inGarden = garden,
            seeds = emptyList(), desires = emptyList()
        )
        val carrotSep1 = s1.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrotSep1)
        assertEquals(9, monthOf(carrotSep1!!.suggestedPlantingDate))

        val sep30 = makeDate(2026, 9, 30)
        val s30 = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space, openingDate = sep30, inGarden = garden,
            seeds = emptyList(), desires = emptyList()
        )
        val carrotSep30 = s30.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrotSep30)
        assertEquals(sep30, carrotSep30!!.suggestedPlantingDate)

        val oct1 = makeDate(2026, 10, 1)
        val sOct = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space, openingDate = oct1, inGarden = garden,
            seeds = emptyList(), desires = emptyList()
        )
        val carrotOct1 = sOct.firstOrNull { it.cropName == "Carrot" }
        assertNull("Carrots should be rejected when opening is after fall window", carrotOct1)
    }

    @Test
    fun plantingWindowName_exposedInSuggestion() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )
        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertEquals("Planting window name should be exposed", "Fall", carrot!!.plantingWindowName)
    }

    @Test
    fun seedShelf_doesNotBlockRecommendations() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )
        assertFalse("Engine should recommend crops even with empty seed shelf", suggestions.isEmpty())
    }

    @Test
    fun desire_doesNotMutateState() {
        val garden = makeGarden()
        val desire = makeDesire("Carrot")
        val engine = DefaultPlanningEngine()
        engine.suggestions(
            forGrowingSpace = makeGrowingSpace("Bed 1"),
            activeOccupancies = emptyList(),
            onDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = emptyList(),
            desires = listOf(desire)
        )
        assertFalse(desire.isFulfilled)
        assertFalse(desire.isCancelled)
        assertFalse(desire.isExpired)
    }

    @Test
    fun killedByFrost_beforeLastFrost() {
        val lastFrost = makeDate(2026, 5, 15)
        val garden = makeGarden(lastFrost = lastFrost)
        val space = makeGrowingSpace("Bed 1")
        val plantingDate = makeDate(2026, 5, 1)
        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            forGrowingSpace = space,
            activeOccupancies = emptyList(),
            onDate = plantingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )
        val tomato = suggestions.firstOrNull { it.cropName == "Tomato" }
        assertNull("Tomatoes should be rejected before last frost date", tomato)
    }

    @Test
    fun suggestionsUsingSeeds_filtersToOwned() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val ownedSeed = makeSeed("Carrot", "Nantes", SeedState.OWN)
        val wantedSeed = makeSeed("Tomato", "Roma", SeedState.WANT)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestions(
            usingSeeds = listOf(ownedSeed, wantedSeed),
            inGarden = garden,
            onDate = makeDate(2026, 8, 17),
            growingSpaces = listOf(space),
            desires = emptyList(),
            allOccupancies = emptyList()
        )

        val cropNames = suggestions.map { it.cropName }
        assertTrue("Owned seed crop should be suggested", cropNames.contains("Carrot"))
        assertFalse("Wanted seed crop should not appear in owned-seeds-only query", cropNames.contains("Tomato"))
    }

    @Test
    fun futureUnknownMaturity_leavesHarvestNil() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = makeDate(2026, 8, 17),
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )
        for (suggestion in suggestions) {
            val harvest = suggestion.estimatedHarvestDate
            if (harvest != null) {
                assertTrue("Harvest should not be before planting", harvest >= suggestion.suggestedPlantingDate)
            }
        }
    }

    @Test
    fun futureOpeningBeforeWindow_preservesIsFuture() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val openingDate = makeDate(2026, 6, 15)
        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = openingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )
        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertTrue("Suggestion should be marked as future even when candidate differs from opening", carrot!!.isFuture)
        assertEquals(openingDate, carrot.openingDate)
        assertTrue("Candidate date should be after opening date", carrot.suggestedPlantingDate > openingDate)
    }

    @Test
    fun futureReasonText_whenOpeningEqualsCandidate() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val openingDate = makeDate(2026, 9, 15)
        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = openingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )
        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertTrue("Reason should say 'Plant when space opens' when candidate equals opening",
            carrot!!.reason.contains("Plant when space opens"))
    }

    @Test
    fun futureReasonText_whenOpeningBeforeCandidate() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val openingDate = makeDate(2026, 6, 15)
        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = openingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )
        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertTrue("Reason should mention space opening", carrot!!.reason.contains("Space opens"))
        assertTrue("Reason should mention planting", carrot.reason.contains("Plant"))
    }

    @Test
    fun explicitOpeningDate_overridesExpectedReleaseDate() {
        val garden = makeGarden()
        val space = makeGrowingSpace("Bed 1")
        val expectedRelease = makeDate(2026, 9, 15)
        val occupancy = makeOccupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedReleaseDate = expectedRelease,
            status = OccupancyStatus.ACTIVE,
            growingSpace = space
        )
        val explicitDate = makeDate(2026, 9, 1)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = explicitDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrot = suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull("Future suggestions should be produced from an explicit opening date", carrot)
        assertEquals("Explicit opening date must take precedence over expected release", explicitDate, carrot!!.openingDate)
        assertEquals("Occupancy must not be mutated", expectedRelease, occupancy.expectedReleaseDate)
    }

    @Test
    fun unknownMaturity_leavesEstimatedHarvestNil() {
        val crop = Crop(
            id = "testcrop",
            name = "TestCrop",
            varieties = listOf(
                Variety(id = "V", name = "V", cropName = "TestCrop", daysToMaturity = null, plantingWindows = emptyList())
            ),
            family = null,
            frostTolerant = false,
            killedByFrost = false,
            transplantSensitive = false
        )
        val engine = DefaultPlanningEngine()
        val harvest = engine.estimatedHarvest(
            date = makeDate(2026, 9, 1),
            variety = null,
            crop = crop
        )
        assertNull("Estimated harvest must be nil when daysToMaturity is unknown", harvest)
    }
}
