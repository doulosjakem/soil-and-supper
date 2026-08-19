package com.soilandsupper.util

actual fun formatDate(pattern: String, epochMillis: Long): String {
    return "[ios date]"
}

actual fun epochMillis(year: Int, month: Int, day: Int, hour: Int, minute: Int, second: Int): Long {
    return 0L
}
