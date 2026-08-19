package com.soilandsupper.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.runtime.remember
import com.soilandsupper.domain.model.GrowingSpace
import com.soilandsupper.domain.model.Occupancy
import com.soilandsupper.domain.model.PlantingSuggestion
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

                if (spaceModel.occupancy != null) {
                    PhaseBadge(phase = spaceModel.occupancy.phase)
                } else if (spaceModel.isAvailable) {
                    PhaseBadge(phase = CropTimelinePhase.NOT_PLANTED, label = "Empty")
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            if (spaceModel.occupancy != null) {
                OccupancyDetails(occupancyModel = spaceModel.occupancy)
            } else if (spaceModel.isAvailable) {
                Text(
                    text = "No current crop",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            if (spaceModel.futureSuggestions != null && spaceModel.futureSuggestions.suggestions.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                FutureSuggestions(suggestions = spaceModel.futureSuggestions.suggestions)
            }
        }
    }
}

@Composable
private fun PhaseBadge(phase: CropTimelinePhase, label: String? = null) {
    val displayLabel = label ?: phase.displayName
    val color = when (phase) {
        CropTimelinePhase.NOT_PLANTED -> MaterialTheme.colorScheme.outline
        CropTimelinePhase.GROWING -> MaterialTheme.colorScheme.primary
        CropTimelinePhase.PRODUCING -> MaterialTheme.colorScheme.primary
        CropTimelinePhase.NEARING_RELEASE -> MaterialTheme.colorScheme.tertiary
        CropTimelinePhase.COMPLETED -> MaterialTheme.colorScheme.outline
    }

    androidx.compose.material3.Surface(
        color = color.copy(alpha = 0.15f),
        contentColor = color,
        shape = androidx.compose.foundation.shape.CircleShape
    ) {
        Text(
            text = displayLabel,
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
            style = MaterialTheme.typography.labelSmall
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
private fun FutureSuggestions(suggestions: List<PlantingSuggestion>) {
    val dateFormat = remember { SimpleDateFormat("MMM d", Locale.getDefault()) }

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
            text = "Next possibilities",
            style = MaterialTheme.typography.titleSmall,
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
                        text = "Plant ${dateFormat.format(suggestion.suggestedPlantingDate)}",
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
