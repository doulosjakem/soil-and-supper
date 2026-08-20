package com.soilandsupper.ai.query

import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.repository.PlantRepository
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Harvest
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.OccupancyStatus
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed
import kotlinx.coroutines.flow.first

class DefaultGardenQuery(
    private val repository: GardenRepository
) : GardenQuery {

    override suspend fun getAllSpaces(): List<GrowingSpace> {
        return repository.getAllGrowingSpaces().first()
    }

    override suspend fun getSpaceById(id: Long): GrowingSpace? {
        return repository.getGrowingSpaceById(id)
    }

    override suspend fun getActiveOccupancies(): List<Occupancy> {
        val all = repository.getAllOccupancies().first()
        return all.filter { it.status == OccupancyStatus.ACTIVE.name }
    }

    override suspend fun getOccupanciesForSpace(spaceId: Long): List<Occupancy> {
        val all = repository.getAllOccupancies().first()
        return all.filter { it.growingSpaceId == spaceId }
    }

    override suspend fun getUpcomingOpenings(beforeDate: Long): List<Occupancy> {
        val all = repository.getAllOccupancies().first()
        return all.filter { occupancy ->
            occupancy.status == OccupancyStatus.ACTIVE.name &&
                occupancy.expectedReleaseDate != null &&
                occupancy.expectedReleaseDate <= beforeDate
        }
    }

    override suspend fun getAllSeeds(): List<Seed> {
        return repository.getAllSeeds().first()
    }

    override suspend fun getAllDesires(): List<Desire> {
        return repository.getAllDesires().first()
    }

    override suspend fun getAllPlants(): List<Plant> {
        val plantRepo = repository as? PlantRepository
        return plantRepo?.getAllPlants()?.first() ?: emptyList()
    }

    override suspend fun getAllHarvests(): List<Harvest> {
        val plantRepo = repository as? PlantRepository
        return plantRepo?.getAllHarvests()?.first() ?: emptyList()
    }

    override suspend fun getHarvestsForPlant(plantId: Long): List<Harvest> {
        val plantRepo = repository as? PlantRepository
        return plantRepo?.getHarvestsForPlant(plantId)?.first() ?: emptyList()
    }
}
