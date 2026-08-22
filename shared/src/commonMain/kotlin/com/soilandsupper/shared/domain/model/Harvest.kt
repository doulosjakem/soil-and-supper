package com.soilandsupper.shared.domain.model

data class Harvest(
    val id: Long = 0,
    val plantId: Long? = null,
    val cropName: String,
    val quantity: Double,
    val unit: String,
    val date: Long = System.currentTimeMillis(),
    val notes: String = ""
)

