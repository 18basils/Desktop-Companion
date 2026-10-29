# Apple Companion v2.0 (iOS, iPadOS & macOS)

A native, multiplatform Apple application built in **SwiftUI and Swift 5.9 / 6** bringing your interactive desktop & mobile pet to **iPhone, iPad, MacBook, and iMac**.

[![Release v2.0.0](https://img.shields.io/badge/release-v2.0.0-blue?logo=github)](https://github.com/18basils/Desktop-Companion/releases/tag/v2.0.0)
[![CodeQL](https://github.com/18basils/Desktop-Companion/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/18basils/Desktop-Companion/actions/workflows/github-code-scanning/codeql)
[![Build Apple](https://github.com/18basils/Desktop-Companion/actions/workflows/build-apple.yml/badge.svg)](https://github.com/18basils/Desktop-Companion/actions/workflows/build-apple.yml)
[![Portal](https://img.shields.io/badge/portal-https%3A%2F%2Fmycompanionhub.web.app-cyan)](https://mycompanionhub.web.app)
![Platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20iOS%20%7C%20iPadOS-brightgreen)
[![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey)](../LICENSE.md)

Live Production Portal: **[https://mycompanionhub.web.app](https://mycompanionhub.web.app)** (scan the on-screen Apple QR code to download directly to your iOS device).

---

## 🌟 Key Highlights & Modern UI

- **Universal Multiplatform Architecture**: Single shared SwiftUI core running seamlessly across iOS, iPadOS, and macOS.
- **10 Native Procedural Mascots (`PetSkinType`)**: Includes Pixel Guy, Cute Kitty, Robo Buddy, Water Slime, Forest Frog, Spooky Ghost, Playful Puppy, Rubber Duck, Mini Dino, and Honey Bear with custom color schemes and taglines.
- **Modern Dark Glassmorphic Design**:
  - Deep space midnight theme (`#080C15`) with Apple `.ultraThinMaterial` glass cards and glowing neon cyan accents.
  - Luminous avatar sanctuary with animated breathing motion, floating particle sparkles, and emotion status pills.
  - Interactive petting hearts: Tap companion on iPhone/iPad screen or Mac overlay to pat it and spawn floating hearts with haptic feedback (`UIImpactFeedbackGenerator` & `NSHapticFeedbackManager`).
- **Circular Glowing Liquid Wave Gauge**:
  - Live animated liquid gauge, percentage metrics, daily goal tracking, and celebratory badges upon goal completion.
  - Quick-log volume buttons (`+250 ml`, `+500 ml`, `+1000 ml`).
- **macOS Native System Integration (MenuBarExtra)**:
  - Just like the Windows System Tray, on macOS it sits in the top Menu Bar as a `💧` status item.
  - Right-click or click `💧` to summon your walking companion overlay, log water, toggle quiet hours, pause for meetings (30m, 1h, 2h), or open the Studio settings.
  - **Floating Transparent Desktop Pet Window**: Walks along the bottom of your Mac screen with the dark glassmorphic speech bubble, action buttons, and drag-and-drop support.
- **Break Reminders**:
  - Hydration (`💧`), 20-20-20 Eye Rest (`👀`), and Posture & Stretches (`🧘`).
- **Working Hours & Quiet Hours**:
  - Monday–Friday routine schedule.
  - Quiet hours (e.g. 10:00 PM – 8:00 AM) strictly silences notifications, popups, and droplet sound effects.

---

## 🔒 Apple OS Security & Privacy Compliance

| Security Requirement | Implementation | Description |
| :--- | :--- | :--- |
| **App Sandbox** | `Apple_Companion_macOS.entitlements` | Enabled (`com.apple.security.app-sandbox = true`) ensuring isolation from system files. |
| **Scoped File Access** | `PhotosPicker` / `NSOpenPanel` | Strictly scoped to files explicitly chosen by the user for custom avatar import. |
| **Zero Network Telemetry** | `com.apple.security.network.client = false` | The app has no network access permissions. 100% private, on-device local execution. |
| **Privacy Manifest** | `PrivacyInfo.xcprivacy` | Official Apple privacy manifest declaring zero tracking and authorized UserDefaults access (`CA92.1`). |
| **Safe Storage** | Sandboxed `UserDefaults` | Configuration, daily intake counters, and custom skins are stored safely within the app's sandboxed container. |
| **Notification Security** | `UNUserNotificationCenter` | Explicit user authorization request (`.alert`, `.sound`, `.badge`) with quiet hours suppression. |

---

## 🚀 How to Open & Build

### Option 1: Open in Xcode (Mac)
1. Copy or transfer the `apple-companion` directory to your Mac.
2. Double-click **`Apple Companion.xcodeproj`** (or open `Package.swift`).
3. Select your target in the top toolbar:
   - **My Mac**: Runs native macOS Menu Bar app + Floating Desktop Pet.
   - **iPhone 15/16 Pro Simulator / Any iOS Device**: Runs iPhone mobile companion.
   - **iPad Simulator / iPad Device**: Runs iPadOS layout.
4. Press **⌘ + R (Run)**!

### Option 2: Command Line (macOS Terminal)
```bash
cd apple-companion

# Build for macOS
xcodebuild -project "Apple Companion.xcodeproj" -scheme "Apple Companion" -destination "platform=macOS" -configuration Release build

# Build for iOS
xcodebuild -project "Apple Companion.xcodeproj" -scheme "Apple Companion" -destination "generic/platform=iOS" -configuration Release archive -archivePath "build/AppleCompanion-iOS.xcarchive"
```

### Option 3: Automated GitHub Actions CI/CD (No Mac Required)
The project includes a ready-to-run GitHub Actions workflow in `.github/workflows/build-apple.yml`:
1. Push this project to your GitHub repository.
2. Go to the **Actions** tab on GitHub and run the **Build Apple Companion** workflow.
3. GitHub automatically spins up a free macOS runner with Xcode and compiles:
   - **`Apple-Companion-macOS.dmg`**: Drag-and-drop installer for macOS (MacBook, iMac, Mac Mini).
   - **`Apple-Companion-iOS.ipa`**: iOS application package installable via Xcode Devices, AltStore, Sideloadly, or TestFlight.
