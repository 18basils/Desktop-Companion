package com.example.phonecompanion.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.phonecompanion.theme.NeonCyan
import com.example.phonecompanion.theme.WaterBlue

@Composable
fun RemindersCard(
    hydrationEnabled: Boolean,
    onToggleHydration: (Boolean) -> Unit,
    hydrationInterval: Int,
    eyeRestEnabled: Boolean,
    onToggleEyeRest: (Boolean) -> Unit,
    eyeRestInterval: Int,
    postureEnabled: Boolean,
    onTogglePosture: (Boolean) -> Unit,
    postureInterval: Int,
    onTestNotification: () -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .shadow(elevation = 14.dp, shape = RoundedCornerShape(28.dp), spotColor = Color(0xFF38BDF8))
            .clip(RoundedCornerShape(28.dp))
            .background(
                Brush.verticalGradient(
                    listOf(
                        Color(0xFF131D31),
                        Color(0xFF0C1322)
                    )
                )
            )
            .border(
                width = 1.2.dp,
                brush = Brush.verticalGradient(
                    listOf(
                        Color(0xFF38BDF8).copy(alpha = 0.4f),
                        Color(0xFF1E293B).copy(alpha = 0.2f),
                        Color(0xFF818CF8).copy(alpha = 0.2f)
                    )
                ),
                shape = RoundedCornerShape(28.dp)
            )
            .padding(20.dp)
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.padding(bottom = 16.dp)
            ) {
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .clip(CircleShape)
                        .background(Color(0xFF818CF8).copy(alpha = 0.25f)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(text = "🔔", fontSize = 18.sp)
                }
                Spacer(modifier = Modifier.width(10.dp))
                Column {
                    Text(
                        text = "Wellness Reminders",
                        color = Color.White,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "Gentle audio & haptic break alerts",
                        color = Color(0xFF94A3B8),
                        fontSize = 11.sp
                    )
                }
            }

            // Hydration reminder item
            ReminderItem(
                icon = "💧",
                iconBg = Color(0xFF0284C7).copy(alpha = 0.35f),
                title = "Hydration Reminder",
                subtitle = "Prompts a fresh glass every $hydrationInterval minutes",
                checked = hydrationEnabled,
                onCheckedChange = onToggleHydration
            )

            Spacer(modifier = Modifier.height(10.dp))

            // 20-20-20 Eye break item
            ReminderItem(
                icon = "👁️",
                iconBg = Color(0xFF8B5CF6).copy(alpha = 0.3f),
                title = "20-20-20 Eye Rest",
                subtitle = "Look 20ft away for 20s every $eyeRestInterval minutes",
                checked = eyeRestEnabled,
                onCheckedChange = onToggleEyeRest
            )

            Spacer(modifier = Modifier.height(10.dp))

            // Posture stretch item
            ReminderItem(
                icon = "🧘",
                iconBg = Color(0xFF10B981).copy(alpha = 0.25f),
                title = "Posture & Stretch",
                subtitle = "Roll shoulders & stand up every $postureInterval minutes",
                checked = postureEnabled,
                onCheckedChange = onTogglePosture
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Send Test Reminder Button
            Button(
                onClick = onTestNotification,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp),
                shape = RoundedCornerShape(14.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color(0xFF1E293B),
                    contentColor = NeonCyan
                ),
                border = ButtonDefaults.outlinedButtonBorder.copy(
                    brush = Brush.horizontalGradient(
                        listOf(
                            Color(0xFF38BDF8).copy(alpha = 0.5f),
                            Color(0xFF818CF8).copy(alpha = 0.4f)
                        )
                    )
                )
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(text = "📢", fontSize = 16.sp, modifier = Modifier.padding(end = 6.dp))
                    Text(
                        text = "Send Test Reminder Notification",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }
    }
}

@Composable
private fun ReminderItem(
    icon: String,
    iconBg: Color,
    title: String,
    subtitle: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF0F172A))
            .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(16.dp))
            .padding(horizontal = 14.dp, vertical = 10.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.weight(1f)
        ) {
            Box(
                modifier = Modifier
                    .size(38.dp)
                    .clip(RoundedCornerShape(10.dp))
                    .background(iconBg),
                contentAlignment = Alignment.Center
            ) {
                Text(text = icon, fontSize = 20.sp)
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column {
                Text(
                    text = title,
                    color = Color.White,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = subtitle,
                    color = Color(0xFF94A3B8),
                    fontSize = 11.5.sp
                )
            }
        }

        Switch(
            checked = checked,
            onCheckedChange = onCheckedChange,
            colors = SwitchDefaults.colors(
                checkedThumbColor = NeonCyan,
                checkedTrackColor = Color(0xFF0369A1),
                uncheckedThumbColor = Color(0xFF94A3B8),
                uncheckedTrackColor = Color(0xFF1E293B)
            )
        )
    }
}
