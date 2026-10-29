# Phone Companion v2.0 (Android) 🤖

An interactive, battery-friendly mobile wellness pet and hydration tracker built in **Kotlin** with modern **Jetpack Compose** and **Material Design 3**.

[![Release v2.0.0](https://img.shields.io/badge/release-v2.0.0-blue?logo=github)](https://github.com/18basils/Desktop-Companion/releases/tag/v2.0.0)
[![Portal](https://img.shields.io/badge/portal-https%3A%2F%2Fmycompanionhub.web.app-cyan)](https://mycompanionhub.web.app)
![Platforms](https://img.shields.io/badge/platform-Android%207.0%2B%20(API%2024%2B)-brightgreen?logo=android)
[![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey)](../LICENSE.md)

Live Production Portal: **[https://mycompanionhub.web.app](https://mycompanionhub.web.app)** (scan the on-screen Android QR code to download `Phone.Companion.apk` directly to your phone).

---

## 🌟 Key Highlights & Mobile UI

* **Modern Jetpack Compose UI**: Built with Material Design 3 surface containers, dynamic color theming, and dark midnight aesthetics (`#080C15`).
* **10 Native Procedural Mascots**: Select between Pixel Guy, Cute Kitty, Robo Buddy, Water Slime, Forest Frog, Spooky Ghost, Playful Puppy, Rubber Duck, Mini Dino, and Honey Bear.
* **Interactive Petting & Haptics**: Tap your companion on the home stage to pat it—triggers celebratory heart particle animations (`❤️`) and tactile vibration feedback.
* **Circular Hydration Gauge & Goal Tracking**:
  * Real-time circular water level indicator with percentage progress.
  * Quick-log buttons (`+250 ml`, `+500 ml`, `+1000 ml`).
  * Automatic midnight counter reset (00:00:00).
* **Smart Wellness Reminders**:
  * Customizable interval reminders for Hydration (`💧`), 20-20-20 Eye Rest (`👀`), and Posture Stretches (`🧘`).
  * Dedicated **Quiet Hours** support (e.g. 10:00 PM – 8:00 AM) to silence all notifications and droplet chimes during rest.
* **Zero Battery Drain**: Background work utilizes Android WorkManager and exact alarms without keeping background wake-locks active.

---

## 🔒 Privacy & Android Security

| Security Feature | Implementation | Description |
| :--- | :--- | :--- |
| **Local-First Storage** | Android DataStore / SharedPrefs | Daily water logs, active pet selection, and preferences remain 100% on-device. |
| **Zero Network Telemetry** | No analytics or tracking SDKs | The application does not communicate with any external telemetry servers. |
| **Scoped Permissions** | Notification & Exact Alarm | Only requests `POST_NOTIFICATIONS` and `SCHEDULE_EXACT_ALARM` permissions. |
| **Clean Architecture** | MVVM + Jetpack Compose | Strict separation of concerns between UI, State, and Data layers. |

---

## 🚀 How to Build & Install

### Option 1: Direct Download via Web Portal QR Code
1. Open **[https://mycompanionhub.web.app](https://mycompanionhub.web.app)** on your computer or laptop.
2. Under **"Scan to Install on Mobile"**, select **Android (.apk)**.
3. Open your Android phone camera, scan the QR code, and tap **Download** to install `Phone.Companion.apk`.

### Option 2: Open in Android Studio
1. Launch **Android Studio** (Giraffe or newer).
2. Click **Open** and select the `phone-companion/` directory.
3. Allow Gradle to sync dependencies (requires JDK 17).
4. Connect an Android physical device with USB debugging enabled, or start an Android Virtual Device (AVD).
5. Click **Run (Shift + F10)**.

### Option 3: Command Line (Gradle)
```powershell
cd phone-companion

# Build Debug APK
./gradlew assembleDebug

# Build Release APK
./gradlew assembleRelease
```
The compiled APK will be output to:
`phone-companion/app/build/outputs/apk/release/app-release.apk`
