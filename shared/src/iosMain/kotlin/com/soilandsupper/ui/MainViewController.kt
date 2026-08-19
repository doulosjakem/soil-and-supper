package com.soilandsupper.ui

import androidx.compose.ui.window.ComposeUIViewController

fun MainViewController(): ComposeUIViewController {
    return ComposeUIViewController {
        SoilAndSupperTheme {
            GardenScreen(
                onPlantClick = {},
                repository = TODO("Provide iOS GardenRepository implementation")
            )
        }
    }
}
