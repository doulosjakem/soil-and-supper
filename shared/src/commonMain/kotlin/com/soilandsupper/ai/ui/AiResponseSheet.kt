package com.soilandsupper.ai.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Undo
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.soilandsupper.ai.command.CommandResult
import com.soilandsupper.ai.orchestration.AIResponse
import com.soilandsupper.ai.orchestration.AICommandProposal

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AiResponseSheet(
    response: AIResponse,
    onDismiss: () -> Unit,
    onConfirm: () -> Unit,
    onCancel: () -> Unit,
    onUndo: () -> Unit,
    onSelectClarification: (String) -> Unit,
    modifier: Modifier = Modifier,
    loading: Boolean = false
) {
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        modifier = modifier
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            if (loading) {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(32.dp),
                        strokeWidth = 3.dp
                    )
                    Text(
                        text = "Working on that...",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                return@Column
            }

            if (response.hasError && response.executedCommands.isEmpty() && response.pendingConfirmation.isEmpty()) {
                AiErrorContent(response = response, onDismiss = onDismiss)
                return@Column
            }

            if (response.message.isNotBlank()) {
                AiMessageBubble(text = response.message)
            }

            if (response.executedCommands.isNotEmpty()) {
                AiExecutedCommands(
                    commands = response.executedCommands,
                    onUndo = onUndo
                )
            }

            if (response.pendingConfirmation.isNotEmpty()) {
                AiConfirmationPanel(
                    proposals = response.pendingConfirmation,
                    onConfirm = onConfirm,
                    onCancel = onCancel
                )
            }

            if (response.needsClarification && response.clarificationQuestion != null) {
                AiClarificationPanel(
                    question = response.clarificationQuestion,
                    pendingProposals = response.pendingConfirmation,
                    onSelectClarification = onSelectClarification,
                    onDismiss = onDismiss
                )
            }

            if (response.hasError && response.executedCommands.isNotEmpty()) {
                AiErrorsList(errors = response.errors)
            }
        }
    }
}

@Composable
private fun AiErrorContent(
    response: AIResponse,
    onDismiss: () -> Unit
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Surface(
            modifier = Modifier.clip(RoundedCornerShape(12.dp)),
            color = MaterialTheme.colorScheme.errorContainer
        ) {
            Text(
                text = response.message.ifBlank { "Something went wrong." },
                modifier = Modifier.padding(16.dp),
                color = MaterialTheme.colorScheme.onErrorContainer,
                style = MaterialTheme.typography.bodyLarge
            )
        }
        TextButton(onClick = onDismiss) {
            Text("Dismiss")
        }
    }
}

@Composable
private fun AiExecutedCommands(
    commands: List<CommandResult>,
    onUndo: () -> Unit
) {
    val succeeded = commands.filter { it.succeeded }
    val failed = commands.filter { !it.succeeded }

    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        if (succeeded.isNotEmpty()) {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                succeeded.forEach { result ->
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        color = MaterialTheme.colorScheme.primaryContainer,
                        shape = RoundedCornerShape(8.dp)
                    ) {
                        Text(
                            text = result.message,
                            modifier = Modifier.padding(12.dp),
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onPrimaryContainer
                        )
                    }
                }
            }
        }

        if (failed.isNotEmpty()) {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    text = "Couldn't do",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.error
                )
                failed.forEach { result ->
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        color = MaterialTheme.colorScheme.errorContainer,
                        shape = RoundedCornerShape(8.dp)
                    ) {
                        Text(
                            text = result.message,
                            modifier = Modifier.padding(12.dp),
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onErrorContainer
                        )
                    }
                }
            }
        }

        if (succeeded.isNotEmpty()) {
            FloatingActionButton(
                onClick = onUndo,
                modifier = Modifier.size(48.dp),
                shape = RoundedCornerShape(16.dp),
                containerColor = MaterialTheme.colorScheme.secondaryContainer
            ) {
                Icon(
                    imageVector = Icons.Default.Undo,
                    contentDescription = "Undo last action",
                    tint = MaterialTheme.colorScheme.onSecondaryContainer
                )
            }
        }
    }
}

@Composable
private fun AiConfirmationPanel(
    proposals: List<com.soilandsupper.ai.orchestration.AICommandProposal>,
    onConfirm: () -> Unit,
    onCancel: () -> Unit
) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(
            text = "Does that sound right?",
            style = MaterialTheme.typography.titleSmall
        )
        proposals.forEach { proposal ->
            Surface(
                modifier = Modifier.fillMaxWidth(),
                color = MaterialTheme.colorScheme.surfaceVariant,
                shape = RoundedCornerShape(8.dp)
            ) {
                Text(
                    text = proposal.explanation.ifBlank { proposal.command.toString() },
                    modifier = Modifier.padding(12.dp),
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            TextButton(
                onClick = onCancel,
                modifier = Modifier.weight(1f)
            ) {
                Text("Cancel")
            }
            Button(
                onClick = onConfirm,
                modifier = Modifier.weight(1f)
            ) {
                Text("Yes, do it")
            }
        }
    }
}

@Composable
private fun AiClarificationPanel(
    question: String,
    pendingProposals: List<com.soilandsupper.ai.orchestration.AICommandProposal>,
    onSelectClarification: (String) -> Unit,
    onDismiss: () -> Unit
) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(
            text = question,
            style = MaterialTheme.typography.titleSmall
        )
        pendingProposals.forEach { proposal ->
            proposal.ambiguities.forEach { ambiguity ->
                Button(
                    onClick = { onSelectClarification(ambiguity) },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.surfaceVariant,
                        contentColor = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                ) {
                    Text(ambiguity)
                }
            }
        }
        TextButton(onClick = onDismiss) {
            Text("Cancel")
        }
    }
}

@Composable
private fun AiErrorsList(errors: List<String>) {
    if (errors.isEmpty()) return
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(
            text = "Couldn't do",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.error
        )
        errors.forEach { error ->
            Text(
                text = error,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.error
            )
        }
    }
}
