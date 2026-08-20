package com.soilandsupper.ai.orchestration

import com.soilandsupper.ai.command.CommandResult

data class AIResponse(
    val message: String,
    val executedCommands: List<CommandResult> = emptyList(),
    val pendingConfirmation: List<AICommandProposal> = emptyList(),
    val errors: List<String> = emptyList(),
    val clarificationQuestion: String? = null
) {
    val isSuccess: Boolean get() = executedCommands.isNotEmpty() && errors.isEmpty()
    val needsConfirmation: Boolean get() = pendingConfirmation.isNotEmpty() && executedCommands.isEmpty()
    val needsClarification: Boolean get() = clarificationQuestion != null
    val hasError: Boolean get() = errors.isNotEmpty()
}
