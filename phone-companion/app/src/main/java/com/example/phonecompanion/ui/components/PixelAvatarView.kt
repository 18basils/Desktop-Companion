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
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.detectTapGestures
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
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Fill
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlin.math.PI
import kotlin.math.sin
import kotlin.random.Random

data class HeartParticle(
    val id: Long,
    val initialX: Float,
    val initialY: Float,
    val driftX: Float,
    var progress: Float = 0f,
    val scale: Float = 1f,
    val color: Color = Color(0xFFF43F5E)
)

data class SparkleParticle(
    val xRatio: Float,
    val yRatio: Float,
    val size: Float,
    val phaseOffset: Float
)

@Composable
fun PixelAvatarView(
    avatarName: String,
    onPet: () -> Unit,
    modifier: Modifier = Modifier
) {
    var isHappy by remember { mutableStateOf(false) }
    var petCombo by remember { mutableIntStateOf(0) }
    var lastPetTime by remember { mutableLongStateOf(0L) }
    val hearts = remember { mutableStateListOf<HeartParticle>() }

    // Ambient floating sparkles around pedestal
    val sparkles = remember {
        List(8) {
            SparkleParticle(
                xRatio = Random.nextFloat() * 0.8f + 0.1f,
                yRatio = Random.nextFloat() * 0.7f + 0.15f,
                size = Random.nextFloat() * 3.5f + 2f,
                phaseOffset = Random.nextFloat() * 2f * PI.toFloat()
            )
        }
    }

    // Rotating companion dialogues
    val quotes = remember {
        listOf(
            "Stay hydrated & refreshed! 💧",
            "A sip of water = +10 Energy! ⚡",
            "Remember the 20-20-20 eye break! 👁️",
            "Roll your shoulders & stretch! 🧘",
            "I love warm headpats! ❤️",
            "You are doing awesome today! 🌟",
            "Keep glowing and staying hydrated! 🥤"
        )
    }
    var currentQuoteIndex by remember { mutableIntStateOf(0) }

    LaunchedEffect(Unit) {
        while (true) {
            delay(10000)
            currentQuoteIndex = (currentQuoteIndex + 1) % quotes.size
        }
    }

    // Breathing / bobbing floating animation
    val infiniteTransition = rememberInfiniteTransition(label = "pet_bob")
    val bobOffset by infiniteTransition.animateFloat(
        initialValue = -8f,
        targetValue = 8f,
        animationSpec = infiniteRepeatable(
            animation = tween(1600, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "bob_offset"
    )

    // Pedestal ambient glow pulsation
    val auraGlow by infiniteTransition.animateFloat(
        initialValue = 0.65f,
        targetValue = 1.0f,
        animationSpec = infiniteRepeatable(
            animation = tween(2200, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "aura_glow"
    )

    // Eye blinking cycle
    val blinkProgress by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(3400, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "blink_cycle"
    )
    val isBlinking = blinkProgress > 0.94f

    // Springy happy jump
    val jumpAnim by animateFloatAsState(
        targetValue = if (isHappy) -28f else 0f,
        animationSpec = tween(200, easing = FastOutSlowInEasing),
        label = "jump_anim"
    )

    // Reset happy mood & combo reset after idle
    LaunchedEffect(isHappy, lastPetTime) {
        if (isHappy) {
            delay(1800)
            isHappy = false
            delay(1200)
            petCombo = 0
        }
    }

    // Heart particle physics loop
    LaunchedEffect(hearts.size) {
        while (hearts.isNotEmpty()) {
            delay(16)
            val iterator = hearts.listIterator()
            while (iterator.hasNext()) {
                val h = iterator.next()
                h.progress += 0.025f
                if (h.progress >= 1f) {
                    iterator.remove()
                }
            }
        }
    }

    Column(
        modifier = modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Floating Frosted Speech Bubble
        Box(
            modifier = Modifier
                .padding(bottom = 12.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(
                    Brush.horizontalGradient(
                        listOf(
                            Color(0xEE1E293B),
                            Color(0xEE0F172A)
                        )
                    )
                )
                .border(
                    width = 1.dp,
                    brush = Brush.horizontalGradient(
                        listOf(
                            Color(0xFF38BDF8).copy(alpha = 0.5f),
                            Color(0xFF818CF8).copy(alpha = 0.2f)
                        )
                    ),
                    shape = RoundedCornerShape(16.dp)
                )
                .padding(horizontal = 16.dp, vertical = 8.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = if (isHappy) "✨ " else "💭 ",
                    fontSize = 14.sp
                )
                Text(
                    text = if (isHappy) "Yay! Thank you for the love! ❤️" else quotes[currentQuoteIndex],
                    color = if (isHappy) Color(0xFFF43F5E) else Color(0xFF38BDF8),
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold
                )
            }
        }

        // Luminous Sanctuary Stage (Pedestal & Avatar)
        Box(
            modifier = Modifier
                .size(220.dp)
                .shadow(elevation = 20.dp, shape = RoundedCornerShape(32.dp), spotColor = Color(0xFF38BDF8))
                .clip(RoundedCornerShape(32.dp))
                .background(
                    Brush.verticalGradient(
                        colors = listOf(
                            Color(0xFF131D31),
                            Color(0xFF090D16)
                        )
                    )
                )
                .border(
                    width = 1.5.dp,
                    brush = Brush.verticalGradient(
                        colors = listOf(
                            Color(0xFF38BDF8).copy(alpha = 0.45f),
                            Color(0xFF1E293B).copy(alpha = 0.3f),
                            Color(0xFF818CF8).copy(alpha = 0.2f)
                        )
                    ),
                    shape = RoundedCornerShape(32.dp)
                )
                .pointerInput(avatarName) {
                    detectTapGestures(
                        onTap = { offset ->
                            val now = System.currentTimeMillis()
                            petCombo = if (now - lastPetTime < 2500) petCombo + 1 else 1
                            lastPetTime = now
                            isHappy = true
                            onPet()

                            // Spawn floating hearts
                            val heartColors = listOf(
                                Color(0xFFF43F5E),
                                Color(0xFFFB7185),
                                Color(0xFFEC4899),
                                Color(0xFF38BDF8)
                            )
                            val count = Random.nextInt(3, 5)
                            for (i in 0 until count) {
                                hearts.add(
                                    HeartParticle(
                                        id = System.nanoTime() + i,
                                        initialX = offset.x + Random.nextFloat() * 40f - 20f,
                                        initialY = offset.y + Random.nextFloat() * 20f - 10f,
                                        driftX = (Random.nextFloat() - 0.5f) * 70f,
                                        scale = Random.nextFloat() * 0.4f + 0.8f,
                                        color = heartColors.random()
                                    )
                                )
                            }
                        }
                    )
                },
            contentAlignment = Alignment.Center
        ) {
            // Interactive Canvas
            Canvas(modifier = Modifier.fillMaxSize()) {
                val canvasWidth = size.width
                val canvasHeight = size.height
                val centerX = canvasWidth / 2f
                val centerY = canvasHeight / 2f + bobOffset + jumpAnim

                // 1. Glowing Sanctuary Stage Pedestal (Floor aura)
                drawOval(
                    brush = Brush.radialGradient(
                        colors = listOf(
                            Color(0xFF38BDF8).copy(alpha = 0.35f * auraGlow),
                            Color(0xFF0284C7).copy(alpha = 0.15f * auraGlow),
                            Color.Transparent
                        ),
                        center = Offset(centerX, canvasHeight - 34f),
                        radius = 85f
                    ),
                    topLeft = Offset(centerX - 85f, canvasHeight - 52f),
                    size = Size(170f, 36f)
                )

                // 2. Platform Inner Ring
                drawOval(
                    color = Color(0xFF0F172A),
                    topLeft = Offset(centerX - 56f, canvasHeight - 40f),
                    size = Size(112f, 22f)
                )
                drawOval(
                    color = Color(0xFF38BDF8).copy(alpha = 0.6f * auraGlow),
                    topLeft = Offset(centerX - 56f, canvasHeight - 40f),
                    size = Size(112f, 22f),
                    style = Stroke(width = 2f)
                )

                // 3. Ambient Sparkle Dust Particles
                sparkles.forEach { sp ->
                    val sparkleX = canvasWidth * sp.xRatio
                    val sparkleY = canvasHeight * sp.yRatio + (bobOffset * 0.4f)
                    val sparkleAlpha = (sin(blinkProgress * 2f * PI.toFloat() + sp.phaseOffset) * 0.4f + 0.5f).coerceIn(0.1f, 0.9f)
                    drawCircle(
                        color = Color(0xFF67E8F9).copy(alpha = sparkleAlpha),
                        radius = sp.size,
                        center = Offset(sparkleX, sparkleY)
                    )
                }

                // 4. Companion Shadow
                drawOval(
                    color = Color.Black.copy(alpha = 0.38f),
                    topLeft = Offset(centerX - 42f, canvasHeight - 36f),
                    size = Size(84f, 15f)
                )

                // 5. Draw selected companion
                when (avatarName) {
                    "Cute Kitty" -> drawKitty(centerX, centerY, isHappy, isBlinking)
                    "Robo Buddy" -> drawRobot(centerX, centerY, isHappy, isBlinking)
                    "Slime" -> drawSlime(centerX, centerY, isHappy, isBlinking, bobOffset)
                    "Frog" -> drawFrog(centerX, centerY, isHappy, isBlinking)
                    "Ghost" -> drawGhost(centerX, centerY, isHappy, isBlinking, bobOffset)
                    else -> drawPixelGuy(centerX, centerY, isHappy, isBlinking)
                }

                // 6. Draw Floating Hearts with Scale & Fade
                hearts.forEach { heart ->
                    val curX = heart.initialX + heart.driftX * heart.progress
                    val curY = heart.initialY - (120f * heart.progress)
                    val alpha = (1f - heart.progress).coerceIn(0f, 1f)
                    drawHeart(curX, curY, heart.scale, alpha, heart.color)
                }
            }

            // Combo Pill Overlay (Top Right of Stage)
            if (petCombo > 1) {
                Box(
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(14.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Color(0xFFE11D48).copy(alpha = 0.9f))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(
                        text = "❤️ x$petCombo Combo!",
                        color = Color.White,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(10.dp))

        // Tap to Pet Hint Pill
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(10.dp))
                .background(Color(0xFF1E293B).copy(alpha = 0.6f))
                .padding(horizontal = 12.dp, vertical = 4.dp)
        ) {
            Text(
                text = "✨ Tap to pet your companion",
                color = Color(0xFF94A3B8),
                fontSize = 11.sp,
                fontWeight = FontWeight.Medium
            )
        }
    }
}

// -------------------------------------------------------------
// COMPANION DRAWING IMPLEMENTATIONS
// -------------------------------------------------------------

private fun DrawScope.drawPixelGuy(cx: Float, cy: Float, happy: Boolean, blinking: Boolean) {
    // Cap / Hair (Blue Cap with Highlight)
    drawRoundRect(
        color = Color(0xFF0284C7),
        topLeft = Offset(cx - 38f, cy - 44f),
        size = Size(76f, 26f),
        cornerRadius = CornerRadius(9f, 9f)
    )
    // Visor Brim
    drawRoundRect(
        color = Color(0xFF0369A1),
        topLeft = Offset(cx - 10f, cy - 25f),
        size = Size(54f, 10f),
        cornerRadius = CornerRadius(5f, 5f)
    )

    // Face / Skin
    drawRoundRect(
        color = Color(0xFFFFD1A4),
        topLeft = Offset(cx - 34f, cy - 22f),
        size = Size(68f, 42f),
        cornerRadius = CornerRadius(12f, 12f)
    )

    // Cheeks
    drawCircle(Color(0xFFFF8B8B).copy(alpha = 0.7f), radius = 6.5f, center = Offset(cx - 22f, cy + 4f))
    drawCircle(Color(0xFFFF8B8B).copy(alpha = 0.7f), radius = 6.5f, center = Offset(cx + 22f, cy + 4f))

    // Eyes
    if (blinking) {
        drawLine(Color(0xFF0F172A), Offset(cx - 22f, cy - 6f), Offset(cx - 10f, cy - 6f), strokeWidth = 3.5f)
        drawLine(Color(0xFF0F172A), Offset(cx + 10f, cy - 6f), Offset(cx + 22f, cy - 6f), strokeWidth = 3.5f)
    } else if (happy) {
        drawArc(
            color = Color(0xFFE11D48),
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(cx - 23f, cy - 13f),
            size = Size(15f, 13f),
            style = Stroke(width = 4f)
        )
        drawArc(
            color = Color(0xFFE11D48),
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(cx + 8f, cy - 13f),
            size = Size(15f, 13f),
            style = Stroke(width = 4f)
        )
    } else {
        // Sparkling round eyes
        drawRoundRect(Color(0xFF0F172A), Offset(cx - 20f, cy - 11f), Size(11f, 13f), CornerRadius(4f, 4f))
        drawCircle(Color.White, radius = 3f, center = Offset(cx - 17f, cy - 9f))

        drawRoundRect(Color(0xFF0F172A), Offset(cx + 9f, cy - 11f), Size(11f, 13f), CornerRadius(4f, 4f))
        drawCircle(Color.White, radius = 3f, center = Offset(cx + 12f, cy - 9f))
    }

    // Mouth
    if (happy) {
        drawArc(
            color = Color(0xFFE11D48),
            startAngle = 0f,
            sweepAngle = 180f,
            useCenter = true,
            topLeft = Offset(cx - 9f, cy + 1f),
            size = Size(18f, 14f)
        )
    } else {
        drawArc(
            color = Color(0xFF991B1B),
            startAngle = 0f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(cx - 7f, cy + 4f),
            size = Size(14f, 8f),
            style = Stroke(width = 2.8f)
        )
    }

    // Body (Blue Overalls)
    drawRoundRect(
        color = Color(0xFF2563EB),
        topLeft = Offset(cx - 25f, cy + 20f),
        size = Size(50f, 34f),
        cornerRadius = CornerRadius(9f, 9f)
    )
    // Shirt White Collar
    drawRoundRect(
        color = Color.White,
        topLeft = Offset(cx - 9f, cy + 20f),
        size = Size(18f, 11f),
        cornerRadius = CornerRadius(3f, 3f)
    )
}

private fun DrawScope.drawKitty(cx: Float, cy: Float, happy: Boolean, blinking: Boolean) {
    val earColor = Color(0xFFF97316)
    val earInner = Color(0xFFFCA5A5)

    // Left Ear
    val leftEar = Path().apply {
        moveTo(cx - 32f, cy - 14f)
        lineTo(cx - 44f, cy - 46f)
        lineTo(cx - 14f, cy - 30f)
        close()
    }
    drawPath(leftEar, color = earColor)
    val leftInner = Path().apply {
        moveTo(cx - 30f, cy - 18f)
        lineTo(cx - 40f, cy - 40f)
        lineTo(cx - 18f, cy - 30f)
        close()
    }
    drawPath(leftInner, color = earInner)

    // Right Ear
    val rightEar = Path().apply {
        moveTo(cx + 32f, cy - 14f)
        lineTo(cx + 44f, cy - 46f)
        lineTo(cx + 14f, cy - 30f)
        close()
    }
    drawPath(rightEar, color = earColor)
    val rightInner = Path().apply {
        moveTo(cx + 30f, cy - 18f)
        lineTo(cx + 40f, cy - 40f)
        lineTo(cx + 18f, cy - 30f)
        close()
    }
    drawPath(rightInner, color = earInner)

    // Head
    drawRoundRect(
        color = Color(0xFFFB923C),
        topLeft = Offset(cx - 36f, cy - 28f),
        size = Size(72f, 54f),
        cornerRadius = CornerRadius(24f, 24f)
    )

    // Cheeks
    drawCircle(Color(0xFFFDA4AF), radius = 6.5f, center = Offset(cx - 23f, cy + 4f))
    drawCircle(Color(0xFFFDA4AF), radius = 6.5f, center = Offset(cx + 23f, cy + 4f))

    // Eyes
    if (blinking || happy) {
        drawArc(
            color = Color(0xFF1E293B),
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(cx - 23f, cy - 11f),
            size = Size(15f, 11f),
            style = Stroke(width = 3.8f)
        )
        drawArc(
            color = Color(0xFF1E293B),
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(cx + 8f, cy - 11f),
            size = Size(15f, 11f),
            style = Stroke(width = 3.8f)
        )
    } else {
        drawCircle(Color(0xFF0F172A), radius = 7f, center = Offset(cx - 16f, cy - 4f))
        drawCircle(Color.White, radius = 2.8f, center = Offset(cx - 18f, cy - 6f))

        drawCircle(Color(0xFF0F172A), radius = 7f, center = Offset(cx + 16f, cy - 4f))
        drawCircle(Color.White, radius = 2.8f, center = Offset(cx + 14f, cy - 6f))
    }

    // Nose
    drawCircle(Color(0xFFF43F5E), radius = 3.8f, center = Offset(cx, cy + 2f))

    // Whiskers
    drawLine(Color(0xFF334155), Offset(cx - 26f, cy + 2f), Offset(cx - 44f, cy - 1f), strokeWidth = 2.2f)
    drawLine(Color(0xFF334155), Offset(cx - 26f, cy + 7f), Offset(cx - 44f, cy + 10f), strokeWidth = 2.2f)
    drawLine(Color(0xFF334155), Offset(cx + 26f, cy + 2f), Offset(cx + 44f, cy - 1f), strokeWidth = 2.2f)
    drawLine(Color(0xFF334155), Offset(cx + 26f, cy + 7f), Offset(cx + 44f, cy + 10f), strokeWidth = 2.2f)

    // Body
    drawRoundRect(
        color = Color(0xFFF97316),
        topLeft = Offset(cx - 23f, cy + 24f),
        size = Size(46f, 28f),
        cornerRadius = CornerRadius(15f, 15f)
    )
    // White chest
    drawRoundRect(
        color = Color(0xFFFFFBEB),
        topLeft = Offset(cx - 13f, cy + 25f),
        size = Size(26f, 20f),
        cornerRadius = CornerRadius(9f, 9f)
    )
}

private fun DrawScope.drawRobot(cx: Float, cy: Float, happy: Boolean, blinking: Boolean) {
    // Antenna
    drawLine(Color(0xFF94A3B8), Offset(cx, cy - 38f), Offset(cx, cy - 54f), strokeWidth = 4.5f)
    drawCircle(if (happy) Color(0xFF22C55E) else Color(0xFF38BDF8), radius = 6.5f, center = Offset(cx, cy - 56f))

    // Head Frame
    drawRoundRect(
        color = Color(0xFF64748B),
        topLeft = Offset(cx - 38f, cy - 38f),
        size = Size(76f, 52f),
        cornerRadius = CornerRadius(14f, 14f)
    )

    // Visor Screen
    drawRoundRect(
        color = Color(0xFF0F172A),
        topLeft = Offset(cx - 30f, cy - 30f),
        size = Size(60f, 36f),
        cornerRadius = CornerRadius(9f, 9f)
    )

    // LED Eyes
    val ledColor = if (happy) Color(0xFFF43F5E) else Color(0xFF38BDF8)
    if (happy) {
        drawCircle(ledColor, radius = 5.5f, center = Offset(cx - 15f, cy - 12f))
        drawCircle(ledColor, radius = 5.5f, center = Offset(cx + 15f, cy - 12f))
    } else if (blinking) {
        drawLine(ledColor, Offset(cx - 22f, cy - 11f), Offset(cx - 8f, cy - 11f), strokeWidth = 3.5f)
        drawLine(ledColor, Offset(cx + 8f, cy - 11f), Offset(cx + 22f, cy - 11f), strokeWidth = 3.5f)
    } else {
        drawRoundRect(ledColor, Offset(cx - 19f, cy - 17f), Size(11f, 11f), CornerRadius(3f, 3f))
        drawRoundRect(ledColor, Offset(cx + 8f, cy - 17f), Size(11f, 11f), CornerRadius(3f, 3f))
    }

    // Body
    drawRoundRect(
        color = Color(0xFF475569),
        topLeft = Offset(cx - 28f, cy + 18f),
        size = Size(56f, 34f),
        cornerRadius = CornerRadius(9f, 9f)
    )
    // Chest lights
    drawCircle(Color(0xFF22C55E), radius = 3.5f, center = Offset(cx - 11f, cy + 30f))
    drawCircle(Color(0xFFEAB308), radius = 3.5f, center = Offset(cx, cy + 30f))
    drawCircle(Color(0xFFEF4444), radius = 3.5f, center = Offset(cx + 11f, cy + 30f))
}

private fun DrawScope.drawSlime(cx: Float, cy: Float, happy: Boolean, blinking: Boolean, bob: Float) {
    val squishW = 72f + (bob * 2.2f)
    val squishH = 56f - (bob * 2.2f)

    // Slime Body
    drawRoundRect(
        color = Color(0xFF10B981),
        topLeft = Offset(cx - squishW / 2f, cy - squishH / 2f),
        size = Size(squishW, squishH),
        cornerRadius = CornerRadius(squishH / 2f, squishH / 2f)
    )
    // Specular Highlight
    drawOval(
        color = Color(0xFF6EE7B7).copy(alpha = 0.85f),
        topLeft = Offset(cx - squishW / 3f, cy - squishH / 2.6f),
        size = Size(20f, 11f)
    )

    // Cheeks
    drawCircle(Color(0xFF34D399), radius = 5.5f, center = Offset(cx - 22f, cy + 6f))
    drawCircle(Color(0xFF34D399), radius = 5.5f, center = Offset(cx + 22f, cy + 6f))

    // Eyes
    if (blinking || happy) {
        drawArc(
            color = Color(0xFF064E3B),
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(cx - 19f, cy - 6f),
            size = Size(13f, 9f),
            style = Stroke(width = 3.5f)
        )
        drawArc(
            color = Color(0xFF064E3B),
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(cx + 6f, cy - 6f),
            size = Size(13f, 9f),
            style = Stroke(width = 3.5f)
        )
    } else {
        drawCircle(Color(0xFF064E3B), radius = 6.5f, center = Offset(cx - 14f, cy - 2f))
        drawCircle(Color.White, radius = 2.4f, center = Offset(cx - 16f, cy - 4f))

        drawCircle(Color(0xFF064E3B), radius = 6.5f, center = Offset(cx + 14f, cy - 2f))
        drawCircle(Color.White, radius = 2.4f, center = Offset(cx + 12f, cy - 4f))
    }

    // Smile
    drawArc(
        color = Color(0xFF064E3B),
        startAngle = 0f,
        sweepAngle = 180f,
        useCenter = false,
        topLeft = Offset(cx - 6f, cy + 3f),
        size = Size(12f, 7f),
        style = Stroke(width = 2.8f)
    )
}

private fun DrawScope.drawFrog(cx: Float, cy: Float, happy: Boolean, blinking: Boolean) {
    // Big Frog Eye Bulges
    drawCircle(Color(0xFF22C55E), radius = 17f, center = Offset(cx - 23f, cy - 19f))
    drawCircle(Color(0xFF22C55E), radius = 17f, center = Offset(cx + 23f, cy - 19f))

    // Frog Head
    drawRoundRect(
        color = Color(0xFF16A34A),
        topLeft = Offset(cx - 40f, cy - 14f),
        size = Size(80f, 50f),
        cornerRadius = CornerRadius(25f, 25f)
    )

    // Eye Pupils
    if (blinking) {
        drawLine(Color(0xFF0F172A), Offset(cx - 30f, cy - 19f), Offset(cx - 16f, cy - 19f), strokeWidth = 3.5f)
        drawLine(Color(0xFF0F172A), Offset(cx + 16f, cy - 19f), Offset(cx + 30f, cy - 19f), strokeWidth = 3.5f)
    } else {
        drawCircle(Color(0xFF0F172A), radius = 7.5f, center = Offset(cx - 23f, cy - 19f))
        drawCircle(Color.White, radius = 3.2f, center = Offset(cx - 25f, cy - 21f))

        drawCircle(Color(0xFF0F172A), radius = 7.5f, center = Offset(cx + 23f, cy - 19f))
        drawCircle(Color.White, radius = 3.2f, center = Offset(cx + 21f, cy - 21f))
    }

    // Rosy Cheeks
    drawCircle(Color(0xFFF472B6).copy(alpha = 0.85f), radius = 6.5f, center = Offset(cx - 25f, cy + 9f))
    drawCircle(Color(0xFFF472B6).copy(alpha = 0.85f), radius = 6.5f, center = Offset(cx + 25f, cy + 9f))

    // Wide Smile
    drawArc(
        color = Color(0xFF052E16),
        startAngle = 0f,
        sweepAngle = 180f,
        useCenter = happy,
        topLeft = Offset(cx - 17f, cy + 4f),
        size = Size(34f, 20f),
        style = if (happy) Fill else Stroke(width = 3.2f)
    )
}

private fun DrawScope.drawGhost(cx: Float, cy: Float, happy: Boolean, blinking: Boolean, bob: Float) {
    val ghostColor = Color(0xFFF8FAFC)

    // Ghost Body Path with Wavy Bottom
    val ghostPath = Path().apply {
        moveTo(cx - 32f, cy + 26f)
        lineTo(cx - 32f, cy - 8f)
        cubicTo(cx - 32f, cy - 38f, cx + 32f, cy - 38f, cx + 32f, cy - 8f)
        lineTo(cx + 32f, cy + 26f)

        quadraticTo(cx + 22f, cy + 19f + bob, cx + 11f, cy + 28f)
        quadraticTo(cx, cy + 19f + bob, cx - 11f, cy + 28f)
        quadraticTo(cx - 22f, cy + 19f + bob, cx - 32f, cy + 26f)
        close()
    }
    drawPath(ghostPath, color = ghostColor)

    // Ghost Eyes
    if (blinking) {
        drawLine(Color(0xFF0F172A), Offset(cx - 19f, cy - 10f), Offset(cx - 8f, cy - 10f), strokeWidth = 3.5f)
        drawLine(Color(0xFF0F172A), Offset(cx + 8f, cy - 10f), Offset(cx + 19f, cy - 10f), strokeWidth = 3.5f)
    } else if (happy) {
        drawArc(
            color = Color(0xFFE11D48),
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(cx - 19f, cy - 15f),
            size = Size(13f, 11f),
            style = Stroke(width = 3.8f)
        )
        drawArc(
            color = Color(0xFFE11D48),
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(cx + 6f, cy - 15f),
            size = Size(13f, 11f),
            style = Stroke(width = 3.8f)
        )
    } else {
        drawOval(Color(0xFF0F172A), topLeft = Offset(cx - 17f, cy - 13f), size = Size(10f, 14f))
        drawCircle(Color.White, radius = 2.4f, center = Offset(cx - 15f, cy - 11f))

        drawOval(Color(0xFF0F172A), topLeft = Offset(cx + 7f, cy - 13f), size = Size(10f, 14f))
        drawCircle(Color.White, radius = 2.4f, center = Offset(cx + 9f, cy - 11f))
    }

    // Rosy Cheeks
    drawCircle(Color(0xFFFDA4AF).copy(alpha = 0.75f), radius = 5.5f, center = Offset(cx - 21f, cy - 1f))
    drawCircle(Color(0xFFFDA4AF).copy(alpha = 0.75f), radius = 5.5f, center = Offset(cx + 21f, cy - 1f))
}

private fun DrawScope.drawHeart(x: Float, y: Float, scale: Float, alpha: Float, color: Color) {
    val heartColor = color.copy(alpha = alpha)
    val s = 15f * scale

    val heartPath = Path().apply {
        moveTo(x, y + s / 4f)
        cubicTo(x - s, y - s / 2f, x - s, y - s, x, y - s / 2f)
        cubicTo(x + s, y - s, x + s, y - s / 2f, x, y + s / 4f)
        close()
    }
    drawPath(heartPath, color = heartColor)
}
