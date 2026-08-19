package com.soilandsupper.shared.domain.model

data class Desire(
    val id: Long = 0,
    val cropName: String,
    val variety: String? = null,
    val notes: String? = null,
    val isFulfilled: Boolean = false,
    val isCancelled: Boolean = false,
    val isExpired: Boolean = false,
    val gardenId: Long? = null,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
) {
    val displayName: String
        get() = if (!variety.isNullOrBlank()) "$variety $cropName" else cropName
}

