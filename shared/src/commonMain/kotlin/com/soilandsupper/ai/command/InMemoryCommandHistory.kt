package com.soilandsupper.ai.command

import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.repository.PlantRepository
import com.soilandsupper.service.GardenService
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Harvest
import com.soilandsupper.shared.domain.model.JournalEntry
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.OccupancyStatus
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed
import kotlinx.coroutines.flow.first

class InMemoryCommandHistory : CommandHistory {
    val size: Int
        get() = entries.size

    private val entries = mutableListOf<HistoryEntry>()

    override suspend fun record(entry: HistoryEntry) {
        entries.add(entry)
    }

    override suspend fun undoLast(repository: GardenRepository): CommandResult? {
        if (entries.isEmpty()) return null

        val lastEntry = entries.removeAt(entries.size - 1)
        val command = lastEntry.command

        return when (command) {
            is GardenCommand.AddGrowingSpace -> {
                val space = repository.getAllGrowingSpaces().first().firstOrNull { it.name == command.name && it.notes == command.notes }
                    ?: return CommandResult.NotFound(command, "GrowingSpace", -1)
                repository.deleteGrowingSpace(space)
                CommandResult.Success(command, "Undone: growing space removed")
            }
            is GardenCommand.UpdateGrowingSpace -> {
                val current = repository.getGrowingSpaceById(command.spaceId)
                    ?: return CommandResult.NotFound(command, "GrowingSpace", command.spaceId)
                val restored = current.copy(
                    name = lastEntry.previousState?.get("name") as? String ?: command.name,
                    notes = lastEntry.previousState?.get("notes") as? String?,
                    spaceType = lastEntry.previousState?.get("spaceType") as? String?,
                    width = lastEntry.previousState?.get("width") as? Double?,
                    length = lastEntry.previousState?.get("length") as? Double?
                )
                repository.updateGrowingSpace(restored)
                CommandResult.Success(command, "Undone: growing space restored")
            }
            is GardenCommand.RemoveGrowingSpace -> {
                val restored = GrowingSpace(
                    id = command.spaceId,
                    name = "",
                    notes = null,
                    spaceType = null,
                    width = null,
                    length = null
                )
                repository.insertGrowingSpace(restored)
                CommandResult.Success(command, "Undone: growing space restored")
            }
            is GardenCommand.PlantCrop -> {
                val occupancy = repository.getAllOccupancies().first().firstOrNull { it.growingSpaceId == command.growingSpaceId && it.cropName == command.cropName }
                    ?: return CommandResult.NotFound(command, "Occupancy", -1)
                val completed = GardenService.completeOccupancy(occupancy, command.startDate)
                repository.updateOccupancy(completed)
                CommandResult.Success(command, "Undone: planting ended")
            }
            is GardenCommand.HarvestCrop -> {
                val plantRepo = repository as? PlantRepository
                    ?: return CommandResult.NotFound(command, "Harvest", -1)
                val harvestId = lastEntry.previousState?.get("harvestId") as? Long
                val harvest = plantRepo.getAllHarvests().first().firstOrNull { it.id == harvestId }
                    ?: return CommandResult.NotFound(command, "Harvest", harvestId ?: -1)
                plantRepo.deleteHarvest(harvest)
                CommandResult.Success(command, "Undone: harvest removed")
            }
            is GardenCommand.EndCrop -> {
                val occupancy = repository.getOccupancyById(command.occupancyId)
                    ?: return CommandResult.NotFound(command, "Occupancy", command.occupancyId)
                val restored = occupancy.copy(
                    endDate = null,
                    status = OccupancyStatus.ACTIVE.name,
                    updatedAt = System.currentTimeMillis()
                )
                repository.updateOccupancy(restored)
                CommandResult.Success(command, "Undone: crop reactivated")
            }
            is GardenCommand.RecordObservation -> {
                val plantRepo = repository as? PlantRepository
                    ?: return CommandResult.NotFound(command, "JournalEntry", -1)
                val entryId = lastEntry.previousState?.get("journalEntryId") as? Long
                val entry = plantRepo.getJournalEntriesForPlant(command.plantId ?: 0).first().firstOrNull { it.id == entryId }
                    ?: return CommandResult.NotFound(command, "JournalEntry", entryId ?: -1)
                plantRepo.deleteJournalEntry(entry)
                CommandResult.Success(command, "Undone: observation removed")
            }
            is GardenCommand.AddSeed -> {
                val seed = repository.getAllSeeds().first().firstOrNull { it.cropName == command.cropName && it.variety == command.variety }
                    ?: return CommandResult.NotFound(command, "Seed", -1)
                repository.deleteSeed(seed)
                CommandResult.Success(command, "Undone: seed removed")
            }
            is GardenCommand.AddDesire -> {
                val desire = repository.getAllDesires().first().firstOrNull { it.cropName == command.cropName && it.variety == command.variety }
                    ?: return CommandResult.NotFound(command, "Desire", -1)
                repository.deleteDesire(desire)
                CommandResult.Success(command, "Undone: desire removed")
            }
            is GardenCommand.FulfillDesire -> {
                val existing = repository.getDesireById(command.desireId)
                    ?: return CommandResult.NotFound(command, "Desire", command.desireId)
                val restored = existing.copy(
                    isFulfilled = false,
                    isCancelled = false,
                    isExpired = false,
                    updatedAt = System.currentTimeMillis()
                )
                repository.updateDesire(restored)
                CommandResult.Success(command, "Undone: desire unfulfilled")
            }
            is GardenCommand.CancelDesire -> {
                val existing = repository.getDesireById(command.desireId)
                    ?: return CommandResult.NotFound(command, "Desire", command.desireId)
                val restored = existing.copy(
                    isFulfilled = false,
                    isCancelled = false,
                    isExpired = false,
                    updatedAt = System.currentTimeMillis()
                )
                repository.updateDesire(restored)
                CommandResult.Success(command, "Undone: desire uncancelled")
            }
            is GardenCommand.RecordPlant -> {
                val plantRepo = repository as? PlantRepository
                val plant = (repository as? PlantRepository)?.getAllPlants()?.first()?.firstOrNull { it.name == command.name && it.plantingDate == command.plantingDate }
                    ?: return CommandResult.NotFound(command, "Plant", -1)
                if (plantRepo != null) {
                    plantRepo.deletePlant(plant)
                }
                CommandResult.Success(command, "Undone: plant removed")
            }
            is GardenCommand.UpdatePlant -> {
                val existing = (repository as? PlantRepository)
                    ?.getPlantById(command.plantId)
                    ?: return CommandResult.NotFound(command, "Plant", command.plantId)
                val restored = existing.copy(
                    name = lastEntry.previousState?.get("name") as? String ?: command.name,
                    variety = lastEntry.previousState?.get("variety") as? String ?: command.variety,
                    plantingDate = lastEntry.previousState?.get("plantingDate") as? Long ?: command.plantingDate,
                    location = lastEntry.previousState?.get("location") as? String ?: command.location,
                    notes = lastEntry.previousState?.get("notes") as? String ?: command.notes,
                    updatedAt = System.currentTimeMillis()
                )
                val plantRepo = repository as? PlantRepository
                if (plantRepo != null) {
                    plantRepo.updatePlant(restored)
                }
                CommandResult.Success(command, "Undone: plant restored")
            }
            is GardenCommand.RemovePlant -> {
                val restored = Plant(
                    id = command.plantId,
                    name = "",
                    variety = "",
                    plantingDate = System.currentTimeMillis(),
                    location = "",
                    notes = ""
                )
                val plantRepo = repository as? PlantRepository
                if (plantRepo != null) {
                    plantRepo.insertPlant(restored)
                }
                CommandResult.Success(command, "Undone: plant restored")
            }
        }
    }

    override fun clear() {
        entries.clear()
    }
}
