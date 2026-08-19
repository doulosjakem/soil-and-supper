package com.soilandsupper.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.soilandsupper.data.repository.GardenRepository
import com.soilandsupper.shared.domain.model.Harvest
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun HarvestScreen(repository: GardenRepository) {
    val harvests by repository.getAllHarvests().collectAsState(initial = emptyList())
    var showAddHarvest by remember { mutableStateOf(false) }
    var cropName by remember { mutableStateOf("") }
    var quantity by remember { mutableStateOf("") }
    var unit by remember { mutableStateOf("lb") }
    var notes by remember { mutableStateOf("") }

    Scaffold(
        floatingActionButton = {
            FloatingActionButton(onClick = { showAddHarvest = true }) {
                Icon(Icons.Default.Add, contentDescription = "Add harvest")
            }
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = "Harvest",
                style = androidx.compose.material3.MaterialTheme.typography.headlineMedium
            )

            if (showAddHarvest) {
                OutlinedTextField(
                    value = cropName,
                    onValueChange = { cropName = it },
                    label = { Text("Crop name") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = quantity,
                    onValueChange = { quantity = it },
                    label = { Text("Quantity") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = unit,
                    onValueChange = { unit = it },
                    label = { Text("Unit") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = notes,
                    onValueChange = { notes = it },
                    label = { Text("Notes") },
                    modifier = Modifier.fillMaxWidth()
                )
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    androidx.compose.material3.Button(onClick = {
                        val qty = quantity.toDoubleOrNull()
                        if (cropName.isNotBlank() && qty != null) {
                            kotlinx.coroutines.GlobalScope.launch(kotlinx.coroutines.Dispatchers.IO) {
                                                            repository.insertHarvest(
                                    Harvest(
                                        plantId = 0,
                                        cropName = cropName,
                                        quantity = qty,
                                        unit = unit,
                                        notes = notes
                                    )
                                )
                            }
                            cropName = ""
                            quantity = ""
                            unit = "lb"
                            notes = ""
                            showAddHarvest = false
                        }
                    }, modifier = Modifier.fillMaxWidth()) {
                        Text("Save")
                    }
                    androidx.compose.material3.Button(
                        onClick = {
                            showAddHarvest = false
                            cropName = ""
                            quantity = ""
                            unit = "lb"
                            notes = ""
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("Cancel")
                    }
                }
            }

            if (harvests.isEmpty()) {
                Text(text = "No harvests yet")
            } else {
                LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(harvests) { harvest ->
                        HarvestItem(
                            harvest = harvest,
                            onDelete = {
                                kotlinx.coroutines.GlobalScope.launch(kotlinx.coroutines.Dispatchers.IO) {
                                    repository.deleteHarvest(harvest)
                                }
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun HarvestItem(harvest: Harvest, onDelete: () -> Unit) {
    val dateFormat = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(text = dateFormat.format(Date(harvest.date)))
            Text(text = "${harvest.cropName}: ${harvest.quantity} ${harvest.unit}")
            if (harvest.notes.isNotBlank()) {
                Text(text = harvest.notes)
            }
        }
        IconButton(onClick = onDelete) {
            Icon(
                imageVector = Icons.Default.Delete,
                contentDescription = "Delete harvest"
            )
        }
    }
}
