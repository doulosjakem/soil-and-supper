package com.soilandsupper.shared.domain.model

data class JournalEntry(
    val id: Long = 0,
    val plantId: Long,
    val date: Long = System.currentTimeMillis(),
    val text: String
)

