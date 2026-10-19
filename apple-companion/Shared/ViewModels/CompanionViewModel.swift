//
//  CompanionViewModel.swift
//  Apple Companion (iOS & macOS)
//

import Foundation
import SwiftUI
import Combine

public final class CompanionViewModel: ObservableObject {
    @Published public var config: CompanionConfig
    @Published public var hearts: [PetHeart] = []
    @Published public var emotionText: String = "Happy & Hydrated ✨"
    @Published public var pausedUntil: Date? = nil

    private let userDefaultsKey = "AppleCompanion_Config_v2"
    private var cancellables = Set<AnyCancellable>()

    public init() {
        if let data = UserDefaults.standard.data(forKey: userDefaultsKey),
           let saved = try? JSONDecoder().decode(CompanionConfig.self, from: data) {
            self.config = saved
        } else {
            self.config = .default
        }

        checkMidnightReset()

        // Notification handler
        NotificationService.shared.onDrinkActionTriggered = { [weak self] in
            self?.logCup()
        }

        // Auto-save on changes
        $config
            .debounce(for: .seconds(0.5), scheduler: RunLoop.main)
            .sink { [weak self] newConfig in
                self?.saveConfig(newConfig)
                NotificationService.shared.scheduleNextReminder(config: newConfig)
            }
            .store(in: &cancellables)
    }

    public func checkMidnightReset() {
        let today = CompanionConfig.todayString()
        if config.lastLogDate != today {
            config.cupsToday = 0
            config.lastLogDate = today
            saveConfig(config)
        }
    }

    public func logCup() {
        checkMidnightReset()
        config.cupsToday += 1
        HapticAndSoundService.playSuccess(hapticsEnabled: config.hapticEnabled)
        HapticAndSoundService.playWaterDroplet(soundEnabled: config.soundEnabled)

        if config.cupsToday >= config.dailyGoalCups {
            emotionText = "Goal Achieved! You're a Legend 🌟👑"
        } else {
            let quotes = [
                "Glug glug! Keep it flowing! 💧",
                "Brain power boosted! 🧠⚡",
                "Fresh, crisp & healthy! 🥤",
                "Your cells are celebrating! 🌊"
            ]
            emotionText = quotes.randomElement() ?? "Hydrated! 💧"
        }
    }

    public func petCompanion(at position: CGPoint = .zero) {
        config.petCount += 1
        HapticAndSoundService.playTick(hapticsEnabled: config.hapticEnabled)

        let heart = PetHeart(
            id: UUID(),
            offset: CGSize(width: Double.random(in: -30...30), height: Double.random(in: -40 ... -10)),
            scale: Double.random(in: 0.9...1.3)
        )
        hearts.append(heart)

        DispatchQueue.main.asyncAfter(deadline: .now() + 1.2) { [weak self] in
            self?.hearts.removeAll { $0.id == heart.id }
        }

        let phrases = [
            "Purr-fect! 💕",
            "You are awesome! ✨",
            "Petted with love! ❤️",
            "Best companion ever! 🐾"
        ]
        emotionText = phrases.randomElement() ?? "Happy! ✨"
    }

    public func pauseReminders(minutes: Int) {
        pausedUntil = Date().addingTimeInterval(TimeInterval(minutes * 60))
        HapticAndSoundService.playTick(hapticsEnabled: config.hapticEnabled)
    }

    public func resumeReminders() {
        pausedUntil = nil
        HapticAndSoundService.playTick(hapticsEnabled: config.hapticEnabled)
    }

    public func resetCupsToday() {
        config.cupsToday = 0
        saveConfig(config)
    }

    public func activeSkin() -> PetSkinType {
        PetSkinType(rawValue: config.selectedSkinKey) ?? .pixelGuy
    }

    public func setSkin(_ skin: PetSkinType) {
        config.dynamicAvatar = false
        config.selectedSkinKey = skin.rawValue
        HapticAndSoundService.playTick(hapticsEnabled: config.hapticEnabled)
    }

    private func saveConfig(_ cfg: CompanionConfig) {
        if let encoded = try? JSONEncoder().encode(cfg) {
            UserDefaults.standard.set(encoded, forKey: userDefaultsKey)
        }
    }
}

public struct PetHeart: Identifiable, Equatable {
    public let id: UUID
    public let offset: CGSize
    public let scale: Double
}
