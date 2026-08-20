package com.soilandsupper.ui

import com.soilandsupper.gardentimeline.CropTimelinePhase
import com.soilandsupper.gardentimeline.buildTimelineSpaces
import com.soilandsupper.ui.fixture.RealisticGardenFixture
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test

class GardenTimelineAccessibilityTest {

    @Test
    fun `lifecycle phases are understandable without color`() {
        val phases = CropTimelinePhase.values()
        phases.forEach { phase ->
            val label = phase.displayName
            assertTrue(
                "Phase $phase must have a non-empty display name for accessibility",
                label.isNotBlank()
            )
            assertTrue(
                "Phase $phase display name must be a readable phrase, got: $label",
                label.any { it.isUpperCase() } && label.any { it.isLowerCase() }
            )
        }
    }

    @Test
    fun `future suggestions have contextual text`() {
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

        val future = spaces.first().futureSuggestions
        assertNotNull(future)
        assertFalse(future?.suggestions?.isEmpty() ?: true)

        future?.suggestions?.forEach { suggestion ->
            assertTrue(
                "Future suggestion ${suggestion.cropName} must have a reason for accessibility",
                suggestion.reason.isNotBlank()
            )
        }
    }

    @Test
    fun `available spaces have clear labels`() {
        val emptyBed = RealisticGardenFixture.spaces.last()
        val selectedDate = RealisticGardenFixture.makeDate(2026, 8, 17)

        val spaces = buildTimelineSpaces(
            growingSpaces = listOf(emptyBed),
            occupancies = emptyList(),
            selectedDate = selectedDate,
            garden = RealisticGardenFixture.garden,
            seeds = emptyList(),
            desires = emptyList()
        )

        val model = spaces.first()
        assertTrue(model.isAvailable)
        assertNotNull(model.currentSuggestions)
    }

    @Test
    fun `seed availability has meaningful labels`() {
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

        val carrot = spaces.first().currentSuggestions!!.suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertEquals("OWNED", carrot!!.seedAvailability.name)
        assertTrue(carrot.seedAvailability.label.isNotBlank())
    }

    @Test
    fun `suggestion ranking has meaningful labels`() {
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

        val carrot = spaces.first().currentSuggestions!!.suggestions.firstOrNull { it.cropName == "Carrot" }
        assertNotNull(carrot)
        assertEquals("BEST_FIT", carrot!!.ranking.name)
        assertTrue(carrot.ranking.label.isNotBlank())
    }

    @Test
    fun `date text is human readable`() {
        val date = RealisticGardenFixture.makeDate(2026, 8, 17)
        val formatted = com.soilandsupper.util.formatDate("MMM d, yyyy", date)
        assertTrue("Date must be human readable", formatted.isNotBlank())
        assertTrue("Date must contain month name", formatted.contains("Aug"))
    }
}
