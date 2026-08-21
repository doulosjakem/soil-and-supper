package com.soilandsupper.ai.command

import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed

data class HistoryEntry(
    val command: GardenCommand,
    val timestamp: Long,
    val previousState: Map<String, Any?>? = null
)

interface CommandHistory {
    suspend fun record(entry: HistoryEntry)
    suspend fun undoLast(repository: GardenRepository): CommandResult?
    fun clear()
}
