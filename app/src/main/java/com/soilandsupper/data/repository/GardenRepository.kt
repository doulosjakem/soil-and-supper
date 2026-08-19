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
import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.repository.PlantRepository
import com.soilandsupper.shared.domain.model.Desire as SharedDesire
import com.soilandsupper.shared.domain.model.Garden as SharedGarden
import com.soilandsupper.shared.domain.model.GrowingSpace as SharedGrowingSpace
import com.soilandsupper.shared.domain.model.Harvest as SharedHarvest
import com.soilandsupper.shared.domain.model.JournalEntry as SharedJournalEntry
import com.soilandsupper.shared.domain.model.Occupancy as SharedOccupancy
import com.soilandsupper.shared.domain.model.Plant as SharedPlant
import com.soilandsupper.shared.domain.model.PlantPhoto as SharedPlantPhoto
import com.soilandsupper.shared.domain.model.PlannedPlanting as SharedPlannedPlanting
import com.soilandsupper.shared.domain.model.Seed as SharedSeed
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

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
) : GardenRepository, PlantRepository {
    override fun getAllGardens(): Flow<List<SharedGarden>> =
        gardenDao.getAllGardens().map { list -> list.map { it.toShared() } }

    override suspend fun getGardenById(id: Long): SharedGarden? =
        gardenDao.getGardenById(id)?.toShared()

    override suspend fun insertGarden(garden: SharedGarden): Long =
        gardenDao.insertGarden(garden.toRoom())

    override suspend fun updateGarden(garden: SharedGarden) =
        gardenDao.updateGarden(garden.toRoom())

    override suspend fun deleteGarden(garden: SharedGarden) =
        gardenDao.deleteGarden(garden.toRoom())

    override fun getAllGrowingSpaces(): Flow<List<SharedGrowingSpace>> =
        growingSpaceDao.getAllGrowingSpaces().map { list -> list.map { it.toShared() } }

    override suspend fun getGrowingSpaceById(id: Long): SharedGrowingSpace? =
        growingSpaceDao.getGrowingSpaceById(id)?.toShared()

    override fun getGrowingSpacesForGarden(gardenId: Long): Flow<List<SharedGrowingSpace>> =
        growingSpaceDao.getGrowingSpacesForGarden(gardenId).map { list -> list.map { it.toShared() } }

    override suspend fun insertGrowingSpace(space: SharedGrowingSpace): Long =
        growingSpaceDao.insertGrowingSpace(space.toRoom())

    override suspend fun updateGrowingSpace(space: SharedGrowingSpace) =
        growingSpaceDao.updateGrowingSpace(space.toRoom())

    override suspend fun deleteGrowingSpace(space: SharedGrowingSpace) =
        growingSpaceDao.deleteGrowingSpace(space.toRoom())

    override fun getAllSeeds(): Flow<List<SharedSeed>> =
        seedDao.getAllSeeds().map { list -> list.map { it.toShared() } }

    override suspend fun getSeedById(id: Long): SharedSeed? =
        seedDao.getSeedById(id)?.toShared()

    override fun getSeedsForGarden(gardenId: Long): Flow<List<SharedSeed>> =
        seedDao.getSeedsForGarden(gardenId).map { list -> list.map { it.toShared() } }

    override suspend fun insertSeed(seed: SharedSeed): Long =
        seedDao.insertSeed(seed.toRoom())

    override suspend fun updateSeed(seed: SharedSeed) =
        seedDao.updateSeed(seed.toRoom())

    override suspend fun deleteSeed(seed: SharedSeed) =
        seedDao.deleteSeed(seed.toRoom())

    override fun getAllDesires(): Flow<List<SharedDesire>> =
        desireDao.getAllDesires().map { list -> list.map { it.toShared() } }

    override suspend fun getDesireById(id: Long): SharedDesire? =
        desireDao.getDesireById(id)?.toShared()

    override fun getDesiresForGarden(gardenId: Long): Flow<List<SharedDesire>> =
        desireDao.getDesiresForGarden(gardenId).map { list -> list.map { it.toShared() } }

    override suspend fun insertDesire(desire: SharedDesire): Long =
        desireDao.insertDesire(desire.toRoom())

    override suspend fun updateDesire(desire: SharedDesire) =
        desireDao.updateDesire(desire.toRoom())

    override suspend fun deleteDesire(desire: SharedDesire) =
        desireDao.deleteDesire(desire.toRoom())

    override fun getAllOccupancies(): Flow<List<SharedOccupancy>> =
        occupancyDao.getAllOccupancies().map { list -> list.map { it.toShared() } }

    override suspend fun getOccupancyById(id: Long): SharedOccupancy? =
        occupancyDao.getOccupancyById(id)?.toShared()

    override fun getOccupanciesForSpace(spaceId: Long): Flow<List<SharedOccupancy>> =
        occupancyDao.getOccupanciesForSpace(spaceId).map { list -> list.map { it.toShared() } }

    override fun getActiveOccupanciesForSpace(spaceId: Long): Flow<List<SharedOccupancy>> =
        occupancyDao.getActiveOccupanciesForSpace(spaceId).map { list -> list.map { it.toShared() } }

    override suspend fun insertOccupancy(occupancy: SharedOccupancy): Long =
        occupancyDao.insertOccupancy(occupancy.toRoom())

    override suspend fun updateOccupancy(occupancy: SharedOccupancy) =
        occupancyDao.updateOccupancy(occupancy.toRoom())

    override suspend fun deleteOccupancy(occupancy: SharedOccupancy) =
        occupancyDao.deleteOccupancy(occupancy.toRoom())

    override fun getAllPlannedPlantings(): Flow<List<SharedPlannedPlanting>> =
        plannedPlantingDao.getAllPlantedPlantings().map { list -> list.map { it.toShared() } }

    override suspend fun getPlannedPlantingById(id: Long): SharedPlannedPlanting? =
        plannedPlantingDao.getPlannedPlantingById(id)?.toShared()

    override fun getPlannedPlantingsForGarden(gardenId: Long): Flow<List<SharedPlannedPlanting>> =
        plannedPlantingDao.getPlannedPlantingsForGarden(gardenId).map { list -> list.map { it.toShared() } }

    override fun getPlannedPlantingsForSpace(spaceId: Long): Flow<List<SharedPlannedPlanting>> =
        plannedPlantingDao.getPlannedPlantingsForSpace(spaceId).map { list -> list.map { it.toShared() } }

    override suspend fun insertPlannedPlanting(plan: SharedPlannedPlanting): Long =
        plannedPlantingDao.insertPlannedPlanting(plan.toRoom())

    override suspend fun updatePlannedPlanting(plan: SharedPlannedPlanting) =
        plannedPlantingDao.updatePlannedPlanting(plan.toRoom())

    override suspend fun deletePlannedPlanting(plan: SharedPlannedPlanting) =
        plannedPlantingDao.deletePlannedPlanting(plan.toRoom())

    override fun getAllPlants(): Flow<List<SharedPlant>> =
        plantDao.getAllPlants().map { list -> list.map { it.toShared() } }

    override suspend fun getPlantById(id: Long): SharedPlant? =
        plantDao.getPlantById(id)?.toShared()

    override suspend fun insertPlant(plant: SharedPlant): Long =
        plantDao.insertPlant(plant.toRoom())

    override suspend fun updatePlant(plant: SharedPlant) =
        plantDao.updatePlant(plant.toRoom())

    override suspend fun deletePlant(plant: SharedPlant) =
        plantDao.deletePlant(plant.toRoom())

    override fun getPhotosForPlant(plantId: Long): Flow<List<SharedPlantPhoto>> =
        plantPhotoDao.getPhotosForPlant(plantId).map { list -> list.map { it.toShared() } }

    override suspend fun insertPhoto(photo: SharedPlantPhoto): Long =
        plantPhotoDao.insertPhoto(photo.toRoom())

    override suspend fun deletePhoto(photo: SharedPlantPhoto) =
        plantPhotoDao.deletePhoto(photo.toRoom())

    override fun getJournalEntriesForPlant(plantId: Long): Flow<List<SharedJournalEntry>> =
        journalEntryDao.getJournalEntriesForPlant(plantId).map { list -> list.map { it.toShared() } }

    override suspend fun insertJournalEntry(entry: SharedJournalEntry): Long =
        journalEntryDao.insertJournalEntry(entry.toRoom())

    override suspend fun updateJournalEntry(entry: SharedJournalEntry) =
        journalEntryDao.updateJournalEntry(entry.toRoom())

    override suspend fun deleteJournalEntry(entry: SharedJournalEntry) =
        journalEntryDao.deleteJournalEntry(entry.toRoom())

    override fun getAllHarvests(): Flow<List<SharedHarvest>> =
        harvestDao.getAllHarvests().map { list -> list.map { it.toShared() } }

    override fun getHarvestsForPlant(plantId: Long): Flow<List<SharedHarvest>> =
        harvestDao.getHarvestsForPlant(plantId).map { list -> list.map { it.toShared() } }

    override suspend fun insertHarvest(harvest: SharedHarvest): Long =
        harvestDao.insertHarvest(harvest.toRoom())

    override suspend fun updateHarvest(harvest: SharedHarvest) =
        harvestDao.updateHarvest(harvest.toRoom())

    override suspend fun deleteHarvest(harvest: SharedHarvest) =
        harvestDao.deleteHarvest(harvest.toRoom())
}

private fun Garden.toShared() = SharedGarden(
    id = id,
    name = name,
    location = location,
    climateZone = climateZone,
    averageLastFrostDate = averageLastFrostDate,
    averageFirstFrostDate = averageFirstFrostDate,
    createdAt = createdAt,
    updatedAt = updatedAt
)

private fun SharedGarden.toRoom() = Garden(
    id = id,
    name = name,
    location = location,
    climateZone = climateZone,
    averageLastFrostDate = averageLastFrostDate,
    averageFirstFrostDate = averageFirstFrostDate
)

private fun GrowingSpace.toShared() = SharedGrowingSpace(
    id = id,
    name = name,
    notes = notes,
    spaceType = spaceType,
    width = width,
    length = length,
    gardenId = gardenId,
    createdAt = createdAt,
    updatedAt = updatedAt
)

private fun SharedGrowingSpace.toRoom() = GrowingSpace(
    id = id,
    name = name,
    notes = notes,
    spaceType = spaceType,
    width = width,
    length = length,
    gardenId = gardenId
)

private fun Occupancy.toShared() = SharedOccupancy(
    id = id,
    cropName = cropName,
    variety = variety,
    startDate = startDate,
    endDate = endDate,
    expectedHarvestDate = expectedHarvestDate,
    expectedReleaseDate = expectedReleaseDate,
    status = status,
    notes = notes,
    growingSpaceId = growingSpaceId,
    plantId = plantId,
    plannedPlantingId = plannedPlantingId,
    createdAt = createdAt,
    updatedAt = updatedAt
)

private fun SharedOccupancy.toRoom() = Occupancy(
    id = id,
    cropName = cropName,
    variety = variety,
    startDate = startDate,
    endDate = endDate,
    expectedHarvestDate = expectedHarvestDate,
    expectedReleaseDate = expectedReleaseDate,
    status = status,
    notes = notes,
    growingSpaceId = growingSpaceId,
    plantId = plantId,
    plannedPlantingId = plannedPlantingId
)

private fun Seed.toShared() = SharedSeed(
    id = id,
    cropName = cropName,
    variety = variety,
    state = state,
    notes = notes,
    gardenId = gardenId,
    createdAt = createdAt,
    updatedAt = updatedAt
)

private fun SharedSeed.toRoom() = Seed(
    id = id,
    cropName = cropName,
    variety = variety,
    state = state,
    notes = notes,
    gardenId = gardenId
)

private fun Desire.toShared() = SharedDesire(
    id = id,
    cropName = cropName,
    variety = variety,
    notes = notes,
    isFulfilled = isFulfilled,
    isCancelled = isCancelled,
    isExpired = isExpired,
    gardenId = gardenId,
    createdAt = createdAt,
    updatedAt = updatedAt
)

private fun SharedDesire.toRoom() = Desire(
    id = id,
    cropName = cropName,
    variety = variety,
    notes = notes,
    isFulfilled = isFulfilled,
    isCancelled = isCancelled,
    isExpired = isExpired,
    gardenId = gardenId
)

private fun PlannedPlanting.toShared() = SharedPlannedPlanting(
    id = id,
    cropName = cropName,
    variety = variety,
    plannedDate = plannedDate,
    actualDate = actualDate,
    status = status,
    notes = notes,
    gardenId = gardenId,
    growingSpaceId = growingSpaceId,
    occupancyId = occupancyId,
    desireId = desireId,
    seedId = seedId,
    createdAt = createdAt,
    updatedAt = updatedAt
)

private fun SharedPlannedPlanting.toRoom() = PlannedPlanting(
    id = id,
    cropName = cropName,
    variety = variety,
    plannedDate = plannedDate,
    actualDate = actualDate,
    status = status,
    notes = notes,
    gardenId = gardenId,
    growingSpaceId = growingSpaceId,
    occupancyId = occupancyId,
    desireId = desireId,
    seedId = seedId
)

private fun Plant.toShared() = SharedPlant(
    id = id,
    name = name,
    variety = variety,
    plantingDate = plantingDate,
    location = location,
    notes = notes,
    createdAt = createdAt,
    updatedAt = updatedAt
)

private fun SharedPlant.toRoom() = Plant(
    id = id,
    name = name,
    variety = variety,
    plantingDate = plantingDate,
    location = location,
    notes = notes
)

private fun PlantPhoto.toShared() = SharedPlantPhoto(
    id = id,
    plantId = plantId,
    uri = uri,
    createdAt = createdAt
)

private fun SharedPlantPhoto.toRoom() = PlantPhoto(
    id = id,
    plantId = plantId,
    uri = uri
)

private fun JournalEntry.toShared() = SharedJournalEntry(
    id = id,
    plantId = plantId,
    date = date,
    text = text
)

private fun SharedJournalEntry.toRoom() = JournalEntry(
    id = id,
    plantId = plantId,
    date = date,
    text = text
)

private fun Harvest.toShared() = SharedHarvest(
    id = id,
    plantId = plantId,
    cropName = cropName,
    quantity = quantity,
    unit = unit,
    date = date,
    notes = notes
)

private fun SharedHarvest.toRoom() = Harvest(
    id = id,
    plantId = plantId,
    cropName = cropName,
    quantity = quantity,
    unit = unit,
    date = date,
    notes = notes
)
