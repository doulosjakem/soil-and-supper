package com.soilandsupper.shared.domain.model

enum class SpaceType {
    BED,
    CONTAINER,
    ROW,
    OTHER;

    val displayName: String
        get() = when (this) {
            BED -> "Bed"
            CONTAINER -> "Container"
            ROW -> "Row"
            OTHER -> "Other"
        }
}

