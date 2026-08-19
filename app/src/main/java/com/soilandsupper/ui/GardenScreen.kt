package com.soilandsupper.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.Scaffold
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.soilandsupper.data.repository.GardenRepository
import com.soilandsupper.domain.model.GrowingSpace

@Composable
fun GardenScreen(
    onPlantClick: (Long) -> Unit,
    onAddPlantClick: () -> Unit,
    repository: GardenRepository
) {
    val plants by repository.getAllPlants().collectAsState(initial = emptyList())
    val growingSpaces by repository.getAllGrowingSpaces().collectAsState(initial = emptyList())
    val occupancies by repository.getAllOccupancies().collectAsState(initial = emptyList())
    val gardens by repository.getAllGardens().collectAsState(initial = emptyList())

    var selectedDate by remember { mutableStateOf(System.currentTimeMillis()) }

    val garden = gardens.firstOrNull()

    val timelineSpaces = remember(growingSpaces, occupancies, selectedDate, garden) {
        buildTimelineSpaces(growingSpaces, occupancies, selectedDate, garden)
    }

    Scaffold(
        floatingActionButton = {
            FloatingActionButton(onClick = onAddPlantClick) {
                Icon(
                                        imageVector = Icons.Default.Add,
                    contentDescription = "Add plant"
                )
            }
        }
    ) { padding ->
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
                    }
                }
            }
        }
    }
}
