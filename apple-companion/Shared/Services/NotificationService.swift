//
//  NotificationService.swift
//  Apple Companion (iOS & macOS)
//  Security & Local Privacy compliant: Zero cloud telemetry, strictly on-device scheduling
//

import Foundation
import UserNotifications

public final class NotificationService: NSObject, UNUserNotificationCenterDelegate {
    public static let shared = NotificationService()

    public static let categoryIdentifier = "COMPANION_HYDRATION_CATEGORY"
    public static let actionDrink = "ACTION_DRINK"
    public static let actionSnooze = "ACTION_SNOOZE"

    public var onDrinkActionTriggered: (() -> Void)?

    private override init() {
        super.init()
        UNUserNotificationCenter.current().delegate = self
        setupCategories()
    }

    public func requestAuthorization(completion: @escaping (Bool) -> Void) {
        let center = UNUserNotificationCenter.current()
        center.requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            DispatchQueue.main.async {
                completion(granted && error == nil)
            }
        }
    }

    private func setupCategories() {
        let drinkAction = UNNotificationAction(
            identifier: Self.actionDrink,
            title: "Drink Water 💧",
            options: [.foreground]
        )

        let snoozeAction = UNNotificationAction(
            identifier: Self.actionSnooze,
            title: "Remind Me in 15m ⏰",
            options: []
        )

        let category = UNNotificationCategory(
            identifier: Self.categoryIdentifier,
            actions: [drinkAction, snoozeAction],
            intentIdentifiers: [],
            options: []
        )

        UNUserNotificationCenter.current().setNotificationCategories([category])
    }

    public func scheduleNextReminder(config: CompanionConfig) {
        let center = UNUserNotificationCenter.current()
        center.removeAllPendingNotificationRequests()

        // Check quiet hours
        if isCurrentlyInQuietHours(config.quietHours) {
            return
        }

        // Check working schedule
        if !isWithinWorkingHours(config.schedule) {
            return
        }

        let content = UNMutableNotificationContent()
        content.title = "Time to Hydrate, \(config.userName)! 💧"
        content.body = "Your desk companion is cheering for you! Grab a fresh cup of water."
        content.sound = config.soundEnabled ? .default : nil
        content.categoryIdentifier = Self.categoryIdentifier

        let triggerSeconds = TimeInterval(max(60, config.intervalMinutes * 60))
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: triggerSeconds, repeats: false)

        let request = UNNotificationRequest(
            identifier: "CompanionReminder_\(UUID().uuidString)",
            content: content,
            trigger: trigger
        )

        center.add(request, withCompletionHandler: nil)
    }

    public func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse,
        withCompletionHandler completionHandler: @escaping () -> Void
    ) {
        if response.actionIdentifier == Self.actionDrink {
            DispatchQueue.main.async {
                self.onDrinkActionTriggered?()
            }
        }
        completionHandler()
    }

    public func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification,
        withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void
    ) {
        // Present banner even if app is in foreground
        completionHandler([.banner, .sound, .badge])
    }

    private func isCurrentlyInQuietHours(_ qh: QuietHoursConfig) -> Bool {
        guard qh.enabled else { return false }
        let now = Date()
        let cal = Calendar.current
        let currentHour = cal.component(.hour, from: now)
        let currentMinute = cal.component(.minute, from: now)
        let currentTime = currentHour * 60 + currentMinute

        let startTime = qh.startHour * 60 + qh.startMinute
        let endTime = qh.endHour * 60 + qh.endMinute

        if startTime <= endTime {
            return currentTime >= startTime && currentTime <= endTime
        } else {
            // Spanning midnight
            return currentTime >= startTime || currentTime <= endTime
        }
    }

    private func isWithinWorkingHours(_ sched: ScheduleConfig) -> Bool {
        guard sched.enabled else { return true }
        let now = Date()
        let cal = Calendar.current
        let weekday = cal.component(.weekday, from: now)
        if !sched.activeDays.contains(weekday) {
            return false
        }

        let currentHour = cal.component(.hour, from: now)
        let currentMinute = cal.component(.minute, from: now)
        let currentTime = currentHour * 60 + currentMinute

        let startTime = sched.startHour * 60 + sched.startMinute
        let endTime = sched.endHour * 60 + sched.endMinute

        if startTime <= endTime {
            return currentTime >= startTime && currentTime <= endTime
        } else {
            return currentTime >= startTime || currentTime <= endTime
        }
    }
}
