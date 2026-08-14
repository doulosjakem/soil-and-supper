package com.soilandsupper

import android.app.Application
import com.soilandsupper.data.local.SoilAndSupperDatabase

class SoilAndSupperApplication : Application() {
    lateinit var database: SoilAndSupperDatabase
        private set

    override fun onCreate() {
        super.onCreate()
        database = SoilAndSupperDatabase.getInstance(this)
    }
}
