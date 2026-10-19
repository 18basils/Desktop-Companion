//
//  MainContentView.swift
//  Apple Companion (iOS & macOS)
//

import SwiftUI

public enum NavigationTab: String, CaseIterable, Identifiable {
    case companion = "Companion"
    case hydration = "Hydration"
    case wellness = "Wellness"
    case studio = "Studio"

    public var id: String { rawValue }

    public var icon: String {
        switch self {
        case .companion: return "pawprint.fill"
        case .hydration: return "drop.fill"
        case .wellness: return "heart.text.square.fill"
        case .studio: return "paintpalette.fill"
        }
    }
}

public struct MainContentView: View {
    @StateObject private var vm = CompanionViewModel()
    @State private var selectedTab: NavigationTab = .companion

    public init() {}

    public var body: some View {
        ZStack {
            // Modern Deep Midnight Navy Background
            LinearGradient(
                colors: [
                    Color(red: 0.03, green: 0.05, blue: 0.09),
                    Color(red: 0.05, green: 0.07, blue: 0.12),
                    Color(red: 0.04, green: 0.06, blue: 0.10)
                ],
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()

            VStack(spacing: 0) {
                // Top App Bar
                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        HStack(spacing: 8) {
                            Text("Apple Companion")
                                .font(.system(size: 20, weight: .heavy, design: .rounded))
                                .foregroundColor(.white)

                            Text("v2.0")
                                .font(.system(size: 10, weight: .bold))
                                .foregroundColor(Color(red: 0.22, green: 0.83, blue: 0.94))
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(
                                    Capsule()
                                        .fill(Color(red: 0.22, green: 0.83, blue: 0.94).opacity(0.18))
                                )
                        }

                        Text("Interactive Desk Pet & Hydration Companion")
                            .font(.system(size: 11, weight: .medium))
                            .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                    }

                    Spacer()

                    // Active Companion Avatar Badge
                    HStack(spacing: 6) {
                        Image(systemName: vm.activeSkin().iconName)
                            .font(.system(size: 13, weight: .bold))
                        Text(vm.activeSkin().displayName.split(separator: " ").first.map(String.init) ?? "Buddy")
                            .font(.system(size: 12, weight: .bold, design: .rounded))
                    }
                    .foregroundColor(Color(red: 0.04, green: 0.07, blue: 0.13))
                    .padding(.horizontal, 10)
                    .padding(.vertical, 5)
                    .background(
                        Capsule()
                            .fill(
                                LinearGradient(
                                    colors: [
                                        Color(red: 0.13, green: 0.65, blue: 0.94),
                                        Color(red: 0.22, green: 0.83, blue: 0.94)
                                    ],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                    )
                }
                .padding(.horizontal, 20)
                .padding(.top, 14)
                .padding(.bottom, 12)

                // Scrollable Content
                ScrollView(.vertical, showsIndicators: false) {
                    VStack(spacing: 16) {
                        switch selectedTab {
                        case .companion:
                            PixelAvatarStageView(vm: vm)
                                .padding(.top, 4)
                            HydrationGaugeView(vm: vm)
                        case .hydration:
                            HydrationGaugeView(vm: vm)
                                .padding(.top, 6)
                        case .wellness:
                            RemindersView(vm: vm)
                                .padding(.top, 6)
                            ScheduleSettingsView(vm: vm)
                        case .studio:
                            AvatarStudioView(vm: vm)
                                .padding(.top, 6)
                        }
                    }
                    .padding(.horizontal, 18)
                    .padding(.bottom, 100) // Spacing for floating bar
                }

                Spacer(minLength: 0)
            }

            // Floating Glass Bottom Navigation Bar
            VStack {
                Spacer()
                HStack {
                    ForEach(NavigationTab.allCases) { tab in
                        let isSelected = tab == selectedTab
                        Button(action: {
                            withAnimation(.spring(response: 0.35, dampingFraction: 0.7)) {
                                selectedTab = tab
                            }
                            HapticAndSoundService.playTick(hapticsEnabled: vm.config.hapticEnabled)
                        }) {
                            HStack(spacing: 6) {
                                Image(systemName: tab.icon)
                                    .font(.system(size: 15, weight: isSelected ? .bold : .medium))
                                if isSelected {
                                    Text(tab.rawValue)
                                        .font(.system(size: 13, weight: .bold, design: .rounded))
                                        .transition(.opacity.combined(with: .scale))
                                }
                            }
                            .foregroundColor(isSelected ? .white : Color(red: 0.58, green: 0.64, blue: 0.72))
                            .padding(.horizontal, isSelected ? 16 : 12)
                            .padding(.vertical, 10)
                            .background(
                                Capsule()
                                    .fill(isSelected ? Color(red: 0.13, green: 0.65, blue: 0.94).opacity(0.35) : Color.clear)
                            )
                        }
                        .buttonStyle(PlainButtonStyle())
                        if tab != NavigationTab.allCases.last {
                            Spacer()
                        }
                    }
                }
                .padding(.horizontal, 14)
                .padding(.vertical, 8)
                .background(
                    Capsule()
                        .fill(Color(red: 0.08, green: 0.12, blue: 0.20).opacity(0.85))
                        .overlay(
                            Capsule()
                                .stroke(Color.white.opacity(0.12), lineWidth: 1)
                        )
                        .shadow(color: Color.black.opacity(0.4), radius: 18, x: 0, y: 8)
                )
                .padding(.horizontal, 24)
                .padding(.bottom, 16)
            }
        }
        .onAppear {
            NotificationService.shared.requestAuthorization { _ in }
            vm.checkMidnightReset()
        }
    }
}
