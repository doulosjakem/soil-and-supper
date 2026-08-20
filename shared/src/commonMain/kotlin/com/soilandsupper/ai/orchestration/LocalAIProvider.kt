package com.soilandsupper.ai.orchestration

interface LocalAIProvider {
    suspend fun interpret(request: AIRequest): AIInterpretation
}
