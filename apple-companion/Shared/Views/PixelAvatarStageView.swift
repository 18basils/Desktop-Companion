//
//  PixelAvatarStageView.swift
//  Apple Companion (iOS & macOS)
//

import SwiftUI

public struct PixelAvatarStageView: View {
    @ObservedObject var vm: CompanionViewModel
    @State private var breathingOffset: CGFloat = 0
    @State private var particlePhase: CGFloat = 0

    public var body: some View {
        let skin = vm.activeSkin()
        let hasSunglasses = vm.config.cupsToday >= 4
        let hasCrown = vm.config.cupsToday >= vm.config.dailyGoalCups

        VStack(spacing: 12) {
            // Live Emotion Pill
            HStack(spacing: 6) {
                Circle()
                    .fill(Color(red: 0.13, green: 0.83, blue: 0.94))
                    .frame(width: 8, height: 8)
                Text(vm.emotionText)
                    .font(.system(size: 13, weight: .semibold, design: .rounded))
                    .foregroundColor(.white)
            }
            .padding(.horizontal, 14)
            .padding(.vertical, 6)
            .background(
                Capsule()
                    .fill(Color(red: 0.06, green: 0.10, blue: 0.18).opacity(0.85))
                    .overlay(
                        Capsule()
                            .stroke(Color.white.opacity(0.12), lineWidth: 1)
                    )
            )

            // Sanctuary Cosmic Stage
            ZStack {
                // Radial Aura Glow
                RadialGradient(
                    colors: [
                        skin.primaryColor.opacity(0.35),
                        skin.primaryColor.opacity(0.08),
                        Color.clear
                    ],
                    center: .center,
                    startRadius: 20,
                    endRadius: 130
                )
                .frame(width: 280, height: 240)

                // Background Sanctuary Disk
                Circle()
                    .fill(
                        LinearGradient(
                            colors: [
                                Color(red: 0.08, green: 0.13, blue: 0.22).opacity(0.8),
                                Color(red: 0.04, green: 0.07, blue: 0.13).opacity(0.95)
                            ],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
                    .frame(width: 220, height: 220)
                    .overlay(
                        Circle()
                            .stroke(
                                LinearGradient(
                                    colors: [skin.primaryColor.opacity(0.5), Color.clear],
                                    startPoint: .top,
                                    endPoint: .bottom
                                ),
                                lineWidth: 2
                            )
                    )
                    .shadow(color: skin.primaryColor.opacity(0.25), radius: 24, x: 0, y: 8)

                // Floating Ambient Sparkles
                ForEach(0..<6) { i in
                    Circle()
                        .fill(skin.primaryColor.opacity(0.6))
                        .frame(width: CGFloat(3 + (i % 3)), height: CGFloat(3 + (i % 3)))
                        .offset(
                            x: CGFloat(cos(Double(i) * 1.05 + Double(particlePhase)) * 85),
                            y: CGFloat(sin(Double(i) * 1.05 + Double(particlePhase)) * 75)
                        )
                }

                // Companion Avatar Character
                VStack(spacing: 2) {
                    ZStack(alignment: .top) {
                        // Avatar Face / Icon
                        Image(systemName: skin.iconName)
                            .resizable()
                            .scaledToFit()
                            .frame(width: 76, height: 76)
                            .foregroundColor(skin.primaryColor)
                            .shadow(color: skin.primaryColor.opacity(0.6), radius: 12)

                        // Crown Accessory (Unlocked at Daily Goal)
                        if hasCrown {
                            Text("👑")
                                .font(.system(size: 26))
                                .offset(y: -22)
                                .transition(.scale.combined(with: .opacity))
                        }

                        // Sunglasses Accessory (Unlocked at 4 Cups)
                        if hasSunglasses {
                            Text("🕶️")
                                .font(.system(size: 22))
                                .offset(y: 14)
                                .transition(.scale.combined(with: .opacity))
                        }
                    }

                    // Pet Tag
                    Text(skin.displayName)
                        .font(.system(size: 15, weight: .bold, design: .rounded))
                        .foregroundColor(.white)
                        .padding(.top, 4)

                    Text(skin.tagline)
                        .font(.system(size: 11, weight: .medium))
                        .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                }
                .offset(y: breathingOffset)
                .contentShape(Rectangle())
                .onTapGesture {
                    withAnimation(.spring(response: 0.3, dampingFraction: 0.6)) {
                        vm.petCompanion()
                    }
                }

                // Flying Petting Hearts
                ForEach(vm.hearts) { heart in
                    Text("❤️")
                        .font(.system(size: 24))
                        .scaleEffect(heart.scale)
                        .offset(heart.offset)
                        .transition(.opacity.combined(with: .move(edge: .bottom)))
                }
            }
            .frame(height: 250)

            // Interaction Cue
            HStack(spacing: 8) {
                Image(systemName: "hand.tap.fill")
                    .foregroundColor(skin.primaryColor)
                Text("Tap companion to pet & spawn love • \(vm.config.petCount) Pets")
                    .font(.system(size: 12, weight: .medium))
                    .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 8)
            .background(
                Capsule()
                    .fill(Color.white.opacity(0.04))
            )
        }
        .onAppear {
            withAnimation(.easeInOut(duration: 1.8).repeatForever(autoreverses: true)) {
                breathingOffset = -6
            }
            withAnimation(.linear(duration: 8.0).repeatForever(autoreverses: false)) {
                particlePhase = .pi * 2
            }
        }
    }
}
