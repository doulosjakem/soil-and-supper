package com.soilandsupper.shared.domain.model

data class Garden(
    val id: Long = 0,
    val name: String,
    val location: String? = null,
    val climateZone: String? = null,
    val averageLastFrostDate: Long? = null,
    val averageFirstFrostDate: Long? = null,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
)

