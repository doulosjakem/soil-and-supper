package com.soilandsupper.domain.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey

@Entity(
    tableName = "desires",
    foreignKeys = [
        ForeignKey(
            entity = Garden::class,
            parentColumns = ["id"],
            childColumns = ["gardenId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class Desire(
    @PrimaryKey(autoGenerate = true)
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
