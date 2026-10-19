//
//  HydrationGaugeView.swift
//  Apple Companion (iOS & macOS)
//

import SwiftUI

public struct HydrationGaugeView: View {
    @ObservedObject var vm: CompanionViewModel
    @State private var wavePhase: Double = 0

    public var body: some View {
        let currentCups = vm.config.cupsToday
        let goalCups = max(1, vm.config.dailyGoalCups)
        let progress = min(1.0, Double(currentCups) / Double(goalCups))
        let percentage = Int(progress * 100)
        let isGoalAchieved = currentCups >= goalCups

        VStack(spacing: 20) {
            // Glass Card Container
            VStack(spacing: 18) {
                // Circular Liquid Wave Progress Ring
                ZStack {
                    // Outer Glow Ring Background
                    Circle()
                        .stroke(Color.white.opacity(0.08), lineWidth: 14)
                        .frame(width: 190, height: 190)

                    // Gradient Progress Arc
                    Circle()
                        .trim(from: 0, to: CGFloat(progress))
                        .stroke(
                            AngularGradient(
                                colors: [
                                    Color(red: 0.13, green: 0.65, blue: 0.94),
                                    Color(red: 0.22, green: 0.83, blue: 0.94),
                                    Color(red: 0.20, green: 0.83, blue: 0.60)
                                ],
                                center: .center
                            ),
                            style: StrokeStyle(lineWidth: 14, lineCap: .round)
                        )
                        .rotationEffect(.degrees(-90))
                        .frame(width: 190, height: 190)
                        .shadow(color: Color(red: 0.13, green: 0.65, blue: 0.94).opacity(0.5), radius: 12)
                        .animation(.spring(response: 0.6, dampingFraction: 0.7), value: progress)

                    // Center Metrics
                    VStack(spacing: 4) {
                        Image(systemName: "drop.fill")
                            .font(.system(size: 24))
                            .foregroundColor(Color(red: 0.22, green: 0.83, blue: 0.94))

                        HStack(alignment: .lastTextBaseline, spacing: 2) {
                            Text("\(currentCups)")
                                .font(.system(size: 38, weight: .heavy, design: .rounded))
                                .foregroundColor(.white)
                            Text("/ \(goalCups)")
                                .font(.system(size: 18, weight: .semibold, design: .rounded))
                                .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                        }

                        Text("\(percentage)% Reached")
                            .font(.system(size: 13, weight: .bold))
                            .foregroundColor(isGoalAchieved ? Color(red: 0.20, green: 0.83, blue: 0.60) : Color(red: 0.22, green: 0.83, blue: 0.94))
                    }
                }
                .padding(.top, 10)

                // Celebration Banner (if achieved)
                if isGoalAchieved {
                    HStack(spacing: 8) {
                        Text("🌟 Daily Target Complete! Outstanding hydration!")
                            .font(.system(size: 13, weight: .bold))
                            .foregroundColor(Color(red: 0.20, green: 0.83, blue: 0.60))
                    }
                    .padding(.horizontal, 16)
                    .padding(.vertical, 8)
                    .background(
                        RoundedRectangle(cornerRadius: 10)
                            .fill(Color(red: 0.20, green: 0.83, blue: 0.60).opacity(0.12))
                            .overlay(
                                RoundedRectangle(cornerRadius: 10)
                                    .stroke(Color(red: 0.20, green: 0.83, blue: 0.60).opacity(0.3), lineWidth: 1)
                            )
                    )
                }

                // Primary Log Cup Action Button
                Button(action: {
                    withAnimation {
                        vm.logCup()
                    }
                }) {
                    HStack(spacing: 10) {
                        Image(systemName: "plus.circle.fill")
                            .font(.system(size: 18, weight: .bold))
                        Text("Log Cup of Water 💧")
                            .font(.system(size: 16, weight: .bold))
                    }
                    .foregroundColor(Color(red: 0.04, green: 0.07, blue: 0.13))
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 14)
                    .background(
                        LinearGradient(
                            colors: [
                                Color(red: 0.13, green: 0.65, blue: 0.94),
                                Color(red: 0.22, green: 0.83, blue: 0.94)
                            ],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .cornerRadius(14)
                    .shadow(color: Color(red: 0.13, green: 0.65, blue: 0.94).opacity(0.4), radius: 8, x: 0, y: 4)
                }
                .buttonStyle(PlainButtonStyle())

                // Quick Add Portions
                HStack(spacing: 10) {
                    quickAddButton(title: "+250 ml", cups: 1)
                    quickAddButton(title: "+500 ml", cups: 2)
                    quickAddButton(title: "+1000 ml", cups: 4)
                }

                // Reset & Sync Row
                HStack {
                    Label("Midnight Auto-Reset Active", systemImage: "clock.arrow.circlepath")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                    Spacer()
                    Button("Reset Count") {
                        vm.resetCupsToday()
                    }
                    .font(.system(size: 11, weight: .semibold))
                    .foregroundColor(Color(red: 0.98, green: 0.45, blue: 0.52))
                }
                .padding(.top, 4)
            }
            .padding(20)
            .background(
                RoundedRectangle(cornerRadius: 20)
                    .fill(Color(red: 0.08, green: 0.12, blue: 0.20).opacity(0.75))
                    .overlay(
                        RoundedRectangle(cornerRadius: 20)
                            .stroke(Color.white.opacity(0.08), lineWidth: 1)
                    )
            )
        }
    }

    private func quickAddButton(title: String, cups: Int) -> some View {
        Button(action: {
            for _ in 0..<cups {
                vm.logCup()
            }
        }) {
            Text(title)
                .font(.system(size: 13, weight: .semibold))
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 9)
                .background(
                    RoundedRectangle(cornerRadius: 10)
                        .fill(Color.white.opacity(0.06))
                        .overlay(
                            RoundedRectangle(cornerRadius: 10)
                                .stroke(Color.white.opacity(0.12), lineWidth: 1)
                        )
                )
        }
        .buttonStyle(PlainButtonStyle())
    }
}
