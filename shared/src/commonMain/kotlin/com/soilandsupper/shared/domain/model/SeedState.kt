package com.soilandsupper.shared.domain.model

enum class SeedState {
    OWN,
    WANT;

    val symbolName: String
        get() = when (this) {
            OWN -> "leaf.fill"
            WANT -> "heart.fill"
        }
}

