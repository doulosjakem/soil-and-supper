package com.soilandsupper.shared.domain.model

data class Seed(
    val id: Long = 0,
    val cropName: String,
    val variety: String? = null,
    val state: String = SeedState.OWN.name,
    val notes: String? = null,
    val gardenId: Long? = null,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
) {
    val displayName: String
        get() = if (!variety.isNullOrBlank()) "$variety $cropName" else cropName
}

