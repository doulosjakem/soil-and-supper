package com.soilandsupper.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.soilandsupper.domain.model.Garden
import kotlinx.coroutines.flow.Flow

@Dao
interface GardenDao {
    @Query("SELECT * FROM gardens ORDER BY updatedAt DESC")
    fun getAllGardens(): Flow<List<Garden>>

    @Query("SELECT * FROM gardens WHERE id = :id")
    suspend fun getGardenById(id: Long): Garden?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertGarden(garden: Garden): Long

    @Update
    suspend fun updateGarden(garden: Garden)

    @Delete
    suspend fun deleteGarden(garden: Garden)
}
