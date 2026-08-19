package com.soilandsupper.ui

import androidx.compose.foundation.background
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
import com.soilandsupper.domain.model.GrowingSpace
import com.soilandsupper.domain.model.Occupancy
import java.text.SimpleDateFormat
import java.util.Locale

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
                    if (!spaceModel.space.notes.isNullOrBlank()) {
                        Text(
                            text = spaceModel.space.notes,
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
            } else if (spaceModel.occupancy != null) {
                OccupancyDetails(occupancyModel = spaceModel.occupancy)
            }

            if (spaceModel.futureSuggestions != null && spaceModel.futureSuggestions.suggestions.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                FutureSuggestions(model = spaceModel.futureSuggestions)
            }
        }
    }
}

@Composable
private fun AvailableSpaceDetails(spaceModel: GrowingSpaceTimelineModel) {
    if (spaceModel.currentSuggestions != null && spaceModel.currentSuggestions.suggestions.isNotEmpty()) {
        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(
                text = "What you can plant now",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(4.dp))
            spaceModel.currentSuggestions.suggestions.take(3).forEach { suggestion ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = suggestion.cropName,
                            style = MaterialTheme.typography.bodyMedium
                        )
                        if (!suggestion.varietyName.isNullOrBlank()) {
                            Text(
                                text = suggestion.varietyName,
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
                            val dateFormat = remember { SimpleDateFormat("MMM d", Locale.getDefault()) }
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
    } else {
        Text(
            text = "Nothing plantable right now",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun OccupancyDetails(occupancyModel: OccupancyTimelineModel) {
    val dateFormat = remember { SimpleDateFormat("MMM d", Locale.getDefault()) }

    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(
            text = occupancyModel.occupancy.displayName,
            style = MaterialTheme.typography.bodyLarge
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

        if (occupancyModel.daysUntilHarvest != null && occupancyModel.daysUntilHarvest > 0) {
            Text(
                text = "Harvest expected in ${occupancyModel.daysUntilHarvest} days",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else if (occupancyModel.occupancy.expectedHarvestDate != null) {
            Text(
                text = "Harvest ~${dateFormat.format(occupancyModel.occupancy.expectedHarvestDate)}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        if (occupancyModel.daysUntilRelease != null && occupancyModel.daysUntilRelease > 0) {
            Text(
                text = "Space opens in ${occupancyModel.daysUntilRelease} days",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else if (occupancyModel.occupancy.expectedReleaseDate != null) {
            Text(
                text = "Expected opening ~${dateFormat.format(occupancyModel.occupancy.expectedReleaseDate)}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
private fun FutureSuggestions(model: FutureSuggestionsTimelineModel) {
    val dateFormat = remember { SimpleDateFormat("MMM d", Locale.getDefault()) }
    val suggestions = model.suggestions
    val openingText = dateFormat.format(model.openingDate)

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(
                color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp)
            )
            .padding(12.dp)
    ) {
        Text(
            text = "After this",
            style = MaterialTheme.typography.titleSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = "Space may open ~$openingText · nothing to plant yet",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        Spacer(modifier = Modifier.height(4.dp))

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
                    if (!suggestion.varietyName.isNullOrBlank()) {
                        Text(
                            text = suggestion.varietyName,
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
