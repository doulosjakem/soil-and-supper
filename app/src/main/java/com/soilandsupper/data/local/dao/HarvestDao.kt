package com.soilandsupper.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.soilandsupper.domain.model.Harvest
import kotlinx.coroutines.flow.Flow

@Dao
interface HarvestDao {
    @Query("SELECT * FROM harvests ORDER BY date DESC")
    fun getAllHarvests(): Flow<List<Harvest>>

    @Query("SELECT * FROM harvests WHERE plantId = :plantId ORDER BY date DESC")
    fun getHarvestsForPlant(plantId: Long): Flow<List<Harvest>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertHarvest(harvest: Harvest): Long

    @Update
    suspend fun updateHarvest(harvest: Harvest)

    @Delete
    suspend fun deleteHarvest(harvest: Harvest)
}
