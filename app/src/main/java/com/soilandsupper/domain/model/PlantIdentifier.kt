package com.soilandsupper.domain.model

interface PlantIdentifier {
    suspend fun identify(image: android.graphics.Bitmap): PlantIdentification
}
