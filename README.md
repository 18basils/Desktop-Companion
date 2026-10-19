# Desktop Companion v2.0 (PixelFriend Style) 💧

A lightweight, secure, and friendly desktop companion for Windows 10 & 11 (x64) that reminds you to stay hydrated, take eye breaks, and stretch during your work day.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011%20x64-brightgreen)
![Resource Usage](https://img.shields.io/badge/Idle%20CPU-0.0%25-success)
![Dependencies](https://img.shields.io/badge/external%20dependencies-zero-brightgreen)
![Security](https://img.shields.io/badge/security-hardened-success)

---

## 🎁 What's New in Version 2.0

### 🌟 Group A: System & Installer Upgrades
* **Official Windows Uninstaller**: Appears in **Windows Settings > Installed apps** (and Control Panel) with publisher info and icon. Includes an uninstallation wizard with an option to preserve your custom avatars and preferences.
* **Visual Settings Panel**: Accessible via tray menu (`⚙️ Settings...`) to easily configure your display name, interval, daily water goal, active schedule, audio chimes, and browse/import custom GIFs.
* **Colleague Setup Wizard (`Desktop Companion Setup.exe`)**: Self-contained, single-file installer that prompts *"What Should I Call You?!"*, automatically deploys the app, configures desktop/start menu/startup shortcuts, and displays complete instructions.

### 💧 Group B: Hydration & Wellness Upgrades
* **Daily Goal & Cup Tracker (System-Synced)**: Progress badge (e.g. `🥛 3 / 8 Cups Today`) with high-precision system clock synchronization. Automatically resets daily intake to 0 at midnight (00:00:00) and upon PC wake from sleep or hibernation.
* **🌙 Quiet Hours**: Silences the companion completely during user-defined rest hours (default: `10:00 PM — 8:00 AM`). Includes a native toggle switch in **Settings > Schedule** and a quick-toggle option in the system tray menu.
* **Meeting Mode / Smart Pause**: Right-click tray menu > `⏸️ Meeting Mode / Pause` to snooze reminders for 30 min, 1 hour, 2 hours, or the rest of the day without closing the app.
* **Multi-Break Variety**: Rotates between Hydration reminders, 20-20-20 Eye Strain breaks (`Look 20 feet away for 20 seconds 👁️`), and Posture Stretches (`Roll shoulders & stretch 🧘`).
* **Gentle Droplet Chime**: Native droplet sound (`drip.wav`) plays softly when the companion walks onscreen (can be muted anytime in Settings).

### 🐱 Group C: Companion & Avatar Polish
* **Interactive Petting**: Click the avatar to pet it and watch floating hearts (`❤️`) float up with cute responses!
* **Drag-and-Drop Positioning**: Click and drag the avatar horizontally across your taskbar to position it wherever convenient.
* **Accessory Evolution**:
  * Unlocks Cool Sunglasses (`🕶️`) at 4 cups!
  * Unlocks the Golden Crown (`👑`) when you reach your daily hydration goal!
* **In-Tray Skin Selector**: Easily switch between characters anytime via tray menu > `🎨 Avatars & Skins` (Pixel Guy, Cute Kitty, Robo Buddy, Water Slime, Forest Frog, Spooky Ghost, or Custom GIFs).
* **0.0% CPU Optimization**: Idle animation timers completely pause when offscreen, ensuring zero measurable CPU drain in the background.

---

## 📦 How to Share with Colleagues

Simply share the single installer file:
```
Desktop Companion Setup.exe
```
* **No Python, Git, or administrative privileges required.**
* When your colleague launches `Desktop Companion Setup.exe`:
  1. It asks: *"What Should I Call You?!"*
  2. Extracts all dependencies cleanly into `%LocalAppData%\Programs\Desktop Companion`.
  3. Creates Desktop, Start Menu, and Windows Startup shortcuts.
  4. Registers the app in Windows Settings so they can manage or uninstall it anytime.
  5. Shows an instruction overview with a button to launch immediately.

---

## ⏰ Work Hours Schedule & Quiet Hours

* **Active Working Days:** Monday to Friday (Customizable)
* **Active Working Hours:** 9:00 AM to 6:30 PM (Customizable)
* **🌙 Quiet Hours:** 10:00 PM to 8:00 AM (Toggleable & Customizable)
* **Default Interval:** Every 30 minutes during active hours (with 15-minute snooze).
* **Drift-Free Clock Sync:** Runs a lightweight system clock check every 10 seconds. Automatically triggers schedule start when workday opens (e.g. 9:00 AM) and recovers seamlessly from laptop sleep/hibernation.

---

## 🖱️ System Tray Menu

Right-click the **💧 Water Droplet** icon in the Windows taskbar tray (or inside the `^` notification overflow):

* **💧 Summon Companion** — Immediately brings the companion onto the screen.
* **🎨 Avatars & Skins** — Pick any character or enable dynamic cycling.
* **⏸️ Meeting Mode / Pause** — Silence reminders for 30m, 1h, 2h, or today.
* **📅 Schedule & Quiet Hours** — View active schedule summary and toggle Quiet Hours on/off with 1 click.
* **⚙️ Settings...** — Opens the visual configuration panel.
* **📁 Open App Folder** — Opens the installation folder and `custom_avatars` directory.
* **❌ Exit** — Completely closes the companion service.

*(Tip: Left-clicking the 💧 icon will also summon the companion immediately!)*

---

## 🗑️ How to Uninstall

Desktop Companion provides two easy uninstall methods:

1. **Via Windows Settings**:
   * Open **Windows Settings > Apps > Installed apps** (or *Apps & features*).
   * Search for **Desktop Companion**.
   * Click the three dots `...` and select **Uninstall**.

2. **Via Start Menu**:
   * Open the Start Menu, search for **Uninstall Desktop Companion**, and click it.
   * You can choose whether to keep or delete your imported avatars and saved preferences.

---

## 🔄 Upgrading from Earlier Versions

**You do NOT need to manually uninstall or delete files from Version 1.**
* The Version 2.0 installer (`Desktop Companion Setup.exe`) automatically detects any running instances of Desktop Companion, closes them safely, upgrades the core binaries, updates Windows registry entries, and **completely preserves your existing user name, configuration, and custom avatars** in `assets/custom_avatars/`.

---

## 🛡️ Software Security & Stability Hardening

* **Zero External Dependencies**: Bundles isolated Python runtimes and Qt libraries into a single file — no Python, Git, or VC++ Redistributable installations required on client machines.
* **Non-Elevated Execution**: Installs cleanly into standard user space (`%LocalAppData%\Programs\Desktop Companion`) with zero UAC / Administrator privileges needed.
* **Zip-Slip Directory Traversal Defense**: Strict canonical path validation during payload extraction.
* **Safe Avatar Importation**: Strict whitelist (`.gif`, `.png`), 15 MB file size limit, and image file header integrity checks via `QImageReader` to prevent malicious payloads or memory crashes.
* **Hardened Local IPC**: Local communication channel (`companion_ipc`) is restricted to whitelisted commands (`SUMMON`), rate-limited to 1.5s, with bounded buffers to prevent buffer overflows or local DoS.
* **Memory & GDI Leak Prevention**: All drawing routines explicitly terminate painters to prevent Windows GDI handle exhaustion over long multi-day runtimes.

