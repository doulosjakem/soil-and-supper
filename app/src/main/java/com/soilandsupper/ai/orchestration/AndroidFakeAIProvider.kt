package com.soilandsupper.ai.orchestration

import com.soilandsupper.ai.command.GardenCommand

class AndroidFakeAIProvider : LocalAIProvider {
    override suspend fun interpret(request: AIRequest): AIInterpretation {
        val text = when (val input = request.input) {
            is AIInput.Text -> input.rawContent.trim().lowercase()
            is AIInput.VoiceTranscript -> input.rawContent.trim().lowercase()
            else -> ""
        }

        return when {
            text.isEmpty() -> AIInterpretation.Uncertainty("Empty input")
            text == "undo" || text == "undo that" -> AIInterpretation.InformationalAnswer("undo")
            text.contains("what") || text.contains("show") || text.contains("list") -> AIInterpretation.InformationalAnswer(
                "You have growing spaces and plants to track. Check the garden timeline."
            )
            text.contains("add") || text.contains("plant") || text.contains("harvest") -> AIInterpretation.CommandProposals(
                proposals = listOf(
                    AICommandProposal(
                        command = GardenCommand.AddGrowingSpace(name = "Bed 2"),
                        explanation = "Add a new growing space"
                    )
                )
            )
            else -> AIInterpretation.Uncertainty("I'm not sure how to help with that yet.")
        }
    }
}
