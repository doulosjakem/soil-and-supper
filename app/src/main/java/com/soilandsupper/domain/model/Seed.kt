package com.soilandsupper.domain.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey

@Entity(
    tableName = "seeds",
    foreignKeys = [
        ForeignKey(
            entity = Garden::class,
            parentColumns = ["id"],
            childColumns = ["gardenId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class Seed(
    @PrimaryKey(autoGenerate = true)
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

enum class SeedState {
    OWN,
    WANT;

    val symbolName: String
        get() = when (this) {
            OWN -> "leaf.fill"
            WANT -> "heart.fill"
        }
}
