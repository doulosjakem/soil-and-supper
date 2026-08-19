package com.soilandsupper.shared.domain.model

data class PlantPhoto(
    val id: Long = 0,
    val plantId: Long,
    val uri: String,
    val createdAt: Long = System.currentTimeMillis()
)

