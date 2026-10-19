//
//  RemindersView.swift
//  Apple Companion (iOS & macOS)
//

import SwiftUI

public struct RemindersView: View {
    @ObservedObject var vm: CompanionViewModel

    public var body: some View {
        VStack(spacing: 16) {
            // Break Variety Card
            VStack(alignment: .leading, spacing: 14) {
                Text("Enabled Reminders & Breaks")
                    .font(.system(size: 15, weight: .bold))
                    .foregroundColor(.white)

                ForEach(BreakType.allCases) { breakItem in
                    let isEnabled = vm.config.enabledBreaks.contains(breakItem.rawValue)
                    HStack(spacing: 12) {
                        ZStack {
                            Circle()
                                .fill(breakItem.accentColor.opacity(0.18))
                                .frame(width: 40, height: 40)
                            Text(breakItem.emoji)
                                .font(.system(size: 18))
                        }

                        VStack(alignment: .leading, spacing: 2) {
                            Text(breakItem.title)
                                .font(.system(size: 14, weight: .bold))
                                .foregroundColor(.white)
                            Text(breakItem.subtitle)
                                .font(.system(size: 11, weight: .regular))
                                .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                        }

                        Spacer()

                        Toggle("", isOn: Binding(
                            get: { isEnabled },
                            set: { on in
                                if on {
                                    if !vm.config.enabledBreaks.contains(breakItem.rawValue) {
                                        vm.config.enabledBreaks.append(breakItem.rawValue)
                                    }
                                } else {
                                    vm.config.enabledBreaks.removeAll { $0 == breakItem.rawValue }
                                    if vm.config.enabledBreaks.isEmpty {
                                        vm.config.enabledBreaks = ["water"]
                                    }
                                }
                            }
                        ))
                        .labelsHidden()
                        .toggleStyle(SwitchToggleStyle(tint: breakItem.accentColor))
                    }
                    if breakItem != BreakType.allCases.last {
                        Divider()
                            .background(Color.white.opacity(0.06))
                    }
                }
            }
            .padding(18)
            .background(
                RoundedRectangle(cornerRadius: 18)
                    .fill(Color(red: 0.08, green: 0.12, blue: 0.20).opacity(0.75))
                    .overlay(
                        RoundedRectangle(cornerRadius: 18)
                            .stroke(Color.white.opacity(0.08), lineWidth: 1)
                    )
            )

            // Cadence & Sound Card
            VStack(alignment: .leading, spacing: 14) {
                Text("Cadence & Sensory Feedback")
                    .font(.system(size: 15, weight: .bold))
                    .foregroundColor(.white)

                // Interval Chips
                VStack(alignment: .leading, spacing: 8) {
                    Text("Reminder Interval")
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))

                    HStack(spacing: 8) {
                        ForEach([15, 20, 30, 45, 60], id: \.self) { mins in
                            let isSelected = vm.config.intervalMinutes == mins
                            Button(action: {
                                vm.config.intervalMinutes = mins
                                HapticAndSoundService.playTick(hapticsEnabled: vm.config.hapticEnabled)
                            }) {
                                Text("\(mins)m")
                                    .font(.system(size: 13, weight: isSelected ? .bold : .medium))
                                    .foregroundColor(isSelected ? Color(red: 0.04, green: 0.07, blue: 0.13) : .white)
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 8)
                                    .background(
                                        RoundedRectangle(cornerRadius: 8)
                                            .fill(isSelected ? Color(red: 0.22, green: 0.83, blue: 0.94) : Color.white.opacity(0.06))
                                    )
                            }
                            .buttonStyle(PlainButtonStyle())
                        }
                    }
                }

                Divider()
                    .background(Color.white.opacity(0.06))

                // Sound & Haptic Toggles
                Toggle(isOn: $vm.config.soundEnabled) {
                    Label("Water Droplet Sound Chime", systemImage: "speaker.wave.2.fill")
                        .font(.system(size: 13, weight: .medium))
                        .foregroundColor(.white)
                }
                .toggleStyle(SwitchToggleStyle(tint: Color(red: 0.13, green: 0.65, blue: 0.94)))

                Toggle(isOn: $vm.config.hapticEnabled) {
                    Label("Haptic Ticks & Success Feedback", systemImage: "iphone.radiowaves.left.and.right")
                        .font(.system(size: 13, weight: .medium))
                        .foregroundColor(.white)
                }
                .toggleStyle(SwitchToggleStyle(tint: Color(red: 0.13, green: 0.65, blue: 0.94)))

                Toggle(isOn: $vm.config.wittyDialogue) {
                    Label("Show Motivational Dialogue Lines", systemImage: "bubble.left.and.bubble.right.fill")
                        .font(.system(size: 13, weight: .medium))
                        .foregroundColor(.white)
                }
                .toggleStyle(SwitchToggleStyle(tint: Color(red: 0.13, green: 0.65, blue: 0.94)))
            }
            .padding(18)
            .background(
                RoundedRectangle(cornerRadius: 18)
                    .fill(Color(red: 0.08, green: 0.12, blue: 0.20).opacity(0.75))
                    .overlay(
                        RoundedRectangle(cornerRadius: 18)
                            .stroke(Color.white.opacity(0.08), lineWidth: 1)
                    )
            )
        }
    }
}
