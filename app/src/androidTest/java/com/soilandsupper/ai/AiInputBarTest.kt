package com.soilandsupper.ai

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performTextInput
import com.soilandsupper.ai.ui.AiInputBar
import org.junit.Before
import org.junit.Rule
import org.junit.Test

class AiInputBarTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun inputBar_rendersPlaceholderAndActions() {
        composeTestRule.setContent {
            AiInputBar(
                value = "",
                onValueChange = {},
                onSend = {},
                onVoice = {},
                onCamera = {},
                onDocument = {}
            )
        }

        composeTestRule.onNodeWithText("Ask about your garden...").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Voice input").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Camera").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Import document").assertIsDisplayed()
    }

    @Test
    fun inputBar_sendButtonCallsOnSend() {
        var sent = false
        composeTestRule.setContent {
            AiInputBar(
                value = "add a bed",
                onValueChange = {},
                onSend = { sent = true },
                onVoice = {},
                onCamera = {},
                onDocument = {}
            )
        }

        composeTestRule.onNodeWithContentDescription("Send").performClick()
        assert(sent)
    }

    @Test
    fun inputBar_voiceButtonCallsOnVoice() {
        var voiceClicked = false
        composeTestRule.setContent {
            AiInputBar(
                value = "",
                onValueChange = {},
                onSend = {},
                onVoice = { voiceClicked = true },
                onCamera = {},
                onDocument = {}
            )
        }

        composeTestRule.onNodeWithContentDescription("Voice input").performClick()
        assert(voiceClicked)
    }

    @Test
    fun inputBar_cameraButtonCallsOnCamera() {
        var cameraClicked = false
        composeTestRule.setContent {
            AiInputBar(
                value = "",
                onValueChange = {},
                onSend = {},
                onVoice = {},
                onCamera = { cameraClicked = true },
                onDocument = {}
            )
        }

        composeTestRule.onNodeWithContentDescription("Camera").performClick()
        assert(cameraClicked)
    }

    @Test
    fun inputBar_documentButtonCallsOnDocument() {
        var documentClicked = false
        composeTestRule.setContent {
            AiInputBar(
                value = "",
                onValueChange = {},
                onSend = {},
                onVoice = {},
                onCamera = {},
                onDocument = { documentClicked = true }
            )
        }

        composeTestRule.onNodeWithContentDescription("Import document").performClick()
        assert(documentClicked)
    }

    @Test
    fun inputBar_clearsAfterSend() {
        var currentValue = "add a bed"
        composeTestRule.setContent {
            AiInputBar(
                value = currentValue,
                onValueChange = { currentValue = it },
                onSend = { currentValue = "" },
                onVoice = {},
                onCamera = {},
                onDocument = {}
            )
        }

        composeTestRule.onNodeWithText("add a bed").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Send").performClick()
        composeTestRule.onNodeWithText("Ask about your garden...").assertIsDisplayed()
    }
}
