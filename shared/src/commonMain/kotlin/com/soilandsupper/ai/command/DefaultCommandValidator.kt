package com.soilandsupper.ai.command

import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.OccupancyStatus
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed

class DefaultCommandValidator : CommandValidator {
    override suspend fun validate(
        command: GardenCommand,
        currentSpaces: List<GrowingSpace>,
        currentOccupancies: List<Occupancy>,
        currentSeeds: List<Seed>,
        currentDesires: List<Desire>,
        currentPlants: List<Plant>
    ): CommandResult {
        return when (command) {
            is GardenCommand.AddGrowingSpace -> validateAddGrowingSpace(command)
            is GardenCommand.UpdateGrowingSpace -> validateUpdateGrowingSpace(command, currentSpaces)
            is GardenCommand.RemoveGrowingSpace -> validateRemoveGrowingSpace(command, currentSpaces, currentOccupancies)
            is GardenCommand.PlantCrop -> validatePlantCrop(command, currentSpaces, currentOccupancies)
            is GardenCommand.HarvestCrop -> validateHarvestCrop(command, currentOccupancies)
            is GardenCommand.EndCrop -> validateEndCrop(command, currentOccupancies)
            is GardenCommand.RecordObservation -> validateRecordObservation(command, currentPlants, currentSpaces)
            is GardenCommand.AddSeed -> validateAddSeed(command)
            is GardenCommand.AddDesire -> validateAddDesire(command)
            is GardenCommand.FulfillDesire -> validateFulfillDesire(command, currentDesires)
            is GardenCommand.CancelDesire -> validateCancelDesire(command, currentDesires)
            is GardenCommand.RecordPlant -> validateRecordPlant(command)
            is GardenCommand.UpdatePlant -> validateUpdatePlant(command, currentPlants)
            is GardenCommand.RemovePlant -> validateRemovePlant(command, currentPlants)
        }
    }

    private fun validateAddGrowingSpace(command: GardenCommand.AddGrowingSpace): CommandResult {
        if (command.name.isBlank()) {
            return CommandResult.ValidationError(command, "Growing space name must not be blank")
        }
        return CommandResult.Success(command)
    }

    private fun validateUpdateGrowingSpace(
        command: GardenCommand.UpdateGrowingSpace,
        currentSpaces: List<GrowingSpace>
    ): CommandResult {
        val space = currentSpaces.firstOrNull { it.id == command.spaceId }
        if (space == null) {
            return CommandResult.NotFound(command, "GrowingSpace", command.spaceId)
        }
        if (command.name.isBlank()) {
            return CommandResult.ValidationError(command, "Growing space name must not be blank")
        }
        return CommandResult.Success(command)
    }

    private fun validateRemoveGrowingSpace(
        command: GardenCommand.RemoveGrowingSpace,
        currentSpaces: List<GrowingSpace>,
        currentOccupancies: List<Occupancy>
    ): CommandResult {
        val space = currentSpaces.firstOrNull { it.id == command.spaceId }
        if (space == null) {
            return CommandResult.NotFound(command, "GrowingSpace", command.spaceId)
        }
        val activeOccupancy = currentOccupancies.firstOrNull {
            it.growingSpaceId == command.spaceId && it.status == OccupancyStatus.ACTIVE.name
        }
        if (activeOccupancy != null) {
            return CommandResult.Conflict(
                command,
                "Cannot remove space with active occupancy: ${activeOccupancy.cropName}"
            )
        }
        return CommandResult.Success(command)
    }

    private fun validatePlantCrop(
        command: GardenCommand.PlantCrop,
        currentSpaces: List<GrowingSpace>,
        currentOccupancies: List<Occupancy>
    ): CommandResult {
        if (command.cropName.isBlank()) {
            return CommandResult.ValidationError(command, "Crop name must not be blank")
        }
        val space = currentSpaces.firstOrNull { it.id == command.growingSpaceId }
        if (space == null) {
            return CommandResult.NotFound(command, "GrowingSpace", command.growingSpaceId)
        }
        val activeOccupancy = currentOccupancies.firstOrNull {
            it.growingSpaceId == command.growingSpaceId && it.status == OccupancyStatus.ACTIVE.name
        }
        if (activeOccupancy != null) {
            return CommandResult.Conflict(
                command,
                "Space is already occupied by ${activeOccupancy.cropName}"
            )
        }
        if (command.expectedHarvestDate != null && command.expectedHarvestDate < command.startDate) {
            return CommandResult.ValidationError(command, "Expected harvest date cannot be before planting date")
        }
        if (command.expectedReleaseDate != null && command.expectedReleaseDate < command.startDate) {
            return CommandResult.ValidationError(command, "Expected release date cannot be before planting date")
        }
        return CommandResult.Success(command)
    }

    private fun validateHarvestCrop(
        command: GardenCommand.HarvestCrop,
        currentOccupancies: List<Occupancy>
    ): CommandResult {
        val occupancy = currentOccupancies.firstOrNull { it.id == command.occupancyId }
        if (occupancy == null) {
            return CommandResult.NotFound(command, "Occupancy", command.occupancyId)
        }
        if (occupancy.status != OccupancyStatus.ACTIVE.name) {
            return CommandResult.Conflict(command, "Cannot harvest from a non-active occupancy")
        }
        if (command.quantity <= 0) {
            return CommandResult.ValidationError(command, "Harvest quantity must be greater than zero")
        }
        if (command.unit.isBlank()) {
            return CommandResult.ValidationError(command, "Harvest unit must not be blank")
        }
        return CommandResult.Success(command)
    }

    private fun validateEndCrop(
        command: GardenCommand.EndCrop,
        currentOccupancies: List<Occupancy>
    ): CommandResult {
        val occupancy = currentOccupancies.firstOrNull { it.id == command.occupancyId }
        if (occupancy == null) {
            return CommandResult.NotFound(command, "Occupancy", command.occupancyId)
        }
        if (occupancy.status != OccupancyStatus.ACTIVE.name) {
            return CommandResult.Conflict(command, "Cannot end a non-active occupancy")
        }
        if (command.endDate < occupancy.startDate) {
            return CommandResult.ValidationError(command, "End date cannot be before planting date")
        }
        return CommandResult.Success(command)
    }

    private fun validateRecordObservation(
        command: GardenCommand.RecordObservation,
        currentPlants: List<Plant>,
        currentSpaces: List<GrowingSpace>
    ): CommandResult {
        if (command.text.isBlank()) {
            return CommandResult.ValidationError(command, "Observation text must not be blank")
        }
        if (command.plantId != null) {
            val plant = currentPlants.firstOrNull { it.id == command.plantId }
            if (plant == null) {
                return CommandResult.NotFound(command, "Plant", command.plantId)
            }
        }
        if (command.growingSpaceId != null) {
            val space = currentSpaces.firstOrNull { it.id == command.growingSpaceId }
            if (space == null) {
                return CommandResult.NotFound(command, "GrowingSpace", command.growingSpaceId)
            }
        }
        return CommandResult.Success(command)
    }

    private fun validateAddSeed(command: GardenCommand.AddSeed): CommandResult {
        if (command.cropName.isBlank()) {
            return CommandResult.ValidationError(command, "Crop name must not be blank")
        }
        return CommandResult.Success(command)
    }

    private fun validateAddDesire(command: GardenCommand.AddDesire): CommandResult {
        if (command.cropName.isBlank()) {
            return CommandResult.ValidationError(command, "Crop name must not be blank")
        }
        return CommandResult.Success(command)
    }

    private fun validateFulfillDesire(
        command: GardenCommand.FulfillDesire,
        currentDesires: List<Desire>
    ): CommandResult {
        val desire = currentDesires.firstOrNull { it.id == command.desireId }
        if (desire == null) {
            return CommandResult.NotFound(command, "Desire", command.desireId)
        }
        if (desire.isFulfilled) {
            return CommandResult.Conflict(command, "Desire is already fulfilled")
        }
        return CommandResult.Success(command)
    }

    private fun validateCancelDesire(
        command: GardenCommand.CancelDesire,
        currentDesires: List<Desire>
    ): CommandResult {
        val desire = currentDesires.firstOrNull { it.id == command.desireId }
        if (desire == null) {
            return CommandResult.NotFound(command, "Desire", command.desireId)
        }
        if (desire.isCancelled) {
            return CommandResult.Conflict(command, "Desire is already cancelled")
        }
        return CommandResult.Success(command)
    }

    private fun validateRecordPlant(command: GardenCommand.RecordPlant): CommandResult {
        if (command.name.isBlank()) {
            return CommandResult.ValidationError(command, "Plant name must not be blank")
        }
        return CommandResult.Success(command)
    }

    private fun validateUpdatePlant(
        command: GardenCommand.UpdatePlant,
        currentPlants: List<Plant>
    ): CommandResult {
        val plant = currentPlants.firstOrNull { it.id == command.plantId }
        if (plant == null) {
            return CommandResult.NotFound(command, "Plant", command.plantId)
        }
        if (command.name.isBlank()) {
            return CommandResult.ValidationError(command, "Plant name must not be blank")
        }
        return CommandResult.Success(command)
    }

    private fun validateRemovePlant(
        command: GardenCommand.RemovePlant,
        currentPlants: List<Plant>
    ): CommandResult {
        val plant = currentPlants.firstOrNull { it.id == command.plantId }
        if (plant == null) {
            return CommandResult.NotFound(command, "Plant", command.plantId)
        }
        return CommandResult.Success(command)
    }
}
