package com.soilandsupper.data.repository

import com.soilandsupper.data.local.dao.DesireDao
import com.soilandsupper.data.local.dao.GardenDao
import com.soilandsupper.data.local.dao.GrowingSpaceDao
import com.soilandsupper.data.local.dao.HarvestDao
import com.soilandsupper.data.local.dao.JournalEntryDao
import com.soilandsupper.data.local.dao.OccupancyDao
import com.soilandsupper.data.local.dao.PlantDao
import com.soilandsupper.data.local.dao.PlantPhotoDao
import com.soilandsupper.data.local.dao.PlannedPlantingDao
import com.soilandsupper.data.local.dao.SeedDao
import com.soilandsupper.domain.model.Desire
import com.soilandsupper.domain.model.Garden
import com.soilandsupper.domain.model.GrowingSpace
import com.soilandsupper.domain.model.Harvest
import com.soilandsupper.domain.model.JournalEntry
import com.soilandsupper.domain.model.Occupancy
import com.soilandsupper.domain.model.Plant
import com.soilandsupper.domain.model.PlantPhoto
import com.soilandsupper.domain.model.PlannedPlanting
import com.soilandsupper.domain.model.Seed
import kotlinx.coroutines.flow.Flow

class GardenRepository(
    private val gardenDao: GardenDao,
    private val growingSpaceDao: GrowingSpaceDao,
    private val plantDao: PlantDao,
    private val plantPhotoDao: PlantPhotoDao,
    private val journalEntryDao: JournalEntryDao,
    private val harvestDao: HarvestDao,
    private val occupancyDao: OccupancyDao,
    private val seedDao: SeedDao,
    private val desireDao: DesireDao,
    private val plannedPlantingDao: PlannedPlantingDao
) {
    // Garden
    fun getAllGardens(): Flow<List<Garden>> = gardenDao.getAllGardens()
    suspend fun getGardenById(id: Long): Garden? = gardenDao.getGardenById(id)
    suspend fun insertGarden(garden: Garden): Long = gardenDao.insertGarden(garden)
    suspend fun updateGarden(garden: Garden) = gardenDao.updateGarden(garden)
    suspend fun deleteGarden(garden: Garden) = gardenDao.deleteGarden(garden)

    // GrowingSpaces
    fun getAllGrowingSpaces(): Flow<List<GrowingSpace>> = growingSpaceDao.getAllGrowingSpaces()
    suspend fun getGrowingSpaceById(id: Long): GrowingSpace? = growingSpaceDao.getGrowingSpaceById(id)
    fun getGrowingSpacesForGarden(gardenId: Long): Flow<List<GrowingSpace>> =
        growingSpaceDao.getGrowingSpacesForGarden(gardenId)
    suspend fun insertGrowingSpace(space: GrowingSpace): Long = growingSpaceDao.insertGrowingSpace(space)
    suspend fun updateGrowingSpace(space: GrowingSpace) = growingSpaceDao.updateGrowingSpace(space)
    suspend fun deleteGrowingSpace(space: GrowingSpace) = growingSpaceDao.deleteGrowingSpace(space)

    // Plants
    fun getAllPlants(): Flow<List<Plant>> = plantDao.getAllPlants()
    suspend fun getPlantById(id: Long): Plant? = plantDao.getPlantById(id)
    suspend fun insertPlant(plant: Plant): Long = plantDao.insertPlant(plant)
    suspend fun updatePlant(plant: Plant) = plantDao.updatePlant(plant)
    suspend fun deletePlant(plant: Plant) = plantDao.deletePlant(plant)

    // Photos
    fun getPhotosForPlant(plantId: Long): Flow<List<PlantPhoto>> =
        plantPhotoDao.getPhotosForPlant(plantId)
    suspend fun insertPhoto(photo: PlantPhoto): Long = plantPhotoDao.insertPhoto(photo)
    suspend fun deletePhoto(photo: PlantPhoto) = plantPhotoDao.deletePhoto(photo)

    // Journals
    fun getJournalEntriesForPlant(plantId: Long): Flow<List<JournalEntry>> =
        journalEntryDao.getJournalEntriesForPlant(plantId)
    suspend fun insertJournalEntry(entry: JournalEntry): Long =
        journalEntryDao.insertJournalEntry(entry)
    suspend fun updateJournalEntry(entry: JournalEntry) =
        journalEntryDao.updateJournalEntry(entry)
    suspend fun deleteJournalEntry(entry: JournalEntry) = journalEntryDao.deleteJournalEntry(entry)

    // Harvests
    fun getAllHarvests(): Flow<List<Harvest>> = harvestDao.getAllHarvests()
    fun getHarvestsForPlant(plantId: Long): Flow<List<Harvest>> =
        harvestDao.getHarvestsForPlant(plantId)
    suspend fun insertHarvest(harvest: Harvest): Long = harvestDao.insertHarvest(harvest)
    suspend fun updateHarvest(harvest: Harvest) = harvestDao.updateHarvest(harvest)
    suspend fun deleteHarvest(harvest: Harvest) = harvestDao.deleteHarvest(harvest)

    // Occupancies
    fun getAllOccupancies(): Flow<List<Occupancy>> = occupancyDao.getAllOccupancies()
    suspend fun getOccupancyById(id: Long): Occupancy? = occupancyDao.getOccupancyById(id)
    fun getOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>> =
        occupancyDao.getOccupanciesForSpace(spaceId)
    fun getActiveOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>> =
        occupancyDao.getActiveOccupanciesForSpace(spaceId)
    suspend fun insertOccupancy(occupancy: Occupancy): Long = occupancyDao.insertOccupancy(occupancy)
    suspend fun updateOccupancy(occupancy: Occupancy) = occupancyDao.updateOccupancy(occupancy)
    suspend fun deleteOccupancy(occupancy: Occupancy) = occupancyDao.deleteOccupancy(occupancy)

    // Seeds
    fun getAllSeeds(): Flow<List<Seed>> = seedDao.getAllSeeds()
    suspend fun getSeedById(id: Long): Seed? = seedDao.getSeedById(id)
    fun getSeedsForGarden(gardenId: Long): Flow<List<Seed>> = seedDao.getSeedsForGarden(gardenId)
    suspend fun insertSeed(seed: Seed): Long = seedDao.insertSeed(seed)
    suspend fun updateSeed(seed: Seed) = seedDao.updateSeed(seed)
    suspend fun deleteSeed(seed: Seed) = seedDao.deleteSeed(seed)

    // Desires
    fun getAllDesires(): Flow<List<Desire>> = desireDao.getAllDesires()
    suspend fun getDesireById(id: Long): Desire? = desireDao.getDesireById(id)
    fun getDesiresForGarden(gardenId: Long): Flow<List<Desire>> = desireDao.getDesiresForGarden(gardenId)
    suspend fun insertDesire(desire: Desire): Long = desireDao.insertDesire(desire)
    suspend fun updateDesire(desire: Desire) = desireDao.updateDesire(desire)
    suspend fun deleteDesire(desire: Desire) = desireDao.deleteDesire(desire)

    // PlannedPlantings
    fun getAllPlannedPlantings(): Flow<List<PlannedPlanting>> = plannedPlantingDao.getAllPlantedPlantings()
    suspend fun getPlannedPlantingById(id: Long): PlannedPlanting? = plannedPlantingDao.getPlannedPlantingById(id)
    fun getPlannedPlantingsForGarden(gardenId: Long): Flow<List<PlannedPlanting>> =
        plannedPlantingDao.getPlannedPlantingsForGarden(gardenId)
    fun getPlannedPlantingsForSpace(spaceId: Long): Flow<List<PlannedPlanting>> =
        plannedPlantingDao.getPlannedPlantingsForSpace(spaceId)
    suspend fun insertPlannedPlanting(plan: PlannedPlanting): Long = plannedPlantingDao.insertPlannedPlanting(plan)
    suspend fun updatePlannedPlanting(plan: PlannedPlanting) = plannedPlantingDao.updatePlannedPlanting(plan)
    suspend fun deletePlannedPlanting(plan: PlannedPlanting) = plannedPlantingDao.deletePlannedPlanting(plan)
}
