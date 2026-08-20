package com.soilandsupper.ui

import com.soilandsupper.repository.GardenRepository
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

class FakeGardenRepository(
    private val initialGardens: List<Garden> = emptyList(),
    private val initialSpaces: List<GrowingSpace> = emptyList(),
    private val initialSeeds: List<Seed> = emptyList(),
    private val initialDesires: List<Desire> = emptyList(),
    private val initialOccupancies: List<Occupancy> = emptyList()
) : GardenRepository {

    private val gardensFlow = MutableStateFlow(initialGardens)
    private val spacesFlow = MutableStateFlow(initialSpaces)
    private val seedsFlow = MutableStateFlow(initialSeeds)
    private val desiresFlow = MutableStateFlow(initialDesires)
    private val occupanciesFlow = MutableStateFlow(initialOccupancies)

    fun setGardens(gardens: List<Garden>) { gardensFlow.value = gardens }
    fun setSpaces(spaces: List<GrowingSpace>) { spacesFlow.value = spaces }
    fun setSeeds(seeds: List<Seed>) { seedsFlow.value = seeds }
    fun setDesires(desires: List<Desire>) { desiresFlow.value = desires }
    fun setOccupancies(occupancies: List<Occupancy>) { occupanciesFlow.value = occupancies }

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
    override fun getPlannedPlantingsForSpace(spaceId: Long): Flow<List<PlannedPlanting>> = throw UnsupportedOperationException()
    override suspend fun insertPlannedPlanting(plan: PlannedPlanting): Long = throw UnsupportedOperationException()
    override suspend fun updatePlannedPlanting(plan: PlannedPlanting) { throw UnsupportedOperationException() }
    override suspend fun deletePlannedPlanting(plan: PlannedPlanting) { throw UnsupportedOperationException() }
}
