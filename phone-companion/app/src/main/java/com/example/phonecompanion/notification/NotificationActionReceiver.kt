package com.example.phonecompanion.notification

import android.app.NotificationManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.example.phonecompanion.data.CompanionPreferences
import com.example.phonecompanion.util.SoundAndHaptics

class NotificationActionReceiver : BroadcastReceiver() {
    companion object {
        const val ACTION_ADD_CUP = "com.example.phonecompanion.ACTION_ADD_CUP"
    }

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == ACTION_ADD_CUP) {
            val prefs = CompanionPreferences(context)
            prefs.cupsCount += 1

            // Play drip feedback if sound enabled
            SoundAndHaptics.playDripSound(context, prefs.soundEnabled)
            SoundAndHaptics.vibrateTick(context, prefs.vibrationEnabled)

            // Dismiss the notification
            val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.cancel(CompanionNotificationManager.NOTIFICATION_ID_BASE)
        }
    }
}
