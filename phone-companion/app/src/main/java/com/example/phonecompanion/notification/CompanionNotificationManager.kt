package com.example.phonecompanion.notification

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.example.phonecompanion.MainActivity
import com.example.phonecompanion.R
import com.example.phonecompanion.data.CompanionPreferences

object CompanionNotificationManager {
    const val CHANNEL_ID = "phone_companion_wellness"
    const val CHANNEL_NAME = "Companion Reminders"
    const val NOTIFICATION_ID_BASE = 1001

    fun createNotificationChannel(context: Context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(
                CHANNEL_ID,
                CHANNEL_NAME,
                importance
            ).apply {
                description = "Periodic hydration, eye rest, and posture reminders"
            }
            val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    fun showReminderNotification(
        context: Context,
        title: String,
        message: String,
        notificationId: Int = NOTIFICATION_ID_BASE
    ) {
        val prefs = CompanionPreferences(context)
        // Respect Quiet Hours
        if (prefs.isWithinQuietHours()) {
            return
        }

        createNotificationChannel(context)

        val intent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent = PendingIntent.getActivity(
            context,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        // Action Intent to Add 1 Cup directly from notification
        val addCupIntent = Intent(context, NotificationActionReceiver::class.java).apply {
            action = NotificationActionReceiver.ACTION_ADD_CUP
        }
        val addCupPendingIntent = PendingIntent.getBroadcast(
            context,
            1,
            addCupIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val builder = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentTitle(title)
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .addAction(0, "💧 +1 Cup", addCupPendingIntent)

        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(notificationId, builder.build())
    }
}
