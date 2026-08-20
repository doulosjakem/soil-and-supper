package com.soilandsupper.ai.command

import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.OccupancyStatus
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed

interface CommandValidator {
    suspend fun validate(
        command: GardenCommand,
        currentSpaces: List<GrowingSpace>,
        currentOccupancies: List<Occupancy>,
        currentSeeds: List<Seed> = emptyList(),
        currentDesires: List<Desire> = emptyList(),
        currentPlants: List<Plant> = emptyList()
    ): CommandResult
}
