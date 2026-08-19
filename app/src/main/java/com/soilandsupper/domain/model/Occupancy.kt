package com.soilandsupper.domain.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey

@Entity(
    tableName = "occupancies",
    foreignKeys = [
        ForeignKey(
            entity = GrowingSpace::class,
            parentColumns = ["id"],
            childColumns = ["growingSpaceId"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = Plant::class,
            parentColumns = ["id"],
            childColumns = ["plantId"],
            onDelete = ForeignKey.SET_NULL
        ),
        ForeignKey(
            entity = PlannedPlanting::class,
            parentColumns = ["id"],
            childColumns = ["plannedPlantingId"],
            onDelete = ForeignKey.SET_NULL
        )
    ]
)
data class Occupancy(
    @PrimaryKey(autoGenerate = true)
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

enum class OccupancyStatus {
    ACTIVE,
    COMPLETED,
    CANCELLED;

    val displayName: String
        get() = when (this) {
            ACTIVE -> "Active"
            COMPLETED -> "Completed"
            CANCELLED -> "Cancelled"
        }
}
