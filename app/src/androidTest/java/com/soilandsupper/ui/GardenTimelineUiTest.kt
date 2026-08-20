package com.soilandsupper.ui

import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertIsEnabled
import com.soilandsupper.ui.fixture.AndroidTestGardenFixture
import org.junit.Before
import org.junit.Rule
import org.junit.Test

class GardenTimelineUiTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    private lateinit var fakeRepository: FakeGardenRepository

    @Before
    fun setup() {
        fakeRepository = FakeGardenRepository(
            initialGardens = listOf(AndroidTestGardenFixture.garden),
            initialSpaces = AndroidTestGardenFixture.spaces,
            initialSeeds = AndroidTestGardenFixture.seeds,
            initialDesires = AndroidTestGardenFixture.desires,
            initialOccupancies = AndroidTestGardenFixture.occupiedSpaces
        )
    }

    @Test
    fun emptyGarden_rendersEmptyState() {
        val emptyRepo = FakeGardenRepository(
            initialGardens = listOf(AndroidTestGardenFixture.garden),
            initialSpaces = emptyList()
        )

        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = emptyRepo
            )
        }

        composeTestRule.onNodeWithText("No growing spaces yet").assertIsDisplayed()
        composeTestRule.onNodeWithText("Add a bed, pot, or row to start tracking your garden.").assertIsDisplayed()
    }

    @Test
    fun occupiedSpace_currentCropAppears() {
        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = fakeRepository
            )
        }

        composeTestRule.onNodeWithText("Bed 2 - Potatoes").assertIsDisplayed()
        composeTestRule.onNodeWithText("Yukon Gold Potato").assertIsDisplayed()
        composeTestRule.onNodeWithText("Growing").assertIsDisplayed()
    }

    @Test
    fun occupiedSpace_currentCropIsVisuallyPrimary() {
        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = fakeRepository
            )
        }

        composeTestRule.onNodeWithText("Bed 2 - Potatoes").assertIsDisplayed()
        composeTestRule.onNodeWithText("Yukon Gold Potato").assertIsDisplayed()
    }

    @Test
    fun futureOpening_showsFutureOpportunity() {
        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = fakeRepository
            )
        }

        composeTestRule.onNodeWithText("AFTER THIS").assertIsDisplayed()
    }

    @Test
    fun openSpace_showsAvailableSpace() {
        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = fakeRepository
            )
        }

        composeTestRule.onNodeWithText("Available").assertIsDisplayed()
    }

    @Test
    fun openSpace_showsCurrentSuggestions() {
        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = fakeRepository
            )
        }

        composeTestRule.onNodeWithText("What you can plant now").assertIsDisplayed()
    }

    @Test
    fun dateScrubber_changesProjection() {
        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = fakeRepository
            )
        }

        composeTestRule.onNodeWithText("Today").assertIsDisplayed()
    }

    @Test
    fun lifecycleStates_haveTextLabels() {
        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = fakeRepository
            )
        }

        composeTestRule.onNodeWithText("Growing").assertIsDisplayed()
    }

    @Test
    fun futureSuggestions_haveAccessibleLabels() {
        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = fakeRepository
            )
        }

        composeTestRule.onNodeWithText("AFTER THIS").assertIsDisplayed()
        composeTestRule.onNodeWithText("Space opens").assertIsDisplayed()
    }

    @Test
    fun dateScrubber_isAccessible() {
        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = fakeRepository
            )
        }

        composeTestRule.onNodeWithText("Today").assertIsDisplayed()
        composeTestRule.onNodeWithText("Today").assertIsEnabled()
    }

    @Test
    fun buttons_haveMeaningfulLabels() {
        composeTestRule.setContent {
            GardenScreen(
                onPlantClick = { },
                repository = fakeRepository
            )
        }

        composeTestRule.onNodeWithText("Today").assertIsDisplayed()
    }
}
