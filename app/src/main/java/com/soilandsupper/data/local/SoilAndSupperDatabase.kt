package com.soilandsupper.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.soilandsupper.data.local.dao.DesireDao
import com.soilandsupper.data.local.dao.GardenDao
import com.soilandsupper.data.local.dao.GrowingSpaceDao
import com.soilandsupper.data.local.dao.HarvestDao
import com.soilandsupper.data.local.dao.JournalEntryDao
import com.soilandsupper.data.local.dao.OccupancyDao
import com.soilandsupper.data.local.dao.PlantDao
import com.soilandsupper.data.local.dao.PlantPhotoDao
import com.soilandsupper.data.local.dao.PlannedPlantingDao
import com.soilandsupper.data.local.dao.SeedDao
import com.soilandsupper.domain.model.Desire
import com.soilandsupper.domain.model.Garden
import com.soilandsupper.domain.model.GrowingSpace
import com.soilandsupper.domain.model.Harvest
import com.soilandsupper.domain.model.JournalEntry
import com.soilandsupper.domain.model.Occupancy
import com.soilandsupper.domain.model.Plant
import com.soilandsupper.domain.model.PlantPhoto
import com.soilandsupper.domain.model.PlannedPlanting
import com.soilandsupper.domain.model.Seed

@Database(
    entities = [
        Garden::class,
        GrowingSpace::class,
        Plant::class,
        PlantPhoto::class,
        JournalEntry::class,
        Harvest::class,
        Occupancy::class,
        Seed::class,
        Desire::class,
        PlannedPlanting::class
    ],
    version = 4,
    exportSchema = false
)
abstract class SoilAndSupperDatabase : RoomDatabase() {
    abstract fun gardenDao(): GardenDao
    abstract fun growingSpaceDao(): GrowingSpaceDao
    abstract fun plantDao(): PlantDao
    abstract fun plantPhotoDao(): PlantPhotoDao
    abstract fun journalEntryDao(): JournalEntryDao
    abstract fun harvestDao(): HarvestDao
    abstract fun occupancyDao(): OccupancyDao
    abstract fun seedDao(): SeedDao
    abstract fun desireDao(): DesireDao
    abstract fun plannedPlantingDao(): PlannedPlantingDao

    companion object {
        @Volatile
        private var INSTANCE: SoilAndSupperDatabase? = null

        fun getInstance(context: Context): SoilAndSupperDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    SoilAndSupperDatabase::class.java,
                    "soil_and_supper_database"
                )
                .fallbackToDestructiveMigration()
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
