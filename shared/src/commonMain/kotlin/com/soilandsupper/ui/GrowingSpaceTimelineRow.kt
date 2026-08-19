package com.soilandsupper.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.soilandsupper.gardentimeline.CropTimelinePhase
import com.soilandsupper.gardentimeline.CurrentSuggestionsTimelineModel
import com.soilandsupper.gardentimeline.FutureSuggestionsTimelineModel
import com.soilandsupper.gardentimeline.GrowingSpaceTimelineModel
import com.soilandsupper.gardentimeline.OccupancyTimelineModel
import com.soilandsupper.shared.domain.model.GrowingSpace
import com.soilandsupper.shared.domain.model.Occupancy
import com.soilandsupper.shared.domain.model.PlantingSuggestion
import com.soilandsupper.util.formatDate

@Composable
fun GrowingSpaceTimelineRow(
    spaceModel: GrowingSpaceTimelineModel,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = spaceModel.space.name,
                        style = MaterialTheme.typography.titleMedium
                    )
                    val notes = spaceModel.space.notes
                    if (notes != null && notes.isNotBlank()) {
                        Text(
                            text = notes,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }

                if (spaceModel.isAvailable) {
                    Surface(
                        color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.6f),
                        contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
                        shape = androidx.compose.foundation.shape.CircleShape
                    ) {
                        Text(
                            text = "Available",
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
                            style = MaterialTheme.typography.labelSmall
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            if (spaceModel.isAvailable) {
                AvailableSpaceDetails(spaceModel = spaceModel)
            } else {
                spaceModel.occupancy?.let { occupancy ->
                    OccupancyDetails(occupancyModel = occupancy)
                }
            }

            spaceModel.futureSuggestions?.let { future ->
                if (future.suggestions.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    FutureSuggestions(model = future)
                }
            }
        }
    }
}

@Composable
private fun AvailableSpaceDetails(spaceModel: GrowingSpaceTimelineModel) {
    val current = spaceModel.currentSuggestions
    if (current != null && current.suggestions.isNotEmpty()) {
        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(
                text = "What you can plant now",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(4.dp))
            current.suggestions.take(3).forEach { suggestion ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = suggestion.cropName,
                            style = MaterialTheme.typography.bodyMedium
                        )
                        val varietyName = suggestion.varietyName
                        if (varietyName != null && varietyName.isNotBlank()) {
                            Text(
                                text = varietyName,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                    Column(horizontalAlignment = androidx.compose.ui.Alignment.End) {
                        Text(
                            text = "Plant now",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        suggestion.estimatedHarvestDate?.let { harvest ->
                            val dateFormat = remember { "MMM d" }
                            Text(
                                text = "Harvest ~${formatDate(dateFormat, harvest)}",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    } else {
        Text(
            text = "Nothing plantable right now",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun OccupancyDetails(occupancyModel: OccupancyTimelineModel) {
    val dateFormat = remember { "MMM d" }

    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(
            text = occupancyModel.occupancy.displayName,
            style = MaterialTheme.typography.titleLarge
        )

        Text(
            text = occupancyModel.phase.displayName,
            style = MaterialTheme.typography.labelLarge,
            color = cropPhaseColor(occupancyModel.phase)
        )

        CropLifecycleIndicator(phase = occupancyModel.phase)

        if (occupancyModel.phase == CropTimelinePhase.PRODUCING) {
            Text(
                text = "Harvesting can begin",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.primary
            )
        }

        val daysUntilHarvest = occupancyModel.daysUntilHarvest
        if (daysUntilHarvest != null && daysUntilHarvest > 0) {
            Text(
                text = "Harvest expected in $daysUntilHarvest days",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            val expectedHarvest = occupancyModel.occupancy.expectedHarvestDate
            if (expectedHarvest != null) {
                Text(
                    text = "Harvest ~${formatDate(dateFormat, expectedHarvest)}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }

        val daysUntilRelease = occupancyModel.daysUntilRelease
        if (daysUntilRelease != null && daysUntilRelease > 0) {
            Text(
                text = "Space opens in $daysUntilRelease days",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            val expectedRelease = occupancyModel.occupancy.expectedReleaseDate
            if (expectedRelease != null) {
                Text(
                    text = "Expected opening ~${formatDate(dateFormat, expectedRelease)}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
private fun FutureSuggestions(model: FutureSuggestionsTimelineModel) {
    val dateFormat = remember { "MMM d" }
    val suggestions = model.suggestions
    val openingText = formatDate(dateFormat, model.openingDate)

    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(
            text = "AFTER THIS",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = "Space opens ~$openingText",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        suggestions.take(3).forEach { suggestion ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = suggestion.cropName,
                        style = MaterialTheme.typography.bodyMedium
                    )
                    val varietyName = suggestion.varietyName
                    if (varietyName != null && varietyName.isNotBlank()) {
                        Text(
                            text = varietyName,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                Column(horizontalAlignment = androidx.compose.ui.Alignment.End) {
                    Text(
                        text = "Plant ~${dateFormat.format(suggestion.suggestedPlantingDate)}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    suggestion.estimatedHarvestDate?.let { harvest ->
                        Text(
                            text = "Harvest ~${dateFormat.format(harvest)}",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
    }
}
