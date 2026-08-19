package com.soilandsupper.domain.model

import com.soilandsupper.shared.domain.model.PlantIdentification

class MockPlantIdentifier : PlantIdentifier {
    override suspend fun identify(image: android.graphics.Bitmap): PlantIdentification {
        kotlinx.coroutines.delay(500)
        return PlantIdentification(
            cropName = "Tomato",
            variety = "Stupice",
            confidence = 0.87f
        )
    }
}
