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
import com.example.phonecompanion.theme.NeonAmber
import com.example.phonecompanion.theme.NeonCyan
import com.example.phonecompanion.theme.WaterBlue

@Composable
fun ScheduleCard(
    statusText: String,
    quietHoursEnabled: Boolean,
    onToggleQuietHours: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    val daysOfWeek = listOf("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
    val workDays = setOf("Mon", "Tue", "Wed", "Thu", "Fri")

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
                        .background(Color(0xFFF59E0B).copy(alpha = 0.25f)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(text = "⏰", fontSize = 18.sp)
                }
                Spacer(modifier = Modifier.width(10.dp))
                Column {
                    Text(
                        text = "Schedule & Quiet Hours",
                        color = Color.White,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "Working times & undisturbed rest",
                        color = Color(0xFF94A3B8),
                        fontSize = 11.sp
                    )
                }
            }

            // Real-time Status Card with Glow Dot
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(Color(0xFF0F172A))
                    .border(1.dp, Color(0xFF38BDF8).copy(alpha = 0.35f), RoundedCornerShape(16.dp))
                    .padding(horizontal = 16.dp, vertical = 12.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(10.dp)
                            .clip(CircleShape)
                            .background(if (statusText.contains("Quiet")) NeonAmber else NeonCyan)
                    )
                    Spacer(modifier = Modifier.width(10.dp))
                    Text(
                        text = statusText,
                        color = if (statusText.contains("Quiet")) NeonAmber else NeonCyan,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.SemiBold
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Working Schedule & Days Chips
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(Color(0xFF0F172A))
                    .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(16.dp))
                    .padding(14.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(
                            text = "Active Schedule",
                            color = Color.White,
                            fontSize = 14.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "9:00 AM – 6:30 PM",
                            color = Color(0xFF38BDF8),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                    }

                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(8.dp))
                            .background(Color(0xFF0284C7).copy(alpha = 0.3f))
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Text(
                            text = "Mon - Fri",
                            color = NeonCyan,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                // Day badges
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    daysOfWeek.forEach { day ->
                        val isWork = workDays.contains(day)
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .height(32.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(
                                    if (isWork) Color(0xFF0284C7).copy(alpha = 0.4f)
                                    else Color(0xFF1E293B)
                                )
                                .border(
                                    1.dp,
                                    if (isWork) NeonCyan.copy(alpha = 0.5f) else Color.Transparent,
                                    RoundedCornerShape(8.dp)
                                ),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = day.take(2),
                                color = if (isWork) Color.White else Color(0xFF64748B),
                                fontSize = 11.sp,
                                fontWeight = if (isWork) FontWeight.Bold else FontWeight.Normal
                            )
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            // Quiet Hours Switch Item
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
                            .background(Color(0xFF6366F1).copy(alpha = 0.25f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(text = "🌙", fontSize = 20.sp)
                    }
                    Spacer(modifier = Modifier.width(12.dp))
                    Column {
                        Text(
                            text = "Quiet Hours",
                            color = Color.White,
                            fontSize = 14.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "10:00 PM – 8:00 AM (Muted)",
                            color = Color(0xFF94A3B8),
                            fontSize = 11.5.sp
                        )
                    }
                }

                Switch(
                    checked = quietHoursEnabled,
                    onCheckedChange = onToggleQuietHours,
                    colors = SwitchDefaults.colors(
                        checkedThumbColor = NeonAmber,
                        checkedTrackColor = Color(0xFFB45309),
                        uncheckedThumbColor = Color(0xFF94A3B8),
                        uncheckedTrackColor = Color(0xFF1E293B)
                    )
                )
            }
        }
    }
}
