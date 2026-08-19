package com.soilandsupper.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.soilandsupper.domain.model.GrowingSpace
import kotlinx.coroutines.flow.Flow

@Dao
interface GrowingSpaceDao {
    @Query("SELECT * FROM growing_spaces ORDER BY updatedAt DESC")
    fun getAllGrowingSpaces(): Flow<List<GrowingSpace>>

    @Query("SELECT * FROM growing_spaces WHERE id = :id")
    suspend fun getGrowingSpaceById(id: Long): GrowingSpace?

    @Query("SELECT * FROM growing_spaces WHERE gardenId = :gardenId ORDER BY updatedAt DESC")
    fun getGrowingSpacesForGarden(gardenId: Long): Flow<List<GrowingSpace>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertGrowingSpace(space: GrowingSpace): Long

    @Update
    suspend fun updateGrowingSpace(space: GrowingSpace)

    @Delete
    suspend fun deleteGrowingSpace(space: GrowingSpace)
}
