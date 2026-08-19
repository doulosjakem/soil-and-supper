package com.soilandsupper.shared.domain.model

data class PlantIdentification(
    val cropName: String,
    val variety: String = "",
    val confidence: Float,
    val metadata: Map<String, String> = emptyMap()
)

