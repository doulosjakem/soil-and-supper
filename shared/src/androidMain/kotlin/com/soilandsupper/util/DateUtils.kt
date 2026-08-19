package com.soilandsupper.util

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

actual fun formatDate(pattern: String, epochMillis: Long): String {
    return SimpleDateFormat(pattern, Locale.getDefault()).format(Date(epochMillis))
}

actual fun epochMillis(year: Int, month: Int, day: Int, hour: Int, minute: Int, second: Int): Long {
    val calendar = java.util.Calendar.getInstance()
    calendar.set(year, month - 1, day, hour, minute, second)
    calendar.set(java.util.Calendar.MILLISECOND, 0)
    return calendar.timeInMillis
}
