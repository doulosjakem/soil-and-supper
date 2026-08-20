package com.soilandsupper.ui.util

import java.util.Calendar

fun epochMillis(year: Int, month: Int, day: Int, hour: Int = 0, minute: Int = 0, second: Int = 0): Long {
    val calendar = Calendar.getInstance()
    calendar.set(year, month - 1, day, hour, minute, second)
    calendar.set(Calendar.MILLISECOND, 0)
    return calendar.timeInMillis
}
