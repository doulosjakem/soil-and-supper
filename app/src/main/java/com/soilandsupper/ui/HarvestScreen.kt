package com.soilandsupper.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.soilandsupper.data.repository.PlantRepository
import com.soilandsupper.domain.model.Harvest

@Composable
fun HarvestScreen(repository: PlantRepository) {
    val harvests by repository.getAllHarvests().collectAsState(initial = emptyList())

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Harvest",
            style = androidx.compose.material3.MaterialTheme.typography.headlineMedium
        )
        if (harvests.isEmpty()) {
            Text(text = "No harvests yet")
        } else {
            harvests.forEach { harvest ->
                Text(text = "${harvest.cropName}: ${harvest.quantity} ${harvest.unit}")
            }
        }
    }
}
