package com.soilandsupper.ui

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Grass
import androidx.compose.material.icons.filled.PhotoCamera
import androidx.compose.material.icons.filled.Restaurant
import androidx.compose.material.icons.filled.Scale

enum class Screen(val route: String, val label: String, val icon: androidx.compose.ui.graphics.vector.ImageVector) {
    Garden("garden", "Garden", Icons.Default.Grass),
    Harvest("harvest", "Harvest", Icons.Default.Scale),
    Identify("identify", "Identify", Icons.Default.PhotoCamera),
    GardenToTable("garden_to_table", "Garden-to-Table", Icons.Default.Restaurant)
}
