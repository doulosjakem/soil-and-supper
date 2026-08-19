package com.soilandsupper.service

import com.soilandsupper.shared.domain.model.Crop
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.Garden
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.OccupancyStatus
import com.soilandsupper.shared.domain.model.PlantingSuggestion
import com.soilandsupper.shared.domain.model.PlantingWindow
import com.soilandsupper.shared.domain.model.Seed
import com.soilandsupper.shared.domain.model.SeedAvailability
import com.soilandsupper.shared.domain.model.SeedState
import com.soilandsupper.shared.domain.model.SuggestionRank
import com.soilandsupper.shared.domain.model.Variety
import kotlinx.datetime.Instant
import kotlinx.datetime.LocalDate
import kotlinx.datetime.TimeZone
import kotlinx.datetime.toLocalDateTime
import com.soilandsupper.util.formatDate

interface PlanningEngine {
    fun suggestions(
        forGrowingSpace: GrowingSpace,
        activeOccupancies: List<Occupancy>,
        onDate: Long,
        inGarden: Garden,
        seeds: List<Seed>,
        desires: List<Desire>
    ): List<PlantingSuggestion>

    fun whatCanBePlantedNow(
        inGarden: Garden,
        growingSpaces: List<GrowingSpace>,
        onDate: Long,
        seeds: List<Seed>,
        desires: List<Desire>,
        allOccupancies: List<Occupancy>
    ): List<PlantingSuggestion>

    fun suggestions(
        usingSeeds: List<Seed>,
        inGarden: Garden,
        onDate: Long,
        growingSpaces: List<GrowingSpace>,
        desires: List<Desire>,
        allOccupancies: List<Occupancy>
    ): List<PlantingSuggestion>

    fun suggestionsForFutureOpening(
        ofGrowingSpace: GrowingSpace,
        openingDate: Long,
        inGarden: Garden,
        seeds: List<Seed>,
        desires: List<Desire>
    ): List<PlantingSuggestion>
}

class DefaultPlanningEngine : PlanningEngine {

    private data class PlantingDecision(
        val allowed: Boolean,
        val warnings: List<String>,
        val candidateDate: Long,
        val windowName: String?
    )

    override fun suggestions(
        forGrowingSpace: GrowingSpace,
        activeOccupancies: List<Occupancy>,
        onDate: Long,
        inGarden: Garden,
        seeds: List<Seed>,
        desires: List<Desire>
    ): List<PlantingSuggestion> {
        if (activeOccupancies.isNotEmpty()) return emptyList()
        return evaluateCrops(forGrowingSpace, onDate, inGarden, seeds, desires)
    }

    override fun whatCanBePlantedNow(
        inGarden: Garden,
        growingSpaces: List<GrowingSpace>,
        onDate: Long,
        seeds: List<Seed>,
        desires: List<Desire>,
        allOccupancies: List<Occupancy>
    ): List<PlantingSuggestion> {
        val openSpaces = growingSpaces.filter { space ->
            allOccupancies.none { it.growingSpaceId == space.id && it.status == OccupancyStatus.ACTIVE.name }
        }
        if (openSpaces.isEmpty()) return emptyList()

        val allSuggestions = mutableListOf<PlantingSuggestion>()
        for (space in openSpaces) {
            val activeForSpace = allOccupancies.filter { it.growingSpaceId == space.id && it.status == OccupancyStatus.ACTIVE.name }
            allSuggestions.addAll(evaluateCrops(space, onDate, inGarden, seeds, desires))
        }
        return deduplicateAndRank(allSuggestions)
    }

    override fun suggestions(
        usingSeeds: List<Seed>,
        inGarden: Garden,
        onDate: Long,
        growingSpaces: List<GrowingSpace>,
        desires: List<Desire>,
        allOccupancies: List<Occupancy>
    ): List<PlantingSuggestion> {
        val ownedSeeds = usingSeeds.filter { it.state == SeedState.OWN.name }
        if (ownedSeeds.isEmpty()) return emptyList()

        val openSpaces = growingSpaces.filter { space ->
            allOccupancies.none { it.growingSpaceId == space.id && it.status == OccupancyStatus.ACTIVE.name }
        }
        if (openSpaces.isEmpty()) return emptyList()

        val allSuggestions = mutableListOf<PlantingSuggestion>()
        for (space in openSpaces) {
            for (seed in ownedSeeds) {
                val crop = CropKnowledge.crop(name = seed.cropName) ?: continue
                val variety = crop.variety(name = seed.variety ?: continue)
                val (allowed, warnings, _, _) = canPlantNow(crop, variety, onDate, inGarden)
                if (!allowed) continue

                val matchingDesire = desires.firstOrNull { desire ->
                    desire.cropName.equals(seed.cropName, ignoreCase = true) &&
                            !desire.isFulfilled && !desire.isCancelled && !desire.isExpired
                }

                val rank = SuggestionRank.BEST_FIT
                val estimatedHarvest = estimatedHarvest(date = onDate, variety = variety, crop = crop)
                val reason = reasonText(
                    seedAvailability = SeedAvailability.OWNED,
                    desire = matchingDesire,
                    futureOpening = false,
                    openingDate = null,
                    windowName = null,
                    candidateDate = onDate
                )

                allSuggestions.add(
                    PlantingSuggestion(
                        cropName = crop.name,
                        varietyName = seed.variety,
                        suggestedPlantingDate = onDate,
                        estimatedHarvestDate = estimatedHarvest,
                        growingSpaceId = space.id,
                        seedAvailability = SeedAvailability.OWNED,
                        ranking = rank,
                        warnings = warnings,
                        reason = reason,
                        isFuture = false,
                        openingDate = null,
                        plantingWindowName = null,
                        hasActiveDesire = matchingDesire != null
                    )
                )
            }
        }
        return allSuggestions.sortedBy { it.ranking }
    }

    override fun suggestionsForFutureOpening(
        ofGrowingSpace: GrowingSpace,
        openingDate: Long,
        inGarden: Garden,
        seeds: List<Seed>,
        desires: List<Desire>
    ): List<PlantingSuggestion> {
        return evaluateCrops(ofGrowingSpace, openingDate, inGarden, seeds, desires, futureOpening = true, openingDate = openingDate)
    }

    private fun evaluateCrops(
        forSpace: GrowingSpace,
        onDate: Long,
        inGarden: Garden,
        seeds: List<Seed>,
        desires: List<Desire>,
        futureOpening: Boolean = false,
        openingDate: Long? = null
    ): List<PlantingSuggestion> {
        val suggestions = mutableListOf<PlantingSuggestion>()
        for (crop in CropKnowledge.allCrops()) {
            val (allowed, warnings, candidateDate, windowName) = canPlantNow(crop, null, onDate, inGarden, futureOpening)
            if (!allowed) continue

            val seedAvailability = seedAvailability(forCropName = crop.name, inSeeds = seeds)
            val matchingDesire = desires.firstOrNull { desire ->
                desire.cropName.equals(crop.name, ignoreCase = true) &&
                        !desire.isFulfilled && !desire.isCancelled && !desire.isExpired
            }
            val rank = rankSuggestion(seedAvailability, matchingDesire)
            val estimatedHarvest = estimatedHarvest(date = candidateDate, variety = null, crop = crop)
            val reason = reasonText(
                seedAvailability = seedAvailability,
                desire = matchingDesire,
                futureOpening = futureOpening,
                openingDate = openingDate,
                windowName = windowName,
                candidateDate = candidateDate
            )

            suggestions.add(
                PlantingSuggestion(
                    cropName = crop.name,
                    varietyName = null,
                    suggestedPlantingDate = candidateDate,
                    estimatedHarvestDate = estimatedHarvest,
                    growingSpaceId = forSpace.id,
                    seedAvailability = seedAvailability,
                    ranking = rank,
                    warnings = warnings,
                    reason = reason,
                    isFuture = futureOpening,
                    openingDate = openingDate,
                    plantingWindowName = windowName,
                    hasActiveDesire = matchingDesire != null
                )
            )
        }
        return suggestions.sortedBy { it.ranking }
    }

    private fun canPlantNow(
        crop: Crop,
        variety: Variety?,
        onDate: Long,
        inGarden: Garden,
        futureOpening: Boolean = false
    ): PlantingDecision {
        val warnings = mutableListOf<String>()
        val currentMonth = monthOf(onDate)
        val windows = variety?.plantingWindows ?: crop.varieties.flatMap { it.plantingWindows }

        val inWindow: Boolean
        val candidateDate: Long
        val windowName: String?

        if (futureOpening) {
            val validWindow = windows.firstOrNull { window ->
                if (window.startMonth <= window.endMonth) {
                    currentMonth <= window.endMonth
                } else {
                    currentMonth >= window.startMonth || currentMonth <= window.endMonth
                }
            }

            if (validWindow == null) {
                return PlantingDecision(false, listOf("Planting window has closed for this crop."), onDate, null)
            }

            inWindow = true
            candidateDate = earliestDate(window = validWindow, date = onDate)
            windowName = validWindow.name
        } else {
            val matchedWindow = windows.firstOrNull { window ->
                if (window.startMonth <= window.endMonth) {
                    currentMonth >= window.startMonth && currentMonth <= window.endMonth
                } else {
                    currentMonth >= window.startMonth || currentMonth <= window.endMonth
                }
            }

            inWindow = matchedWindow != null
            candidateDate = onDate
            windowName = matchedWindow?.name
        }

        if (!inWindow) {
            return PlantingDecision(false, listOf("Planting window has closed for this crop."), onDate, null)
        }

        if (crop.killedByFrost) {
            val lastFrost = inGarden.averageLastFrostDate
            if (lastFrost != null && candidateDate < lastFrost) {
                return PlantingDecision(false, listOf("This crop is killed by frost. Wait until after the average last frost."), candidateDate, windowName)
            }
        }

        val firstFrost = inGarden.averageFirstFrostDate
        val daysToMaturity = variety?.daysToMaturity ?: crop.defaultVariety?.daysToMaturity
        if (firstFrost != null && daysToMaturity != null) {
            val daysRemaining = daysBetween(candidateDate, firstFrost)
            if (daysRemaining < daysToMaturity) {
                if (crop.frostTolerant) {
                    warnings.add("Frost-tolerant crop may survive light frost after $daysToMaturity days.")
                } else {
                    return PlantingDecision(false, listOf("Too little season remaining. Needs $daysToMaturity days but only $daysRemaining days until first frost."), candidateDate, windowName)
                }
            }
        }

        return PlantingDecision(true, warnings, candidateDate, windowName)
    }

    private fun earliestDate(window: PlantingWindow, date: Long): Long {
        val currentMonth = monthOf(date)
        val targetMonth = if (window.startMonth <= window.endMonth) {
            maxOf(currentMonth, window.startMonth)
        } else {
            if (currentMonth >= window.startMonth) currentMonth else window.startMonth
        }

        val instant = Instant.fromEpochMilliseconds(date)
        val localDateTime = instant.toLocalDateTime(TimeZone.UTC)
        val year = localDateTime.year

        val targetDate = LocalDate(year, targetMonth, 1)
        val targetInstant = Instant.fromEpochMilliseconds(targetDate.toEpochDay() * 86400000L)

        return maxOf(targetInstant.toEpochMilliseconds(), date)
    }

    private fun seedAvailability(forCropName: String, inSeeds: List<Seed>): SeedAvailability {
        val owned = inSeeds.any { it.state == SeedState.OWN.name && it.cropName.equals(forCropName, ignoreCase = true) }
        if (owned) return SeedAvailability.OWNED

        val wanted = inSeeds.any { it.state == SeedState.WANT.name && it.cropName.equals(forCropName, ignoreCase = true) }
        if (wanted) return SeedAvailability.WANTED

        return SeedAvailability.NOT_TRACKED
    }

    private fun rankSuggestion(seedAvailability: SeedAvailability, desire: Desire?): SuggestionRank {
        return if (seedAvailability == SeedAvailability.OWNED) {
            if (desire != null) SuggestionRank.BEST_FIT else SuggestionRank.BEST_FIT
        } else if (seedAvailability == SeedAvailability.WANTED) {
            if (desire != null) SuggestionRank.ALSO_GOOD else SuggestionRank.ALSO_GOOD
        } else if (desire != null) {
            SuggestionRank.ALSO_GOOD
        } else {
            SuggestionRank.ALSO_GOOD
        }
    }

    fun estimatedHarvest(date: Long, variety: Variety?, crop: Crop): Long? {
        val daysToMaturity = variety?.daysToMaturity ?: crop.defaultVariety?.daysToMaturity ?: return null
        return addDays(date, daysToMaturity)
    }

    private fun reasonText(
        seedAvailability: SeedAvailability,
        desire: Desire?,
        futureOpening: Boolean,
        openingDate: Long?,
        windowName: String?,
        candidateDate: Long
    ): String {
        val parts = mutableListOf<String>()

        if (seedAvailability == SeedAvailability.OWNED) {
            parts.add("You have seeds for this.")
        } else if (seedAvailability == SeedAvailability.WANTED) {
            parts.add("You want these seeds.")
        }

        if (desire != null) {
            parts.add("This matches a desire.")
        }

        if (futureOpening && openingDate != null) {
            val openingStr = formatDate("MMM d", openingDate)
            val candidateStr = formatDate("MMM d", candidateDate)

            if (isSameDay(openingDate, candidateDate)) {
                parts.add(if (windowName != null) "Plant when space opens for $windowName planting." else "Plant when space opens.")
            } else if (candidateDate > openingDate) {
                parts.add(if (windowName != null) "Space opens ~$openingStr. Plant $candidateStr for $windowName planting." else "Space opens ~$openingStr. Plant $candidateStr.")
            }
        } else if (windowName != null) {
            parts.add("$windowName planting.")
        } else {
            parts.add("Fits the current season.")
        }

        return parts.joinToString(" ")
    }

    private fun deduplicateAndRank(suggestions: List<PlantingSuggestion>): List<PlantingSuggestion> {
        val grouped = suggestions.groupBy { it.cropName }
        return grouped.mapNotNull { entry ->
            entry.value.minByOrNull { it.ranking }
        }.sortedBy { it.ranking }
    }
}

private fun monthOf(millis: Long): Int {
    val instant = Instant.fromEpochMilliseconds(millis)
    val localDate = instant.toLocalDateTime(TimeZone.UTC).date
    return localDate.monthNumber
}

private fun addDays(millis: Long, days: Int): Long {
    return millis + days * 86_400_000L
}

private fun daysBetween(start: Long, end: Long): Int {
    return ((end - start) / 86_400_000L).toInt()
}

private fun isSameDay(date1: Long, date2: Long): Boolean {
    val d1 = Instant.fromEpochMilliseconds(date1).toLocalDateTime(TimeZone.UTC).date
    val d2 = Instant.fromEpochMilliseconds(date2).toLocalDateTime(TimeZone.UTC).date
    return d1 == d2
}

