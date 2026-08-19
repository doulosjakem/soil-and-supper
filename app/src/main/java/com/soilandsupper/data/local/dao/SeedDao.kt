package com.soilandsupper.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.soilandsupper.domain.model.Seed
import kotlinx.coroutines.flow.Flow

@Dao
interface SeedDao {
    @Query("SELECT * FROM seeds ORDER BY updatedAt DESC")
    fun getAllSeeds(): Flow<List<Seed>>

    @Query("SELECT * FROM seeds WHERE id = :id")
    suspend fun getSeedById(id: Long): Seed?

    @Query("SELECT * FROM seeds WHERE gardenId = :gardenId ORDER BY updatedAt DESC")
    fun getSeedsForGarden(gardenId: Long): Flow<List<Seed>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSeed(seed: Seed): Long

    @Update
    suspend fun updateSeed(seed: Seed)

    @Delete
    suspend fun deleteSeed(seed: Seed)
}
