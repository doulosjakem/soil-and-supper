package com.soilandsupper.ai.orchestration

import com.soilandsupper.ai.command.GardenCommand

class AndroidFakeAIProvider : LocalAIProvider {
    override suspend fun interpret(request: AIRequest): AIInterpretation {
        val text = when (val input = request.input) {
            is AIInput.Text -> input.rawContent.trim()
            is AIInput.VoiceTranscript -> input.rawContent.trim()
            else -> ""
        }
        val lower = text.lowercase()

        if (lower.isEmpty()) return AIInterpretation.Uncertainty("Empty input")

        if (lower.startsWith("undo")) {
            return AIInterpretation.InformationalAnswer("undo")
        }

        if ((lower.contains("what") && lower.contains("growing")) ||
            lower.contains("currently growing") ||
            (lower.contains("show") && lower.contains("garden")) ||
            (lower.contains("list") && lower.contains("growing"))) {
            val active = request.gardenContext?.activeOccupancies ?: emptyList()
            val spaces = request.gardenContext?.spaces ?: emptyList()
            return if (active.isEmpty()) {
                AIInterpretation.InformationalAnswer("Nothing is currently growing in your garden.")
            } else {
                val summary = active.joinToString(", ") { occ ->
                    val spaceName = spaces.firstOrNull { it.id == occ.growingSpaceId }?.name ?: "unknown"
                    "${occ.cropName} in $spaceName"
                }
                AIInterpretation.InformationalAnswer("Currently growing: $summary")
            }
        }

        if (lower.contains("harvest")) {
            val active = request.gardenContext?.activeOccupancies ?: emptyList()
            val cropMatch = extractCropName(lower)
            val targets = if (cropMatch != null) {
                active.filter { it.cropName.equals(cropMatch, ignoreCase = true) }
            } else active

            return if (targets.isEmpty()) {
                AIInterpretation.InformationalAnswer("Nothing to harvest right now.")
            } else {
                val proposals = targets.map { occ ->
                    AICommandProposal(
                        command = GardenCommand.HarvestCrop(
                            occupancyId = occ.id,
                            quantity = 1.0,
                            unit = "lb",
                            date = System.currentTimeMillis()
                        ),
                        explanation = "Harvest ${occ.cropName}"
                    )
                }
                AIInterpretation.CommandProposals(proposals = proposals)
            }
        }

        val cropName = extractCropName(lower)
        val bedMatch = Regex("bed\\s*(\\d+)").find(lower)
        val mentionedBed = bedMatch?.groupValues?.getOrNull(1)?.let { "Bed $it" }

        if (lower.contains("plant") && cropName != null) {
            val spaces = request.gardenContext?.spaces ?: emptyList()
            return if (mentionedBed != null) {
                val target = spaces.firstOrNull { it.name.equals(mentionedBed, ignoreCase = true) }
                if (target != null) {
                    AIInterpretation.CommandProposals(
                        proposals = listOf(
                            AICommandProposal(
                                command = GardenCommand.PlantCrop(
                                    cropName = cropName,
                                    growingSpaceId = target.id,
                                    startDate = System.currentTimeMillis()
                                ),
                                explanation = "Plant $cropName in ${target.name}"
                            )
                        )
                    )
                } else {
                    AIInterpretation.Uncertainty("$mentionedBed not found.")
                }
            } else if (spaces.isNotEmpty()) {
                val first = spaces.first()
                AIInterpretation.ClarificationRequest(
                    question = "Which bed would you like to plant $cropName in?",
                    pendingProposals = listOf(
                        AICommandProposal(
                            command = GardenCommand.PlantCrop(
                                cropName = cropName,
                                growingSpaceId = first.id,
                                startDate = System.currentTimeMillis()
                            ),
                            explanation = "Plant $cropName in ${first.name}",
                            ambiguities = spaces.map { it.name }
                        )
                    )
                )
            } else {
                AIInterpretation.Uncertainty("No growing spaces available.")
            }
        }

        if (lower.contains("replant") && cropName != null) {
            val active = request.gardenContext?.activeOccupancies ?: emptyList()
            val spaces = request.gardenContext?.spaces ?: emptyList()
            val proposals = mutableListOf<AICommandProposal>()
            val targetSpace = mentionedBed?.let { name -> spaces.firstOrNull { s -> s.name.equals(name, ignoreCase = true) } }
            val occupancyToHarvest = targetSpace?.let { space ->
                active.firstOrNull { it.growingSpaceId == space.id }
            } ?: active.firstOrNull()

            if (occupancyToHarvest != null) {
                proposals.add(
                    AICommandProposal(
                        command = GardenCommand.HarvestCrop(
                            occupancyId = occupancyToHarvest.id,
                            quantity = 1.0,
                            unit = "lb",
                            date = System.currentTimeMillis()
                        ),
                        explanation = "Harvest ${occupancyToHarvest.cropName}"
                    )
                )
            }
            val plantSpace = targetSpace ?: spaces.firstOrNull()
            if (plantSpace != null) {
                proposals.add(
                    AICommandProposal(
                        command = GardenCommand.PlantCrop(
                            cropName = cropName,
                            growingSpaceId = plantSpace.id,
                            startDate = System.currentTimeMillis()
                        ),
                        explanation = "Plant $cropName in ${plantSpace.name}"
                    )
                )
            }
            if (lower.contains("note") || lower.contains("dry")) {
                proposals.add(
                    AICommandProposal(
                        command = GardenCommand.RecordObservation(
                            text = "Soil was really dry",
                            date = System.currentTimeMillis()
                        ),
                        explanation = "Note: soil was really dry"
                    )
                )
            }
            return if (proposals.isNotEmpty()) {
                AIInterpretation.CommandProposals(proposals = proposals)
            } else {
                AIInterpretation.Uncertainty("I'm not sure how to help with that yet.")
            }
        }

        if (lower.contains("identify") || lower.contains("what's this") || lower.contains("what is this")) {
            return AIInterpretation.RecognitionResult("Unknown plant", confidence = 0.3f)
        }

        return AIInterpretation.Uncertainty("I'm not sure how to help with that yet.")
    }

    private fun extractCropName(text: String): String? {
        val verbs = listOf("plant", "harvest", "add")
        val cleaned = text.replace(Regex("[^a-zA-Z\\s]"), "").trim()
        for (verb in verbs) {
            val idx = cleaned.indexOf(verb)
            if (idx >= 0) {
                val after = cleaned.substring(idx + verb.length).trim()
                val words = after.split("\\s+".toRegex())
                if (words.isNotEmpty() && words.first().length > 1) {
                    return words.first()
                        .replaceFirstChar { it.titlecase() }
                }
            }
        }
        return null
    }
}
