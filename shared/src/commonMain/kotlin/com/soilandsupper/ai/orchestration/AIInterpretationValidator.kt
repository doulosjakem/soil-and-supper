package com.soilandsupper.ai.orchestration

class AIInterpretationValidator {

    fun validate(interpretation: AIInterpretation): ValidationResult {
        return when (interpretation) {
            is AIInterpretation.InformationalAnswer -> validateInformationalAnswer(interpretation)
            is AIInterpretation.CommandProposals -> validateCommandProposals(interpretation)
            is AIInterpretation.ClarificationRequest -> validateClarificationRequest(interpretation)
            is AIInterpretation.Uncertainty -> validateUncertainty(interpretation)
            is AIInterpretation.RecognitionResult -> validateRecognitionResult(interpretation)
        }
    }

    private fun validateInformationalAnswer(
        answer: AIInterpretation.InformationalAnswer
    ): ValidationResult {
        if (answer.message.isBlank()) {
            return ValidationResult.Invalid(listOf("InformationalAnswer message must not be blank"))
        }
        return ValidationResult.Valid
    }

    private fun validateCommandProposals(
        proposals: AIInterpretation.CommandProposals
    ): ValidationResult {
        if (proposals.proposals.isEmpty()) {
            return ValidationResult.Invalid(listOf("CommandProposals must contain at least one proposal"))
        }
        val errors = mutableListOf<String>()
        proposals.proposals.forEachIndexed { index, proposal ->
            if (proposal.explanation.isBlank()) {
                errors.add("Proposal[$index] explanation must not be blank")
            }
            val confidence = proposal.confidence
            if (confidence != null && (confidence < 0f || confidence > 1f)) {
                errors.add("Proposal[$index] confidence must be between 0.0 and 1.0")
            }
        }
        return if (errors.isNotEmpty()) {
            ValidationResult.Invalid(errors)
        } else {
            ValidationResult.Valid
        }
    }

    private fun validateClarificationRequest(
        request: AIInterpretation.ClarificationRequest
    ): ValidationResult {
        val errors = mutableListOf<String>()
        if (request.question.isBlank()) {
            errors.add("ClarificationRequest question must not be blank")
        }
        request.pendingProposals.forEachIndexed { index, proposal ->
            if (proposal.explanation.isBlank()) {
                errors.add("Pending proposal[$index] explanation must not be blank")
            }
            val confidence = proposal.confidence
            if (confidence != null && (confidence < 0f || confidence > 1f)) {
                errors.add("Pending proposal[$index] confidence must be between 0.0 and 1.0")
            }
        }
        return if (errors.isNotEmpty()) {
            ValidationResult.Invalid(errors)
        } else {
            ValidationResult.Valid
        }
    }

    private fun validateUncertainty(
        uncertainty: AIInterpretation.Uncertainty
    ): ValidationResult {
        if (uncertainty.reason.isBlank()) {
            return ValidationResult.Invalid(listOf("Uncertainty reason must not be blank"))
        }
        return ValidationResult.Valid
    }

    private fun validateRecognitionResult(
        result: AIInterpretation.RecognitionResult
    ): ValidationResult {
        val errors = mutableListOf<String>()
        if (result.recognized.isBlank()) {
            errors.add("RecognitionResult recognized value must not be blank")
        }
        if (result.confidence < 0f || result.confidence > 1f) {
            errors.add("RecognitionResult confidence must be between 0.0 and 1.0")
        }
        return if (errors.isNotEmpty()) {
            ValidationResult.Invalid(errors)
        } else {
            ValidationResult.Valid
        }
    }

    sealed interface ValidationResult {
        data object Valid : ValidationResult
        data class Invalid(val errors: List<String>) : ValidationResult

        val isValid: Boolean get() = this is Valid
        val isInvalid: Boolean get() = this is Invalid
    }
}
