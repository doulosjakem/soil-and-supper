package com.soilandsupper.ai.orchestration

import com.soilandsupper.ai.command.GardenCommand

data class AICommandProposal(
    val command: GardenCommand,
    val explanation: String,
    val confidence: Float? = null,
    val ambiguities: List<String> = emptyList()
)
