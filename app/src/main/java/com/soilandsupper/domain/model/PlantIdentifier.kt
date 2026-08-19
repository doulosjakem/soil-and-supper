package com.soilandsupper.domain.model

import com.soilandsupper.shared.domain.model.PlantIdentification

interface PlantIdentifier {
    suspend fun identify(image: android.graphics.Bitmap): PlantIdentification
}
