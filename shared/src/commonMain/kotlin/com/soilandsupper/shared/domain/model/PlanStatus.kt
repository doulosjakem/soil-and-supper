package com.soilandsupper.shared.domain.model

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

