package com.soilandsupper.ui

import androidx.compose.ui.window.ComposeUIViewController
import com.soilandsupper.repository.IosGardenRepository

fun MainViewController(): ComposeUIViewController {
    return ComposeUIViewController {
        SoilAndSupperTheme {
            GardenScreen(
                onPlantClick = {},
                repository = IosGardenRepository()
            )
        }
    }
}
