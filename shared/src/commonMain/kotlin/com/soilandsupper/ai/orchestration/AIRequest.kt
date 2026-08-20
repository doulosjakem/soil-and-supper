package com.soilandsupper.ai.orchestration

import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed

data class GardenContext(
    val spaces: List<GrowingSpace> = emptyList(),
    val activeOccupancies: List<Occupancy> = emptyList(),
    val seeds: List<Seed> = emptyList(),
    val desires: List<Desire> = emptyList(),
    val plants: List<Plant> = emptyList()
)

data class ConversationContext(
    val sessionId: String,
    val turnCount: Int = 0,
    val lastInterpretation: AIInterpretation? = null
)

data class AIRequest(
    val input: AIInput,
    val conversationContext: ConversationContext? = null,
    val gardenContext: GardenContext? = null
)
