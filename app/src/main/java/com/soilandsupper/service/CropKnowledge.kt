package com.soilandsupper.service

import com.soilandsupper.domain.model.Crop
import com.soilandsupper.domain.model.PlantingWindow
import com.soilandsupper.domain.model.Variety

object CropKnowledge {

    private val catalog = listOf(
        Crop(
            id = "carrot",
            name = "Carrot",
            varieties = listOf(
                Variety(name = "Nantes", cropName = "Carrot", daysToMaturity = 60, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 5, frostTolerant = true, notes = "Can be sown as soon as soil can be worked"),
                    PlantingWindow(name = "Fall", startMonth = 7, endMonth = 9, frostTolerant = true, notes = "Sow 8-10 weeks before first frost")
                )),
                Variety(name = "Napoli", cropName = "Carrot", daysToMaturity = 70, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 5, frostTolerant = true),
                    PlantingWindow(name = "Fall", startMonth = 7, endMonth = 9, frostTolerant = true)
                )),
                Variety(name = "Danvers", cropName = "Carrot", daysToMaturity = 75, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 5, frostTolerant = true),
                    PlantingWindow(name = "Fall", startMonth = 7, endMonth = 9, frostTolerant = true)
                ))
            ),
            family = "Apiaceae",
            frostTolerant = true,
            killedByFrost = false,
            transplantSensitive = true
        ),
        Crop(
            id = "radish",
            name = "Radish",
            varieties = listOf(
                Variety(name = "Cherry Belle", cropName = "Radish", daysToMaturity = 22, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 5, frostTolerant = true),
                    PlantingWindow(name = "Fall", startMonth = 8, endMonth = 9, frostTolerant = true)
                )),
                Variety(name = "French Breakfast", cropName = "Radish", daysToMaturity = 25, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 5, frostTolerant = true),
                    PlantingWindow(name = "Fall", startMonth = 8, endMonth = 9, frostTolerant = true)
                ))
            ),
            family = "Brassicaceae",
            frostTolerant = true,
            killedByFrost = false,
            transplantSensitive = true
        ),
        Crop(
            id = "lettuce",
            name = "Lettuce",
            varieties = listOf(
                Variety(name = "Romaine", cropName = "Lettuce", daysToMaturity = 70, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 5, frostTolerant = true),
                    PlantingWindow(name = "Summer", startMonth = 6, endMonth = 8, frostTolerant = false, notes = "Heat-sensitive; provide afternoon shade"),
                    PlantingWindow(name = "Fall", startMonth = 8, endMonth = 10, frostTolerant = true)
                )),
                Variety(name = "Butterhead", cropName = "Lettuce", daysToMaturity = 60, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 5, frostTolerant = true),
                    PlantingWindow(name = "Fall", startMonth = 8, endMonth = 10, frostTolerant = true)
                )),
                Variety(name = "Salanova", cropName = "Lettuce", daysToMaturity = 45, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 5, frostTolerant = true),
                    PlantingWindow(name = "Fall", startMonth = 8, endMonth = 10, frostTolerant = true)
                ))
            ),
            family = "Asteraceae",
            frostTolerant = true,
            killedByFrost = false,
            transplantSensitive = false
        ),
        Crop(
            id = "spinach",
            name = "Spinach",
            varieties = listOf(
                Variety(name = "Bloomsdale", cropName = "Spinach", daysToMaturity = 40, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 5, frostTolerant = true),
                    PlantingWindow(name = "Fall", startMonth = 8, endMonth = 10, frostTolerant = true),
                    PlantingWindow(name = "Overwinter", startMonth = 9, endMonth = 11, frostTolerant = true, notes = "Sow late for early spring harvest")
                )),
                Variety(name = "Space", cropName = "Spinach", daysToMaturity = 45, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 5, frostTolerant = true),
                    PlantingWindow(name = "Fall", startMonth = 8, endMonth = 10, frostTolerant = true)
                ))
            ),
            family = "Amaranthaceae",
            frostTolerant = true,
            killedByFrost = false,
            transplantSensitive = true
        ),
        Crop(
            id = "bush-bean",
            name = "Bush Bean",
            varieties = listOf(
                Variety(name = "Blue Lake 274", cropName = "Bush Bean", daysToMaturity = 55, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 5, endMonth = 6, frostTolerant = false, notes = "Sow after last frost"),
                    PlantingWindow(name = "Summer", startMonth = 7, endMonth = 8, frostTolerant = false)
                )),
                Variety(name = "Provider", cropName = "Bush Bean", daysToMaturity = 50, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 5, endMonth = 6, frostTolerant = false, notes = "Sow after last frost"),
                    PlantingWindow(name = "Summer", startMonth = 7, endMonth = 8, frostTolerant = false)
                ))
            ),
            family = "Fabaceae",
            frostTolerant = false,
            killedByFrost = true,
            transplantSensitive = true
        ),
        Crop(
            id = "broccoli",
            name = "Broccoli",
            varieties = listOf(
                Variety(name = "Waltham 26", cropName = "Broccoli", daysToMaturity = 70, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 4, frostTolerant = true, notes = "Transplant after last frost"),
                    PlantingWindow(name = "Fall", startMonth = 7, endMonth = 8, frostTolerant = true, notes = "Sow midsummer for fall harvest")
                )),
                Variety(name = "Di Cicco", cropName = "Broccoli", daysToMaturity = 60, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 4, frostTolerant = true),
                    PlantingWindow(name = "Fall", startMonth = 7, endMonth = 8, frostTolerant = true)
                ))
            ),
            family = "Brassicaceae",
            frostTolerant = true,
            killedByFrost = false,
            transplantSensitive = false
        ),
        Crop(
            id = "tomato",
            name = "Tomato",
            varieties = listOf(
                Variety(name = "San Marzano", cropName = "Tomato", daysToMaturity = 80, plantingWindows = listOf(
                    PlantingWindow(name = "Summer", startMonth = 5, endMonth = 6, frostTolerant = false, notes = "Transplant after last frost")
                )),
                Variety(name = "Roma", cropName = "Tomato", daysToMaturity = 75, plantingWindows = listOf(
                    PlantingWindow(name = "Summer", startMonth = 5, endMonth = 6, frostTolerant = false, notes = "Transplant after last frost")
                )),
                Variety(name = "Cherry", cropName = "Tomato", daysToMaturity = 65, plantingWindows = listOf(
                    PlantingWindow(name = "Summer", startMonth = 5, endMonth = 6, frostTolerant = false, notes = "Transplant after last frost")
                ))
            ),
            family = "Solanaceae",
            frostTolerant = false,
            killedByFrost = true,
            transplantSensitive = false
        ),
        Crop(
            id = "cucumber",
            name = "Cucumber",
            varieties = listOf(
                Variety(name = "Marketmore 76", cropName = "Cucumber", daysToMaturity = 60, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 5, endMonth = 6, frostTolerant = false, notes = "Sow after last frost"),
                    PlantingWindow(name = "Summer", startMonth = 7, endMonth = 7, frostTolerant = false)
                )),
                Variety(name = "Straight Eight", cropName = "Cucumber", daysToMaturity = 58, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 5, endMonth = 6, frostTolerant = false, notes = "Sow after last frost"),
                    PlantingWindow(name = "Summer", startMonth = 7, endMonth = 7, frostTolerant = false)
                ))
            ),
            family = "Cucurbitaceae",
            frostTolerant = false,
            killedByFrost = true,
            transplantSensitive = true
        ),
        Crop(
            id = "potato",
            name = "Potato",
            varieties = listOf(
                Variety(name = "Yukon Gold", cropName = "Potato", daysToMaturity = 70, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 4, frostTolerant = false, notes = "Plant seed potatoes as soon as soil can be worked")
                )),
                Variety(name = "Russet", cropName = "Potato", daysToMaturity = 90, plantingWindows = listOf(
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 4, frostTolerant = false, notes = "Plant seed potatoes as soon as soil can be worked")
                ))
            ),
            family = "Solanaceae",
            frostTolerant = false,
            killedByFrost = false,
            transplantSensitive = false
        ),
        Crop(
            id = "garlic",
            name = "Garlic",
            varieties = listOf(
                Variety(name = "Hardneck", cropName = "Garlic", daysToMaturity = 240, plantingWindows = listOf(
                    PlantingWindow(name = "Fall", startMonth = 10, endMonth = 11, frostTolerant = true, notes = "Plant cloves 4-6 weeks before first frost")
                )),
                Variety(name = "Softneck", cropName = "Garlic", daysToMaturity = 180, plantingWindows = listOf(
                    PlantingWindow(name = "Fall", startMonth = 10, endMonth = 11, frostTolerant = true, notes = "Plant cloves 4-6 weeks before first frost"),
                    PlantingWindow(name = "Spring", startMonth = 3, endMonth = 4, frostTolerant = true, notes = "Plant as soon as soil thaws")
                ))
            ),
            family = "Amaryllidaceae",
            frostTolerant = true,
            killedByFrost = false,
            transplantSensitive = false
        )
    )

    fun crop(name: String): Crop? =
        catalog.firstOrNull { it.name.equals(name, ignoreCase = true) }

    fun varieties(cropName: String): List<Variety> {
        val crop = catalog.firstOrNull { it.name.equals(cropName, ignoreCase = true) } ?: return emptyList()
        return crop.varieties
    }

    fun variety(varietyName: String, cropName: String): Variety? {
        val crop = catalog.firstOrNull { it.name.equals(cropName, ignoreCase = true) } ?: return null
        return crop.variety(name = varietyName)
    }

    fun plantingWindows(cropName: String, variety: String? = null): List<PlantingWindow> {
        val crop = catalog.firstOrNull { it.name.equals(cropName, ignoreCase = true) } ?: return emptyList()
        return if (variety != null) {
            crop.variety(name = variety)?.plantingWindows ?: emptyList()
        } else {
            crop.varieties.flatMap { it.plantingWindows }.distinctBy { it.name }.sortedBy { it.startMonth }
        }
    }

    fun maturityDays(cropName: String, variety: String? = null): Int? {
        val crop = catalog.firstOrNull { it.name.equals(cropName, ignoreCase = true) } ?: return null
        return if (variety != null) {
            crop.variety(name = variety)?.daysToMaturity
        } else {
            crop.defaultVariety?.daysToMaturity
        }
    }

    fun characteristics(cropName: String): com.soilandsupper.domain.model.CropCharacteristics? {
        val crop = catalog.firstOrNull { it.name.equals(cropName, ignoreCase = true) } ?: return null
        return com.soilandsupper.domain.model.CropCharacteristics(
            frostTolerant = crop.frostTolerant,
            killedByFrost = crop.killedByFrost,
            transplantSensitive = crop.transplantSensitive,
            minimumGerminationTempCelsius = null,
            preferredTempRangeCelsius = null
        )
    }

    fun allCrops(): List<Crop> = catalog
}
