package com.soilandsupper.domain.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "harvests",
    indices = [Index(value = ["plantId"])],
    foreignKeys = [
        ForeignKey(
            entity = Plant::class,
            parentColumns = ["id"],
            childColumns = ["plantId"],
            onDelete = ForeignKey.SET_NULL
        )
    ]
)
data class Harvest(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val plantId: Long? = null,
    val cropName: String,
    val quantity: Double,
    val unit: String,
    val date: Long = System.currentTimeMillis(),
    val notes: String = ""
)
