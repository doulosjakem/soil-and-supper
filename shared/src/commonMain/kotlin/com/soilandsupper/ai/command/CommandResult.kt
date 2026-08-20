package com.soilandsupper.ai.command

sealed interface CommandResult {
    val succeeded: Boolean
    val command: GardenCommand
    val message: String

    data class Success(
        override val command: GardenCommand,
        override val message: String = "Command executed successfully"
    ) : CommandResult {
        override val succeeded: Boolean = true
    }

    data class ValidationError(
        override val command: GardenCommand,
        val reason: String,
        override val message: String = "Validation failed: $reason"
    ) : CommandResult {
        override val succeeded: Boolean = false
    }

    data class NotFound(
        override val command: GardenCommand,
        val entityType: String,
        val entityId: Long,
        override val message: String = "$entityType with id $entityId not found"
    ) : CommandResult {
        override val succeeded: Boolean = false
    }

    data class Conflict(
        override val command: GardenCommand,
        val reason: String,
        override val message: String = "Conflict: $reason"
    ) : CommandResult {
        override val succeeded: Boolean = false
    }

    data class NeedsClarification(
        override val command: GardenCommand,
        val question: String,
        override val message: String = "Needs clarification: $question"
    ) : CommandResult {
        override val succeeded: Boolean = false
    }

    data class NotSupported(
        override val command: GardenCommand,
        override val message: String = "Command not supported"
    ) : CommandResult {
        override val succeeded: Boolean = false
    }
}
