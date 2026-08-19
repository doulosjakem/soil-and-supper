package com.soilandsupper.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.soilandsupper.domain.model.PlannedPlanting
import kotlinx.coroutines.flow.Flow

@Dao
interface PlannedPlantingDao {
    @Query("SELECT * FROM planned_plantings ORDER BY updatedAt DESC")
    fun getAllPlantedPlantings(): Flow<List<PlannedPlanting>>

    @Query("SELECT * FROM planned_plantings WHERE id = :id")
    suspend fun getPlannedPlantingById(id: Long): PlannedPlanting?

    @Query("SELECT * FROM planned_plantings WHERE gardenId = :gardenId ORDER BY updatedAt DESC")
    fun getPlannedPlantingsForGarden(gardenId: Long): Flow<List<PlannedPlanting>>

    @Query("SELECT * FROM planned_plantings WHERE growingSpaceId = :spaceId ORDER BY updatedAt DESC")
    fun getPlannedPlantingsForSpace(spaceId: Long): Flow<List<PlannedPlanting>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPlannedPlanting(plan: PlannedPlanting): Long

    @Update
    suspend fun updatePlannedPlanting(plan: PlannedPlanting)

    @Delete
    suspend fun deletePlannedPlanting(plan: PlannedPlanting)
}
