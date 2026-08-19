package com.soilandsupper.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.soilandsupper.domain.model.Desire
import kotlinx.coroutines.flow.Flow

@Dao
interface DesireDao {
    @Query("SELECT * FROM desires ORDER BY updatedAt DESC")
    fun getAllDesires(): Flow<List<Desire>>

    @Query("SELECT * FROM desires WHERE id = :id")
    suspend fun getDesireById(id: Long): Desire?

    @Query("SELECT * FROM desires WHERE gardenId = :gardenId ORDER BY updatedAt DESC")
    fun getDesiresForGarden(gardenId: Long): Flow<List<Desire>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertDesire(desire: Desire): Long

    @Update
    suspend fun updateDesire(desire: Desire)

    @Delete
    suspend fun deleteDesire(desire: Desire)
}
