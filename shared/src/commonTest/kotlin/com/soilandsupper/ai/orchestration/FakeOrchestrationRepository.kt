package com.soilandsupper.ai.orchestration

import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.repository.PlantRepository
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.Garden
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Harvest
import com.soilandsupper.shared.domain.model.JournalEntry
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.OccupancyStatus
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.PlantPhoto
import com.soilandsupper.shared.domain.model.PlannedPlanting
import com.soilandsupper.shared.domain.model.Seed
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.flowOf

class FakeOrchestrationRepository(
    initialSpaces: List<GrowingSpace> = emptyList(),
    initialOccupancies: List<Occupancy> = emptyList(),
    initialSeeds: List<Seed> = emptyList(),
    initialDesires: List<Desire> = emptyList(),
    initialPlants: List<Plant> = emptyList()
) : GardenRepository, PlantRepository {

    private val spacesFlow = MutableStateFlow(initialSpaces)
    private val occupanciesFlow = MutableStateFlow(initialOccupancies)
    private val seedsFlow = MutableStateFlow(initialSeeds)
    private val desiresFlow = MutableStateFlow(initialDesires)
    private val plantsFlow = MutableStateFlow(initialPlants)

    override fun getAllGardens(): Flow<List<Garden>> = flowOf(emptyList())
    override suspend fun getGardenById(id: Long): Garden? = null
    override suspend fun insertGarden(garden: Garden): Long = 0
    override suspend fun updateGarden(garden: Garden) {}
    override suspend fun deleteGarden(garden: Garden) {}

    override fun getAllGrowingSpaces(): Flow<List<GrowingSpace>> = spacesFlow.asStateFlow()
    override suspend fun getGrowingSpaceById(id: Long): GrowingSpace? = spacesFlow.value.firstOrNull { it.id == id }
    override fun getGrowingSpacesForGarden(gardenId: Long): Flow<List<GrowingSpace>> = flowOf(spacesFlow.value)
    override suspend fun insertGrowingSpace(space: GrowingSpace): Long { spacesFlow.value = spacesFlow.value + space; return space.id }
    override suspend fun updateGrowingSpace(space: GrowingSpace) { spacesFlow.value = spacesFlow.value.map { if (it.id == space.id) space else it } }
    override suspend fun deleteGrowingSpace(space: GrowingSpace) { spacesFlow.value = spacesFlow.value - space }

    override fun getAllSeeds(): Flow<List<Seed>> = seedsFlow.asStateFlow()
    override suspend fun getSeedById(id: Long): Seed? = seedsFlow.value.firstOrNull { it.id == id }
    override fun getSeedsForGarden(gardenId: Long): Flow<List<Seed>> = flowOf(seedsFlow.value)
    override suspend fun insertSeed(seed: Seed): Long { seedsFlow.value = seedsFlow.value + seed; return seed.id }
    override suspend fun updateSeed(seed: Seed) { seedsFlow.value = seedsFlow.value.map { if (it.id == seed.id) seed else it } }
    override suspend fun deleteSeed(seed: Seed) { seedsFlow.value = seedsFlow.value - seed }

    override fun getAllDesires(): Flow<List<Desire>> = desiresFlow.asStateFlow()
    override suspend fun getDesireById(id: Long): Desire? = desiresFlow.value.firstOrNull { it.id == id }
    override fun getDesiresForGarden(gardenId: Long): Flow<List<Desire>> = flowOf(desiresFlow.value)
    override suspend fun insertDesire(desire: Desire): Long { desiresFlow.value = desiresFlow.value + desire; return desire.id }
    override suspend fun updateDesire(desire: Desire) { desiresFlow.value = desiresFlow.value.map { if (it.id == desire.id) desire else it } }
    override suspend fun deleteDesire(desire: Desire) { desiresFlow.value = desiresFlow.value - desire }

    override fun getAllOccupancies(): Flow<List<Occupancy>> = occupanciesFlow.asStateFlow()
    override suspend fun getOccupancyById(id: Long): Occupancy? = occupanciesFlow.value.firstOrNull { it.id == id }
    override fun getOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>> = flowOf(occupanciesFlow.value.filter { it.growingSpaceId == spaceId })
    override fun getActiveOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>> = flowOf(occupanciesFlow.value.filter { it.growingSpaceId == spaceId && it.status == OccupancyStatus.ACTIVE.name })
    override suspend fun insertOccupancy(occupancy: Occupancy): Long { occupanciesFlow.value = occupanciesFlow.value + occupancy; return occupancy.id }
    override suspend fun updateOccupancy(occupancy: Occupancy) { occupanciesFlow.value = occupanciesFlow.value.map { if (it.id == occupancy.id) occupancy else it } }
    override suspend fun deleteOccupancy(occupancy: Occupancy) { occupanciesFlow.value = occupanciesFlow.value - occupancy }

    override fun getAllPlannedPlantings(): Flow<List<PlannedPlanting>> = flowOf(emptyList())
    override suspend fun getPlannedPlantingById(id: Long): PlannedPlanting? = null
    override fun getPlannedPlantingsForGarden(gardenId: Long): Flow<List<PlannedPlanting>> = flowOf(emptyList())
    override fun getPlannedPlantingsForSpace(spaceId: Long): Flow<List<PlannedPlanting>> = flowOf(emptyList())
    override suspend fun insertPlannedPlanting(plan: PlannedPlanting): Long = 0
    override suspend fun updatePlannedPlanting(plan: PlannedPlanting) {}
    override suspend fun deletePlannedPlanting(plan: PlannedPlanting) {}

    override fun getAllPlants(): Flow<List<Plant>> = plantsFlow.asStateFlow()
    override suspend fun getPlantById(id: Long): Plant? = plantsFlow.value.firstOrNull { it.id == id }
    override suspend fun insertPlant(plant: Plant): Long { plantsFlow.value = plantsFlow.value + plant; return plant.id }
    override suspend fun updatePlant(plant: Plant) { plantsFlow.value = plantsFlow.value.map { if (it.id == plant.id) plant else it } }
    override suspend fun deletePlant(plant: Plant) { plantsFlow.value = plantsFlow.value - plant }
    override fun getPhotosForPlant(plantId: Long): Flow<List<PlantPhoto>> = flowOf(emptyList())
    override suspend fun insertPhoto(photo: PlantPhoto): Long { return 0 }
    override suspend fun deletePhoto(photo: PlantPhoto) {}
    override fun getJournalEntriesForPlant(plantId: Long): Flow<List<JournalEntry>> = flowOf(emptyList())
    override suspend fun getJournalEntryById(id: Long): JournalEntry? = null
    override suspend fun insertJournalEntry(entry: JournalEntry): Long { return 0 }
    override suspend fun updateJournalEntry(entry: JournalEntry) {}
    override suspend fun deleteJournalEntry(entry: JournalEntry) {}
    override fun getAllHarvests(): Flow<List<Harvest>> = flowOf(emptyList())
    override fun getHarvestsForPlant(plantId: Long): Flow<List<Harvest>> = flowOf(emptyList())
    override suspend fun insertHarvest(harvest: Harvest): Long = 0
    override suspend fun updateHarvest(harvest: Harvest) {}
    override suspend fun deleteHarvest(harvest: Harvest) {}
}
