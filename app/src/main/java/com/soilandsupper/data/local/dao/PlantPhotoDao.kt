package com.soilandsupper.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.soilandsupper.domain.model.PlantPhoto
import kotlinx.coroutines.flow.Flow

@Dao
interface PlantPhotoDao {
    @Query("SELECT * FROM plant_photos WHERE plantId = :plantId ORDER BY createdAt DESC")
    fun getPhotosForPlant(plantId: Long): Flow<List<PlantPhoto>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPhoto(photo: PlantPhoto): Long

    @Delete
    suspend fun deletePhoto(photo: PlantPhoto)
}
