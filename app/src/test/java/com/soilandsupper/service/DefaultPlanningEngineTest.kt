package com.soilandsupper.service

import com.soilandsupper.domain.model.Garden
import com.soilandsupper.domain.model.GrowingSpace
import com.soilandsupper.domain.model.Occupancy
import com.soilandsupper.domain.model.OccupancyStatus
import com.soilandsupper.domain.model.PlantingSuggestion
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.Calendar

class DefaultPlanningEngineTest {

    private fun makeDate(year: Int, month: Int, day: Int): Long {
        val calendar = Calendar.getInstance()
        calendar.set(year, month - 1, day, 12, 0, 0)
        calendar.set(Calendar.MILLISECOND, 0)
        return calendar.timeInMillis
    }

    @Test
    fun `open space produces current suggestions`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
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

        val carrotSuggestions = suggestions.filter { it.cropName == "Carrot" }
        assertFalse(carrotSuggestions.isEmpty())
        assertFalse(carrotSuggestions.first().isFuture)
    }

    @Test
    fun `occupied space suppresses current suggestions`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
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

        assertTrue(suggestions.isEmpty())
    }

    @Test
    fun `future opening inside planting window produces future suggestions`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val openingDate = makeDate(2026, 9, 15)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = openingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val carrotSuggestions = suggestions.filter { it.cropName == "Carrot" }
        assertFalse(carrotSuggestions.isEmpty())
        assertTrue(carrotSuggestions.first().isFuture)
        assertEquals(openingDate, carrotSuggestions.first().openingDate)
    }

    @Test
    fun `known maturity produces harvest estimate`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val plantingDate = makeDate(2026, 9, 1)

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = plantingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val radishSuggestions = suggestions.filter { it.cropName == "Radish" }
        assertFalse(radishSuggestions.isEmpty())
        val harvest = radishSuggestions.first().estimatedHarvestDate
        assertTrue(harvest != null)
        val days = daysBetween(plantingDate, harvest!!)
        assertEquals(22, days)
    }

    @Test
    fun `future opening with active occupancy still produces suggestions`() {
        val garden = Garden(name = "Test Garden")
        val space = GrowingSpace(id = 1L, name = "Bed 1", gardenId = garden.id)
        val openingDate = makeDate(2026, 9, 15)
        val occupancy = Occupancy(
            cropName = "Tomato",
            startDate = makeDate(2026, 5, 15),
            expectedReleaseDate = openingDate,
            status = OccupancyStatus.ACTIVE.name,
            growingSpaceId = space.id
        )

        val engine = DefaultPlanningEngine()
        val suggestions = engine.suggestionsForFutureOpening(
            ofGrowingSpace = space,
            openingDate = openingDate,
            inGarden = garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        assertFalse(suggestions.isEmpty())
        assertTrue(suggestions.all { it.isFuture })
        assertEquals(openingDate, suggestions.first().openingDate)
    }

    private fun daysBetween(start: Long, end: Long): Int {
        val calendar1 = Calendar.getInstance()
        calendar1.timeInMillis = start
        val calendar2 = Calendar.getInstance()
        calendar2.timeInMillis = end
        val diff = calendar2.timeInMillis - calendar1.timeInMillis
        return (diff / (1000 * 60 * 60 * 24)).toInt()
    }
}
