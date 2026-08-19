package com.soilandsupper.repository

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

/**
 * Temporary in-memory repository for iOS UI verification.
 *
 * This implementation is NOT a persistence layer. It exists solely to prove
 * that the shared Compose UI can render on iOS without a real backend.
 *
 * MUST be replaced with a real iOS persistence implementation before any
 * production iOS use.
 */
class IosGardenRepository : GardenRepository, PlantRepository {
    private val gardens = MutableStateFlow<List<Garden>>(emptyList())
    private val growingSpaces = MutableStateFlow<List<GrowingSpace>>(emptyList())
    private val plants = MutableStateFlow<List<Plant>>(emptyList())
    private val plantPhotos = MutableStateFlow<List<PlantPhoto>>(emptyList())
    private val journalEntries = MutableStateFlow<List<JournalEntry>>(emptyList())
    private val harvests = MutableStateFlow<List<Harvest>>(emptyList())
    private val occupancies = MutableStateFlow<List<Occupancy>>(emptyList())
    private val seeds = MutableStateFlow<List<Seed>>(emptyList())
    private val desires = MutableStateFlow<List<Desire>>(emptyList())
    private val plannedPlantings = MutableStateFlow<List<PlannedPlanting>>(emptyList())

    override fun getAllGardens(): Flow<List<Garden>> = gardens.asStateFlow()
    override suspend fun getGardenById(id: Long): Garden? = gardens.value.firstOrNull { it.id == id }
    override suspend fun insertGarden(garden: Garden): Long {
        val newGarden = garden.copy(id = System.currentTimeMillis())
        gardens.value = gardens.value + newGarden
        return newGarden.id
    }
    override suspend fun updateGarden(garden: Garden) {
        gardens.value = gardens.value.map { if (it.id == garden.id) garden else it }
    }
    override suspend fun deleteGarden(garden: Garden) {
        gardens.value = gardens.value - garden
    }

    override fun getAllGrowingSpaces(): Flow<List<GrowingSpace>> = growingSpaces.asStateFlow()
    override suspend fun getGrowingSpaceById(id: Long): GrowingSpace? = growingSpaces.value.firstOrNull { it.id == id }
    override fun getGrowingSpacesForGarden(gardenId: Long): Flow<List<GrowingSpace>> = growingSpaces
    override suspend fun insertGrowingSpace(space: GrowingSpace): Long {
        val newSpace = space.copy(id = System.currentTimeMillis())
        growingSpaces.value = growingSpaces.value + newSpace
        return newSpace.id
    }
    override suspend fun updateGrowingSpace(space: GrowingSpace) {
        growingSpaces.value = growingSpaces.value.map { if (it.id == space.id) space else it }
    }
    override suspend fun deleteGrowingSpace(space: GrowingSpace) {
        growingSpaces.value = growingSpaces.value - space
    }

    override fun getAllPlants(): Flow<List<Plant>> = plants.asStateFlow()
    override suspend fun getPlantById(id: Long): Plant? = plants.value.firstOrNull { it.id == id }
    override suspend fun insertPlant(plant: Plant): Long {
        val newPlant = plant.copy(id = System.currentTimeMillis())
        plants.value = plants.value + newPlant
        return newPlant.id
    }
    override suspend fun updatePlant(plant: Plant) {
        plants.value = plants.value.map { if (it.id == plant.id) plant else it }
    }
    override suspend fun deletePlant(plant: Plant) {
        plants.value = plants.value - plant
    }

    override fun getPhotosForPlant(plantId: Long): Flow<List<PlantPhoto>> = plantPhotos
    override suspend fun insertPhoto(photo: PlantPhoto): Long {
        val newPhoto = photo.copy(id = System.currentTimeMillis())
        plantPhotos.value = plantPhotos.value + newPhoto
        return newPhoto.id
    }
    override suspend fun deletePhoto(photo: PlantPhoto) {
        plantPhotos.value = plantPhotos.value - photo
    }

    override fun getJournalEntriesForPlant(plantId: Long): Flow<List<JournalEntry>> = journalEntries
    override suspend fun insertJournalEntry(entry: JournalEntry): Long {
        val newEntry = entry.copy(id = System.currentTimeMillis())
        journalEntries.value = journalEntries.value + newEntry
        return newEntry.id
    }
    override suspend fun updateJournalEntry(entry: JournalEntry) {
        journalEntries.value = journalEntries.value.map { if (it.id == entry.id) entry else it }
    }
    override suspend fun deleteJournalEntry(entry: JournalEntry) {
        journalEntries.value = journalEntries.value - entry
    }

    override fun getAllHarvests(): Flow<List<Harvest>> = harvests.asStateFlow()
    override fun getHarvestsForPlant(plantId: Long): Flow<List<Harvest>> = harvests
    override suspend fun insertHarvest(harvest: Harvest): Long {
        val newHarvest = harvest.copy(id = System.currentTimeMillis())
        harvests.value = harvests.value + newHarvest
        return newHarvest.id
    }
    override suspend fun updateHarvest(harvest: Harvest) {
        harvests.value = harvests.value.map { if (it.id == harvest.id) harvest else it }
    }
    override suspend fun deleteHarvest(harvest: Harvest) {
        harvests.value = harvests.value - harvest
    }

    override fun getAllSeeds(): Flow<List<Seed>> = seeds.asStateFlow()
    override suspend fun getSeedById(id: Long): Seed? = seeds.value.firstOrNull { it.id == id }
    override fun getSeedsForGarden(gardenId: Long): Flow<List<Seed>> = seeds
    override suspend fun insertSeed(seed: Seed): Long {
        val newSeed = seed.copy(id = System.currentTimeMillis())
        seeds.value = seeds.value + newSeed
        return newSeed.id
    }
    override suspend fun updateSeed(seed: Seed) {
        seeds.value = seeds.value.map { if (it.id == seed.id) seed else it }
    }
    override suspend fun deleteSeed(seed: Seed) {
        seeds.value = seeds.value - seed
    }

    override fun getAllDesires(): Flow<List<Desire>> = desires.asStateFlow()
    override suspend fun getDesireById(id: Long): Desire? = desires.value.firstOrNull { it.id == id }
    override fun getDesiresForGarden(gardenId: Long): Flow<List<Desire>> = desires
    override suspend fun insertDesire(desire: Desire): Long {
        val newDesire = desire.copy(id = System.currentTimeMillis())
        desires.value = desires.value + newDesire
        return newDesire.id
    }
    override suspend fun updateDesire(desire: Desire) {
        desires.value = desires.value.map { if (it.id == desire.id) desire else it }
    }
    override suspend fun deleteDesire(desire: Desire) {
        desires.value = desires.value - desire
    }

    override fun getAllOccupancies(): Flow<List<Occupancy>> = occupancies.asStateFlow()
    override suspend fun getOccupancyById(id: Long): Occupancy? = occupancies.value.firstOrNull { it.id == id }
    override fun getOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>> = occupancies
    override fun getActiveOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>> = occupancies
    override suspend fun insertOccupancy(occupancy: Occupancy): Long {
        val newOccupancy = occupancy.copy(id = System.currentTimeMillis())
        occupancies.value = occupancies.value + newOccupancy
        return newOccupancy.id
    }
    override suspend fun updateOccupancy(occupancy: Occupancy) {
        occupancies.value = occupancies.value.map { if (it.id == occupancy.id) occupancy else it }
    }
    override suspend fun deleteOccupancy(occupancy: Occupancy) {
        occupancies.value = occupancies.value - occupancy
    }

    override fun getAllPlannedPlantings(): Flow<List<PlannedPlanting>> = plannedPlantings.asStateFlow()
    override suspend fun getPlannedPlantingById(id: Long): PlannedPlanting? = plannedPlantings.value.firstOrNull { it.id == id }
    override fun getPlannedPlantingsForGarden(gardenId: Long): Flow<List<PlannedPlanting>> = plannedPlantings
    override fun getPlannedPlantingsForSpace(spaceId: Long): Flow<List<PlannedPlanting>> = plannedPlantings
    override suspend fun insertPlannedPlanting(plan: PlannedPlanting): Long {
        val newPlan = plan.copy(id = System.currentTimeMillis())
        plannedPlantings.value = plannedPlantings.value + newPlan
        return newPlan.id
    }
    override suspend fun updatePlannedPlanting(plan: PlannedPlanting) {
        plannedPlantings.value = plannedPlantings.value.map { if (it.id == plan.id) plan else it }
    }
    override suspend fun deletePlannedPlanting(plan: PlannedPlanting) {
        plannedPlantings.value = plannedPlantings.value - plan
    }
}
