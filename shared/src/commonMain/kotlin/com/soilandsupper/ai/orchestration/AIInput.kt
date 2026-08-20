package com.soilandsupper.ai.orchestration

sealed interface AIInput {
    val rawContent: String

    data class Text(
        override val rawContent: String
    ) : AIInput

    data class VoiceTranscript(
        override val rawContent: String,
        val confidence: Float? = null
    ) : AIInput

    data class ImageReference(
        override val rawContent: String,
        val imageId: String,
        val description: String? = null
    ) : AIInput

    data class DocumentText(
        override val rawContent: String,
        val documentType: String? = null
    ) : AIInput
}
