package com.example.phonecompanion.util

import android.content.Context
import android.media.MediaPlayer
import android.os.Build
import android.os.CombinedVibration
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import com.example.phonecompanion.R

object SoundAndHaptics {

    fun playDripSound(context: Context, soundEnabled: Boolean) {
        if (!soundEnabled) return
        try {
            val mp = MediaPlayer.create(context, R.raw.drip)
            mp.setOnCompletionListener { player ->
                player.release()
            }
            mp.start()
        } catch (_: Exception) {
            // Ignore sound playback errors if device audio is busy
        }
    }

    fun vibrateTick(context: Context, vibrationEnabled: Boolean) {
        if (!vibrationEnabled) return
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val vm = context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
                vm?.defaultVibrator?.vibrate(VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK))
            } else {
                @Suppress("DEPRECATION")
                val v = context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    v?.vibrate(VibrationEffect.createOneShot(35, VibrationEffect.DEFAULT_AMPLITUDE))
                } else {
                    @Suppress("DEPRECATION")
                    v?.vibrate(35)
                }
            }
        } catch (_: Exception) {
            // Safe fallback if vibration permission or hardware unavailable
        }
    }

    fun vibrateCelebration(context: Context, vibrationEnabled: Boolean) {
        if (!vibrationEnabled) return
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                val v = context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
                val timings = longArrayOf(0, 80, 80, 120, 80, 150)
                val amplitudes = intArrayOf(0, 180, 0, 220, 0, 255)
                v?.vibrate(VibrationEffect.createWaveform(timings, amplitudes, -1))
            }
        } catch (_: Exception) {
        }
    }
}
