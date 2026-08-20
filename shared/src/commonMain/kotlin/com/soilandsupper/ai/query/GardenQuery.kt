package com.soilandsupper.ai.query

import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Harvest
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.Seed

interface GardenQuery {
    suspend fun getAllSpaces(): List<GrowingSpace>
    suspend fun getSpaceById(id: Long): GrowingSpace?
    suspend fun getActiveOccupancies(): List<Occupancy>
    suspend fun getOccupanciesForSpace(spaceId: Long): List<Occupancy>
    suspend fun getUpcomingOpenings(beforeDate: Long): List<Occupancy>
    suspend fun getAllSeeds(): List<Seed>
    suspend fun getAllDesires(): List<Desire>
    suspend fun getAllPlants(): List<Plant>
    suspend fun getAllHarvests(): List<Harvest>
    suspend fun getHarvestsForPlant(plantId: Long): List<Harvest>
}
