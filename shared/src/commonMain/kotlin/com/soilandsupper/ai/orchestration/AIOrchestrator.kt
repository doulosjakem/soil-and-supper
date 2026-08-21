package com.soilandsupper.ai.orchestration

import com.soilandsupper.ai.command.CommandExecutor
import com.soilandsupper.ai.command.CommandHistory
import com.soilandsupper.ai.command.CommandResult
import com.soilandsupper.ai.command.CommandValidator
import com.soilandsupper.ai.command.GardenCommand
import com.soilandsupper.ai.query.GardenQuery
import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed

class AIOrchestrator(
    private val provider: LocalAIProvider,
    private val query: GardenQuery,
    private val validator: CommandValidator,
    private val executor: CommandExecutor,
    private val history: CommandHistory,
    private val repository: GardenRepository
) {
    suspend fun process(request: AIRequest): AIResponse {
        if (isUndoRequest(request.input)) {
            return handleUndo()
        }

        val gardenContext = request.gardenContext ?: buildGardenContext()
        val enrichedRequest = request.copy(gardenContext = gardenContext)

        val interpretation = provider.interpret(enrichedRequest)

        return when (interpretation) {
            is AIInterpretation.InformationalAnswer -> AIResponse(message = interpretation.message)
            is AIInterpretation.RecognitionResult -> AIResponse(
                message = "Recognized: ${interpretation.recognized} (confidence: ${interpretation.confidence})"
            )
            is AIInterpretation.Uncertainty -> AIResponse(
                message = "I'm not sure: ${interpretation.reason}",
                errors = listOf(interpretation.reason)
            )
            is AIInterpretation.ClarificationRequest -> AIResponse(
                message = interpretation.question,
                clarificationQuestion = interpretation.question,
                pendingConfirmation = interpretation.pendingProposals
            )
            is AIInterpretation.CommandProposals -> handleCommandProposals(interpretation.proposals)
        }
    }

    private suspend fun handleCommandProposals(proposals: List<AICommandProposal>): AIResponse {
        if (proposals.isEmpty()) {
            return AIResponse(message = "No commands to execute.")
        }

        val ambiguousProposals = proposals.filter { it.ambiguities.isNotEmpty() }
        if (ambiguousProposals.isNotEmpty()) {
            val question = "I need more information: ${ambiguousProposals.flatMap { it.ambiguities }.distinct().joinToString(", ")}"
            return AIResponse(
                message = question,
                clarificationQuestion = question,
                pendingConfirmation = proposals
            )
        }

        val lowConfidence = proposals.any { (it.confidence ?: 1f) < 0.5f }
        if (lowConfidence) {
            val question = "I'm not confident enough to do that. Can you confirm?"
            return AIResponse(
                message = question,
                clarificationQuestion = question,
                pendingConfirmation = proposals
            )
        }

        val results = mutableListOf<CommandResult>()
        val failures = mutableListOf<CommandResult>()
        for (proposal in proposals) {
            val validation = validator.validate(
                command = proposal.command,
                currentSpaces = query.getAllSpaces(),
                currentOccupancies = query.getActiveOccupancies(),
                currentSeeds = query.getAllSeeds(),
                currentDesires = query.getAllDesires(),
                currentPlants = query.getAllPlants()
            )

            if (validation !is CommandResult.Success) {
                results.add(validation)
                failures.add(validation)
                continue
            }

            val result = executor.execute(proposal.command, repository)
            results.add(result)
            if (!result.succeeded) {
                failures.add(result)
            }
        }

        val message = buildString {
            if (results.isNotEmpty()) {
                appendLine("Executed ${results.size} command(s).")
                results.forEach { appendLine("- ${it.message}") }
            }
            if (failures.isNotEmpty()) {
                if (results.isNotEmpty()) appendLine()
                appendLine("Failed:")
                failures.forEach { appendLine("- ${it.message}") }
            }
        }

        return AIResponse(
            message = message.trim(),
            executedCommands = results,
            errors = failures.map { it.message }
        )
    }

    private suspend fun handleUndo(): AIResponse {
        val result = history.undoLast(repository)
        return if (result != null && result.succeeded) {
            AIResponse(message = "Undone: ${result.message}", executedCommands = listOf(result))
        } else {
            AIResponse(message = "Nothing to undo.", errors = listOf("No commands in history"))
        }
    }

    private suspend fun buildGardenContext(): GardenContext {
        return GardenContext(
            spaces = query.getAllSpaces(),
            activeOccupancies = query.getActiveOccupancies(),
            seeds = query.getAllSeeds(),
            desires = query.getAllDesires(),
            plants = query.getAllPlants()
        )
    }

    private fun isUndoRequest(input: AIInput): Boolean {
        return when (input) {
            is AIInput.Text -> input.rawContent.trim().startsWith("undo", ignoreCase = true)
            is AIInput.VoiceTranscript -> input.rawContent.trim().startsWith("undo", ignoreCase = true)
            else -> false
        }
    }
}
