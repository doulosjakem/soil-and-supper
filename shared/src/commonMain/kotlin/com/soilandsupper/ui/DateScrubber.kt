package com.soilandsupper.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.Button
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.soilandsupper.util.epochMillis
import com.soilandsupper.util.formatDate
import kotlinx.datetime.Instant
import kotlinx.datetime.TimeZone
import kotlinx.datetime.toLocalDateTime

@Composable
fun DateScrubber(
    selectedDate: Long,
    onDateSelected: (Long) -> Unit,
    modifier: Modifier = Modifier
) {
    val currentYear = remember(selectedDate) {
        val instant = kotlinx.datetime.Instant.fromEpochMilliseconds(selectedDate)
        instant.toLocalDateTime(kotlinx.datetime.TimeZone.UTC).year
    }

    val startOfYear = remember(currentYear) {
        epochMillis(currentYear, 1, 1, 0, 0, 0)
    }

    val endOfYear = remember(currentYear) {
        epochMillis(currentYear, 12, 31, 23, 59, 59)
    }

    val dateFormat = remember { "MMM d, yyyy" }
    val monthFormat = remember { "MMM" }

    val totalDays = ((endOfYear - startOfYear) / (1000 * 60 * 60 * 24)).toFloat()
    val isToday = isSameDay(selectedDate, System.currentTimeMillis())

    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = if (isToday) "Today · ${formatDate(dateFormat, selectedDate)}" else formatDate(dateFormat, selectedDate),
            style = MaterialTheme.typography.titleLarge,
            color = MaterialTheme.colorScheme.primary
        )

        androidx.compose.material3.Slider(
            value = ((selectedDate - startOfYear).toFloat() / totalDays).coerceIn(0f, 1f),
            onValueChange = { fraction ->
                val newDate = (startOfYear + (fraction * totalDays).toLong()).coerceIn(startOfYear, endOfYear)
                onDateSelected(newDate)
            },
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp)
        )

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = formatDate(monthFormat, startOfYear),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Text(
                text = formatDate(monthFormat, endOfYear),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Center
        ) {
            Button(onClick = { onDateSelected(System.currentTimeMillis()) }) {
                Text("Today")
            }
        }
    }
}

private fun isSameDay(a: Long, b: Long): Boolean {
    val instantA = kotlinx.datetime.Instant.fromEpochMilliseconds(a)
    val instantB = kotlinx.datetime.Instant.fromEpochMilliseconds(b)
    val dateA = instantA.toLocalDateTime(kotlinx.datetime.TimeZone.UTC).date
    val dateB = instantB.toLocalDateTime(kotlinx.datetime.TimeZone.UTC).date
    return dateA == dateB
}
