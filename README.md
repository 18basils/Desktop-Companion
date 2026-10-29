# Companion Hub (Desktop & Mobile Pet) 💧

A lightweight, secure, and interactive cross-platform wellness companion for Windows, Android, macOS, and iOS that keeps you hydrated, reminds you of posture and eye breaks, and brings life to your workspace.

[![Release v2.0.0](https://img.shields.io/badge/release-v2.0.0-blue?logo=github)](https://github.com/18basils/Desktop-Companion/releases/tag/v2.0.0)
![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20Android%20%7C%20macOS%20%7C%20iOS-brightgreen)
![Mascots](https://img.shields.io/badge/mascots-10%20Native%20%2B%208%20Community%20GIFs-orange)
[![Portal](https://img.shields.io/badge/portal-https%3A%2F%2Fmycompanionhub.web.app-cyan)](https://mycompanionhub.web.app)
[![Security Policy](https://img.shields.io/badge/security-SECURITY.md-blue)](SECURITY.md)
[![Contributing Guidelines](https://img.shields.io/badge/contributing-CONTRIBUTING.md-green)](CONTRIBUTING.md)
[![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey)](LICENSE.md)

---

## 🌐 Official Web Portal & Downloads

Live Production Portal: **[https://mycompanionhub.web.app](https://mycompanionhub.web.app)**

* **Smart OS Auto-Detection**: Automatically identifies visitor operating systems (Windows, Android, macOS, iOS) and highlights the corresponding download card.
* **Handcrafted 3D Isometric Platform Cards**: Built with high-fidelity, responsive 3D SVG vectors and uniform, straight-aligned download action buttons.
* **10 Pixel Companions Showcase**: Interactive browser preview of all 10 procedural companion characters with live petting reactions, heart particles (`❤️`), and unique personality quotes.
* **Free Community Avatar Extension Pack**: Dedicated download card for `Companion-Avatar-Pack.zip` (~12 KB) featuring 8 extra animated companions and a 1-click batch installer for existing users that preserves configurations without reinstallation.
* **On-Screen Dual QR Code Hub**: Point your phone camera directly at the screen to instantly download the Android APK or Apple SwiftUI packages.
* **Quick Start & Customization Guide**: Built-in instructions covering accessory evolution (sunglasses & golden crown), meeting mode snoozing, working/quiet hours, custom avatar importing, and clean uninstallation.
* **Hardened Web Security & Anti-Abuse**: Strict Content Security Policy (CSP), HSTS preload, zero-clickjacking headers, verified search engine & social media bot permissions in `robots.txt`, and complete bandwidth shielding for binary downloads.

---

## 🐾 Mascot & Avatar System

Desktop Companion includes **18 ready-to-use companions** out of the box, with full support for custom animated imports:

### 1. 10 Built-In Procedural Pixel Mascots
Procedurally drawn pixel art with zero image asset load overhead and crisp scaling across Retina and high-DPI displays:
1. 🧢 **Pixel Guy**: Focused desk buddy and hydration companion.
2. 🐱 **Cute Kitty**: Gentle ginger tabby with cozy purring animations.
3. 🤖 **Robo Buddy**: Cyber wellness AI with animated antenna and LED screen.
4. 💧 **Water Slime**: Bouncing pure hydration mascot with droplet ripples.
5. 🐸 **Forest Frog**: Zen stretch master encouraging posture and neck rolls.
6. 👻 **Spooky Ghost**: Translucent lilac phantom keeping you alert at your screen.
7. 🐶 **Playful Puppy**: Golden retriever pup with floppy ears and a wagging tail.
8. 🦆 **Rubber Duck**: Classic yellow duck with an orange bill for coding & debugging.
9. 🦖 **Mini Dino**: Forest-green chibi dinosaur with dorsal spine plates.
10. 🐻 **Honey Bear**: Cozy caramel bear with rounded ears and a warm tummy.

### 2. 8 Pre-Bundled Community Animated GIFs
Fresh installations automatically bundle 8 animated pixel companions into `assets/custom_avatars/`:
* 🐕 **Shiba Inu** (`shiba_inu.gif`)
* 🐲 **Baby Dragon** (`baby_dragon.gif`)
* 🐼 **Bouncing Panda** (`bouncing_panda.gif`)
* 🐧 **Waddling Penguin** (`waddling_penguin.gif`)
* 🦫 **Chill Capybara** (`chill_capybara.gif`)
* 🦎 **Pink Axolotl** (`pink_axolotl.gif`)
* ⭐ **Golden Star** (`golden_star.gif`)
* 🧪 **Magic Potion** (`magic_potion.gif`)

### 3. Standalone Avatar Pack for Existing Users (Option 3)
Existing users can download [`Companion-Avatar-Pack.zip`](https://github.com/18basils/Desktop-Companion/releases/download/v2.0.0/Companion-Avatar-Pack.zip) (12.7 KB) directly from GitHub Releases or from the [Web Portal](https://mycompanionhub.web.app/downloads/Companion-Avatar-Pack.zip). Running `Install-Avatars.bat` automatically injects all 8 animated mascots into `%LocalAppData%\Programs\Desktop Companion\assets\custom_avatars\` without touching `config.json`. **Existing schedules, cup counts, and user names remain 100% intact.**

### 4. Custom Avatar Importer
Drop any animated `.gif` or `.png` into `assets/custom_avatars/` or use the in-app file browser in Settings. The companion automatically loads and walks with your custom avatar!

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
│   ├── downloads/                   # Downloadable ZIPs (Windows, Android, Apple, Avatar Pack)
│   └── assets/                      # Web icons, OpenGraph cards, audio
├── firebase.json, .firebaserc       # Firebase hosting, CSP & security configuration
└── assets/                          # App audio, tray icons, and bundled custom avatars
```

---

## 💻 1. Windows Desktop App

* **Daily Goal & Cup Tracker**: Progress badge (e.g. `🥛 3 / 8 Cups Today`) with high-precision system clock synchronization. Automatically resets daily intake to 0 at midnight (00:00:00) and upon PC wake from sleep or hibernation.
* **👑 Accessory Evolution**: Reaching 4 cups unlocks **pixel sunglasses 🕶️**; completing your daily goal unlocks a **golden celebration crown 👑** with confetti!
* **🌙 Working & Quiet Hours**: By default, runs during office hours (`Mon–Fri, 9:00 AM – 6:30 PM`) and completely silences reminders during quiet rest hours (`10:00 PM — 8:00 AM`).
* **⏸️ Meeting Mode / Smart Snooze**: Right-click tray menu > `Meeting Mode / Pause` to snooze reminders for 30m, 1h, 2h, or today without closing the application.
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
* Includes full hydration progress cards, character selection across native pixel skins, alarm/notification manager, and sound/haptics.
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

* Hosted on Firebase Hosting.
* Features smart device detection, on-screen dual QR codes, OpenGraph/Twitter cards for social sharing, PWA manifest, and Google Analytics 4 integration (`G-DDFQ122CDZ`).

### Deploying to Firebase on a New PC:
```powershell
npm install -g firebase-tools
firebase login
firebase deploy --only hosting
```

---

## 🛡️ Security & Bot Defense Configuration

Companion Hub enforces defense-in-depth across the desktop app, mobile targets, and web portal:

### Desktop & Client Hardening
* **Non-Elevated Execution**: Windows app runs strictly in user space with zero administrator or UAC prompts.
* **Zip-Slip Traversal Protection**: Canonical path validation during archive extraction.
* **Safe Avatar Importation**: Strict file extension whitelisting (`.gif`, `.png`), 15 MB file size limit, and header validation via `QImageReader`.
* **Hardened Local IPC**: Local communication channel (`companion_ipc`) is restricted to whitelisted commands (`SUMMON`), rate-limited to 1.5s, with bounded buffers to prevent buffer overflows or local DoS.
* **Memory & GDI Leak Prevention**: All drawing routines explicitly terminate painters to prevent Windows GDI handle exhaustion over long multi-day runtimes.

### Web Infrastructure & Crawler Defense
* **HTTP Security Headers**: HSTS (`max-age=31536000; preload`), `X-Frame-Options: DENY` (anti-clickjacking), `X-Content-Type-Options: nosniff`, and strict `Permissions-Policy`.
* **Content Security Policy (CSP)**: Whitelists only trusted origins (`'self'`, Google Tag Manager, Google Analytics, QR Server).
* **Crawler Policy (`robots.txt`)**: Allows verified search crawlers (Google, Bing, Apple) and social preview bots (WhatsApp, Twitter/X, LinkedIn, Slack) while strictly blocking aggressive SEO scrapers (Ahrefs, Semrush, Bytespider), AI harvesters (GPTBot, CCBot, ClaudeBot), and exploit scanners (sqlmap, Nmap, WPScan).
* **Download Abuse Safeguards**: Route `/downloads/**` enforces `X-Robots-Tag: noindex, nofollow`, `Content-Disposition: attachment`, and 24-hour Edge CDN caching to eliminate server bandwidth exhaustion.

---

## 📦 Official Downloads & Distribution Package

You can download pre-compiled packages directly from the official [v2.0.0 GitHub Release](https://github.com/18basils/Desktop-Companion/releases/tag/v2.0.0) (unlimited, fast global CDN) or through the [Web Portal](https://mycompanionhub.web.app):

| Platform / Target | Package Type | Direct CDN Download Link | Size |
| :--- | :--- | :--- | :--- |
| **Windows 10 / 11** | Setup Wizard (`.exe`) | [📥 Desktop.Companion.Setup.exe](https://github.com/18basils/Desktop-Companion/releases/download/v2.0.0/Desktop.Companion.Setup.exe) | ~72 MB |
| **Windows 10 / 11** | Portable Bundle (`.zip`) | [📥 Desktop-Companion-Windows.zip](https://github.com/18basils/Desktop-Companion/releases/download/v2.0.0/Desktop-Companion-Windows.zip) | ~71 MB |
| **Android Phone** | Direct APK (`.apk`) | [📥 Phone.Companion.apk](https://github.com/18basils/Desktop-Companion/releases/download/v2.0.0/Phone.Companion.apk) | ~8.1 MB |
| **Android Phone** | Package (`.zip`) | [📥 Phone-Companion-Android.zip](https://github.com/18basils/Desktop-Companion/releases/download/v2.0.0/Phone-Companion-Android.zip) | ~7.6 MB |
| **Apple (macOS & iOS)** | SwiftUI & Overlay (`.zip`) | [📥 Apple-Companion.zip](https://github.com/18basils/Desktop-Companion/releases/download/v2.0.0/Apple-Companion.zip) | ~29 KB |
| **Community Avatars** | Extension Pack (`.zip`) | [🎁 Companion-Avatar-Pack.zip](https://github.com/18basils/Desktop-Companion/releases/download/v2.0.0/Companion-Avatar-Pack.zip) | ~12.7 KB |

* **Web Portal with QR Codes**: [https://mycompanionhub.web.app](https://mycompanionhub.web.app) (Point your phone camera at your computer screen for instant mobile download).

---

## 📜 Community & Legal

* **[Security Policy (SECURITY.md)](SECURITY.md)**: Vulnerability disclosure policies, response SLAs, and local IPC/memory defense architecture.
* **[Contributing Guidelines (CONTRIBUTING.md)](CONTRIBUTING.md)**: Setup guides for Windows (PyQt6), Android (Compose), and Apple (SwiftUI), plus avatar contribution rules.
* **[License Terms (LICENSE.md)](LICENSE.md)**: Copyright © 2026 Basil Shaji. All rights reserved.

