package com.soilandsupper.data.repository

import com.soilandsupper.data.local.dao.HarvestDao
import com.soilandsupper.data.local.dao.JournalEntryDao
import com.soilandsupper.data.local.dao.PlantDao
import com.soilandsupper.data.local.dao.PlantPhotoDao
import com.soilandsupper.domain.model.Harvest
import com.soilandsupper.domain.model.JournalEntry
import com.soilandsupper.domain.model.Plant
import com.soilandsupper.domain.model.PlantPhoto
import kotlinx.coroutines.flow.Flow

class PlantRepository(
    private val plantDao: PlantDao,
    private val plantPhotoDao: PlantPhotoDao,
    private val journalEntryDao: JournalEntryDao,
    private val harvestDao: HarvestDao
) {
    fun getAllPlants(): Flow<List<Plant>> = plantDao.getAllPlants()

    suspend fun getPlantById(id: Long): Plant? = plantDao.getPlantById(id)

    suspend fun insertPlant(plant: Plant): Long = plantDao.insertPlant(plant)

    suspend fun updatePlant(plant: Plant) = plantDao.updatePlant(plant)

    suspend fun deletePlant(plant: Plant) = plantDao.deletePlant(plant)

    fun getPhotosForPlant(plantId: Long): Flow<List<PlantPhoto>> =
        plantPhotoDao.getPhotosForPlant(plantId)

    suspend fun insertPhoto(photo: PlantPhoto): Long = plantPhotoDao.insertPhoto(photo)

    suspend fun deletePhoto(photo: PlantPhoto) = plantPhotoDao.deletePhoto(photo)

    fun getJournalEntriesForPlant(plantId: Long): Flow<List<JournalEntry>> =
        journalEntryDao.getJournalEntriesForPlant(plantId)

    suspend fun insertJournalEntry(entry: JournalEntry): Long =
        journalEntryDao.insertJournalEntry(entry)

    suspend fun updateJournalEntry(entry: JournalEntry) =
        journalEntryDao.updateJournalEntry(entry)

    suspend fun deleteJournalEntry(entry: JournalEntry) =
        journalEntryDao.deleteJournalEntry(entry)

    fun getAllHarvests(): Flow<List<Harvest>> = harvestDao.getAllHarvests()

    fun getHarvestsForPlant(plantId: Long): Flow<List<Harvest>> =
        harvestDao.getHarvestsForPlant(plantId)

    suspend fun insertHarvest(harvest: Harvest): Long = harvestDao.insertHarvest(harvest)

    suspend fun updateHarvest(harvest: Harvest) = harvestDao.updateHarvest(harvest)

    suspend fun deleteHarvest(harvest: Harvest) = harvestDao.deleteHarvest(harvest)
}
