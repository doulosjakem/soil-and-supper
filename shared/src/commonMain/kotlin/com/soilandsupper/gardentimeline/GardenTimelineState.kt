package com.soilandsupper.gardentimeline

import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.Garden
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.OccupancyStatus
import com.soilandsupper.shared.domain.model.PlantingSuggestion
import com.soilandsupper.shared.domain.model.Seed
import com.soilandsupper.service.DefaultPlanningEngine
import com.soilandsupper.util.formatDate

enum class CropTimelinePhase {
    NOT_PLANTED,
    ESTABLISHING,
    GROWING,
    PRODUCING,
    NEARING_RELEASE,
    COMPLETED;

    val displayName: String
        get() = when (this) {
            NOT_PLANTED -> "Not planted"
            ESTABLISHING -> "Establishing"
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

data class CurrentSuggestionsTimelineModel(
    val suggestions: List<PlantingSuggestion>
)

data class GrowingSpaceTimelineModel(
    val space: GrowingSpace,
    val occupancy: OccupancyTimelineModel?,
    val pastOccupancies: List<Occupancy>,
    val futureSuggestions: FutureSuggestionsTimelineModel?,
    val currentSuggestions: CurrentSuggestionsTimelineModel?,
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
    garden: com.soilandsupper.shared.domain.model.Garden?,
    seeds: List<Seed> = emptyList(),
    desires: List<Desire> = emptyList()
): List<GrowingSpaceTimelineModel> {
    val engine = DefaultPlanningEngine()

    return growingSpaces.map { space ->
        val spaceOccupancies = occupancies.filter { it.growingSpaceId == space.id }
        val activeOccupancy = spaceOccupancies.firstOrNull { occupancy ->
            occupancy.status == OccupancyStatus.ACTIVE.name &&
                occupancy.startDate <= selectedDate &&
                (occupancy.endDate == null || selectedDate < occupancy.endDate)
        }

        val otherOccupancies = spaceOccupancies.filter { it != activeOccupancy }
        val pastOccupancies = otherOccupancies.filter { occupancy ->
            occupancy.status != OccupancyStatus.ACTIVE.name ||
                occupancy.startDate > selectedDate ||
                (occupancy.endDate != null && selectedDate >= occupancy.endDate)
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

        val futureModel: FutureSuggestionsTimelineModel? =
            if (seeds.isEmpty() && desires.isEmpty()) null
            else activeOccupancy?.let { occupancy ->
                val expectedRelease = occupancy.expectedReleaseDate
                if (expectedRelease != null && selectedDate < expectedRelease) {
                    val effectiveGarden = garden ?: com.soilandsupper.shared.domain.model.Garden(name = "Default")
                    val suggestions = engine.suggestionsForFutureOpening(
                        ofGrowingSpace = space,
                        openingDate = expectedRelease,
                        inGarden = effectiveGarden,
                        seeds = seeds,
                        desires = desires
                    )
                    FutureSuggestionsTimelineModel(
                        suggestions = suggestions,
                        openingDate = expectedRelease
                    )
                } else null
            }

        val currentModel: CurrentSuggestionsTimelineModel? = if (activeOccupancy == null) {
            val effectiveGarden = garden ?: com.soilandsupper.shared.domain.model.Garden(name = "Default")
            val suggestions = engine.suggestions(
                forGrowingSpace = space,
                activeOccupancies = emptyList(),
                onDate = selectedDate,
                inGarden = effectiveGarden,
                seeds = seeds,
                desires = desires
            )
            CurrentSuggestionsTimelineModel(suggestions = suggestions)
        } else null

        val isAvailable = activeOccupancy == null && spaceOccupancies.all { occ ->
            occ.status != OccupancyStatus.ACTIVE.name ||
                occ.startDate > selectedDate ||
                (occ.endDate != null && selectedDate >= occ.endDate)
        }

        GrowingSpaceTimelineModel(
            space = space,
            occupancy = occupancyModel,
            pastOccupancies = pastOccupancies,
            futureSuggestions = futureModel,
            currentSuggestions = currentModel,
            isAvailable = isAvailable
        )
    }
}

private const val ESTABLISHING_WINDOW_DAYS = 21

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
    val daysSincePlanting = daysBetween(occupancy.startDate, date)
    if (daysSincePlanting != null && daysSincePlanting < ESTABLISHING_WINDOW_DAYS) {
        return CropTimelinePhase.ESTABLISHING
    }
    return CropTimelinePhase.GROWING
}

private fun daysBetween(start: Long, end: Long?): Int? {
    if (end == null) return null
    return ((end - start) / (1000 * 60 * 60 * 24)).toInt()
}

