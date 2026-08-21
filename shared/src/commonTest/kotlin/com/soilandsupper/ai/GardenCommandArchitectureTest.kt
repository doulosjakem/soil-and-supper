package com.soilandsupper.ai

import com.soilandsupper.ai.command.CommandResult
import com.soilandsupper.ai.command.DefaultCommandExecutor
import com.soilandsupper.ai.command.DefaultCommandValidator
import com.soilandsupper.ai.command.GardenCommand
import com.soilandsupper.ai.command.InMemoryCommandHistory
import com.soilandsupper.ai.query.DefaultGardenQuery
import com.soilandsupper.ai.query.GardenQuery
import com.soilandsupper.repository.PlantRepository
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Harvest
import com.soilandsupper.shared.domain.model.JournalEntry
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

class GardenCommandArchitectureTest {

    private lateinit var repository: FakeGardenRepository
    private lateinit var executor: DefaultCommandExecutor
    private lateinit var history: InMemoryCommandHistory
    private lateinit var query: GardenQuery

    @Before
    fun setup() {
        repository = FakeGardenRepository(
            initialSpaces = listOf(
                GrowingSpace(id = 1L, name = "Bed 1"),
                GrowingSpace(id = 2L, name = "Bed 2")
            ),
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
            initialSeeds = listOf(
                Seed(id = 1L, cropName = "Carrot", variety = "Nantes", state = SeedState.OWN.name)
            ),
            initialDesires = listOf(
                Desire(id = 1L, cropName = "Bean")
            ),
            initialPlants = listOf(
                Plant(id = 1L, name = "Old Tomato", plantingDate = epochMillis(2026, 5, 1))
            )
        )
        history = InMemoryCommandHistory()
        executor = DefaultCommandExecutor(DefaultCommandValidator(), history)
        query = DefaultGardenQuery(repository)
    }

    @Test
    fun `valid command executes successfully`() = runBlocking {
        val result = executor.execute(
            GardenCommand.AddGrowingSpace(name = "Bed 3"),
            repository
        )
        assertTrue(result is CommandResult.Success)
        assertTrue(result.succeeded)
    }

    @Test
    fun `invalid command is rejected`() = runBlocking {
        val result = executor.execute(
            GardenCommand.AddGrowingSpace(name = ""),
            repository
        )
        assertTrue(result is CommandResult.ValidationError)
        assertFalse(result.succeeded)
    }

    @Test
    fun `nonexistent growing space is rejected for plant crop`() = runBlocking {
        val result = executor.execute(
            GardenCommand.PlantCrop(
                cropName = "Carrot",
                growingSpaceId = 999L,
                startDate = epochMillis(2026, 6, 1)
            ),
            repository
        )
        assertTrue(result is CommandResult.NotFound)
        assertFalse(result.succeeded)
    }

    @Test
    fun `nonexistent desire is rejected for fulfill`() = runBlocking {
        val result = executor.execute(
            GardenCommand.FulfillDesire(desireId = 999L),
            repository
        )
        assertTrue(result is CommandResult.NotFound)
        assertFalse(result.succeeded)
    }

    @Test
    fun `successful mutation is recorded in command history`() = runBlocking {
        executor.execute(GardenCommand.AddGrowingSpace(name = "Bed 3"), repository)
        assertEquals(1, history.size)
    }

    @Test
    fun `failed command does not create history entry`() = runBlocking {
        executor.execute(GardenCommand.AddGrowingSpace(name = ""), repository)
        assertEquals(0, history.size)
    }

    @Test
    fun `undo restores previous state after add growing space`() = runBlocking {
        executor.execute(GardenCommand.AddGrowingSpace(name = "Bed 3"), repository)
        assertTrue(history.size == 1)

        var spacesBefore: List<GrowingSpace> = emptyList()
        repository.getAllGrowingSpaces().collect { spacesBefore = it }
        assertEquals(3, spacesBefore.size)

        val undoResult = history.undoLast(repository)
        assertNotNull(undoResult)
        assertTrue(undoResult!!.succeeded)

        var spacesAfter: List<GrowingSpace> = emptyList()
        repository.getAllGrowingSpaces().collect { spacesAfter = it }
        assertEquals(2, spacesAfter.size)
    }

    @Test
    fun `undo restores previous state after update growing space`() = runBlocking {
        executor.execute(
            GardenCommand.UpdateGrowingSpace(
                spaceId = 1L,
                name = "Renamed Bed",
                notes = null,
                spaceType = null,
                width = null,
                length = null
            ),
            repository
        )
        assertTrue(history.size == 1)

        val undoResult = history.undoLast(repository)
        assertNotNull(undoResult)
        assertTrue(undoResult!!.succeeded)

        val space = query.getSpaceById(1L)
        assertNotNull(space)
        assertEquals("Bed 1", space!!.name)
    }

    @Test
    fun `undo restores previous state after update plant`() = runBlocking {
        repository = FakeGardenRepository(
            initialPlants = listOf(
                Plant(id = 1L, name = "Old Tomato", variety = "Roma", plantingDate = epochMillis(2026, 5, 1), location = "Garden", notes = "Original")
            ),
            initialSpaces = listOf(GrowingSpace(id = 1L, name = "Bed 1")),
            initialOccupancies = emptyList()
        )
        history = InMemoryCommandHistory()
        executor = DefaultCommandExecutor(DefaultCommandValidator(), history)

        executor.execute(
            GardenCommand.UpdatePlant(
                plantId = 1L,
                name = "New Tomato",
                variety = "Cherry",
                plantingDate = epochMillis(2026, 6, 1),
                location = "Patio",
                notes = "Updated"
            ),
            repository
        )
        assertTrue(history.size == 1)

        val undoResult = history.undoLast(repository)
        assertNotNull(undoResult)
        assertTrue(undoResult!!.succeeded)

        val plant = (repository as PlantRepository).getPlantById(1L)
        assertNotNull(plant)
        assertEquals("Old Tomato", plant!!.name)
        assertEquals("Roma", plant.variety)
        assertEquals("Garden", plant.location)
        assertEquals("Original", plant.notes)
    }

    @Test
    fun `undo restores previous state after harvest crop`() = runBlocking {
        repository = FakeGardenRepository(
            initialSpaces = listOf(GrowingSpace(id = 1L, name = "Bed 1")),
            initialOccupancies = listOf(
                Occupancy(
                    id = 1L,
                    cropName = "Tomato",
                    variety = "Roma",
                    startDate = epochMillis(2026, 5, 1),
                    status = OccupancyStatus.ACTIVE.name,
                    growingSpaceId = 1L,
                    plantId = 10L
                )
            ),
            initialPlants = emptyList()
        )
        history = InMemoryCommandHistory()
        executor = DefaultCommandExecutor(DefaultCommandValidator(), history)

        executor.execute(
            GardenCommand.HarvestCrop(
                occupancyId = 1L,
                quantity = 5.0,
                unit = "lb",
                date = epochMillis(2026, 8, 1)
            ),
            repository
        )
        assertTrue(history.size == 1)

        var harvestsBefore: List<Harvest> = emptyList()
        (repository as PlantRepository).getAllHarvests().collect { harvestsBefore = it }
        assertEquals(1, harvestsBefore.size)

        val undoResult = history.undoLast(repository)
        assertNotNull(undoResult)
        assertTrue(undoResult!!.succeeded)

        var harvestsAfter: List<Harvest> = emptyList()
        (repository as PlantRepository).getAllHarvests().collect { harvestsAfter = it }
        assertTrue(harvestsAfter.isEmpty())
    }

    @Test
    fun `undo restores previous state after record observation`() = runBlocking {
        repository = FakeGardenRepository(
            initialPlants = listOf(
                Plant(id = 1L, name = "Tomato", plantingDate = epochMillis(2026, 5, 1))
            ),
            initialSpaces = listOf(GrowingSpace(id = 1L, name = "Bed 1")),
            initialOccupancies = emptyList(),
            initialJournalEntries = emptyList()
        )
        history = InMemoryCommandHistory()
        executor = DefaultCommandExecutor(DefaultCommandValidator(), history)

        executor.execute(
            GardenCommand.RecordObservation(
                plantId = 1L,
                text = "First fruit appeared",
                date = epochMillis(2026, 7, 1)
            ),
            repository
        )
        assertTrue(history.size == 1)

        var entriesBefore: List<JournalEntry> = emptyList()
        (repository as PlantRepository).getJournalEntriesForPlant(1L).collect { entriesBefore = it }
        assertEquals(1, entriesBefore.size)

        val undoResult = history.undoLast(repository)
        assertNotNull(undoResult)
        assertTrue(undoResult!!.succeeded)

        var entriesAfter: List<JournalEntry> = emptyList()
        (repository as PlantRepository).getJournalEntriesForPlant(1L).collect { entriesAfter = it }
        assertTrue(entriesAfter.isEmpty())
    }

    @Test
    fun `multiple commands can be represented as a batch`() = runBlocking {
        val commands = listOf(
            GardenCommand.AddGrowingSpace(name = "Bed 3"),
            GardenCommand.AddGrowingSpace(name = "Bed 4"),
            GardenCommand.AddSeed(cropName = "Lettuce")
        )

        val results = commands.map { cmd ->
            executor.execute(cmd, repository)
        }

        assertTrue(results.all { it.succeeded })
        assertEquals(3, history.size)
    }

    @Test
    fun `batch with invalid command produces explicit structured result`() = runBlocking {
        val commands = listOf(
            GardenCommand.AddGrowingSpace(name = "Bed 3"),
            GardenCommand.AddGrowingSpace(name = ""),
            GardenCommand.AddSeed(cropName = "Lettuce")
        )

        val results = commands.map { cmd ->
            executor.execute(cmd, repository)
        }

        assertEquals(1, results.count { !it.succeeded })
        assertTrue(results[0] is CommandResult.Success)
        assertTrue(results[1] is CommandResult.ValidationError)
        assertTrue(results[2] is CommandResult.Success)
        assertEquals(2, history.size)
    }

    @Test
    fun `read query returns current authoritative state`() = runBlocking {
        val spaces = query.getAllSpaces()
        assertEquals(2, spaces.size)

        val activeOccupancies = query.getActiveOccupancies()
        assertEquals(1, activeOccupancies.size)
        assertEquals("Tomato", activeOccupancies.first().cropName)

        val seeds = query.getAllSeeds()
        assertEquals(1, seeds.size)
        assertEquals("Carrot", seeds.first().cropName)
    }

    @Test
    fun `projections are not converted into mutations`() = runBlocking {
        val futureDate = epochMillis(2026, 9, 15)
        val openings = query.getUpcomingOpenings(beforeDate = futureDate)
        assertTrue(openings.isNotEmpty())

        val occupancy = openings.first()
        assertEquals(OccupancyStatus.ACTIVE.name, occupancy.status)
        assertNotNull(occupancy.expectedReleaseDate)
    }

    @Test
    fun `commands remain deterministic`() = runBlocking {
        val cmd = GardenCommand.AddGrowingSpace(name = "Deterministic Bed")
        val result1 = executor.execute(cmd, repository)
        val result2 = executor.execute(cmd, repository)

        assertTrue(result1 is CommandResult.Success)
        assertTrue(result2 is CommandResult.Success)
        assertEquals(result1.message, result2.message)
    }

    @Test
    fun `plant crop with active occupancy in space is rejected`() = runBlocking {
        val result = executor.execute(
            GardenCommand.PlantCrop(
                cropName = "Carrot",
                growingSpaceId = 1L,
                startDate = epochMillis(2026, 6, 1)
            ),
            repository
        )
        assertTrue(result is CommandResult.Conflict)
        assertFalse(result.succeeded)
    }

    @Test
    fun `harvest crop with invalid occupancy is rejected`() = runBlocking {
        val result = executor.execute(
            GardenCommand.HarvestCrop(
                occupancyId = 999L,
                quantity = 5.0,
                unit = "lb",
                date = epochMillis(2026, 8, 1)
            ),
            repository
        )
        assertTrue(result is CommandResult.NotFound)
        assertFalse(result.succeeded)
    }

    @Test
    fun `end crop with nonexistent occupancy is rejected`() = runBlocking {
        val result = executor.execute(
            GardenCommand.EndCrop(
                occupancyId = 999L,
                endDate = epochMillis(2026, 9, 1)
            ),
            repository
        )
        assertTrue(result is CommandResult.NotFound)
        assertFalse(result.succeeded)
    }

    @Test
    fun `record observation without text is rejected`() = runBlocking {
        val result = executor.execute(
            GardenCommand.RecordObservation(text = "", date = epochMillis(2026, 6, 1)),
            repository
        )
        assertTrue(result is CommandResult.ValidationError)
        assertFalse(result.succeeded)
    }

    @Test
    fun `add seed without crop name is rejected`() = runBlocking {
        val result = executor.execute(
            GardenCommand.AddSeed(cropName = ""),
            repository
        )
        assertTrue(result is CommandResult.ValidationError)
        assertFalse(result.succeeded)
    }

    @Test
    fun `add desire without crop name is rejected`() = runBlocking {
        val result = executor.execute(
            GardenCommand.AddDesire(cropName = ""),
            repository
        )
        assertTrue(result is CommandResult.ValidationError)
        assertFalse(result.succeeded)
    }

    @Test
    fun `fulfill already fulfilled desire is rejected`() = runBlocking {
        val desire = Desire(id = 1L, cropName = "Bean", isFulfilled = true)
        repository = FakeGardenRepository(
            initialDesires = listOf(desire),
            initialSpaces = listOf(GrowingSpace(id = 1L, name = "Bed 1")),
            initialOccupancies = emptyList()
        )
        history = InMemoryCommandHistory()
        executor = DefaultCommandExecutor(DefaultCommandValidator(), history)

        val result = executor.execute(
            GardenCommand.FulfillDesire(desireId = 1L),
            repository
        )
        assertTrue(result is CommandResult.Conflict)
        assertFalse(result.succeeded)
    }

    @Test
    fun `cancel already cancelled desire is rejected`() = runBlocking {
        val desire = Desire(id = 1L, cropName = "Bean", isCancelled = true)
        repository = FakeGardenRepository(
            initialDesires = listOf(desire),
            initialSpaces = listOf(GrowingSpace(id = 1L, name = "Bed 1")),
            initialOccupancies = emptyList()
        )
        history = InMemoryCommandHistory()
        executor = DefaultCommandExecutor(DefaultCommandValidator(), history)

        val result = executor.execute(
            GardenCommand.CancelDesire(desireId = 1L),
            repository
        )
        assertTrue(result is CommandResult.Conflict)
        assertFalse(result.succeeded)
    }

    @Test
    fun `record plant without name is rejected`() = runBlocking {
        val result = executor.execute(
            GardenCommand.RecordPlant(name = "", plantingDate = epochMillis(2026, 6, 1)),
            repository
        )
        assertTrue(result is CommandResult.ValidationError)
        assertFalse(result.succeeded)
    }

    @Test
    fun `update nonexistent plant is rejected`() = runBlocking {
        val result = executor.execute(
            GardenCommand.UpdatePlant(
                plantId = 999L,
                name = "New Name",
                variety = "",
                plantingDate = epochMillis(2026, 6, 1),
                location = "",
                notes = ""
            ),
            repository
        )
        assertTrue(result is CommandResult.NotFound)
        assertFalse(result.succeeded)
    }

    @Test
    fun `remove nonexistent plant is rejected`() = runBlocking {
        val result = executor.execute(
            GardenCommand.RemovePlant(plantId = 999L),
            repository
        )
        assertTrue(result is CommandResult.NotFound)
        assertFalse(result.succeeded)
    }
}
