package com.soilandsupper.util

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

actual fun formatDate(pattern: String, epochMillis: Long): String {
    return SimpleDateFormat(pattern, Locale.getDefault()).format(Date(epochMillis))
}
