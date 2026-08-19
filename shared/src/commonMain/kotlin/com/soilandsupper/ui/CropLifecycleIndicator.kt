package com.soilandsupper.ui

import com.soilandsupper.gardentimeline.CropTimelinePhase
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

/**
 * Lifecycle stage accent color. Yes-GROWING and PRODUCING share the primary hue; downtime
 * (not planted, establishing, completed) and transition (nearing release) use distinct,
 * more muted hues so the indicator reads as stages rather than a completion meter.
 */
@Composable
internal fun cropPhaseColor(phase: CropTimelinePhase): Color = when (phase) {
    CropTimelinePhase.NOT_PLANTED -> MaterialTheme.colorScheme.outline
    CropTimelinePhase.ESTABLISHING -> MaterialTheme.colorScheme.outline
    CropTimelinePhase.GROWING -> MaterialTheme.colorScheme.primary
    CropTimelinePhase.PRODUCING -> MaterialTheme.colorScheme.primary
    CropTimelinePhase.NEARING_RELEASE -> MaterialTheme.colorScheme.tertiary
    CropTimelinePhase.COMPLETED -> MaterialTheme.colorScheme.outline
}

/**
 * A lifecycle *stage band*, deliberately not a progress meter (no 0% -> 100% -> DONE):
 *
 *  - Not planted / Completed: near-empty trace.
 *  - Establishing: minimal, outline-only presence.
 *  - Growing: a real, stronger fill.
 *  - Producing: full, strong fill with a subtle harvest notch.
 *  - Nearing release: a subdued, transitional band (the crop is still there, the space
 *    may simply open around this time - it is not "almost finished").
 *
 * The fill never advances monotonically to a crisp "done", so it cannot be read as a
 * completion percentage.
 */
@Composable
fun CropLifecycleIndicator(
    phase: CropTimelinePhase,
    modifier: Modifier = Modifier
) {
    val trackColor = MaterialTheme.colorScheme.outline.copy(alpha = 0.18f)
    val fillColor = when (phase) {
        CropTimelinePhase.NOT_PLANTED -> trackColor
        CropTimelinePhase.ESTABLISHING -> MaterialTheme.colorScheme.outline.copy(alpha = 0.75f)
        CropTimelinePhase.GROWING -> MaterialTheme.colorScheme.primary.copy(alpha = 0.7f)
        CropTimelinePhase.PRODUCING -> MaterialTheme.colorScheme.primary
        CropTimelinePhase.NEARING_RELEASE -> MaterialTheme.colorScheme.tertiary.copy(alpha = 0.6f)
        CropTimelinePhase.COMPLETED -> MaterialTheme.colorScheme.outline.copy(alpha = 0.3f)
    }
    val fillFraction = when (phase) {
        CropTimelinePhase.NOT_PLANTED -> 0f
        CropTimelinePhase.ESTABLISHING -> 0.35f
        CropTimelinePhase.GROWING -> 0.7f
        CropTimelinePhase.PRODUCING -> 1f
        CropTimelinePhase.NEARING_RELEASE -> 0.5f
        CropTimelinePhase.COMPLETED -> 0.12f
    }
    val isProducing = phase == CropTimelinePhase.PRODUCING
    val harvestNotchColor = MaterialTheme.colorScheme.background.copy(alpha = 0.7f)

    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(8.dp)
    ) {
        val radius = CornerRadius(size.height / 2f, size.height / 2f)
        // Track
        drawRoundRect(color = trackColor, topLeft = Offset.Zero, size = size, cornerRadius = radius)

        if (fillFraction > 0f) {
            drawRoundRect(
                color = fillColor,
                topLeft = Offset.Zero,
                size = Size(size.width * fillFraction, size.height),
                cornerRadius = radius
            )
        }

        // Subtle "harvesting can begin" cue at the leading edge while producing.
        if (isProducing) {
            drawCircle(
                color = harvestNotchColor,
                radius = size.height * 0.22f,
                center = Offset(size.height * 0.5f, size.height / 2f)
            )
        }
    }
}
