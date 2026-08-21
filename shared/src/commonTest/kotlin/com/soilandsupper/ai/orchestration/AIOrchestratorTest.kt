package com.soilandsupper.ai.orchestration

import com.soilandsupper.ai.command.CommandResult
import com.soilandsupper.ai.command.DefaultCommandExecutor
import com.soilandsupper.ai.command.DefaultCommandValidator
import com.soilandsupper.ai.command.GardenCommand
import com.soilandsupper.ai.command.InMemoryCommandHistory
import com.soilandsupper.ai.query.DefaultGardenQuery
import com.soilandsupper.ai.query.GardenQuery
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.OccupancyStatus
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed
import com.soilandsupper.shared.domain.model.SeedState
import com.soilandsupper.util.epochMillis
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

class AIOrchestratorTest {

    private lateinit var repository: FakeOrchestrationRepository
    private lateinit var provider: FakeAIProvider
    private lateinit var history: InMemoryCommandHistory
    private lateinit var orchestrator: AIOrchestrator
    private lateinit var query: GardenQuery

    @Before
    fun setup() {
        repository = FakeOrchestrationRepository(
            initialSpaces = listOf(GrowingSpace(id = 1L, name = "Bed 1")),
            initialOccupancies = listOf(
                Occupancy(
                    id = 1L,
                    cropName = "Tomato",
                    variety = "Roma",
                    startDate = epochMillis(2026, 5, 1),
                    expectedHarvestDate = epochMillis(2026, 8, 1),
                    expectedReleaseDate = epochMillis(2026, 9, 1),
                    status = OccupancyStatus.ACTIVE.name,
                    growingSpaceId = 1L
                )
            ),
            initialSeeds = listOf(Seed(id = 1L, cropName = "Carrot", variety = "Nantes", state = SeedState.OWN.name)),
            initialDesires = listOf(Desire(id = 1L, cropName = "Bean")),
            initialPlants = listOf(Plant(id = 1L, name = "Old Tomato", plantingDate = epochMillis(2026, 5, 1)))
        )
        provider = FakeAIProvider()
        history = InMemoryCommandHistory()
        query = DefaultGardenQuery(repository)
        orchestrator = AIOrchestrator(
            provider = provider,
            query = query,
            validator = DefaultCommandValidator(),
            executor = DefaultCommandExecutor(DefaultCommandValidator(), history),
            history = history,
            repository = repository
        )
    }

    @Test
    fun `read-only query returns informational answer`() = runBlocking {
        provider.setResponse("what's growing in bed 1", AIInterpretation.InformationalAnswer("Tomato is growing in Bed 1"))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("what's growing in bed 1")
            )
        )

        assertFalse(response.hasError)
        assertEquals("Tomato is growing in Bed 1", response.message)
        assertTrue(response.executedCommands.isEmpty())
    }

    @Test
    fun `single valid mutation executes successfully`() = runBlocking {
        provider.setResponse("add a new bed", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.AddGrowingSpace(name = "Bed 2"),
                    explanation = "Add a new growing space"
                )
            )
        ))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("add a new bed")
            )
        )

        assertTrue(response.isSuccess)
        assertEquals(1, response.executedCommands.size)
        assertTrue(response.executedCommands.first().succeeded)
        assertEquals(1, history.size)
    }

    @Test
    fun `multi-command mutation executes all commands`() = runBlocking {
        provider.setResponse("add seeds and desires", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.AddSeed(cropName = "Lettuce"),
                    explanation = "Add lettuce seed"
                ),
                AICommandProposal(
                    command = GardenCommand.AddDesire(cropName = "Radish"),
                    explanation = "Add radish desire"
                )
            )
        ))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("add seeds and desires")
            )
        )

        assertTrue(response.isSuccess)
        assertEquals(2, response.executedCommands.size)
        assertEquals(2, history.size)
    }

    @Test
    fun `invalid command is rejected by domain`() = runBlocking {
        provider.setResponse("plant in nonexistent bed", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.PlantCrop(cropName = "Carrot", growingSpaceId = 999L, startDate = epochMillis(2026, 6, 1)),
                    explanation = "Plant carrots"
                )
            )
        ))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("plant in nonexistent bed")
            )
        )

        assertTrue(response.hasError)
        assertEquals(1, response.executedCommands.size)
        assertFalse(response.executedCommands.first().succeeded)
        assertEquals(0, history.size)
    }

    @Test
    fun `ambiguous request produces clarification`() = runBlocking {
        provider.setResponse("plant beans", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.PlantCrop(cropName = "Bean", growingSpaceId = 1L, startDate = epochMillis(2026, 6, 1)),
                    explanation = "Plant beans",
                    ambiguities = listOf("Which bed?")
                )
            )
        ))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("plant beans")
            )
        )

        assertTrue(response.needsClarification)
        assertNotNull(response.clarificationQuestion)
        assertTrue(response.pendingConfirmation.isNotEmpty())
        assertTrue(response.executedCommands.isEmpty())
    }

    @Test
    fun `model uncertainty does not execute automatically`() = runBlocking {
        provider.setResponse("something random", AIInterpretation.Uncertainty("Could not understand intent"))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("something random")
            )
        )

        assertTrue(response.hasError)
        assertTrue(response.executedCommands.isEmpty())
        assertEquals(0, history.size)
    }

    @Test
    fun `command execution records history`() = runBlocking {
        provider.setResponse("add a bed", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.AddGrowingSpace(name = "Bed 2"),
                    explanation = "Add a new bed"
                )
            )
        ))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("add a bed")
            )
        )

        assertTrue(response.isSuccess)
        assertEquals(1, history.size)
    }

    @Test
    fun `undo with extended phrase reaches CommandHistory`() = runBlocking {
        provider.setResponse("add a bed", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.AddGrowingSpace(name = "Bed 2"),
                    explanation = "Add a new bed"
                )
            )
        ))

        orchestrator.process(AIRequest(input = AIInput.Text("add a bed")))
        assertEquals(1, history.size)

        provider.setResponse("undo that, i meant the carrots not the beets", AIInterpretation.InformationalAnswer("undo"))
        val response = orchestrator.process(AIRequest(input = AIInput.Text("undo that, i meant the carrots not the beets")))

        assertTrue(response.message.contains("Undone"))
        assertEquals(0, history.size)
    }

    @Test
    fun `repository remains authoritative`() = runBlocking {
        provider.setResponse("add a bed", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.AddGrowingSpace(name = "Bed 2"),
                    explanation = "Add a new bed"
                )
            )
        ))

        orchestrator.process(AIRequest(input = AIInput.Text("add a bed")))
        val spaces = query.getAllSpaces()
        assertEquals(2, spaces.size)
    }

    @Test
    fun `ai cannot bypass CommandExecutor`() = runBlocking {
        provider.setResponse("add a bed", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.AddGrowingSpace(name = "Bed 2"),
                    explanation = "Add a new bed"
                )
            )
        ))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("add a bed")
            )
        )

        assertTrue(response.executedCommands.isNotEmpty())
        assertTrue(response.executedCommands.first().succeeded)
    }

    @Test
    fun `ai response accurately describes executed commands`() = runBlocking {
        provider.setResponse("add a bed", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.AddGrowingSpace(name = "Bed 2"),
                    explanation = "Add a new bed"
                )
            )
        ))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("add a bed")
            )
        )

        assertTrue(response.message.contains("Executed 1 command(s)"))
    }

    @Test
    fun `partial failure behavior`() = runBlocking {
        provider.setResponse("add two beds", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.AddGrowingSpace(name = "Bed 2"),
                    explanation = "Add Bed 2"
                ),
                AICommandProposal(
                    command = GardenCommand.AddGrowingSpace(name = ""),
                    explanation = "Add invalid bed"
                )
            )
        ))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("add two beds")
            )
        )

        assertTrue(response.hasError)
        assertTrue(response.executedCommands.isNotEmpty())
        assertTrue(response.executedCommands.count { !it.succeeded } > 0)
    }

    @Test
    fun `empty input produces uncertainty`() = runBlocking {
        provider.setDefault(AIInterpretation.Uncertainty("Empty input"))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("")
            )
        )

        assertTrue(response.hasError)
        assertTrue(response.executedCommands.isEmpty())
    }

    @Test
    fun `unknown request produces uncertainty`() = runBlocking {
        provider.setDefault(AIInterpretation.Uncertainty("Unknown request"))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("xyzzy")
            )
        )

        assertTrue(response.hasError)
        assertTrue(response.executedCommands.isEmpty())
    }

    @Test
    fun `conversation context does not mutate domain state`() = runBlocking {
        provider.setResponse("add a bed", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.AddGrowingSpace(name = "Bed 2"),
                    explanation = "Add a new bed"
                )
            )
        ))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("add a bed"),
                conversationContext = ConversationContext(sessionId = "session1", turnCount = 1)
            )
        )

        assertTrue(response.isSuccess)
        assertEquals(1, history.size)
    }

    @Test
    fun `garden context is supplied to provider`() = runBlocking {
        provider.setResponse("add a bed", AIInterpretation.InformationalAnswer("ok"))

        orchestrator.process(
            AIRequest(
                input = AIInput.Text("add a bed"),
                gardenContext = GardenContext(
                    spaces = listOf(GrowingSpace(id = 1L, name = "Bed 1")),
                    activeOccupancies = emptyList()
                )
            )
        )

        val spaces = query.getAllSpaces()
        assertEquals(1, spaces.size)
    }

    @Test
    fun `low confidence produces confirmation request`() = runBlocking {
        provider.setResponse("maybe plant beans", AIInterpretation.CommandProposals(
            proposals = listOf(
                AICommandProposal(
                    command = GardenCommand.PlantCrop(cropName = "Bean", growingSpaceId = 1L, startDate = epochMillis(2026, 6, 1)),
                    explanation = "Plant beans",
                    confidence = 0.3f
                )
            )
        ))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("maybe plant beans")
            )
        )

        assertTrue(response.needsConfirmation)
        assertTrue(response.pendingConfirmation.isNotEmpty())
        assertTrue(response.executedCommands.isEmpty())
    }

    @Test
    fun `voice transcript input is handled`() = runBlocking {
        provider.setResponse("add a bed", AIInterpretation.InformationalAnswer("Voice command received"))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.VoiceTranscript(rawContent = "add a bed", confidence = 0.9f)
            )
        )

        assertFalse(response.hasError)
        assertEquals("Voice command received", response.message)
    }

    @Test
    fun `undo when no history returns error`() = runBlocking {
        provider.setResponse("undo", AIInterpretation.InformationalAnswer("undo"))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("undo")
            )
        )

        assertTrue(response.hasError)
        assertTrue(response.message.contains("Nothing to undo"))
    }

    @Test
    fun `recognition result is returned without mutation`() = runBlocking {
        provider.setResponse("what's this plant", AIInterpretation.RecognitionResult("Tomato", confidence = 0.92f))

        val response = orchestrator.process(
            AIRequest(
                input = AIInput.Text("what's this plant")
            )
        )

        assertFalse(response.hasError)
        assertTrue(response.message.contains("Tomato"))
        assertTrue(response.executedCommands.isEmpty())
    }
}
