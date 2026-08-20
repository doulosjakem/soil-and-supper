package com.soilandsupper.ai

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.performClick
import com.soilandsupper.ai.command.CommandResult
import com.soilandsupper.ai.orchestration.AICommandProposal
import com.soilandsupper.ai.orchestration.AIResponse
import com.soilandsupper.ai.ui.AiMessageBubble
import org.junit.Before
import org.junit.Rule
import org.junit.Test

class AiMessageBubbleTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun messageBubble_displaysText() {
        composeTestRule.setContent {
            AiMessageBubble(text = "Hello from your garden assistant")
        }

        composeTestRule.onNodeWithText("Hello from your garden assistant").assertIsDisplayed()
    }
}

class AiResponseSheetStateTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun readOnlyResponse_displaysMessage() {
        composeTestRule.setContent {
            AiResponseSheetContent(
                response = AIResponse(
                    message = "You have 2 growing spaces."
                ),
                onDismiss = {},
                onConfirm = {},
                onCancel = {},
                onUndo = {},
                onSelectClarification = {}
            )
        }

        composeTestRule.onNodeWithText("You have 2 growing spaces.").assertIsDisplayed()
    }

    @Test
    fun executedCommands_displaysSuccessAndUndo() {
        var undoClicked = false
        composeTestRule.setContent {
            AiResponseSheetContent(
                response = AIResponse(
                    message = "Added Bed 2.",
                    executedCommands = listOf(
                        CommandResult.Success(
                            command = com.soilandsupper.ai.command.GardenCommand.AddGrowingSpace(name = "Bed 2"),
                            message = "Growing space added: Bed 2"
                        )
                    )
                ),
                onDismiss = {},
                onConfirm = {},
                onCancel = {},
                onUndo = { undoClicked = true },
                onSelectClarification = {}
            )
        }

        composeTestRule.onNodeWithText("Executed").assertIsDisplayed()
        composeTestRule.onNodeWithText("Growing space added: Bed 2").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Undo last action").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Undo last action").performClick()
        assert(undoClicked)
    }

    @Test
    fun errorResponse_displaysError() {
        composeTestRule.setContent {
            AiResponseSheetContent(
                response = AIResponse(
                    message = "I'm not sure how to help with that yet.",
                    errors = listOf("Unknown request")
                ),
                onDismiss = {},
                onConfirm = {},
                onCancel = {},
                onUndo = {},
                onSelectClarification = {}
            )
        }

        composeTestRule.onNodeWithText("I'm not sure how to help with that yet.").assertIsDisplayed()
        composeTestRule.onNodeWithText("Unknown request").assertIsDisplayed()
    }
}

@Composable
private fun AiResponseSheetContent(
    response: AIResponse,
    onDismiss: () -> Unit,
    onConfirm: () -> Unit,
    onCancel: () -> Unit,
    onUndo: () -> Unit,
    onSelectClarification: (String) -> Unit
) {
    androidx.compose.material3.Surface(
        modifier = androidx.compose.ui.Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        com.soilandsupper.ai.ui.AiResponseSheet(
            response = response,
            onDismiss = onDismiss,
            onConfirm = onConfirm,
            onCancel = onCancel,
            onUndo = onUndo,
            onSelectClarification = onSelectClarification
        )
    }
}
