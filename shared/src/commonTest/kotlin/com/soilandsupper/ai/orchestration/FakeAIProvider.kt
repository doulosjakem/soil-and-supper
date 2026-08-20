package com.soilandsupper.ai.orchestration

class FakeAIProvider : LocalAIProvider {
    private val exactResponses = mutableMapOf<String, AIInterpretation>()
    private var defaultResponse: AIInterpretation = AIInterpretation.Uncertainty("Unknown input")

    fun setResponse(input: String, interpretation: AIInterpretation) {
        exactResponses[input.lowercase()] = interpretation
    }

    fun setDefault(interpretation: AIInterpretation) {
        defaultResponse = interpretation
    }

    fun clear() {
        exactResponses.clear()
        defaultResponse = AIInterpretation.Uncertainty("Unknown input")
    }

    override suspend fun interpret(request: AIRequest): AIInterpretation {
        val text = when (val input = request.input) {
            is AIInput.Text -> input.rawContent.lowercase()
            is AIInput.VoiceTranscript -> input.rawContent.lowercase()
            else -> ""
        }
        return exactResponses[text] ?: defaultResponse
    }
}
