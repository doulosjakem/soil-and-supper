package com.soilandsupper.shared.domain.model

data class Occupancy(
    val id: Long = 0,
    val cropName: String,
    val variety: String? = null,
    val startDate: Long,
    val endDate: Long? = null,
    val expectedHarvestDate: Long? = null,
    val expectedReleaseDate: Long? = null,
    val status: String = OccupancyStatus.ACTIVE.name,
    val notes: String? = null,
    val growingSpaceId: Long? = null,
    val plantId: Long? = null,
    val plannedPlantingId: Long? = null,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
) {
    val displayName: String
        get() = if (!variety.isNullOrBlank()) "$variety $cropName" else cropName
}

