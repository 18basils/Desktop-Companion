package com.example.phonecompanion.data

import android.content.Context
import android.content.SharedPreferences
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class CompanionPreferences(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences("phone_companion_prefs", Context.MODE_PRIVATE)

    companion object {
        const val PREF_CUPS_COUNT = "cups_count"
        const val PREF_DAILY_GOAL = "daily_goal"
        const val PREF_LAST_RESET_DATE = "last_reset_date"
        const val PREF_AVATAR = "current_avatar"
        const val PREF_AUTO_CYCLE = "auto_cycle_avatars"
        const val PREF_HYDRATION_INT = "hydration_interval"
        const val PREF_EYE_INT = "eye_rest_interval"
        const val PREF_POSTURE_INT = "posture_interval"
        const val PREF_HYDRATION_ON = "hydration_enabled"
        const val PREF_EYE_ON = "eye_rest_enabled"
        const val PREF_POSTURE_ON = "posture_enabled"
        const val PREF_QUIET_HOURS_ON = "quiet_hours_enabled"
        const val PREF_QUIET_START_H = "quiet_hours_start_hour"
        const val PREF_QUIET_START_M = "quiet_hours_start_min"
        const val PREF_QUIET_END_H = "quiet_hours_end_hour"
        const val PREF_QUIET_END_M = "quiet_hours_end_min"
        const val PREF_WORK_START_H = "work_start_hour"
        const val PREF_WORK_START_M = "work_start_min"
        const val PREF_WORK_END_H = "work_end_hour"
        const val PREF_WORK_END_M = "work_end_min"
        const val PREF_SOUND_ON = "sound_enabled"
        const val PREF_VIBRATE_ON = "vibration_enabled"
        const val PREF_PET_COUNT = "pet_count"

        val AVATAR_LIST = listOf(
            "Pixel Guy",
            "Cute Kitty",
            "Robo Buddy",
            "Slime",
            "Frog",
            "Ghost"
        )
    }

    private val dateFormat = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())

    var cupsCount: Int
        get() {
            checkMidnightReset()
            return prefs.getInt(PREF_CUPS_COUNT, 0)
        }
        set(value) {
            prefs.edit().putInt(PREF_CUPS_COUNT, value.coerceAtLeast(0)).apply()
        }

    var dailyGoal: Int
        get() = prefs.getInt(PREF_DAILY_GOAL, 8)
        set(value) = prefs.edit().putInt(PREF_DAILY_GOAL, value.coerceIn(1, 20)).apply()

    var lastResetDate: String
        get() = prefs.getString(PREF_LAST_RESET_DATE, "") ?: ""
        set(value) = prefs.edit().putString(PREF_LAST_RESET_DATE, value).apply()

    var currentAvatar: String
        get() = prefs.getString(PREF_AVATAR, "Pixel Guy") ?: "Pixel Guy"
        set(value) = prefs.edit().putString(PREF_AVATAR, value).apply()

    var autoCycleAvatars: Boolean
        get() = prefs.getBoolean(PREF_AUTO_CYCLE, true)
        set(value) = prefs.edit().putBoolean(PREF_AUTO_CYCLE, value).apply()

    var hydrationInterval: Int
        get() = prefs.getInt(PREF_HYDRATION_INT, 45)
        set(value) = prefs.edit().putInt(PREF_HYDRATION_INT, value).apply()

    var eyeRestInterval: Int
        get() = prefs.getInt(PREF_EYE_INT, 20)
        set(value) = prefs.edit().putInt(PREF_EYE_INT, value).apply()

    var postureInterval: Int
        get() = prefs.getInt(PREF_POSTURE_INT, 60)
        set(value) = prefs.edit().putInt(PREF_POSTURE_INT, value).apply()

    var hydrationEnabled: Boolean
        get() = prefs.getBoolean(PREF_HYDRATION_ON, true)
        set(value) = prefs.edit().putBoolean(PREF_HYDRATION_ON, value).apply()

    var eyeRestEnabled: Boolean
        get() = prefs.getBoolean(PREF_EYE_ON, true)
        set(value) = prefs.edit().putBoolean(PREF_EYE_ON, value).apply()

    var postureEnabled: Boolean
        get() = prefs.getBoolean(PREF_POSTURE_ON, true)
        set(value) = prefs.edit().putBoolean(PREF_POSTURE_ON, value).apply()

    var quietHoursEnabled: Boolean
        get() = prefs.getBoolean(PREF_QUIET_HOURS_ON, true)
        set(value) = prefs.edit().putBoolean(PREF_QUIET_HOURS_ON, value).apply()

    var quietStartHour: Int
        get() = prefs.getInt(PREF_QUIET_START_H, 22) // 10:00 PM
        set(value) = prefs.edit().putInt(PREF_QUIET_START_H, value).apply()

    var quietStartMin: Int
        get() = prefs.getInt(PREF_QUIET_START_M, 0)
        set(value) = prefs.edit().putInt(PREF_QUIET_START_M, value).apply()

    var quietEndHour: Int
        get() = prefs.getInt(PREF_QUIET_END_H, 8) // 8:00 AM
        set(value) = prefs.edit().putInt(PREF_QUIET_END_H, value).apply()

    var quietEndMin: Int
        get() = prefs.getInt(PREF_QUIET_END_M, 0)
        set(value) = prefs.edit().putInt(PREF_QUIET_END_M, value).apply()

    var workStartHour: Int
        get() = prefs.getInt(PREF_WORK_START_H, 9) // 9:00 AM
        set(value) = prefs.edit().putInt(PREF_WORK_START_H, value).apply()

    var workStartMin: Int
        get() = prefs.getInt(PREF_WORK_START_M, 0)
        set(value) = prefs.edit().putInt(PREF_WORK_START_M, value).apply()

    var workEndHour: Int
        get() = prefs.getInt(PREF_WORK_END_H, 18) // 6:30 PM
        set(value) = prefs.edit().putInt(PREF_WORK_END_H, value).apply()

    var workEndMin: Int
        get() = prefs.getInt(PREF_WORK_END_M, 30)
        set(value) = prefs.edit().putInt(PREF_WORK_END_M, value).apply()

    var soundEnabled: Boolean
        get() = prefs.getBoolean(PREF_SOUND_ON, true)
        set(value) = prefs.edit().putBoolean(PREF_SOUND_ON, value).apply()

    var vibrationEnabled: Boolean
        get() = prefs.getBoolean(PREF_VIBRATE_ON, true)
        set(value) = prefs.edit().putBoolean(PREF_VIBRATE_ON, value).apply()

    var petCount: Int
        get() = prefs.getInt(PREF_PET_COUNT, 0)
        set(value) = prefs.edit().putInt(PREF_PET_COUNT, value).apply()

    /**
     * Checks if local date has changed past midnight.
     * If so, resets cupsCount to 0 and stores current date.
     */
    fun checkMidnightReset(): Boolean {
        val todayStr = dateFormat.format(Date())
        val savedDate = prefs.getString(PREF_LAST_RESET_DATE, "")
        if (savedDate != todayStr) {
            prefs.edit()
                .putInt(PREF_CUPS_COUNT, 0)
                .putString(PREF_LAST_RESET_DATE, todayStr)
                .apply()
            return true
        }
        return false
    }

    /**
     * Cycles to the next companion avatar.
     */
    fun cycleNextAvatar(): String {
        val currentIdx = AVATAR_LIST.indexOf(currentAvatar)
        val nextIdx = (if (currentIdx >= 0) currentIdx + 1 else 0) % AVATAR_LIST.size
        val nextName = AVATAR_LIST[nextIdx]
        currentAvatar = nextName
        return nextName
    }

    /**
     * Checks whether current system time falls within Quiet Hours (e.g. 22:00 to 08:00).
     */
    fun isWithinQuietHours(): Boolean {
        if (!quietHoursEnabled) return false
        val cal = Calendar.getInstance()
        val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
        val startMinutes = quietStartHour * 60 + quietStartMin
        val endMinutes = quietEndHour * 60 + quietEndMin

        return if (startMinutes < endMinutes) {
            currentMinutes in startMinutes until endMinutes
        } else {
            // Spans over midnight, e.g., 22:00 (1320) to 08:00 (480)
            currentMinutes >= startMinutes || currentMinutes < endMinutes
        }
    }

    /**
     * Checks whether current day and time falls within Monday-Friday work schedule (9:00 AM to 6:30 PM).
     */
    fun isWithinWorkSchedule(): Boolean {
        val cal = Calendar.getInstance()
        val dayOfWeek = cal.get(Calendar.DAY_OF_WEEK) // Sunday=1, Monday=2, Friday=6, Sat=7
        val isWorkDay = dayOfWeek in Calendar.MONDAY..Calendar.FRIDAY
        if (!isWorkDay) return false

        val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
        val startMinutes = workStartHour * 60 + workStartMin
        val endMinutes = workEndHour * 60 + workEndMin
        return currentMinutes in startMinutes until endMinutes
    }

    /**
     * Returns a human status string for display.
     */
    fun getScheduleStatus(): String {
        return when {
            isWithinQuietHours() -> "🌙 Quiet Hours Active (Reminders Muted)"
            isWithinWorkSchedule() -> "🟢 Active Work Hours (Monitoring Schedule)"
            else -> "☕ Off-Schedule (Resting & Hydrated)"
        }
    }
}
