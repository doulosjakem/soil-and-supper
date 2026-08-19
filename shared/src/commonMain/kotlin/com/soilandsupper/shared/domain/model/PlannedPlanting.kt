package com.soilandsupper.shared.domain.model

data class PlannedPlanting(
    val id: Long = 0,
    val cropName: String,
    val variety: String? = null,
    val plannedDate: Long? = null,
    val actualDate: Long? = null,
    val status: String = PlanStatus.PLANNED.name,
    val notes: String? = null,
    val gardenId: Long? = null,
    val growingSpaceId: Long? = null,
    val occupancyId: Long? = null,
    val desireId: Long? = null,
    val seedId: Long? = null,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
) {
    val displayName: String
        get() = if (!variety.isNullOrBlank()) "$variety $cropName" else cropName
}

