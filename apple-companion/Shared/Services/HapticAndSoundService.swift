//
//  HapticAndSoundService.swift
//  Apple Companion (iOS & macOS)
//

import Foundation
import SwiftUI

#if os(iOS)
import UIKit
import AudioToolbox
#elseif os(macOS)
import AppKit
#endif

public struct HapticAndSoundService {
    public static func playTick(hapticsEnabled: Bool) {
        guard hapticsEnabled else { return }
        #if os(iOS)
        let generator = UIImpactFeedbackGenerator(style: .light)
        generator.prepare()
        generator.impactOccurred()
        #elseif os(macOS)
        NSHapticFeedbackManager.defaultPerformer.perform(
            .alignment,
            performanceTime: .default
        )
        #endif
    }

    public static func playSuccess(hapticsEnabled: Bool) {
        guard hapticsEnabled else { return }
        #if os(iOS)
        let generator = UINotificationFeedbackGenerator()
        generator.prepare()
        generator.notificationOccurred(.success)
        #elseif os(macOS)
        NSHapticFeedbackManager.defaultPerformer.perform(
            .levelChange,
            performanceTime: .default
        )
        #endif
    }

    public static func playWaterDroplet(soundEnabled: Bool) {
        guard soundEnabled else { return }
        #if os(iOS)
        // Standard water-drop frequency chime tone
        AudioServicesPlaySystemSound(1057) // Gentle SMS/water tone
        #elseif os(macOS)
        if let sound = NSSound(named: "Hero") ?? NSSound(named: "Pop") {
            sound.play()
        }
        #endif
    }
}
