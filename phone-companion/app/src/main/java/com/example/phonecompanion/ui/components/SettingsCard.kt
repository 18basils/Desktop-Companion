package com.example.phonecompanion.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
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
fun SettingsCard(
    dailyGoal: Int,
    onChangeDailyGoal: (Int) -> Unit,
    soundEnabled: Boolean,
    onToggleSound: (Boolean) -> Unit,
    vibrationEnabled: Boolean,
    onToggleVibration: (Boolean) -> Unit,
    petCount: Int,
    modifier: Modifier = Modifier
) {
    val goalOptions = listOf(6, 8, 10, 12)

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
                        .background(Color(0xFF14B8A6).copy(alpha = 0.25f)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(text = "⚙️", fontSize = 18.sp)
                }
                Spacer(modifier = Modifier.width(10.dp))
                Column {
                    Text(
                        text = "Preferences & Goal",
                        color = Color.White,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "Customize feedback and target",
                        color = Color(0xFF94A3B8),
                        fontSize = 11.sp
                    )
                }
            }

            // Daily Target Selector
            Text(
                text = "Daily Target: $dailyGoal Cups (${dailyGoal * 250} ml)",
                color = Color.White,
                fontSize = 14.sp,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier.padding(bottom = 10.dp)
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                goalOptions.forEach { cups ->
                    val isSelected = cups == dailyGoal
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .height(42.dp)
                            .clip(RoundedCornerShape(12.dp))
                            .background(
                                if (isSelected) Color(0xFF0284C7).copy(alpha = 0.4f)
                                else Color(0xFF0F172A)
                            )
                            .border(
                                1.5.dp,
                                if (isSelected) NeonCyan else Color(0xFF1E293B),
                                RoundedCornerShape(12.dp)
                            )
                            .clickable { onChangeDailyGoal(cups) },
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "$cups 🥛",
                            color = if (isSelected) Color.White else Color(0xFF94A3B8),
                            fontSize = 13.sp,
                            fontWeight = if (isSelected) FontWeight.ExtraBold else FontWeight.Medium
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Sound Effects Switch
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
                            .background(Color(0xFF06B6D4).copy(alpha = 0.25f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(text = "🔊", fontSize = 20.sp)
                    }
                    Spacer(modifier = Modifier.width(12.dp))
                    Column {
                        Text(
                            text = "Droplet Sound Effects",
                            color = Color.White,
                            fontSize = 14.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "Plays authentic water chime",
                            color = Color(0xFF94A3B8),
                            fontSize = 11.5.sp
                        )
                    }
                }

                Switch(
                    checked = soundEnabled,
                    onCheckedChange = onToggleSound,
                    colors = SwitchDefaults.colors(
                        checkedThumbColor = NeonCyan,
                        checkedTrackColor = Color(0xFF0369A1),
                        uncheckedThumbColor = Color(0xFF94A3B8),
                        uncheckedTrackColor = Color(0xFF1E293B)
                    )
                )
            }

            Spacer(modifier = Modifier.height(10.dp))

            // Vibration Feedback Switch
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
                            .background(Color(0xFFF43F5E).copy(alpha = 0.25f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(text = "📳", fontSize = 20.sp)
                    }
                    Spacer(modifier = Modifier.width(12.dp))
                    Column {
                        Text(
                            text = "Haptic Vibration",
                            color = Color.White,
                            fontSize = 14.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "Tactile response on petting & drinking",
                            color = Color(0xFF94A3B8),
                            fontSize = 11.5.sp
                        )
                    }
                }

                Switch(
                    checked = vibrationEnabled,
                    onCheckedChange = onToggleVibration,
                    colors = SwitchDefaults.colors(
                        checkedThumbColor = NeonCyan,
                        checkedTrackColor = Color(0xFF0369A1),
                        uncheckedThumbColor = Color(0xFF94A3B8),
                        uncheckedTrackColor = Color(0xFF1E293B)
                    )
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Pet Stats & App Version Info
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(14.dp))
                    .background(Color(0xFF0F172A))
                    .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(14.dp))
                    .padding(horizontal = 14.dp, vertical = 12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(text = "❤️", fontSize = 16.sp, modifier = Modifier.padding(end = 6.dp))
                        Text(
                            text = "Headpats Given: $petCount",
                            color = Color(0xFFF43F5E),
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                    Text(
                        text = "Phone Companion v2.0",
                        color = Color(0xFF64748B),
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
            }
        }
    }
}
