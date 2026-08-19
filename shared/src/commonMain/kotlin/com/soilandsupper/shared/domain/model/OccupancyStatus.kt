package com.soilandsupper.shared.domain.model

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

