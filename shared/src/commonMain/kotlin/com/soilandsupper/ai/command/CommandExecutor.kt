package com.soilandsupper.ai.command

import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.service.GardenService

interface CommandExecutor {
    suspend fun execute(
        command: GardenCommand,
        repository: GardenRepository
    ): CommandResult
}
