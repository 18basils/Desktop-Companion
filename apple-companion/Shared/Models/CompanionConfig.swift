//
//  CompanionConfig.swift
//  Apple Companion (iOS & macOS)
//  Version 2.0 - Security & Modern Glassmorphism Edition
//

import Foundation

public struct ScheduleConfig: Codable, Equatable {
    public var enabled: Bool
    public var activeDays: [Int] // 1 = Sunday, 2 = Monday ... 6 = Friday, 7 = Saturday
    public var startHour: Int
    public var startMinute: Int
    public var endHour: Int
    public var endMinute: Int

    public static let `default` = ScheduleConfig(
        enabled: true,
        activeDays: [2, 3, 4, 5, 6], // Monday to Friday
        startHour: 9,
        startMinute: 0,
        endHour: 18,
        endMinute: 30
    )
}

public struct QuietHoursConfig: Codable, Equatable {
    public var enabled: Bool
    public var startHour: Int
    public var startMinute: Int
    public var endHour: Int
    public var endMinute: Int

    public static let `default` = QuietHoursConfig(
        enabled: true,
        startHour: 22, // 10:00 PM
        startMinute: 0,
        endHour: 8,    // 08:00 AM
        endMinute: 0
    )

    public var formattedRange: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "h:mm a"

        var cal = Calendar.current
        var comps = DateComponents()
        comps.hour = startHour
        comps.minute = startMinute
        let startDate = cal.date(from: comps) ?? Date()

        comps.hour = endHour
        comps.minute = endMinute
        let endDate = cal.date(from: comps) ?? Date()

        return "\(formatter.string(from: startDate)) — \(formatter.string(from: endDate))"
    }
}

public struct CompanionConfig: Codable, Equatable {
    public var userName: String
    public var intervalMinutes: Int
    public var snoozeMinutes: Int
    public var dailyGoalCups: Int
    public var cupsToday: Int
    public var lastLogDate: String
    public var soundEnabled: Bool
    public var hapticEnabled: Bool
    public var wittyDialogue: Bool
    public var enabledBreaks: [String]
    public var schedule: ScheduleConfig
    public var quietHours: QuietHoursConfig
    public var selectedSkinKey: String
    public var dynamicAvatar: Bool
    public var petCount: Int
    public var customAvatarData: Data?

    public static let `default` = CompanionConfig(
        userName: "Friend",
        intervalMinutes: 30,
        snoozeMinutes: 15,
        dailyGoalCups: 8,
        cupsToday: 0,
        lastLogDate: CompanionConfig.todayString(),
        soundEnabled: true,
        hapticEnabled: true,
        wittyDialogue: true,
        enabledBreaks: ["water", "eye_rest", "stretch"],
        schedule: .default,
        quietHours: .default,
        selectedSkinKey: "pixel_guy",
        dynamicAvatar: true,
        petCount: 0,
        customAvatarData: nil
    )

    public static func todayString() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        formatter.timeZone = TimeZone.current
        return formatter.string(from: Date())
    }
}
