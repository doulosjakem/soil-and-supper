package com.soilandsupper.domain.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey

@Entity(
    tableName = "planned_plantings",
    foreignKeys = [
        ForeignKey(
            entity = Garden::class,
            parentColumns = ["id"],
            childColumns = ["gardenId"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = GrowingSpace::class,
            parentColumns = ["id"],
            childColumns = ["growingSpaceId"],
            onDelete = ForeignKey.SET_NULL
        ),
        ForeignKey(
            entity = Occupancy::class,
            parentColumns = ["id"],
            childColumns = ["occupancyId"],
            onDelete = ForeignKey.SET_NULL
        ),
        ForeignKey(
            entity = Desire::class,
            parentColumns = ["id"],
            childColumns = ["desireId"],
            onDelete = ForeignKey.SET_NULL
        ),
        ForeignKey(
            entity = Seed::class,
            parentColumns = ["id"],
            childColumns = ["seedId"],
            onDelete = ForeignKey.SET_NULL
        )
    ]
)
data class PlannedPlanting(
    @PrimaryKey(autoGenerate = true)
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

enum class PlanStatus {
    PLANNED,
    PLANTED,
    CANCELLED;

    val displayName: String
        get() = when (this) {
            PLANNED -> "Planned"
            PLANTED -> "Planted"
            CANCELLED -> "Cancelled"
        }
}
