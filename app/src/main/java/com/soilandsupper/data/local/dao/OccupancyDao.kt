package com.soilandsupper.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.soilandsupper.domain.model.Occupancy
import kotlinx.coroutines.flow.Flow

@Dao
interface OccupancyDao {
    @Query("SELECT * FROM occupancies ORDER BY startDate DESC")
    fun getAllOccupancies(): Flow<List<Occupancy>>

    @Query("SELECT * FROM occupancies WHERE id = :id")
    suspend fun getOccupancyById(id: Long): Occupancy?

    @Query("SELECT * FROM occupancies WHERE growingSpaceId = :spaceId ORDER BY startDate DESC")
    fun getOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>>

    @Query("SELECT * FROM occupancies WHERE growingSpaceId = :spaceId AND status = 'ACTIVE' ORDER BY startDate DESC")
    fun getActiveOccupanciesForSpace(spaceId: Long): Flow<List<Occupancy>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOccupancy(occupancy: Occupancy): Long

    @Update
    suspend fun updateOccupancy(occupancy: Occupancy)

    @Delete
    suspend fun deleteOccupancy(occupancy: Occupancy)
}
