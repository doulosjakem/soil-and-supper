package com.soilandsupper.ui

import com.soilandsupper.domain.model.GrowingSpace
import com.soilandsupper.domain.model.Occupancy
import com.soilandsupper.domain.model.OccupancyStatus
import com.soilandsupper.domain.model.PlantingSuggestion
import com.soilandsupper.service.DefaultPlanningEngine
import java.util.Calendar

enum class CropTimelinePhase {
    NOT_PLANTED,
    GROWING,
    PRODUCING,
    NEARING_RELEASE,
    COMPLETED;

    val displayName: String
        get() = when (this) {
            NOT_PLANTED -> "Not planted"
            GROWING -> "Growing"
            PRODUCING -> "Producing"
            NEARING_RELEASE -> "Space opening soon"
            COMPLETED -> "Completed"
        }
}

data class OccupancyTimelineModel(
    val occupancy: Occupancy,
    val phase: CropTimelinePhase,
    val daysUntilHarvest: Int?,
    val daysUntilRelease: Int?
)

data class FutureSuggestionsTimelineModel(
    val suggestions: List<PlantingSuggestion>,
    val openingDate: Long
)

data class GrowingSpaceTimelineModel(
    val space: GrowingSpace,
    val occupancy: OccupancyTimelineModel?,
    val pastOccupancies: List<Occupancy>,
    val futureSuggestions: FutureSuggestionsTimelineModel?,
    val isAvailable: Boolean
)

data class GardenTimelineUiState(
    val selectedDate: Long,
    val spaces: List<GrowingSpaceTimelineModel>
)

fun buildTimelineSpaces(
    growingSpaces: List<GrowingSpace>,
    occupancies: List<Occupancy>,
    selectedDate: Long,
    garden: com.soilandsupper.domain.model.Garden?
): List<GrowingSpaceTimelineModel> {
    val engine = DefaultPlanningEngine()

    return growingSpaces.map { space ->
        val spaceOccupancies = occupancies.filter { it.growingSpaceId == space.id }
        val activeOccupancy = spaceOccupancies.firstOrNull { occupancy ->
            occupancy.status == OccupancyStatus.ACTIVE.name && occupancy.startDate <= selectedDate
        }

        val otherOccupancies = spaceOccupancies.filter { it != activeOccupancy }
        val pastOccupancies = otherOccupancies.filter { occupancy ->
            occupancy.status != OccupancyStatus.ACTIVE.name || occupancy.startDate > selectedDate
        }

        val occupancyModel: OccupancyTimelineModel? = activeOccupancy?.let { occupancy ->
            val phase = timelinePhaseFor(occupancy, selectedDate)
            val daysUntilHarvest = daysBetween(selectedDate, occupancy.expectedHarvestDate)
            val daysUntilRelease = daysBetween(selectedDate, occupancy.expectedReleaseDate)
            OccupancyTimelineModel(
                occupancy = occupancy,
                phase = phase,
                daysUntilHarvest = daysUntilHarvest,
                daysUntilRelease = daysUntilRelease
            )
        }

        val futureModel: FutureSuggestionsTimelineModel? = activeOccupancy?.let { occupancy ->
            val expectedRelease = occupancy.expectedReleaseDate
            if (expectedRelease != null && selectedDate < expectedRelease) {
                val effectiveGarden = garden ?: com.soilandsupper.domain.model.Garden(name = "Default")
                val suggestions = engine.suggestionsForFutureOpening(
                    ofGrowingSpace = space,
                    openingDate = expectedRelease,
                    inGarden = effectiveGarden,
                    seeds = emptyList(),
                    desires = emptyList()
                )
                FutureSuggestionsTimelineModel(
                    suggestions = suggestions,
                    openingDate = expectedRelease
                )
            } else null
        }

        val isAvailable = activeOccupancy == null && spaceOccupancies.all { it.status != OccupancyStatus.ACTIVE.name || it.startDate > selectedDate }

        GrowingSpaceTimelineModel(
            space = space,
            occupancy = occupancyModel,
            pastOccupancies = pastOccupancies,
            futureSuggestions = futureModel,
            isAvailable = isAvailable
        )
    }
}

private fun timelinePhaseFor(occupancy: Occupancy, date: Long): CropTimelinePhase {
    if (occupancy.status != OccupancyStatus.ACTIVE.name || occupancy.startDate > date) {
        return CropTimelinePhase.NOT_PLANTED
    }
    if (occupancy.endDate != null && date >= occupancy.endDate) {
        return CropTimelinePhase.COMPLETED
    }
    if (occupancy.expectedReleaseDate != null && date >= occupancy.expectedReleaseDate) {
        return CropTimelinePhase.NEARING_RELEASE
    }
    if (occupancy.expectedHarvestDate != null && date >= occupancy.expectedHarvestDate) {
        return CropTimelinePhase.PRODUCING
    }
    return CropTimelinePhase.GROWING
}

private fun daysBetween(start: Long, end: Long?): Int? {
    if (end == null) return null
    val calendar1 = Calendar.getInstance()
    calendar1.timeInMillis = start
    val calendar2 = Calendar.getInstance()
    calendar2.timeInMillis = end
    val diff = calendar2.timeInMillis - calendar1.timeInMillis
    return (diff / (1000 * 60 * 60 * 24)).toInt()
}
