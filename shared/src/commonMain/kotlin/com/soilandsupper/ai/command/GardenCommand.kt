package com.soilandsupper.ai.command

import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Harvest
import com.soilandsupper.shared.domain.model.JournalEntry
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed

sealed interface GardenCommand {
    val timestamp: Long

    data class AddGrowingSpace(
        val name: String,
        val notes: String? = null,
        val spaceType: String? = null,
        val width: Double? = null,
        val length: Double? = null,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class UpdateGrowingSpace(
        val spaceId: Long,
        val name: String,
        val notes: String? = null,
        val spaceType: String? = null,
        val width: Double? = null,
        val length: Double? = null,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class RemoveGrowingSpace(
        val spaceId: Long,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class PlantCrop(
        val cropName: String,
        val variety: String? = null,
        val growingSpaceId: Long,
        val startDate: Long,
        val expectedHarvestDate: Long? = null,
        val expectedReleaseDate: Long? = null,
        val notes: String? = null,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class HarvestCrop(
        val occupancyId: Long,
        val quantity: Double,
        val unit: String,
        val date: Long,
        val notes: String = "",
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class EndCrop(
        val occupancyId: Long,
        val endDate: Long,
        val notes: String? = null,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class RecordObservation(
        val text: String,
        val date: Long,
        val plantId: Long? = null,
        val growingSpaceId: Long? = null,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class AddSeed(
        val cropName: String,
        val variety: String? = null,
        val state: String = com.soilandsupper.shared.domain.model.SeedState.OWN.name,
        val notes: String? = null,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class AddDesire(
        val cropName: String,
        val variety: String? = null,
        val notes: String? = null,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class FulfillDesire(
        val desireId: Long,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class CancelDesire(
        val desireId: Long,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class RecordPlant(
        val name: String,
        val variety: String = "",
        val plantingDate: Long,
        val location: String = "",
        val notes: String = "",
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class UpdatePlant(
        val plantId: Long,
        val name: String,
        val variety: String,
        val plantingDate: Long,
        val location: String,
        val notes: String,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand

    data class RemovePlant(
        val plantId: Long,
        override val timestamp: Long = System.currentTimeMillis()
    ) : GardenCommand
}
