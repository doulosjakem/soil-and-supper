package com.soilandsupper.domain.model

data class Crop(
    val id: String,
    val name: String,
    val varieties: List<Variety>,
    val family: String?,
    val frostTolerant: Boolean,
    val killedByFrost: Boolean,
    val transplantSensitive: Boolean
) {
    val defaultVariety: Variety?
        get() = varieties.firstOrNull()

    fun variety(name: String): Variety? =
        varieties.firstOrNull { it.name.equals(name, ignoreCase = true) }
}

data class Variety(
    val id: String = "",
    val name: String,
    val cropName: String,
    val daysToMaturity: Int? = null,
    val plantingWindows: List<PlantingWindow> = emptyList()
)

data class PlantingWindow(
    val name: String,
    val startMonth: Int,
    val endMonth: Int,
    val frostTolerant: Boolean = false,
    val notes: String? = null
)

data class CropCharacteristics(
    val frostTolerant: Boolean,
    val killedByFrost: Boolean,
    val transplantSensitive: Boolean,
    val minimumGerminationTempCelsius: Int? = null,
    val preferredTempRangeCelsius: Pair<Int, Int>? = null
)
