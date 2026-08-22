package com.soilandsupper.ui

import com.soilandsupper.shared.domain.model.JournalEntry
import com.soilandsupper.shared.domain.model.Plant
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class JournalRepositoryTest {

    @Test
    fun `getJournalEntriesForPlant returns entries for selected plant`() = runBlocking {
        val plant1 = Plant(id = 1L, name = "Tomato", plantingDate = 1L, location = "", notes = "")
        val plant2 = Plant(id = 2L, name = "Pepper", plantingDate = 1L, location = "", notes = "")
        val repo = FakeGardenRepository(
            initialPlants = listOf(plant1, plant2),
            initialJournalEntries = listOf(
                JournalEntry(id = 1L, plantId = 1L, text = "Tomato note", date = 1L),
                JournalEntry(id = 2L, plantId = 2L, text = "Pepper note", date = 2L)
            )
        )

        val entries = repo.getJournalEntriesForPlant(1L).first()
        assertEquals(1, entries.size)
        assertEquals("Tomato note", entries.first().text)
    }

    @Test
    fun `getJournalEntriesForPlant excludes other plant entries`() = runBlocking {
        val plant1 = Plant(id = 1L, name = "Tomato", plantingDate = 1L, location = "", notes = "")
        val plant2 = Plant(id = 2L, name = "Pepper", plantingDate = 1L, location = "", notes = "")
        val repo = FakeGardenRepository(
            initialPlants = listOf(plant1, plant2),
            initialJournalEntries = listOf(
                JournalEntry(id = 1L, plantId = 1L, text = "Tomato note", date = 1L),
                JournalEntry(id = 2L, plantId = 2L, text = "Pepper note", date = 2L)
            )
        )

        val entries = repo.getJournalEntriesForPlant(2L).first()
        assertEquals(1, entries.size)
        assertEquals("Pepper note", entries.first().text)
    }

    @Test
    fun `getJournalEntriesForPlant returns empty for unknown plant`() = runBlocking {
        val repo = FakeGardenRepository(
            initialJournalEntries = listOf(
                JournalEntry(id = 1L, plantId = 1L, text = "Tomato note", date = 1L)
            )
        )

        val entries = repo.getJournalEntriesForPlant(999L).first()
        assertTrue(entries.isEmpty())
    }
}
