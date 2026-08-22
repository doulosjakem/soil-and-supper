package com.soilandsupper.ai.command

import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.repository.PlantRepository
import com.soilandsupper.service.GardenService
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Harvest
import com.soilandsupper.shared.domain.model.JournalEntry
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed
import kotlinx.coroutines.flow.first

class DefaultCommandExecutor(
    private val validator: CommandValidator = DefaultCommandValidator(),
    private val history: CommandHistory = InMemoryCommandHistory()
) : CommandExecutor {

    override suspend fun execute(
        command: GardenCommand,
        repository: GardenRepository
    ): CommandResult {
        val spaces = repository.getAllGrowingSpaces().first()

        val occupancies = repository.getAllOccupancies().first()

        val seeds = repository.getAllSeeds().first()

        val desires = repository.getAllDesires().first()

        val plantRepository = repository as? PlantRepository
        val plants = plantRepository?.getAllPlants()?.first() ?: emptyList()

        val validation = validator.validate(
            command = command,
            currentSpaces = spaces,
            currentOccupancies = occupancies,
            currentSeeds = seeds,
            currentDesires = desires,
            currentPlants = plants
        )

        if (validation !is CommandResult.Success) {
            return validation
        }

        var createdHarvestId: Long? = null
        var createdJournalEntryId: Long? = null

        val previousState = when (command) {
            is GardenCommand.UpdateGrowingSpace -> {
                val existing = repository.getGrowingSpaceById(command.spaceId)
                existing?.let {
                    mapOf(
                        "name" to it.name,
                        "notes" to it.notes,
                        "spaceType" to it.spaceType,
                        "width" to it.width,
                        "length" to it.length
                    )
                }
            }
            is GardenCommand.UpdatePlant -> {
                val existing = (repository as? PlantRepository)?.getPlantById(command.plantId)
                existing?.let {
                    mapOf(
                        "name" to it.name,
                        "variety" to it.variety,
                        "plantingDate" to it.plantingDate,
                        "location" to it.location,
                        "notes" to it.notes
                    )
                }
            }
            else -> null
        }

        val result = when (command) {
            is GardenCommand.AddGrowingSpace -> executeAddGrowingSpace(command, repository)
            is GardenCommand.UpdateGrowingSpace -> executeUpdateGrowingSpace(command, repository)
            is GardenCommand.RemoveGrowingSpace -> executeRemoveGrowingSpace(command, repository)
            is GardenCommand.PlantCrop -> executePlantCrop(command, repository)
            is GardenCommand.HarvestCrop -> {
                val occupancy = repository.getOccupancyById(command.occupancyId)
                    ?: return CommandResult.NotFound(command, "Occupancy", command.occupancyId)

                val harvest = Harvest(
                    plantId = occupancy.plantId,
                    cropName = occupancy.cropName,
                    quantity = command.quantity,
                    unit = command.unit,
                    date = command.date,
                    notes = command.notes
                )

                val plantRepo = repository as? PlantRepository
                createdHarvestId = plantRepo?.insertHarvest(harvest)
                CommandResult.Success(command, "Harvested ${command.quantity} ${command.unit} of ${occupancy.cropName}")
            }
            is GardenCommand.EndCrop -> executeEndCrop(command, repository)
            is GardenCommand.RecordObservation -> {
                val entry = JournalEntry(
                    plantId = command.plantId,
                    date = command.date,
                    text = command.text
                )
                val plantRepo = repository as? PlantRepository
                createdJournalEntryId = plantRepo?.insertJournalEntry(entry)
                CommandResult.Success(command, "Observation recorded")
            }
            is GardenCommand.AddSeed -> executeAddSeed(command, repository)
            is GardenCommand.AddDesire -> executeAddDesire(command, repository)
            is GardenCommand.FulfillDesire -> executeFulfillDesire(command, repository)
            is GardenCommand.CancelDesire -> executeCancelDesire(command, repository)
            is GardenCommand.RecordPlant -> executeRecordPlant(command, repository)
            is GardenCommand.UpdatePlant -> executeUpdatePlant(command, repository)
            is GardenCommand.RemovePlant -> executeRemovePlant(command, repository)
        }

        if (result is CommandResult.Success) {
            history.record(
                HistoryEntry(
                    command = command,
                    timestamp = System.currentTimeMillis(),
                    previousState = when (command) {
                        is GardenCommand.HarvestCrop -> mapOf("harvestId" to createdHarvestId)
                        is GardenCommand.RecordObservation -> mapOf("journalEntryId" to createdJournalEntryId)
                        else -> previousState
                    }
                )
            )
        }

        return result
    }

    private suspend fun executeAddGrowingSpace(
        command: GardenCommand.AddGrowingSpace,
        repository: GardenRepository
    ): CommandResult {
        val space = GardenService.addGrowingSpace(
            name = command.name,
            notes = command.notes,
            spaceType = command.spaceType,
            width = command.width,
            length = command.length
        )
        repository.insertGrowingSpace(space)
        return CommandResult.Success(command, "Growing space added: ${space.name}")
    }

    private suspend fun executeUpdateGrowingSpace(
        command: GardenCommand.UpdateGrowingSpace,
        repository: GardenRepository
    ): CommandResult {
        val existing = repository.getGrowingSpaceById(command.spaceId)
            ?: return CommandResult.NotFound(command, "GrowingSpace", command.spaceId)
        val updated = GardenService.updateGrowingSpace(
            space = existing,
            name = command.name,
            notes = command.notes,
            spaceType = command.spaceType,
            width = command.width,
            length = command.length
        )
        repository.updateGrowingSpace(updated)
        return CommandResult.Success(command, "Growing space updated: ${updated.name}")
    }

    private suspend fun executeRemoveGrowingSpace(
        command: GardenCommand.RemoveGrowingSpace,
        repository: GardenRepository
    ): CommandResult {
        val space = repository.getGrowingSpaceById(command.spaceId)
            ?: return CommandResult.NotFound(command, "GrowingSpace", command.spaceId)
        repository.deleteGrowingSpace(space)
        return CommandResult.Success(command, "Growing space removed")
    }

    private suspend fun executePlantCrop(
        command: GardenCommand.PlantCrop,
        repository: GardenRepository
    ): CommandResult {
        val space = repository.getGrowingSpaceById(command.growingSpaceId)
            ?: return CommandResult.NotFound(command, "GrowingSpace", command.growingSpaceId)
        val occupancy = GardenService.recordPlanting(
            cropName = command.cropName,
            variety = command.variety,
            startDate = command.startDate,
            growingSpace = space,
            expectedHarvestDate = command.expectedHarvestDate,
            expectedReleaseDate = command.expectedReleaseDate,
            notes = command.notes
        )
        repository.insertOccupancy(occupancy)
        return CommandResult.Success(command, "Planted ${command.cropName} in ${space.name}")
    }

    private suspend fun executeEndCrop(
        command: GardenCommand.EndCrop,
        repository: GardenRepository
    ): CommandResult {
        val existing = repository.getOccupancyById(command.occupancyId)
            ?: return CommandResult.NotFound(command, "Occupancy", command.occupancyId)
        val completed = GardenService.completeOccupancy(existing, command.endDate)
        repository.updateOccupancy(completed)
        return CommandResult.Success(command, "Ended ${existing.cropName}")
    }

    private suspend fun executeAddSeed(
        command: GardenCommand.AddSeed,
        repository: GardenRepository
    ): CommandResult {
        val seed = GardenService.addSeed(
            cropName = command.cropName,
            variety = command.variety,
            state = com.soilandsupper.shared.domain.model.SeedState.valueOf(command.state),
            notes = command.notes
        )
        repository.insertSeed(seed)
        return CommandResult.Success(command, "Seed added: ${seed.displayName}")
    }

    private suspend fun executeAddDesire(
        command: GardenCommand.AddDesire,
        repository: GardenRepository
    ): CommandResult {
        val desire = GardenService.createDesire(
            cropName = command.cropName,
            variety = command.variety,
            notes = command.notes
        )
        repository.insertDesire(desire)
        return CommandResult.Success(command, "Desire added: ${desire.displayName}")
    }

    private suspend fun executeFulfillDesire(
        command: GardenCommand.FulfillDesire,
        repository: GardenRepository
    ): CommandResult {
        val existing = repository.getDesireById(command.desireId)
            ?: return CommandResult.NotFound(command, "Desire", command.desireId)
        val updated = GardenService.fulfillDesire(existing)
        repository.updateDesire(updated)
        return CommandResult.Success(command, "Desire fulfilled: ${updated.displayName}")
    }

    private suspend fun executeCancelDesire(
        command: GardenCommand.CancelDesire,
        repository: GardenRepository
    ): CommandResult {
        val existing = repository.getDesireById(command.desireId)
            ?: return CommandResult.NotFound(command, "Desire", command.desireId)
        val updated = GardenService.cancelDesire(existing)
        repository.updateDesire(updated)
        return CommandResult.Success(command, "Desire cancelled: ${updated.displayName}")
    }

    private suspend fun executeRecordPlant(
        command: GardenCommand.RecordPlant,
        repository: GardenRepository
    ): CommandResult {
        val plant = Plant(
            name = command.name,
            variety = command.variety,
            plantingDate = command.plantingDate,
            location = command.location,
            notes = command.notes
        )
        val plantRepo = repository as? PlantRepository
        if (plantRepo != null) {
            plantRepo.insertPlant(plant)
        }
        return CommandResult.Success(command, "Plant recorded: ${plant.name}")
    }

    private suspend fun executeUpdatePlant(
        command: GardenCommand.UpdatePlant,
        repository: GardenRepository
    ): CommandResult {
        val existing = (repository as? PlantRepository)
            ?.getPlantById(command.plantId)
            ?: return CommandResult.NotFound(command, "Plant", command.plantId)
        val updated = existing.copy(
            name = command.name,
            variety = command.variety,
            plantingDate = command.plantingDate,
            location = command.location,
            notes = command.notes,
            updatedAt = System.currentTimeMillis()
        )
        val plantRepo = repository as? PlantRepository
        if (plantRepo != null) {
            plantRepo.updatePlant(updated)
        }
        return CommandResult.Success(command, "Plant updated: ${updated.name}")
    }

    private suspend fun executeRemovePlant(
        command: GardenCommand.RemovePlant,
        repository: GardenRepository
    ): CommandResult {
        val plantRepo = repository as? PlantRepository
        if (plantRepo != null) {
            val existing = plantRepo.getPlantById(command.plantId)
            if (existing != null) {
                plantRepo.deletePlant(existing)
            }
        }
        return CommandResult.Success(command, "Plant removed")
    }
}
