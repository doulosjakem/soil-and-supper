package com.soilandsupper.shared.domain.model

data class Plant(
    val id: Long = 0,
    val name: String,
    val variety: String = "",
    val plantingDate: Long = System.currentTimeMillis(),
    val location: String = "",
    val notes: String = "",
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
)

