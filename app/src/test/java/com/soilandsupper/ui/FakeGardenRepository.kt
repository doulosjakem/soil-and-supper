package com.soilandsupper.ui

import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.repository.PlantRepository
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.Garden
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Harvest
import com.soilandsupper.shared.domain.model.JournalEntry
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.PlantPhoto
import com.soilandsupper.shared.domain.model.PlannedPlanting
import com.soilandsupper.shared.domain.model.Seed
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map

class FakeGardenRepository(
    private val initialGardens: List<Garden> = emptyList(),
    private val initialSpaces: List<GrowingSpace> = emptyList(),
    private val initialSeeds: List<Seed> = emptyList(),
    private val initialDesires: List<Desire> = emptyList(),
    private val initialOccupancies: List<Occupancy> = emptyList(),
    private val initialPlants: List<Plant> = emptyList(),
    private val initialHarvests: List<Harvest> = emptyList(),
    private val initialJournalEntries: List<JournalEntry> = emptyList(),
    private val initialPhotos: List<PlantPhoto> = emptyList()
) : GardenRepository, PlantRepository {

    private val gardensFlow = MutableStateFlow(initialGardens)
    private val spacesFlow = MutableStateFlow(initialSpaces)
    private val seedsFlow = MutableStateFlow(initialSeeds)
    private val desiresFlow = MutableStateFlow(initialDesires)
    private val occupanciesFlow = MutableStateFlow(initialOccupancies)
    private val plantsFlow = MutableStateFlow(initialPlants)
    private val harvestsFlow = MutableStateFlow(initialHarvests)
    private val journalEntriesFlow = MutableStateFlow(initialJournalEntries)
    private val photosFlow = MutableStateFlow(initialPhotos)

    fun setGardens(gardens: List<Garden>) { gardensFlow.value = gardens }
    fun setSpaces(spaces: List<GrowingSpace>) { spacesFlow.value = spaces }
    fun setSeeds(seeds: List<Seed>) { seedsFlow.value = seeds }
    fun setDesires(desires: List<Desire>) { desiresFlow.value = desires }
    fun setOccupancies(occupancies: List<Occupancy>) { occupanciesFlow.value = occupancies }
    fun setPlants(plants: List<Plant>) { plantsFlow.value = plants }
    fun setHarvests(harvests: List<Harvest>) { harvestsFlow.value = harvests }
    fun setJournalEntries(entries: List<JournalEntry>) { journalEntriesFlow.value = entries }
    fun setPhotos(photos: List<PlantPhoto>) { photosFlow.value = photos }

    override fun getAllGardens(): Flow<List<Garden>> = gardensFlow.asStateFlow()
    override suspend fun getGardenById(id: Long): Garden? = initialGardens.firstOrNull { it.id == id }
    override suspend fun insertGarden(garden: Garden): Long = throw UnsupportedOperationException()
    override suspend fun updateGarden(garden: Garden) { throw UnsupportedOperationException() }
    override suspend fun deleteGarden(garden: Garden) { throw UnsupportedOperationException() }

    override fun getAllGrowingSpaces(): Flow<List<GrowingSpace>> = spacesFlow.asStateFlow()
    override suspend fun getGrowingSpaceById(id: Long): GrowingSpace? = initialSpaces.firstOrNull { it.id == id }
    override fun getGrowingSpacesForGarden(gardenId: Long): Flow<List<GrowingSpace>> = throw UnsupportedOperationException()
    override suspend fun insertGrowingSpace(space: GrowingSpace): Long = throw UnsupportedOperationException()
    override suspend fun updateGrowingSpace(space: GrowingSpace) { throw UnsupportedOperationException() }
    override suspend fun deleteGrowingSpace(space: GrowingSpace) { throw UnsupportedOperationException() }

    override fun getAllSeeds(): Flow<List<Seed>> = seedsFlow.asStateFlow()
    override suspend fun getSeedById(id: Long): Seed? = initialSeeds.firstOrNull { it.id == id }
    override fun getSeedsForGarden(gardenId: Long): Flow<List<Seed>> = throw UnsupportedOperationException()
    override suspend fun insertSeed(seed: Seed): Long = throw UnsupportedOperationException()
    override suspend fun updateSeed(seed: Seed) { throw UnsupportedOperationException() }
    override suspend fun deleteSeed(seed: Seed) { throw UnsupportedOperationException() }

    override fun getAllDesires(): Flow<List<Desire>> = desiresFlow.asStateFlow()
    override suspend fun getDesireById(id: Long): Desire? = initialDesires.firstOrNull { it.id == id }
    override fun getDesiresForGarden(gardenId: Long): Flow<List<Desire>> = throw UnsupportedOperationException()
    override suspend fun insertDesire(desire: Desire): Long = throw UnsupportedOperationException()
    override suspend fun updateDesire(desire: Desire) { throw UnsupportedOperationException() }
    override suspend fun deleteDesire(desire: Desire) { throw UnsupportedOperationException() }

    override fun getAllOccupancies(): Flow<List<Occupancy>> = occupanciesFlow.asStateFlow()
    override suspend fun getOccupancyById(id: Long): Occupancy? = initialOccupancies.firstOrNull { it.id == id }
    override fun getOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>> = throw UnsupportedOperationException()
    override fun getActiveOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>> = throw UnsupportedOperationException()
    override suspend fun insertOccupancy(occupancy: Occupancy): Long = throw UnsupportedOperationException()
    override suspend fun updateOccupancy(occupancy: Occupancy) { throw UnsupportedOperationException() }
    override suspend fun deleteOccupancy(occupancy: Occupancy) { throw UnsupportedOperationException() }

    override fun getAllPlannedPlantings(): Flow<List<PlannedPlanting>> = throw UnsupportedOperationException()
    override suspend fun getPlannedPlantingById(id: Long): PlannedPlanting? = throw UnsupportedOperationException()
    override fun getPlannedPlantingsForGarden(gardenId: Long): Flow<List<PlannedPlanting>> = throw UnsupportedOperationException()
    override suspend fun insertPlannedPlanting(plan: PlannedPlanting): Long = throw UnsupportedOperationException()
    override suspend fun updatePlannedPlanting(plan: PlannedPlanting) = throw UnsupportedOperationException()
    override suspend fun deletePlannedPlanting(plan: PlannedPlanting) = throw UnsupportedOperationException()
    override fun getPlannedPlantingsForSpace(spaceId: Long): Flow<List<PlannedPlanting>> = throw UnsupportedOperationException()

    override fun getAllPlants(): Flow<List<Plant>> = plantsFlow.asStateFlow()
    override suspend fun getPlantById(id: Long): Plant? = initialPlants.firstOrNull { it.id == id }
    override suspend fun insertPlant(plant: Plant): Long = throw UnsupportedOperationException()
    override suspend fun updatePlant(plant: Plant) { throw UnsupportedOperationException() }
    override suspend fun deletePlant(plant: Plant) { throw UnsupportedOperationException() }

    override fun getPhotosForPlant(plantId: Long): Flow<List<PlantPhoto>> = throw UnsupportedOperationException()
    override suspend fun insertPhoto(photo: PlantPhoto) = throw UnsupportedOperationException()
    override suspend fun deletePhoto(photo: PlantPhoto) = throw UnsupportedOperationException()

    override fun getJournalEntriesForPlant(plantId: Long): Flow<List<JournalEntry>> =
        journalEntriesFlow.map { entries -> entries.filter { it.plantId == plantId } }

    override suspend fun getJournalEntryById(id: Long): JournalEntry? =
        journalEntriesFlow.value.firstOrNull { it.id == id }

    override suspend fun insertJournalEntry(entry: JournalEntry): Long = throw UnsupportedOperationException()
    override suspend fun updateJournalEntry(entry: JournalEntry) = throw UnsupportedOperationException()
    override suspend fun deleteJournalEntry(entry: JournalEntry) = throw UnsupportedOperationException()

    override fun getAllHarvests(): Flow<List<Harvest>> = throw UnsupportedOperationException()
    override fun getHarvestsForPlant(plantId: Long): Flow<List<Harvest>> = throw UnsupportedOperationException()
    override suspend fun insertHarvest(harvest: Harvest): Long = throw UnsupportedOperationException()
    override suspend fun updateHarvest(harvest: Harvest) = throw UnsupportedOperationException()
    override suspend fun deleteHarvest(harvest: Harvest) = throw UnsupportedOperationException()
}
