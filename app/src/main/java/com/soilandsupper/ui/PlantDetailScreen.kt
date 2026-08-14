package com.soilandsupper.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.soilandsupper.data.repository.PlantRepository
import com.soilandsupper.domain.model.Plant
import kotlinx.coroutines.launch

@Composable
fun PlantDetailScreen(
    plantId: Long,
    onBack: () -> Unit,
    repository: PlantRepository
) {
    var plant by remember { mutableStateOf<Plant?>(null) }

    androidx.compose.runtime.LaunchedEffect(plantId) {
        launch {
            plant = repository.getPlantById(plantId)
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        if (plant != null) {
            Text(
                text = plant!!.name,
                style = androidx.compose.material3.MaterialTheme.typography.headlineMedium
            )
            if (plant!!.variety.isNotBlank()) {
                Text(text = "Variety: ${plant!!.variety}")
            }
            Text(text = "Location: ${plant!!.location}")
            Text(text = "Notes: ${plant!!.notes}")
        } else {
            Text(text = "Plant not found")
        }
        Button(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
            Text("Back")
        }
    }
}
