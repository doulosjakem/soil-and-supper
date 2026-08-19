package com.soilandsupper.shared.domain.model

data class GrowingSpace(
    val id: Long = 0,
    val name: String,
    val notes: String? = null,
    val spaceType: String? = null,
    val width: Double? = null,
    val length: Double? = null,
    val gardenId: Long? = null,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
) {
    val area: Double?
        get() = if (width != null && length != null && width > 0 && length > 0) width * length else null
}

