package com.soilandsupper.util

import platform.Foundation.NSDate
import platform.Foundation.NSDateComponents
import platform.Foundation.NSDateFormatter
import platform.Foundation.NSCalendar
import platform.Foundation.dateWithTimeIntervalSince1970

actual fun formatDate(pattern: String, epochMillis: Long): String {
    val date = NSDate.dateWithTimeIntervalSince1970(epochMillis / 1000.0)
    val formatter = NSDateFormatter()
    formatter.dateFormat = pattern
    return formatter.stringFromDate(date)
}

actual fun epochMillis(year: Int, month: Int, day: Int, hour: Int, minute: Int, second: Int): Long {
    val calendar = NSCalendar.currentCalendar
    val components = NSDateComponents().apply {
        this.year = year
        this.month = month
        this.day = day
        this.hour = hour
        this.minute = minute
        this.second = second
    }
    val date = calendar.dateFromComponents(components)
    return date?.timeIntervalSince1970?.times(1000)?.toLong() ?: 0L
}
