package com.soilandsupper.domain.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "gardens")
data class Garden(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val name: String,
    val location: String? = null,
    val climateZone: String? = null,
    val averageLastFrostDate: Long? = null,
    val averageFirstFrostDate: Long? = null,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
)
