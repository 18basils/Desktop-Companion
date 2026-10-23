# Companion Hub (Desktop & Mobile Pet) 💧

A lightweight, secure, and interactive cross-platform wellness companion for Windows, Android, macOS, and iOS that keeps you hydrated, reminds you of posture and eye breaks, and brings life to your workspace.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20Android%20%7C%20macOS%20%7C%20iOS-brightgreen)
![Portal](https://img.shields.io/badge/portal-https%3A%2F%2Fmycompanionhub.web.app-cyan)

---

## 🌐 Official Web Portal & Downloads

Live Production Portal: **[https://mycompanionhub.web.app](https://mycompanionhub.web.app)**

* **Smart Device Detection**: Automatically highlights the download option matching the visitor's operating system.
* **On-Screen QR Codes**: Point your mobile camera at your laptop screen to download the Android APK or Apple package directly.
* **Pixel Companion Showcase**: Live interactive animation preview of all 6 companion characters (Pixel Guy, Cute Kitty, Robo Buddy, Water Slime, Forest Frog, and Spooky Ghost).
* **SEO & Crawler Protection**: Verified crawlers allowed (Googlebot, Bingbot, Applebot, Social media link previews), aggressive scrapers blocked, and downloads safeguarded with anti-abuse headers.

---

## 📱 Multi-Platform Architecture

```
Desktop-Companion/
├── companion.py, settings_dialog.py # Windows Desktop App (PyQt6 / Python)
├── installer.py, uninstaller.py     # Windows Setup Wizard & System Uninstaller
├── Desktop Companion*.spec          # PyInstaller build recipes
├── build_windows.py                 # Automated one-click build script
├── phone-companion/                 # Android Native App (Kotlin, Jetpack Compose, Material3)
├── apple-companion/                 # Apple Universal App (SwiftUI, macOS AppKit Overlay, iOS)
├── .github/workflows/               # GitHub Actions CI/CD (Automated macOS & iOS builds)
├── public/                          # Firebase Hosting portal (HTML5, PWA manifest, robots.txt)
├── firebase.json, .firebaserc       # Firebase hosting & security configuration
└── assets/                          # Shared audio, tray icons, and custom avatar templates
```

---

## 💻 1. Windows Desktop App

* **Daily Goal & Cup Tracker**: Progress badge (e.g. `🥛 3 / 8 Cups Today`) with high-precision system clock synchronization. Automatically resets daily intake to 0 at midnight (00:00:00) and upon PC wake from sleep or hibernation.
* **🌙 Quiet Hours**: Silences reminders completely during rest hours (default: `10:00 PM — 8:00 AM`). Toggleable from Settings or directly from the system tray menu.
* **Meeting Mode / Smart Pause**: Right-click tray menu > `⏸️ Meeting Mode / Pause` to snooze reminders for 30m, 1h, 2h, or today without quitting.
* **Multi-Break Variety**: Rotates between Hydration reminders, 20-20-20 Eye Strain breaks (`Look 20 feet away for 20 seconds 👁️`), and Posture Stretches (`Roll shoulders & stretch 🧘`).
* **Gentle Droplet Chime**: Native droplet sound (`drip.wav`) plays softly when the companion walks onscreen.
* **Interactive Petting**: Click the avatar to pet it and watch floating hearts (`❤️`) float up with cute responses!
* **Zero Idle CPU**: Animation timers stop completely when offscreen, ensuring zero background CPU drain.

### Windows Development & Building on a New PC:
```powershell
# 1. Setup Python Virtual Environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Run Directly
python companion.py

# 4. Automate Full Build (App, Uninstaller, Setup.exe, and Download Zip)
python build_windows.py
```

---

## 🤖 2. Android App (Phone Companion)

* Built with **Jetpack Compose**, **Kotlin Coroutines**, and **Material Design 3**.
* Includes full hydration progress cards, character selection, alarm/notification manager, and sound/haptics.
* Supports Android 8.0 (API 26) through Android 15+.

### Android Development & Building on a New PC:
```powershell
cd phone-companion

# Build Debug APK
./gradlew assembleDebug

# Build Release APK
./gradlew assembleRelease
```
Or open the `phone-companion` directory in **Android Studio** and click **Run**.

---

## 🍎 3. Apple App (macOS & iOS)

* Built with pure **SwiftUI** and native **Combine** architecture.
* **macOS Target**: Floats as a transparent desktop pet overlay across multi-monitor spaces with taskbar dock/menu bar controls.
* **iOS Target**: Interactive wellness tracker, home screen widgets, and lock screen hydration notifications.
* **Automated Cloud CI/CD**: Pushing to `main` runs `.github/workflows/build-apple.yml` on a GitHub `macos-latest` runner with Xcode to build `.dmg` and `.ipa` artifacts automatically.

### Apple Development on a Mac:
```bash
cd apple-companion
open "Apple Companion.xcodeproj"
# Press Cmd + R in Xcode to build and run
```

---

## 🔥 4. Firebase Web Portal & Hosting

* Hosted on Firebase Hosting Spark plan.
* Includes smart device detection, on-screen QR codes, OpenGraph link unfurling cards for WhatsApp/LinkedIn/Slack, PWA manifest, and Google Analytics 4 integration (`G-DDFQ122CDZ`).

### Deploying to Firebase on a New PC:
```powershell
npm install -g firebase-tools
firebase login
firebase deploy --only hosting
```

---

## 📦 Colleague Distribution Package

Simply share:
* **Windows**: `Desktop Companion Setup.exe` (or `Desktop-Companion-Windows.zip`) — Zero dependencies, non-admin install to `%LocalAppData%\Programs\Desktop Companion`.
* **Android**: `Phone Companion.apk` (or `Phone-Companion-Android.zip`).
* **Apple**: `Apple Companion (iOS & macOS).zip` or download the pre-compiled `.dmg`/`.ipa` from the GitHub Actions Artifacts tab.
* **Web**: Share [https://mycompanionhub.web.app](https://mycompanionhub.web.app).

---

## 🛡️ Security & Hardening

* **Non-Elevated Execution**: Windows app runs strictly in user space with zero administrator or UAC prompts.
* **Zip-Slip Traversal Protection**: Canonical path validation during archive extraction.
* **Safe Avatar Importation**: Strict file extension whitelisting (`.gif`, `.png`), 15 MB file size limit, and header validation via `QImageReader`.
* **Hardened Local IPC**: Local communication channel (`companion_ipc`) is restricted to whitelisted commands (`SUMMON`), rate-limited to 1.5s, with bounded buffers to prevent buffer overflows or local DoS.
* **Memory & GDI Leak Prevention**: All drawing routines explicitly terminate painters to prevent Windows GDI handle exhaustion over long multi-day runtimes.
* **Web Headers**: Strict CSP, HSTS with preload, `X-Content-Type-Options: nosniff`, and `X-Frame-Options: DENY`.
