package com.soilandsupper.domain.model

enum class SeedAvailability {
    OWNED,
    WANTED,
    NOT_TRACKED;

    val label: String
        get() = when (this) {
            OWNED -> "You have seeds"
            WANTED -> "You want seeds"
            NOT_TRACKED -> "Not on your Seed Shelf"
        }
}

enum class SuggestionRank {
    BEST_FIT,
    ALSO_GOOD,
    NOT_RECOMMENDED;

    val label: String
        get() = when (this) {
            BEST_FIT -> "Best fit"
            ALSO_GOOD -> "Also good"
            NOT_RECOMMENDED -> "Not recommended"
        }
}

data class PlantingSuggestion(
    val id: Long = 0,
    val cropName: String,
    val varietyName: String? = null,
    val suggestedPlantingDate: Long,
    val estimatedHarvestDate: Long? = null,
    val estimatedReleaseDate: Long? = null,
    val growingSpaceId: Long? = null,
    val seedAvailability: SeedAvailability = SeedAvailability.NOT_TRACKED,
    val ranking: SuggestionRank = SuggestionRank.ALSO_GOOD,
    val warnings: List<String> = emptyList(),
    val reason: String = "",
    val isFuture: Boolean = false,
    val openingDate: Long? = null,
    val plantingWindowName: String? = null,
    val hasActiveDesire: Boolean = false
)
