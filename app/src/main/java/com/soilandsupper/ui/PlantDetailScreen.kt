package com.soilandsupper.ui

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.Button
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
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
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.unit.dp
import com.soilandsupper.ai.command.CommandExecutor
import com.soilandsupper.ai.command.GardenCommand
import com.soilandsupper.data.repository.GardenRepository
import com.soilandsupper.shared.domain.model.Harvest
import com.soilandsupper.shared.domain.model.JournalEntry
import com.soilandsupper.shared.domain.model.Plant
import com.soilandsupper.shared.domain.model.PlantPhoto
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun PlantDetailScreen(
    plantId: Long,
    onBack: () -> Unit,
    repository: GardenRepository,
    commandExecutor: CommandExecutor
) {
    var plant by remember { mutableStateOf<Plant?>(null) }
    var photos by remember { mutableStateOf<List<PlantPhoto>>(emptyList()) }
    var journalEntries by remember { mutableStateOf<List<JournalEntry>>(emptyList()) }
    var harvests by remember { mutableStateOf<List<Harvest>>(emptyList()) }
    var showAddJournal by remember { mutableStateOf(false) }
    var newJournalText by remember { mutableStateOf("") }
    var showAddHarvest by remember { mutableStateOf(false) }
    var harvestQuantity by remember { mutableStateOf("") }
    var harvestUnit by remember { mutableStateOf("lb") }
    var harvestNotes by remember { mutableStateOf("") }
    val scope = rememberCoroutineScope()

    LaunchedEffect(plantId) {
        launch {
            plant = repository.getPlantById(plantId)
        }
        repository.getPhotosForPlant(plantId).collect { photos = it }
        repository.getJournalEntriesForPlant(plantId).collect { journalEntries = it }
        repository.getHarvestsForPlant(plantId).collect { harvests = it }
    }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        if (plant != null) {
            item {
                Text(
                    text = plant!!.name,
                    style = androidx.compose.material3.MaterialTheme.typography.headlineMedium
                )
            }
            if (plant!!.variety.isNotBlank()) {
                item { Text(text = "Variety: ${plant!!.variety}") }
            }
            item { Text(text = "Location: ${plant!!.location}") }
            item { Text(text = "Notes: ${plant!!.notes}") }

            item {
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Photos",
                    style = androidx.compose.material3.MaterialTheme.typography.titleMedium
                )
            }

            item {
                LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(photos) { photo ->
                        PhotoThumbnail(
                            uriString = photo.uri,
                            onDelete = {
                                scope.launch(kotlinx.coroutines.Dispatchers.IO) {
                                    repository.deletePhoto(photo)
                                }
                            }
                        )
                    }
                    item {
                        AddPhotoButton(onPhotoSelected = { uri ->
                            scope.launch(kotlinx.coroutines.Dispatchers.IO) {
                                repository.insertPhoto(
                                    PlantPhoto(
                                        plantId = plantId,
                                        uri = uri.toString()
                                    )
                                )
                            }
                        })
                    }
                }
            }

            item {
                Spacer(modifier = Modifier.height(16.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = "Journal",
                        style = androidx.compose.material3.MaterialTheme.typography.titleMedium
                    )
                    FloatingActionButton(
                        onClick = { showAddJournal = true },
                        modifier = Modifier.size(48.dp)
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "Add observation")
                    }
                }
            }

            if (showAddJournal) {
                item {
                    OutlinedTextField(
                        value = newJournalText,
                        onValueChange = { newJournalText = it },
                        label = { Text("Observation") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(onClick = {
                            if (newJournalText.isNotBlank()) {
                                scope.launch(kotlinx.coroutines.Dispatchers.IO) {
                                    commandExecutor.execute(
                                        GardenCommand.RecordObservation(
                                            text = newJournalText,
                                            date = System.currentTimeMillis(),
                                            plantId = plantId
                                        ),
                                        repository
                                    )
                                }
                                newJournalText = ""
                                showAddJournal = false
                            }
                        }) {
                            Text("Save")
                        }
                        Button(onClick = {
                            showAddJournal = false
                            newJournalText = ""
                        }) {
                            Text("Cancel")
                        }
                    }
                }
            }

            if (journalEntries.isEmpty()) {
                item {
                    Text(
                        text = "No observations yet",
                        modifier = Modifier.padding(vertical = 8.dp)
                    )
                }
            } else {
                items(journalEntries) { entry ->
                    JournalEntryItem(
                        entry = entry,
                        onDelete = {
                            scope.launch(kotlinx.coroutines.Dispatchers.IO) {
                                repository.deleteJournalEntry(entry)
                            }
                        }
                    )
                }
            }

            item {
                Spacer(modifier = Modifier.height(16.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = "Harvests",
                        style = androidx.compose.material3.MaterialTheme.typography.titleMedium
                    )
                    FloatingActionButton(
                        onClick = { showAddHarvest = true },
                        modifier = Modifier.size(48.dp)
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "Add harvest")
                    }
                }
            }

            if (showAddHarvest) {
                item {
                    OutlinedTextField(
                        value = harvestQuantity,
                        onValueChange = { harvestQuantity = it },
                        label = { Text("Quantity") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    OutlinedTextField(
                        value = harvestUnit,
                        onValueChange = { harvestUnit = it },
                        label = { Text("Unit") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    OutlinedTextField(
                        value = harvestNotes,
                        onValueChange = { harvestNotes = it },
                        label = { Text("Notes") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(onClick = {
                            val qty = harvestQuantity.toDoubleOrNull()
                            if (qty != null) {
                                scope.launch(kotlinx.coroutines.Dispatchers.IO) {
                                    repository.insertHarvest(
                                        Harvest(
                                            plantId = plantId,
                                            cropName = plant!!.name,
                                            quantity = qty,
                                            unit = harvestUnit,
                                            notes = harvestNotes
                                        )
                                    )
                                }
                                harvestQuantity = ""
                                harvestUnit = "lb"
                                harvestNotes = ""
                                showAddHarvest = false
                            }
                        }) {
                            Text("Save")
                        }
                        Button(onClick = {
                            showAddHarvest = false
                            harvestQuantity = ""
                            harvestUnit = "lb"
                            harvestNotes = ""
                        }) {
                            Text("Cancel")
                        }
                    }
                }
            }

            items(harvests) { harvest ->
                HarvestItem(
                    harvest = harvest,
                    onDelete = {
                        scope.launch(kotlinx.coroutines.Dispatchers.IO) {
                            repository.deleteHarvest(harvest)
                        }
                    }
                )
            }

            item {
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
                    Text("Back")
                }
            }
        } else {
            item { Text(text = "Plant not found") }
            item {
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
                    Text("Back")
                }
            }
        }
    }
}

@Composable
fun PhotoThumbnail(uriString: String, onDelete: () -> Unit) {
    val context = androidx.compose.ui.platform.LocalContext.current
    var bitmap by remember { mutableStateOf<android.graphics.Bitmap?>(null) }

    LaunchedEffect(uriString) {
        launch(kotlinx.coroutines.Dispatchers.IO) {
            try {
                val contentResolver = context.contentResolver
                val inputStream = contentResolver.openInputStream(Uri.parse(uriString))
                bitmap = android.graphics.BitmapFactory.decodeStream(inputStream)
                inputStream?.close()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    Column {
        bitmap?.let {
            Image(
                bitmap = it.asImageBitmap(),
                contentDescription = "Plant photo",
                modifier = Modifier.size(120.dp)
            )
        } ?: androidx.compose.foundation.layout.Box(
            modifier = Modifier.size(120.dp),
            contentAlignment = androidx.compose.ui.Alignment.Center
        ) {
            Text("Loading...")
        }
        IconButton(onClick = onDelete) {
            Icon(
                imageVector = Icons.Default.Delete,
                contentDescription = "Delete photo"
            )
        }
    }
}

@Composable
fun AddPhotoButton(onPhotoSelected: (Uri) -> Unit) {
    val photoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia(),
        onResult = { uri ->
            uri?.let { onPhotoSelected(it) }
        }
    )

    FloatingActionButton(onClick = {
        photoPickerLauncher.launch(
            PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
        )
    }) {
        Icon(
            imageVector = Icons.Default.Add,
            contentDescription = "Add photo"
        )
    }
}

@Composable
fun JournalEntryItem(entry: JournalEntry, onDelete: () -> Unit) {
    val dateFormat = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(text = dateFormat.format(Date(entry.date)))
            Text(text = entry.text)
        }
        IconButton(onClick = onDelete) {
            Icon(
                imageVector = Icons.Default.Delete,
                contentDescription = "Delete entry"
            )
        }
    }
}
