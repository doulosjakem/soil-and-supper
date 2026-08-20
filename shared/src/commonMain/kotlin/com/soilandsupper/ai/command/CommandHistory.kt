package com.soilandsupper.ai.command

import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed

data class HistoryEntry(
    val command: GardenCommand,
    val timestamp: Long
)

interface CommandHistory {
    suspend fun record(command: GardenCommand)
    suspend fun undoLast(repository: GardenRepository): CommandResult?
    fun clear()
}
