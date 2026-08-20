package com.soilandsupper.ai.orchestration

import com.soilandsupper.ai.command.GardenCommand

sealed interface AIInterpretation {
    data class InformationalAnswer(val message: String) : AIInterpretation
    data class CommandProposals(val proposals: List<AICommandProposal>) : AIInterpretation
    data class ClarificationRequest(
        val question: String,
        val pendingProposals: List<AICommandProposal> = emptyList()
    ) : AIInterpretation
    data class Uncertainty(val reason: String) : AIInterpretation
    data class RecognitionResult(val recognized: String, val confidence: Float) : AIInterpretation
}
