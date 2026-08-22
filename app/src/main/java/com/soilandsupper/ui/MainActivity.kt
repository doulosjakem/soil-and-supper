package com.soilandsupper.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.soilandsupper.ai.command.DefaultCommandExecutor
import com.soilandsupper.ai.command.DefaultCommandValidator
import com.soilandsupper.ai.command.InMemoryCommandHistory
import com.soilandsupper.ai.orchestration.AIOrchestrator
import com.soilandsupper.ai.orchestration.AIRequest
import com.soilandsupper.ai.orchestration.AIResponse
import com.soilandsupper.ai.orchestration.AIInput
import com.soilandsupper.ai.orchestration.AndroidFakeAIProvider
import com.soilandsupper.ai.orchestration.ConversationContext
import com.soilandsupper.ai.query.DefaultGardenQuery
import com.soilandsupper.ai.ui.AiResponseSheet
import com.soilandsupper.data.local.SoilAndSupperDatabase
import com.soilandsupper.data.repository.GardenRepository
import com.soilandsupper.domain.model.MockPlantIdentifier
import com.soilandsupper.ui.theme.SoilAndSupperTheme
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val database = SoilAndSupperDatabase.getInstance(this)
        val repository = GardenRepository(
            gardenDao = database.gardenDao(),
            growingSpaceDao = database.growingSpaceDao(),
            plantDao = database.plantDao(),
            plantPhotoDao = database.plantPhotoDao(),
            journalEntryDao = database.journalEntryDao(),
            harvestDao = database.harvestDao(),
            occupancyDao = database.occupancyDao(),
            seedDao = database.seedDao(),
            desireDao = database.desireDao(),
            plannedPlantingDao = database.plannedPlantingDao()
        )
        val plantIdentifier = MockPlantIdentifier()

        val history = InMemoryCommandHistory()
        val executor = DefaultCommandExecutor(DefaultCommandValidator(), history)
        val query = DefaultGardenQuery(repository)
        val orchestrator = AIOrchestrator(
            provider = AndroidFakeAIProvider(),
            query = query,
            validator = DefaultCommandValidator(),
            executor = executor,
            history = history,
            repository = repository
        )

        setContent {
            SoilAndSupperTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    AppNavigation(
                        repository = repository,
                        plantIdentifier = plantIdentifier,
                        orchestrator = orchestrator,
                        commandExecutor = executor
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppNavigation(
    repository: GardenRepository,
    plantIdentifier: MockPlantIdentifier,
    orchestrator: AIOrchestrator,
    commandExecutor: com.soilandsupper.ai.command.CommandExecutor
) {
    val navController = rememberNavController()
    val navBackStackEntry = navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry.value?.destination?.route

    var aiResponse by remember { mutableStateOf<AIResponse?>(null) }
    var aiLoading by remember { mutableStateOf(false) }
    var showFabMenu by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val scope = remember { CoroutineScope(Dispatchers.Main.immediate) }

    LaunchedEffect(aiResponse) {
        if (aiResponse != null) {
            sheetState.show()
        } else {
            sheetState.hide()
        }
    }

    Scaffold(
        bottomBar = {
            NavigationBar {
                Screen.values().forEach { screen ->
                    NavigationBarItem(
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
                        label = { Text(screen.label) }
                    )
                }
            }
        },
        floatingActionButton = {
            if (currentRoute == Screen.Garden.route) {
                FloatingActionButton(onClick = {
                    showFabMenu = true
                }) {
                    Icon(
                        imageVector = Icons.Default.Add,
                        contentDescription = "Add to garden"
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
                    repository = repository,
                    onAiSubmit = { text ->
                        aiLoading = true
                        scope.launch(Dispatchers.Main.immediate) {
                            try {
                                val request = AIRequest(input = AIInput.Text(text))
                                val response = orchestrator.process(request)
                                aiResponse = response
                            } finally {
                                aiLoading = false
                            }
                        }
                    },
                    onAiVoice = {
                        aiLoading = true
                        scope.launch(Dispatchers.Main.immediate) {
                            try {
                                val request = AIRequest(input = AIInput.VoiceTranscript(rawContent = "", confidence = null))
                                val response = orchestrator.process(request)
                                aiResponse = response
                            } finally {
                                aiLoading = false
                            }
                        }
                    },
                    loading = aiLoading
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
            composable("plant_crop") {
                PlantCropScreen(
                    onBack = { navController.popBackStack() },
                    repository = repository
                )
            }
            composable("plant_detail/{plantId}") { backStackEntry ->
                val plantId = backStackEntry.arguments?.getString("plantId")?.toLongOrNull()
                if (plantId != null) {
                    PlantDetailScreen(
                        plantId = plantId,
                        onBack = { navController.popBackStack() },
                        repository = repository,
                        commandExecutor = commandExecutor
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

    if (showFabMenu) {
        AlertDialog(
            onDismissRequest = { showFabMenu = false },
            title = { Text("Add to garden") },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = {
                            showFabMenu = false
                            navController.navigate("plant_crop")
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("Plant crop in a growing space")
                    }
                    TextButton(
                        onClick = {
                            showFabMenu = false
                            navController.navigate("add_plant")
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("Record an individual plant")
                    }
                }
            },
            confirmButton = {}
        )
    }

    aiResponse?.let { response ->
        ModalBottomSheet(
            onDismissRequest = { aiResponse = null },
            sheetState = sheetState
        ) {
            AiResponseSheet(
                response = response,
                onDismiss = { aiResponse = null },
                onConfirm = {
                    scope.launch(Dispatchers.Main.immediate) {
                        val confirmRequest = AIRequest(
                            input = AIInput.Text("confirm"),
                            conversationContext = com.soilandsupper.ai.orchestration.ConversationContext(
                                sessionId = "ui",
                                turnCount = 1
                            )
                        )
                        val confirmResponse = orchestrator.process(confirmRequest)
                        aiResponse = confirmResponse
                    }
                },
                onCancel = { aiResponse = null },
                onUndo = {
                    scope.launch(Dispatchers.Main.immediate) {
                        val undoRequest = AIRequest(input = AIInput.Text("undo"))
                        val undoResponse = orchestrator.process(undoRequest)
                        aiResponse = undoResponse
                    }
                },
                onSelectClarification = { clarification ->
                    scope.launch(Dispatchers.Main.immediate) {
                        val clarifyRequest = AIRequest(input = AIInput.Text(clarification))
                        val clarifyResponse = orchestrator.process(clarifyRequest)
                        aiResponse = clarifyResponse
                    }
                }
            )
        }
    }
}