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

class DefaultGardenQuery(
    private val repository: GardenRepository
) : GardenQuery {

    override suspend fun getAllSpaces(): List<GrowingSpace> {
        var spaces: List<GrowingSpace> = emptyList()
        repository.getAllGrowingSpaces().collect { spaces = it }
        return spaces
    }

    override suspend fun getSpaceById(id: Long): GrowingSpace? {
        return repository.getGrowingSpaceById(id)
    }

    override suspend fun getActiveOccupancies(): List<Occupancy> {
        var all: List<Occupancy> = emptyList()
        repository.getAllOccupancies().collect { all = it }
        return all.filter { it.status == OccupancyStatus.ACTIVE.name }
    }

    override suspend fun getOccupanciesForSpace(spaceId: Long): List<Occupancy> {
        var all: List<Occupancy> = emptyList()
        repository.getAllOccupancies().collect { all = it }
        return all.filter { it.growingSpaceId == spaceId }
    }

    override suspend fun getUpcomingOpenings(beforeDate: Long): List<Occupancy> {
        var all: List<Occupancy> = emptyList()
        repository.getAllOccupancies().collect { all = it }
        return all.filter { occupancy ->
            occupancy.status == OccupancyStatus.ACTIVE.name &&
                occupancy.expectedReleaseDate != null &&
                occupancy.expectedReleaseDate <= beforeDate
        }
    }

    override suspend fun getAllSeeds(): List<Seed> {
        var seeds: List<Seed> = emptyList()
        repository.getAllSeeds().collect { seeds = it }
        return seeds
    }

    override suspend fun getAllDesires(): List<Desire> {
        var desires: List<Desire> = emptyList()
        repository.getAllDesires().collect { desires = it }
        return desires
    }

    override suspend fun getAllPlants(): List<Plant> {
        val plantRepo = repository as? PlantRepository
        var plants: List<Plant> = emptyList()
        plantRepo?.getAllPlants()?.collect { plants = it }
        return plants
    }

    override suspend fun getAllHarvests(): List<Harvest> {
        val plantRepo = repository as? PlantRepository
        var harvests: List<Harvest> = emptyList()
        plantRepo?.getAllHarvests()?.collect { harvests = it }
        return harvests
    }

    override suspend fun getHarvestsForPlant(plantId: Long): List<Harvest> {
        val plantRepo = repository as? PlantRepository
        var harvests: List<Harvest> = emptyList()
        plantRepo?.getHarvestsForPlant(plantId)?.collect { harvests = it }
        return harvests
    }
}
