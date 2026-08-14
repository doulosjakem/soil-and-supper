package com.soilandsupper.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.soilandsupper.data.local.dao.HarvestDao
import com.soilandsupper.data.local.dao.JournalEntryDao
import com.soilandsupper.data.local.dao.PlantDao
import com.soilandsupper.data.local.dao.PlantPhotoDao
import com.soilandsupper.domain.model.Harvest
import com.soilandsupper.domain.model.JournalEntry
import com.soilandsupper.domain.model.Plant
import com.soilandsupper.domain.model.PlantPhoto

@Database(
    entities = [Plant::class, PlantPhoto::class, JournalEntry::class, Harvest::class],
    version = 1,
    exportSchema = false
)
abstract class SoilAndSupperDatabase : RoomDatabase() {
    abstract fun plantDao(): PlantDao
    abstract fun plantPhotoDao(): PlantPhotoDao
    abstract fun journalEntryDao(): JournalEntryDao
    abstract fun harvestDao(): HarvestDao

    companion object {
        @Volatile
        private var INSTANCE: SoilAndSupperDatabase? = null

        fun getInstance(context: Context): SoilAndSupperDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    SoilAndSupperDatabase::class.java,
                    "soil_and_supper_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
