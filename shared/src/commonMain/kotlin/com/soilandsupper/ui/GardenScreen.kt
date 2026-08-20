package com.soilandsupper.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.soilandsupper.ai.ui.AiInputBar
import com.soilandsupper.gardentimeline.buildTimelineSpaces
import com.soilandsupper.repository.GardenRepository
import com.soilandsupper.shared.domain.model.Desire
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Seed

@Composable
fun GardenScreen(
    onPlantClick: (Long) -> Unit,
    repository: GardenRepository,
    onAiSubmit: (String) -> Unit = {},
    onAiVoice: () -> Unit = {},
    onAiCamera: () -> Unit = {},
    onAiDocument: () -> Unit = {}
) {
    val growingSpaces by repository.getAllGrowingSpaces().collectAsState(initial = emptyList())
    val occupancies by repository.getAllOccupancies().collectAsState(initial = emptyList())
    val gardens by repository.getAllGardens().collectAsState(initial = emptyList())
    val seeds by repository.getAllSeeds().collectAsState(initial = emptyList())
    val desires by repository.getAllDesires().collectAsState(initial = emptyList())

    var selectedDate by remember { mutableStateOf(System.currentTimeMillis()) }

    val garden = gardens.firstOrNull()

    val timelineSpaces = remember(growingSpaces, occupancies, selectedDate, garden, seeds, desires) {
        buildTimelineSpaces(growingSpaces, occupancies, selectedDate, garden, seeds, desires)
    }

    var aiInput by remember { mutableStateOf("") }

    Column(modifier = Modifier.fillMaxSize()) {
        Scaffold { padding ->
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentPadding = androidx.compose.foundation.layout.PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                item {
                    DateScrubber(
                        selectedDate = selectedDate,
                        onDateSelected = { selectedDate = it }
                    )
                }

                items(timelineSpaces) { spaceModel ->
                    GrowingSpaceTimelineRow(spaceModel = spaceModel)
                }

                if (growingSpaces.isEmpty()) {
                    item {
                        Column(
                            modifier = Modifier.fillMaxSize(),
                            verticalArrangement = Arrangement.Center,
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = "No growing spaces yet",
                                style = MaterialTheme.typography.bodyLarge
                            )
                            Text(
                                text = "Add a bed, pot, or row to start tracking your garden.",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(top = 8.dp)
                            )
                        }
                    }
                }
            }
        }

        AiInputBar(
            value = aiInput,
            onValueChange = { aiInput = it },
            onSend = {
                onAiSubmit(aiInput)
                aiInput = ""
            },
            onVoice = onAiVoice,
            onCamera = onAiCamera,
            onDocument = onAiDocument
        )
    }
}
