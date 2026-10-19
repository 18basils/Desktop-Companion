package com.example.phonecompanion.ui.main

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.example.phonecompanion.data.CompanionPreferences
import com.example.phonecompanion.notification.CompanionNotificationManager
import com.example.phonecompanion.theme.DarkBg
import com.example.phonecompanion.theme.DeepNavy
import com.example.phonecompanion.theme.NeonCyan
import com.example.phonecompanion.theme.WaterBlue
import com.example.phonecompanion.ui.components.AvatarSelectorCard
import com.example.phonecompanion.ui.components.HydrationCard
import com.example.phonecompanion.ui.components.PixelAvatarView
import com.example.phonecompanion.ui.components.RemindersCard
import com.example.phonecompanion.ui.components.ScheduleCard
import com.example.phonecompanion.ui.components.SettingsCard
import com.example.phonecompanion.util.SoundAndHaptics
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

enum class CompanionTab(val title: String, val icon: String) {
    COMPANION("Companion", "🐾"),
    HYDRATION("Hydration", "💧"),
    WELLNESS("Wellness", "⏰"),
    SETTINGS("Studio", "⚙️")
}

@Composable
fun MainScreen(modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val prefs = remember { CompanionPreferences(context) }
    val scope = rememberCoroutineScope()
    val snackbarHostState = remember { SnackbarHostState() }

    // State bindings synced with CompanionPreferences
    var selectedTab by remember { mutableStateOf(CompanionTab.COMPANION) }
    var cupsCount by remember { mutableIntStateOf(prefs.cupsCount) }
    var dailyGoal by remember { mutableIntStateOf(prefs.dailyGoal) }
    var currentAvatar by remember { mutableStateOf(prefs.currentAvatar) }
    var autoCycleAvatars by remember { mutableStateOf(prefs.autoCycleAvatars) }
    var hydrationEnabled by remember { mutableStateOf(prefs.hydrationEnabled) }
    var eyeRestEnabled by remember { mutableStateOf(prefs.eyeRestEnabled) }
    var postureEnabled by remember { mutableStateOf(prefs.postureEnabled) }
    var quietHoursEnabled by remember { mutableStateOf(prefs.quietHoursEnabled) }
    var soundEnabled by remember { mutableStateOf(prefs.soundEnabled) }
    var vibrationEnabled by remember { mutableStateOf(prefs.vibrationEnabled) }
    var petCount by remember { mutableIntStateOf(prefs.petCount) }
    var scheduleStatus by remember { mutableStateOf(prefs.getScheduleStatus()) }

    // Permission launcher for Android 13+
    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { _ -> }

    LaunchedEffect(Unit) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED
            ) {
                permissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
            }
        }
    }

    // High precision system clock loop: Checks midnight cup reset and status every 10 seconds
    LaunchedEffect(Unit) {
        while (true) {
            delay(10000)
            if (prefs.checkMidnightReset()) {
                cupsCount = prefs.cupsCount
                scope.launch {
                    snackbarHostState.showSnackbar("🕛 Midnight reached: Daily cups reset for the new day!")
                }
            }
            scheduleStatus = prefs.getScheduleStatus()
        }
    }

    Scaffold(
        modifier = modifier.fillMaxSize(),
        containerColor = DeepNavy,
        snackbarHost = { SnackbarHost(snackbarHostState) },
        bottomBar = {
            // Modern Floating Bottom Navigation Bar
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .navigationBarsPadding()
                    .padding(horizontal = 16.dp, vertical = 10.dp)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .shadow(elevation = 20.dp, shape = RoundedCornerShape(24.dp), spotColor = Color(0xFF38BDF8))
                        .clip(RoundedCornerShape(24.dp))
                        .background(
                            Brush.horizontalGradient(
                                listOf(
                                    Color(0xFF131D31).copy(alpha = 0.95f),
                                    Color(0xFF0F172A).copy(alpha = 0.95f)
                                )
                            )
                        )
                        .border(
                            1.dp,
                            Brush.horizontalGradient(
                                listOf(
                                    Color(0xFF38BDF8).copy(alpha = 0.4f),
                                    Color(0xFF818CF8).copy(alpha = 0.2f)
                                )
                            ),
                            RoundedCornerShape(24.dp)
                        )
                        .padding(horizontal = 8.dp, vertical = 8.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceAround,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        CompanionTab.values().forEach { tab ->
                            val isSelected = tab == selectedTab
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(16.dp))
                                    .background(
                                        if (isSelected) Color(0xFF0284C7).copy(alpha = 0.35f) else Color.Transparent
                                    )
                                    .clickable {
                                        selectedTab = tab
                                        SoundAndHaptics.vibrateTick(context, vibrationEnabled)
                                    }
                                    .padding(horizontal = 14.dp, vertical = 8.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Text(
                                        text = tab.icon,
                                        fontSize = 18.sp,
                                        modifier = Modifier.padding(end = if (isSelected) 6.dp else 0.dp)
                                    )
                                    if (isSelected) {
                                        Text(
                                            text = tab.title,
                                            color = Color.White,
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .statusBarsPadding()
                .padding(horizontal = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Sleek Top App Bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 10.dp, bottom = 12.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "Phone Companion",
                            color = Color.White,
                            fontSize = 22.sp,
                            fontWeight = FontWeight.ExtraBold
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(6.dp))
                                .background(Color(0xFF0284C7).copy(alpha = 0.3f))
                                .padding(horizontal = 6.dp, vertical = 2.dp)
                        ) {
                            Text(
                                text = "v2.0",
                                color = NeonCyan,
                                fontSize = 10.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                    Text(
                        text = "Your Interactive Desktop & Mobile Buddy",
                        color = Color(0xFF94A3B8),
                        fontSize = 12.sp
                    )
                }

                // Active Companion Avatar Tag
                Box(
                    modifier = Modifier
                        .shadow(elevation = 8.dp, shape = RoundedCornerShape(14.dp), spotColor = Color(0xFF38BDF8))
                        .clip(RoundedCornerShape(14.dp))
                        .background(
                            Brush.horizontalGradient(
                                listOf(
                                    Color(0xFF0284C7),
                                    WaterBlue
                                )
                            )
                        )
                        .clickable {
                            selectedTab = CompanionTab.SETTINGS
                        }
                        .padding(horizontal = 12.dp, vertical = 6.dp)
                ) {
                    Text(
                        text = currentAvatar,
                        color = Color(0xFF080C15),
                        fontSize = 12.5.sp,
                        fontWeight = FontWeight.ExtraBold
                    )
                }
            }

            // Tab Content with Animated Fade Transition
            AnimatedContent(
                targetState = selectedTab,
                transitionSpec = { fadeIn(tween(250)) togetherWith fadeOut(tween(200)) },
                label = "tab_content_anim"
            ) { targetTab ->
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .verticalScroll(rememberScrollState())
                        .padding(bottom = 20.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    when (targetTab) {
                        CompanionTab.COMPANION -> {
                            Spacer(modifier = Modifier.height(6.dp))

                            // Hero Luminous Companion Stage
                            PixelAvatarView(
                                avatarName = currentAvatar,
                                onPet = {
                                    prefs.petCount += 1
                                    petCount = prefs.petCount
                                    SoundAndHaptics.playDripSound(context, soundEnabled)
                                    SoundAndHaptics.vibrateTick(context, vibrationEnabled)
                                }
                            )

                            Spacer(modifier = Modifier.height(18.dp))

                            // Hydration Card (Compact view)
                            HydrationCard(
                                cupsCount = cupsCount,
                                dailyGoal = dailyGoal,
                                onAddCup = {
                                    prefs.cupsCount += 1
                                    cupsCount = prefs.cupsCount
                                    SoundAndHaptics.playDripSound(context, soundEnabled)
                                    SoundAndHaptics.vibrateTick(context, vibrationEnabled)

                                    if (cupsCount >= dailyGoal) {
                                        SoundAndHaptics.vibrateCelebration(context, vibrationEnabled)
                                        scope.launch {
                                            snackbarHostState.showSnackbar("🎉 Daily Goal Achieved! Keep staying hydrated!")
                                        }
                                    }

                                    if (autoCycleAvatars) {
                                        currentAvatar = prefs.cycleNextAvatar()
                                    }
                                },
                                onRemoveCup = {
                                    if (cupsCount > 0) {
                                        prefs.cupsCount -= 1
                                        cupsCount = prefs.cupsCount
                                        SoundAndHaptics.vibrateTick(context, vibrationEnabled)
                                    }
                                },
                                onReset = {
                                    prefs.cupsCount = 0
                                    cupsCount = 0
                                    SoundAndHaptics.vibrateTick(context, vibrationEnabled)
                                    scope.launch {
                                        snackbarHostState.showSnackbar("Cups counter reset to 0.")
                                    }
                                }
                            )
                        }

                        CompanionTab.HYDRATION -> {
                            Spacer(modifier = Modifier.height(8.dp))

                            HydrationCard(
                                cupsCount = cupsCount,
                                dailyGoal = dailyGoal,
                                onAddCup = {
                                    prefs.cupsCount += 1
                                    cupsCount = prefs.cupsCount
                                    SoundAndHaptics.playDripSound(context, soundEnabled)
                                    SoundAndHaptics.vibrateTick(context, vibrationEnabled)

                                    if (cupsCount >= dailyGoal) {
                                        SoundAndHaptics.vibrateCelebration(context, vibrationEnabled)
                                        scope.launch {
                                            snackbarHostState.showSnackbar("🎉 Daily Goal Achieved! Great hydration!")
                                        }
                                    }

                                    if (autoCycleAvatars) {
                                        currentAvatar = prefs.cycleNextAvatar()
                                    }
                                },
                                onRemoveCup = {
                                    if (cupsCount > 0) {
                                        prefs.cupsCount -= 1
                                        cupsCount = prefs.cupsCount
                                        SoundAndHaptics.vibrateTick(context, vibrationEnabled)
                                    }
                                },
                                onReset = {
                                    prefs.cupsCount = 0
                                    cupsCount = 0
                                    SoundAndHaptics.vibrateTick(context, vibrationEnabled)
                                    scope.launch {
                                        snackbarHostState.showSnackbar("Cups counter reset to 0.")
                                    }
                                }
                            )

                            Spacer(modifier = Modifier.height(18.dp))

                            // Settings for Target Cups
                            SettingsCard(
                                dailyGoal = dailyGoal,
                                onChangeDailyGoal = { newGoal ->
                                    prefs.dailyGoal = newGoal
                                    dailyGoal = newGoal
                                    SoundAndHaptics.vibrateTick(context, vibrationEnabled)
                                },
                                soundEnabled = soundEnabled,
                                onToggleSound = {
                                    prefs.soundEnabled = it
                                    soundEnabled = it
                                },
                                vibrationEnabled = vibrationEnabled,
                                onToggleVibration = {
                                    prefs.vibrationEnabled = it
                                    vibrationEnabled = it
                                },
                                petCount = petCount
                            )
                        }

                        CompanionTab.WELLNESS -> {
                            Spacer(modifier = Modifier.height(8.dp))

                            RemindersCard(
                                hydrationEnabled = hydrationEnabled,
                                onToggleHydration = {
                                    prefs.hydrationEnabled = it
                                    hydrationEnabled = it
                                },
                                hydrationInterval = prefs.hydrationInterval,
                                eyeRestEnabled = eyeRestEnabled,
                                onToggleEyeRest = {
                                    prefs.eyeRestEnabled = it
                                    eyeRestEnabled = it
                                },
                                eyeRestInterval = prefs.eyeRestInterval,
                                postureEnabled = postureEnabled,
                                onTogglePosture = {
                                    prefs.postureEnabled = it
                                    postureEnabled = it
                                },
                                postureInterval = prefs.postureInterval,
                                onTestNotification = {
                                    CompanionNotificationManager.showReminderNotification(
                                        context = context,
                                        title = "$currentAvatar says: Time to Hydrate! 💧",
                                        message = "Take a moment to drink a cup of fresh water (250 ml)!"
                                    )
                                    SoundAndHaptics.playDripSound(context, soundEnabled)
                                    SoundAndHaptics.vibrateTick(context, vibrationEnabled)
                                    scope.launch {
                                        snackbarHostState.showSnackbar("Reminder notification sent!")
                                    }
                                }
                            )

                            Spacer(modifier = Modifier.height(18.dp))

                            ScheduleCard(
                                statusText = scheduleStatus,
                                quietHoursEnabled = quietHoursEnabled,
                                onToggleQuietHours = {
                                    prefs.quietHoursEnabled = it
                                    quietHoursEnabled = it
                                    scheduleStatus = prefs.getScheduleStatus()
                                }
                            )
                        }

                        CompanionTab.SETTINGS -> {
                            Spacer(modifier = Modifier.height(8.dp))

                            AvatarSelectorCard(
                                currentAvatar = currentAvatar,
                                onSelectAvatar = { selected ->
                                    prefs.currentAvatar = selected
                                    currentAvatar = selected
                                    SoundAndHaptics.vibrateTick(context, vibrationEnabled)
                                },
                                autoCycleEnabled = autoCycleAvatars,
                                onToggleAutoCycle = {
                                    prefs.autoCycleAvatars = it
                                    autoCycleAvatars = it
                                }
                            )

                            Spacer(modifier = Modifier.height(18.dp))

                            SettingsCard(
                                dailyGoal = dailyGoal,
                                onChangeDailyGoal = { newGoal ->
                                    prefs.dailyGoal = newGoal
                                    dailyGoal = newGoal
                                    SoundAndHaptics.vibrateTick(context, vibrationEnabled)
                                },
                                soundEnabled = soundEnabled,
                                onToggleSound = {
                                    prefs.soundEnabled = it
                                    soundEnabled = it
                                },
                                vibrationEnabled = vibrationEnabled,
                                onToggleVibration = {
                                    prefs.vibrationEnabled = it
                                    vibrationEnabled = it
                                },
                                petCount = petCount
                            )
                        }
                    }
                }
            }
        }
    }
}
