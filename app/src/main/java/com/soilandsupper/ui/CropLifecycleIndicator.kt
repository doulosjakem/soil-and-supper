package com.soilandsupper.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.RoundRect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun CropLifecycleIndicator(
    phase: CropTimelinePhase,
    modifier: Modifier = Modifier
) {
    val color = when (phase) {
        CropTimelinePhase.NOT_PLANTED -> MaterialTheme.colorScheme.outline
        CropTimelinePhase.GROWING -> MaterialTheme.colorScheme.primary.copy(alpha = 0.4f)
        CropTimelinePhase.PRODUCING -> MaterialTheme.colorScheme.primary
        CropTimelinePhase.NEARING_RELEASE -> MaterialTheme.colorScheme.tertiary.copy(alpha = 0.6f)
        CropTimelinePhase.COMPLETED -> MaterialTheme.colorScheme.outline.copy(alpha = 0.3f)
    }

    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(8.dp)
    ) {
        val cornerRadius = CornerRadius(4.dp.toPx(), 4.dp.toPx())
        val rect = RoundRect(
            left = 0f,
            top = 0f,
            right = size.width,
            bottom = size.height,
            cornerRadius = cornerRadius
        )
        drawRoundRect(color = color, topLeft = androidx.compose.ui.geometry.Offset.Zero, size = size, cornerRadius = CornerRadius(4.dp.toPx()))
    }
}
