//
//  BreakType.swift
//  Apple Companion (iOS & macOS)
//

import SwiftUI

public enum BreakType: String, CaseIterable, Identifiable, Codable {
    case water = "water"
    case eyeRest = "eye_rest"
    case stretch = "stretch"

    public var id: String { rawValue }

    public var title: String {
        switch self {
        case .water: return "Hydration"
        case .eyeRest: return "20-20-20 Eye Rest"
        case .stretch: return "Posture & Stretch"
        }
    }

    public var emoji: String {
        switch self {
        case .water: return "💧"
        case .eyeRest: return "👀"
        case .stretch: return "🧘"
        }
    }

    public var subtitle: String {
        switch self {
        case .water: return "Drink a refreshing cup of water to stay sharp."
        case .eyeRest: return "Focus on an object 20ft away for 20 seconds."
        case .stretch: return "Roll your shoulders and gently stretch your neck."
        }
    }

    public var accentColor: Color {
        switch self {
        case .water: return Color(red: 0.22, green: 0.74, blue: 0.97)
        case .eyeRest: return Color(red: 0.65, green: 0.35, blue: 0.96)
        case .stretch: return Color(red: 0.20, green: 0.83, blue: 0.60)
        }
    }
}
