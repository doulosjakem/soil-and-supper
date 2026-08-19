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

interface GardenRepository {
    fun getAllGardens(): Flow<List<Garden>>
    suspend fun getGardenById(id: Long): Garden?
    suspend fun insertGarden(garden: Garden): Long
    suspend fun updateGarden(garden: Garden)
    suspend fun deleteGarden(garden: Garden)

    fun getAllGrowingSpaces(): Flow<List<GrowingSpace>>
    suspend fun getGrowingSpaceById(id: Long): GrowingSpace?
    fun getGrowingSpacesForGarden(gardenId: Long): Flow<List<GrowingSpace>>
    suspend fun insertGrowingSpace(space: GrowingSpace): Long
    suspend fun updateGrowingSpace(space: GrowingSpace)
    suspend fun deleteGrowingSpace(space: GrowingSpace)

    fun getAllSeeds(): Flow<List<Seed>>
    suspend fun getSeedById(id: Long): Seed?
    fun getSeedsForGarden(gardenId: Long): Flow<List<Seed>>
    suspend fun insertSeed(seed: Seed): Long
    suspend fun updateSeed(seed: Seed)
    suspend fun deleteSeed(seed: Seed)

    fun getAllDesires(): Flow<List<Desire>>
    suspend fun getDesireById(id: Long): Desire?
    fun getDesiresForGarden(gardenId: Long): Flow<List<Desire>>
    suspend fun insertDesire(desire: Desire): Long
    suspend fun updateDesire(desire: Desire)
    suspend fun deleteDesire(desire: Desire)

    fun getAllOccupancies(): Flow<List<Occupancy>>
    suspend fun getOccupancyById(id: Long): Occupancy?
    fun getOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>>
    fun getActiveOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>>
    suspend fun insertOccupancy(occupancy: Occupancy): Long
    suspend fun updateOccupancy(occupancy: Occupancy)
    suspend fun deleteOccupancy(occupancy: Occupancy)

    fun getAllPlannedPlantings(): Flow<List<PlannedPlanting>>
    suspend fun getPlannedPlantingById(id: Long): PlannedPlanting?
    fun getPlannedPlantingsForGarden(gardenId: Long): Flow<List<PlannedPlanting>>
    fun getPlannedPlantingsForSpace(spaceId: Long): Flow<List<PlannedPlanting>>
    suspend fun insertPlannedPlanting(plan: PlannedPlanting): Long
    suspend fun updatePlannedPlanting(plan: PlannedPlanting)
    suspend fun deletePlannedPlanting(plan: PlannedPlanting)
}

