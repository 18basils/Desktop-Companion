package com.example.phonecompanion.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.phonecompanion.theme.NeonCyan
import com.example.phonecompanion.theme.WaterBlue
import com.example.phonecompanion.theme.WaterBlueDark

@Composable
fun HydrationCard(
    cupsCount: Int,
    dailyGoal: Int,
    onAddCup: () -> Unit,
    onAddBottle: () -> Unit = {},
    onRemoveCup: () -> Unit,
    onReset: () -> Unit,
    modifier: Modifier = Modifier
) {
    val progress = (cupsCount.toFloat() / dailyGoal.toFloat().coerceAtLeast(1f)).coerceIn(0f, 1f)
    val animatedProgress by animateFloatAsState(
        targetValue = progress,
        animationSpec = tween(700, easing = FastOutSlowInEasing),
        label = "circular_cup_progress"
    )

    val isGoalAchieved = cupsCount >= dailyGoal
    val percentInt = (progress * 100).toInt()

    // Pulse animation for liquid ring
    val infiniteTransition = rememberInfiniteTransition(label = "ring_glow")
    val ringGlow by infiniteTransition.animateFloat(
        initialValue = 0.7f,
        targetValue = 1.0f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "ring_glow_val"
    )

    Box(
        modifier = modifier
            .fillMaxWidth()
            .shadow(elevation = 16.dp, shape = RoundedCornerShape(28.dp), spotColor = Color(0xFF38BDF8))
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
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.fillMaxWidth()
        ) {
            // Header Row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(CircleShape)
                            .background(Color(0xFF0369A1).copy(alpha = 0.35f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(text = "💧", fontSize = 18.sp)
                    }
                    Spacer(modifier = Modifier.width(10.dp))
                    Column {
                        Text(
                            text = "Daily Hydration",
                            color = Color.White,
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "Synced with system midnight",
                            color = Color(0xFF94A3B8),
                            fontSize = 11.sp
                        )
                    }
                }

                // Midnight Reset Tag
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(10.dp))
                        .background(Color(0xFF0F172A))
                        .border(1.dp, Color(0xFF334155), RoundedCornerShape(10.dp))
                        .padding(horizontal = 10.dp, vertical = 5.dp)
                ) {
                    Text(
                        text = "🕛 12AM Reset",
                        color = Color(0xFF38BDF8),
                        fontSize = 11.sp,
                        fontWeight = FontWeight.SemiBold
                    )
                }
            }

            Spacer(modifier = Modifier.height(20.dp))

            // Circular Water Dial
            Box(
                modifier = Modifier.size(175.dp),
                contentAlignment = Alignment.Center
            ) {
                Canvas(modifier = Modifier.fillMaxSize()) {
                    val strokeW = 14.dp.toPx()
                    val radius = (size.minDimension - strokeW) / 2f
                    val arcTopLeft = Offset(strokeW / 2f, strokeW / 2f)
                    val arcSize = Size(radius * 2, radius * 2)

                    // Background Track
                    drawArc(
                        color = Color(0xFF0F172A),
                        startAngle = 140f,
                        sweepAngle = 260f,
                        useCenter = false,
                        topLeft = arcTopLeft,
                        size = arcSize,
                        style = Stroke(width = strokeW, cap = StrokeCap.Round)
                    )

                    // Active Glowing Progress Arc
                    if (animatedProgress > 0f) {
                        drawArc(
                            brush = Brush.sweepGradient(
                                colors = listOf(
                                    WaterBlueDark,
                                    WaterBlue,
                                    NeonCyan,
                                    Color(0xFF818CF8)
                                )
                            ),
                            startAngle = 140f,
                            sweepAngle = 260f * animatedProgress,
                            useCenter = false,
                            topLeft = arcTopLeft,
                            size = arcSize,
                            style = Stroke(width = strokeW, cap = StrokeCap.Round)
                        )
                    }
                }

                // Dial Center Metrics
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(
                        text = "$cupsCount",
                        color = if (isGoalAchieved) NeonCyan else Color.White,
                        fontSize = 38.sp,
                        fontWeight = FontWeight.ExtraBold
                    )
                    Text(
                        text = "of $dailyGoal Cups",
                        color = Color(0xFF94A3B8),
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Medium
                    )
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(
                        text = "$percentInt%",
                        color = Color(0xFF38BDF8),
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            Text(
                text = "${cupsCount * 250} ml / ${dailyGoal * 250} ml consumed today",
                color = Color(0xFF94A3B8),
                fontSize = 13.sp,
                textAlign = TextAlign.Center
            )

            // Goal Achieved Confetti Banner
            AnimatedVisibility(
                visible = isGoalAchieved,
                enter = fadeIn(),
                exit = fadeOut()
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 12.dp)
                        .clip(RoundedCornerShape(14.dp))
                        .background(
                            Brush.horizontalGradient(
                                listOf(
                                    Color(0xFF065F46).copy(alpha = 0.7f),
                                    Color(0xFF047857).copy(alpha = 0.5f)
                                )
                            )
                        )
                        .border(1.dp, Color(0xFF10B981), RoundedCornerShape(14.dp))
                        .padding(horizontal = 14.dp, vertical = 8.dp)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(text = "🏆", fontSize = 16.sp, modifier = Modifier.padding(end = 6.dp))
                        Text(
                            text = "Daily Hydration Goal Crushed! 🎉",
                            color = Color(0xFF6EE7B7),
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(18.dp))

            // Primary Glowing +1 Cup Button
            Button(
                onClick = onAddCup,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp)
                    .shadow(elevation = 10.dp, shape = RoundedCornerShape(16.dp), spotColor = Color(0xFF38BDF8)),
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = WaterBlue,
                    contentColor = Color(0xFF080C15)
                )
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(text = "💧", fontSize = 18.sp, modifier = Modifier.padding(end = 6.dp))
                    Text(
                        text = "Drink +1 Cup (250 ml)",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.ExtraBold
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            // Secondary Controls (-1 Cup, +500ml Bottle, Reset)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedButton(
                    onClick = onRemoveCup,
                    enabled = cupsCount > 0,
                    modifier = Modifier
                        .weight(1f)
                        .height(42.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.outlinedButtonColors(
                        contentColor = Color(0xFFE2E8F0)
                    ),
                    border = ButtonDefaults.outlinedButtonBorder.copy(
                        brush = Brush.horizontalGradient(listOf(Color(0xFF334155), Color(0xFF334155)))
                    )
                ) {
                    Text("-1 Cup", fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                }

                OutlinedButton(
                    onClick = onReset,
                    modifier = Modifier
                        .weight(1f)
                        .height(42.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.outlinedButtonColors(
                        contentColor = Color(0xFF94A3B8)
                    ),
                    border = ButtonDefaults.outlinedButtonBorder.copy(
                        brush = Brush.horizontalGradient(listOf(Color(0xFF334155), Color(0xFF334155)))
                    )
                ) {
                    Text("🔄 Reset", fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
    }
}
