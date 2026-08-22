package com.soilandsupper.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.soilandsupper.data.repository.GardenRepository
import com.soilandsupper.service.GardenService
import com.soilandsupper.shared.domain.model.GrowingSpace
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

@Composable
fun PlantCropScreen(
    onBack: () -> Unit,
    repository: GardenRepository
) {
    val scope = rememberCoroutineScope()
    var spaces by remember { mutableStateOf<List<GrowingSpace>>(emptyList()) }
    var cropName by remember { mutableStateOf("") }
    var selectedSpace by remember { mutableStateOf<GrowingSpace?>(null) }
    var spaceMenuExpanded by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text("Plant crop", modifier = Modifier.padding(bottom = 8.dp))

        Box(modifier = Modifier.fillMaxWidth()) {
            OutlinedTextField(
                value = selectedSpace?.name ?: "",
                onValueChange = {},
                readOnly = true,
                label = { Text("Growing space") },
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { spaceMenuExpanded = true }
            )
            DropdownMenu(
                expanded = spaceMenuExpanded,
                onDismissRequest = { spaceMenuExpanded = false },
                modifier = Modifier.fillMaxWidth()
            ) {
                spaces.forEach { space ->
                    DropdownMenuItem(
                        text = { Text(space.name) },
                        onClick = {
                            selectedSpace = space
                            spaceMenuExpanded = false
                        }
                    )
                }
            }
        }

        OutlinedTextField(
            value = cropName,
            onValueChange = { cropName = it },
            label = { Text("Crop name") },
            modifier = Modifier.fillMaxWidth()
        )

        error?.let {
            Text(it, color = androidx.compose.ui.graphics.Color.Red)
        }

        Button(
            onClick = {
                val space = selectedSpace
                if (space == null) {
                    error = "Select a growing space"
                    return@Button
                }
                if (cropName.isBlank()) {
                    error = "Enter a crop name"
                    return@Button
                }
                error = null
                scope.launch {
                    val occupancy = GardenService.recordPlanting(
                        cropName = cropName.trim(),
                        startDate = System.currentTimeMillis(),
                        growingSpace = space
                    )
                    repository.insertOccupancy(occupancy)
                    onBack()
                }
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = cropName.isNotBlank()
        ) {
            Text("Plant")
        }
    }

    androidx.compose.runtime.LaunchedEffect(Unit) {
        spaces = repository.getAllGrowingSpaces().first()
    }
}
