//
//  ScheduleSettingsView.swift
//  Apple Companion (iOS & macOS)
//

import SwiftUI

public struct ScheduleSettingsView: View {
    @ObservedObject var vm: CompanionViewModel

    private let weekdayLabels: [(day: Int, name: String)] = [
        (2, "Mon"),
        (3, "Tue"),
        (4, "Wed"),
        (5, "Thu"),
        (6, "Fri"),
        (7, "Sat"),
        (1, "Sun")
    ]

    public var body: some View {
        VStack(spacing: 16) {
            // Working Hours Schedule Card
            VStack(alignment: .leading, spacing: 14) {
                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("Working Hours Schedule")
                            .font(.system(size: 15, weight: .bold))
                            .foregroundColor(.white)
                        Text("Active only during your office / focus routine")
                            .font(.system(size: 11))
                            .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                    }
                    Spacer()
                    Toggle("", isOn: $vm.config.schedule.enabled)
                        .labelsHidden()
                        .toggleStyle(SwitchToggleStyle(tint: Color(red: 0.13, green: 0.65, blue: 0.94)))
                }

                if vm.config.schedule.enabled {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Active Days")
                            .font(.system(size: 12, weight: .semibold))
                            .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))

                        HStack(spacing: 6) {
                            ForEach(weekdayLabels, id: \.day) { item in
                                let isActive = vm.config.schedule.activeDays.contains(item.day)
                                Button(action: {
                                    if isActive {
                                        vm.config.schedule.activeDays.removeAll { $0 == item.day }
                                    } else {
                                        vm.config.schedule.activeDays.append(item.day)
                                    }
                                    HapticAndSoundService.playTick(hapticsEnabled: vm.config.hapticEnabled)
                                }) {
                                    Text(item.name)
                                        .font(.system(size: 12, weight: isActive ? .bold : .medium))
                                        .foregroundColor(isActive ? Color(red: 0.04, green: 0.07, blue: 0.13) : .white)
                                        .frame(maxWidth: .infinity)
                                        .padding(.vertical, 8)
                                        .background(
                                            RoundedRectangle(cornerRadius: 8)
                                                .fill(isActive ? Color(red: 0.22, green: 0.83, blue: 0.94) : Color.white.opacity(0.06))
                                        )
                                }
                                .buttonStyle(PlainButtonStyle())
                            }
                        }
                    }

                    HStack(spacing: 16) {
                        VStack(alignment: .leading, spacing: 4) {
                            Text("Start Time")
                                .font(.system(size: 11, weight: .semibold))
                                .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                            timePicker(hour: $vm.config.schedule.startHour, minute: $vm.config.schedule.startMinute)
                        }

                        VStack(alignment: .leading, spacing: 4) {
                            Text("End Time")
                                .font(.system(size: 11, weight: .semibold))
                                .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                            timePicker(hour: $vm.config.schedule.endHour, minute: $vm.config.schedule.endMinute)
                        }
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

            // Quiet Hours Card
            VStack(alignment: .leading, spacing: 14) {
                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("Quiet Hours")
                            .font(.system(size: 15, weight: .bold))
                            .foregroundColor(.white)
                        Text(vm.config.quietHours.enabled ? vm.config.quietHours.formattedRange : "Disabled (Off)")
                            .font(.system(size: 12, weight: .semibold))
                            .foregroundColor(vm.config.quietHours.enabled ? Color(red: 0.22, green: 0.83, blue: 0.94) : Color(red: 0.58, green: 0.64, blue: 0.72))
                    }
                    Spacer()
                    Toggle("", isOn: $vm.config.quietHours.enabled)
                        .labelsHidden()
                        .toggleStyle(SwitchToggleStyle(tint: Color(red: 0.13, green: 0.65, blue: 0.94)))
                }

                if vm.config.quietHours.enabled {
                    HStack(spacing: 16) {
                        VStack(alignment: .leading, spacing: 4) {
                            Text("Mute From")
                                .font(.system(size: 11, weight: .semibold))
                                .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                            timePicker(hour: $vm.config.quietHours.startHour, minute: $vm.config.quietHours.startMinute)
                        }

                        VStack(alignment: .leading, spacing: 4) {
                            Text("Until")
                                .font(.system(size: 11, weight: .semibold))
                                .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                            timePicker(hour: $vm.config.quietHours.endHour, minute: $vm.config.quietHours.endMinute)
                        }
                    }

                    Label("🌙 Silences all companion popups, reminders & droplet sounds completely.", systemImage: "moon.stars.fill")
                        .font(.system(size: 11))
                        .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                        .padding(.top, 4)
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
        }
    }

    private func timePicker(hour: Binding<Int>, minute: Binding<Int>) -> some View {
        HStack(spacing: 4) {
            Picker("Hour", selection: hour) {
                ForEach(0..<24, id: \.self) { h in
                    Text(String(format: "%02d", h)).tag(h)
                }
            }
            .pickerStyle(MenuPickerStyle())
            .accentColor(.white)

            Text(":")
                .foregroundColor(.white)

            Picker("Minute", selection: minute) {
                ForEach([0, 15, 30, 45], id: \.self) { m in
                    Text(String(format: "%02d", m)).tag(m)
                }
            }
            .pickerStyle(MenuPickerStyle())
            .accentColor(.white)
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 6)
        .background(
            RoundedRectangle(cornerRadius: 8)
                .fill(Color.white.opacity(0.06))
        )
    }
}
