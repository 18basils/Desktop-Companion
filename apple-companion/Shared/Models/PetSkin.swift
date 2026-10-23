//
//  PetSkin.swift
//  Apple Companion (iOS & macOS)
//

import SwiftUI

public enum PetSkinType: String, CaseIterable, Identifiable, Codable {
    case pixelGuy = "pixel_guy"
    case pixelCat = "pixel_cat"
    case pixelRobot = "pixel_robot"
    case pixelSlime = "pixel_slime"
    case pixelFrog = "pixel_frog"
    case pixelGhost = "pixel_ghost"
    case pixelPuppy = "pixel_puppy"
    case pixelDuck = "pixel_duck"
    case pixelDino = "pixel_dino"
    case pixelBear = "pixel_bear"

    public var id: String { rawValue }

    public var displayName: String {
        switch self {
        case .pixelGuy: return "Pixel Guy 🧢"
        case .pixelCat: return "Cute Kitty 🐱"
        case .pixelRobot: return "Robo Buddy 🤖"
        case .pixelSlime: return "Water Slime 💧"
        case .pixelFrog: return "Forest Frog 🐸"
        case .pixelGhost: return "Spooky Ghost 👻"
        case .pixelPuppy: return "Playful Puppy 🐶"
        case .pixelDuck: return "Rubber Duck 🦆"
        case .pixelDino: return "Mini Dino 🦖"
        case .pixelBear: return "Honey Bear 🐻"
        }
    }

    public var iconName: String {
        switch self {
        case .pixelGuy: return "person.crop.circle.fill"
        case .pixelCat: return "cat.fill"
        case .pixelRobot: return "cpu.fill"
        case .pixelSlime: return "drop.fill"
        case .pixelFrog: return "leaf.fill"
        case .pixelGhost: return "sparkles"
        case .pixelPuppy: return "pawprint.fill"
        case .pixelDuck: return "bird.fill"
        case .pixelDino: return "tortoise.fill"
        case .pixelBear: return "teddybear.fill"
        }
    }

    public var primaryColor: Color {
        switch self {
        case .pixelGuy: return Color(red: 0.13, green: 0.65, blue: 0.94) // Ocean Blue
        case .pixelCat: return Color(red: 0.98, green: 0.60, blue: 0.20) // Ginger Orange
        case .pixelRobot: return Color(red: 0.38, green: 0.85, blue: 0.98) // Cyber Cyan
        case .pixelSlime: return Color(red: 0.22, green: 0.82, blue: 0.98) // Aqua Neon
        case .pixelFrog: return Color(red: 0.20, green: 0.82, blue: 0.45) // Forest Green
        case .pixelGhost: return Color(red: 0.75, green: 0.55, blue: 0.98) // Ethereal Purple
        case .pixelPuppy: return Color(red: 0.96, green: 0.62, blue: 0.04) // Puppy Gold
        case .pixelDuck: return Color(red: 0.98, green: 0.80, blue: 0.08) // Duckling Yellow
        case .pixelDino: return Color(red: 0.06, green: 0.72, blue: 0.51) // Dino Emerald
        case .pixelBear: return Color(red: 0.57, green: 0.25, blue: 0.05) // Honey Bear Brown
        }
    }

    public var tagline: String {
        switch self {
        case .pixelGuy: return "Focused & Hydrated Worker"
        case .pixelCat: return "Purring Desk Companion"
        case .pixelRobot: return "Precision Wellness AI"
        case .pixelSlime: return "Pure Hydration Mascot"
        case .pixelFrog: return "Zen Stretches & Deep Sips"
        case .pixelGhost: return "Hauntingly Good Posture"
        }
    }
}
