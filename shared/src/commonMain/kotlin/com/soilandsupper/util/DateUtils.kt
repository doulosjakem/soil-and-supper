package com.soilandsupper.util

expect fun formatDate(pattern: String, epochMillis: Long): String

expect fun epochMillis(year: Int, month: Int, day: Int, hour: Int = 0, minute: Int = 0, second: Int = 0): Long
