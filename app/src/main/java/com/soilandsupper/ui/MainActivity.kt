package com.soilandsupper.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.soilandsupper.data.local.SoilAndSupperDatabase
import com.soilandsupper.data.repository.PlantRepository
import com.soilandsupper.domain.model.MockPlantIdentifier
import com.soilandsupper.ui.theme.SoilAndSupperTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val database = SoilAndSupperDatabase.getInstance(this)
        val repository = PlantRepository(
            plantDao = database.plantDao(),
            plantPhotoDao = database.plantPhotoDao(),
            journalEntryDao = database.journalEntryDao(),
            harvestDao = database.harvestDao()
        )
        val plantIdentifier = MockPlantIdentifier()

        setContent {
            SoilAndSupperTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    AppNavigation(
                        repository = repository,
                        plantIdentifier = plantIdentifier
                    )
                }
            }
        }
    }
}

@Composable
fun AppNavigation(
    repository: PlantRepository,
    plantIdentifier: MockPlantIdentifier
) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    androidx.compose.material3.Scaffold(
        bottomBar = {
            androidx.compose.material3.NavigationBar {
                Screen.values().forEach { screen ->
                    androidx.compose.material3.NavigationBarItem(
                        selected = currentRoute == screen.route,
                        onClick = {
                            navController.navigate(screen.route) {
                                launchSingleTop = true
                                restoreState = true
                                popUpTo(navController.graph.startDestinationId) {
                                    saveState = true
                                }
                            }
                        },
                        icon = {
                            androidx.compose.material3.Icon(
                                imageVector = screen.icon,
                                contentDescription = screen.label
                            )
                        },
                        label = { androidx.compose.material3.Text(screen.label) }
                    )
                }
            }
        },
        floatingActionButton = {
            if (currentRoute == Screen.Garden.route) {
                FloatingActionButton(onClick = {
                    navController.navigate("add_plant")
                }) {
                    Icon(
                        imageVector = Icons.Default.Add,
                        contentDescription = "Add plant"
                    )
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Garden.route,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(Screen.Garden.route) {
                GardenScreen(
                    onPlantClick = { plantId ->
                        navController.navigate("plant_detail/$plantId")
                    },
                    onAddPlantClick = {
                        navController.navigate("add_plant")
                    },
                    repository = repository
                )
            }
            composable("add_plant") {
                AddPlantScreen(
                    onPlantSaved = {
                        navController.popBackStack()
                    },
                    onCancel = {
                        navController.popBackStack()
                    },
                    repository = repository
                )
            }
            composable("plant_detail/{plantId}") { backStackEntry ->
                val plantId = backStackEntry.arguments?.getString("plantId")?.toLongOrNull()
                if (plantId != null) {
                    PlantDetailScreen(
                        plantId = plantId,
                        onBack = { navController.popBackStack() },
                        repository = repository
                    )
                }
            }
            composable(Screen.Harvest.route) {
                HarvestScreen(repository = repository)
            }
            composable(Screen.Identify.route) {
                IdentifyScreen(plantIdentifier = plantIdentifier)
            }
            composable(Screen.GardenToTable.route) {
                GardenToTableScreen()
            }
        }
    }
}
