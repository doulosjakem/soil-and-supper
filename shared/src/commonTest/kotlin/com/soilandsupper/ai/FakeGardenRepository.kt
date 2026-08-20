package com.soilandsupper.ai

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
import kotlinx.coroutines.flow.flowOf

class FakeGardenRepository(
    initialGardens: List<Garden> = emptyList(),
    initialSpaces: List<GrowingSpace> = emptyList(),
    initialSeeds: List<Seed> = emptyList(),
    initialDesires: List<Desire> = emptyList(),
    initialOccupancies: List<Occupancy> = emptyList(),
    initialPlants: List<Plant> = emptyList(),
    initialHarvests: List<Harvest> = emptyList(),
    initialJournalEntries: List<JournalEntry> = emptyList()
) : GardenRepository, PlantRepository {

    private var gardens = initialGardens.toMutableList()
    private var spaces = initialSpaces.toMutableList()
    private var seeds = initialSeeds.toMutableList()
    private var desires = initialDesires.toMutableList()
    private var occupancies = initialOccupancies.toMutableList()
    private var plants = initialPlants.toMutableList()
    private var harvests = initialHarvests.toMutableList()
    private var journalEntries = initialJournalEntries.toMutableList()

    var nextId = 1L
        private set

    fun nextId(): Long = nextId++

    fun setSpaces(newSpaces: List<GrowingSpace>) { spaces = newSpaces.toMutableList() }
    fun setOccupancies(newOccupancies: List<Occupancy>) { occupancies = newOccupancies.toMutableList() }
    fun setSeeds(newSeeds: List<Seed>) { seeds = newSeeds.toMutableList() }
    fun setDesires(newDesires: List<Desire>) { desires = newDesires.toMutableList() }
    fun setPlants(newPlants: List<Plant>) { plants = newPlants.toMutableList() }

    override fun getAllGardens(): Flow<List<Garden>> = flowOf(gardens.toList())
    override suspend fun getGardenById(id: Long): Garden? = gardens.firstOrNull { it.id == id }
    override suspend fun insertGarden(garden: Garden): Long { val id = nextId(); gardens.add(garden.copy(id = id)); return id }
    override suspend fun updateGarden(garden: Garden) { }
    override suspend fun deleteGarden(garden: Garden) { gardens.remove(garden) }

    override fun getAllGrowingSpaces(): Flow<List<GrowingSpace>> = flowOf(spaces.toList())
    override suspend fun getGrowingSpaceById(id: Long): GrowingSpace? = spaces.firstOrNull { it.id == id }
    override fun getGrowingSpacesForGarden(gardenId: Long): Flow<List<GrowingSpace>> = throw UnsupportedOperationException()
    override suspend fun insertGrowingSpace(space: GrowingSpace): Long { val id = nextId(); spaces.add(space.copy(id = id)); return id }
    override suspend fun updateGrowingSpace(space: GrowingSpace) { val idx = spaces.indexOfFirst { it.id == space.id }; if (idx >= 0) spaces[idx] = space }
    override suspend fun deleteGrowingSpace(space: GrowingSpace) { spaces.remove(space) }

    override fun getAllSeeds(): Flow<List<Seed>> = flowOf(seeds.toList())
    override suspend fun getSeedById(id: Long): Seed? = seeds.firstOrNull { it.id == id }
    override fun getSeedsForGarden(gardenId: Long): Flow<List<Seed>> = throw UnsupportedOperationException()
    override suspend fun insertSeed(seed: Seed): Long { val id = nextId(); seeds.add(seed.copy(id = id)); return id }
    override suspend fun updateSeed(seed: Seed) { val idx = seeds.indexOfFirst { it.id == seed.id }; if (idx >= 0) seeds[idx] = seed }
    override suspend fun deleteSeed(seed: Seed) { seeds.remove(seed) }

    override fun getAllDesires(): Flow<List<Desire>> = flowOf(desires.toList())
    override suspend fun getDesireById(id: Long): Desire? = desires.firstOrNull { it.id == id }
    override fun getDesiresForGarden(gardenId: Long): Flow<List<Desire>> = throw UnsupportedOperationException()
    override suspend fun insertDesire(desire: Desire): Long { val id = nextId(); desires.add(desire.copy(id = id)); return id }
    override suspend fun updateDesire(desire: Desire) { val idx = desires.indexOfFirst { it.id == desire.id }; if (idx >= 0) desires[idx] = desire }
    override suspend fun deleteDesire(desire: Desire) { desires.remove(desire) }

    override fun getAllOccupancies(): Flow<List<Occupancy>> = flowOf(occupancies.toList())
    override suspend fun getOccupancyById(id: Long): Occupancy? = occupancies.firstOrNull { it.id == id }
    override fun getOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>> = throw UnsupportedOperationException()
    override fun getActiveOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>> = throw UnsupportedOperationException()
    override suspend fun insertOccupancy(occupancy: Occupancy): Long { val id = nextId(); occupancies.add(occupancy.copy(id = id)); return id }
    override suspend fun updateOccupancy(occupancy: Occupancy) { val idx = occupancies.indexOfFirst { it.id == occupancy.id }; if (idx >= 0) occupancies[idx] = occupancy }
    override suspend fun deleteOccupancy(occupancy: Occupancy) { occupancies.remove(occupancy) }

    override fun getAllPlannedPlantings(): Flow<List<PlannedPlanting>> = throw UnsupportedOperationException()
    override suspend fun getPlannedPlantingById(id: Long): PlannedPlanting? = throw UnsupportedOperationException()
    override fun getPlannedPlantingsForGarden(gardenId: Long): Flow<List<PlannedPlanting>> = throw UnsupportedOperationException()
    override fun getPlannedPlantingsForSpace(spaceId: Long): Flow<List<PlannedPlanting>> = throw UnsupportedOperationException()
    override suspend fun insertPlannedPlanting(plan: PlannedPlanting): Long = throw UnsupportedOperationException()
    override suspend fun updatePlannedPlanting(plan: PlannedPlanting) = throw UnsupportedOperationException()
    override suspend fun deletePlannedPlanting(plan: PlannedPlanting) = throw UnsupportedOperationException()

    override fun getAllPlants(): Flow<List<Plant>> = flowOf(plants.toList())
    override suspend fun getPlantById(id: Long): Plant? = plants.firstOrNull { it.id == id }
    override suspend fun insertPlant(plant: Plant): Long { val id = nextId(); plants.add(plant.copy(id = id)); return id }
    override suspend fun updatePlant(plant: Plant) { val idx = plants.indexOfFirst { it.id == plant.id }; if (idx >= 0) plants[idx] = plant }
    override suspend fun deletePlant(plant: Plant) { plants.remove(plant) }
    override fun getPhotosForPlant(plantId: Long): Flow<List<PlantPhoto>> = throw UnsupportedOperationException()
    override suspend fun insertPhoto(photo: PlantPhoto) = throw UnsupportedOperationException()
    override suspend fun deletePhoto(photo: PlantPhoto) = throw UnsupportedOperationException()
    override fun getJournalEntriesForPlant(plantId: Long): Flow<List<JournalEntry>> = throw UnsupportedOperationException()
    override suspend fun insertJournalEntry(entry: JournalEntry): Long { val id = nextId(); journalEntries.add(entry.copy(id = id)); return id }
    override suspend fun updateJournalEntry(entry: JournalEntry) = throw UnsupportedOperationException()
    override suspend fun deleteJournalEntry(entry: JournalEntry) { journalEntries.remove(entry) }
    override fun getAllHarvests(): Flow<List<Harvest>> = flowOf(harvests.toList())
    override fun getHarvestsForPlant(plantId: Long): Flow<List<Harvest>> = throw UnsupportedOperationException()
    override suspend fun insertHarvest(harvest: Harvest): Long { val id = nextId(); harvests.add(harvest.copy(id = id)); return id }
    override suspend fun updateHarvest(harvest: Harvest) = throw UnsupportedOperationException()
    override suspend fun deleteHarvest(harvest: Harvest) { harvests.remove(harvest) }
}
