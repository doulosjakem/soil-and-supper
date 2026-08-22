package com.soilandsupper.repository

import com.soilandsupper.shared.domain.model.Harvest
import com.soilandsupper.shared.domain.model.JournalEntry
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.PlantPhoto
import kotlinx.coroutines.flow.Flow

interface PlantRepository {
    fun getAllPlants(): Flow<List<Plant>>

    suspend fun getPlantById(id: Long): Plant?

    suspend fun insertPlant(plant: Plant): Long

    suspend fun updatePlant(plant: Plant)

    suspend fun deletePlant(plant: Plant)

    fun getPhotosForPlant(plantId: Long): Flow<List<PlantPhoto>>

    suspend fun insertPhoto(photo: PlantPhoto): Long

    suspend fun deletePhoto(photo: PlantPhoto)

    fun getJournalEntriesForPlant(plantId: Long): Flow<List<JournalEntry>>

    suspend fun getJournalEntryById(id: Long): JournalEntry?

    suspend fun insertJournalEntry(entry: JournalEntry): Long

    suspend fun updateJournalEntry(entry: JournalEntry)

    suspend fun deleteJournalEntry(entry: JournalEntry)

    fun getAllHarvests(): Flow<List<Harvest>>

    fun getHarvestsForPlant(plantId: Long): Flow<List<Harvest>>

    suspend fun insertHarvest(harvest: Harvest): Long

    suspend fun updateHarvest(harvest: Harvest)

    suspend fun deleteHarvest(harvest: Harvest)
}
