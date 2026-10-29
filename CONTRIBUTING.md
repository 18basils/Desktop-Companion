# Contributing to Desktop Companion

Thank you for your interest in contributing to **Desktop Companion & Companion Hub**! Whether you are fixing a bug, adding a new animated pet, improving accessibility, or refining documentation, your contributions are welcome.

---

## 📋 Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Features](#suggesting-features)
   - [Contributing New Pet Avatars](#contributing-new-pet-avatars)
   - [Code Contributions](#code-contributions)
3. [Development Setup](#development-setup)
   - [Windows App (PyQt6)](#windows-app-pyqt6)
   - [Android App (Kotlin & Jetpack Compose)](#android-app-kotlin--jetpack-compose)
   - [Apple App (SwiftUI & Xcode)](#apple-app-swiftui--xcode)
   - [Web Portal (Firebase Hosting)](#web-portal-firebase-hosting)
4. [Pull Request Process](#pull-request-process)
5. [Coding & Style Standards](#coding--style-standards)

---

## Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all contributors. Please be respectful, constructive, and collaborative in all issues, pull requests, and discussions.

---

## How Can I Contribute?

### Reporting Bugs
Before submitting a bug report:
1. Check the [Issues](https://github.com/18basils/Desktop-Companion/issues) tab to see if the bug has already been reported.
2. If not, open a new issue using a descriptive title.
3. Include:
   * **Platform & OS version** (e.g., Windows 11 23H2, Android 14, macOS Sonoma).
   * **Steps to reproduce** the unexpected behavior.
   * **Expected vs. actual behavior**.
   * Relevant logs (from `app.log`) or screenshots.

### Suggesting Features
Have an idea for a new companion break type, widget, or customization?
* Open a feature suggestion under [Issues](https://github.com/18basils/Desktop-Companion/issues).
* Clearly explain the motivation, how users would interact with it, and on which platforms it should be available.

### Contributing New Pet Avatars
We welcome community-created pixel pets and animated avatars!
* **Requirements**:
  * Format: Transparent animated `.gif` or sequence of `.png` files.
  * Recommended canvas size: `32x32` to `64x64` pixels (pixel art style).
  * Safe & Friendly: Suitable for all audiences.
* Add your files to `assets/custom_avatars/` and test them using the in-app Avatar Settings tab.

---

## Development Setup

### Windows App (PyQt6)
1. Ensure Python 3.10+ is installed.
2. Clone the repository and navigate to the project directory:
   ```powershell
   git clone https://github.com/18basils/Desktop-Companion.git
   cd Desktop-Companion
   ```
3. Set up a virtual environment and install dependencies:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Run the app in development mode:
   ```powershell
   python companion.py
   ```
5. To test a full standalone build:
   ```powershell
   python build_windows.py
   ```

### Android App (Kotlin & Jetpack Compose)
1. Open the `phone-companion` directory in **Android Studio** (Giraffe or newer).
2. Allow Gradle sync to complete (requires Android SDK 34 / Java 17).
3. Run the app on an Android Virtual Device (AVD) or connected physical device:
   ```powershell
   cd phone-companion
   ./gradlew assembleDebug
   ```

### Apple App (SwiftUI & Xcode)
1. Open `apple-companion/Apple Companion.xcodeproj` in **Xcode** on macOS.
2. Select your target:
   * **macOS**: Transparent menu bar overlay & floating pet.
   * **iOS**: Hydration coach & home screen widgets.
3. Build and run with `Cmd + R`.

### Web Portal (Firebase Hosting)
1. The production web portal is live at **[https://mycompanionhub.web.app](https://mycompanionhub.web.app)**.
2. Web source files live in the `public/` directory (HTML5, CSS, responsive 3D SVG icons, and PWA manifest).
3. Test locally using any static web server:
   ```powershell
   python -m http.server 8000 --directory public
   ```
4. Deploy updates using the Firebase CLI:
   ```powershell
   firebase deploy --only hosting
   ```

---

## Pull Request Process

1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and test across your target platforms.
3. Ensure no unnecessary files or credentials are committed (check `.gitignore`).
4. Commit your changes with clear, descriptive commit messages:
   ```bash
   git commit -m "Add waddling penguin animation to community avatar pack"
   ```
5. Push to your fork and open a Pull Request against `main`.
6. Describe the changes, link relevant issues, and provide screenshots or GIF recordings of UI changes where applicable.

---

## Coding & Style Standards

* **Python**: Follow PEP 8 guidelines. Keep functions modular and maintain explicit error handling around file I/O and GDI operations.
* **Kotlin**: Follow official Kotlin coding conventions and Jetpack Compose best practices.
* **Swift**: Follow standard Swift API Design Guidelines.
* **HTML/CSS**: Keep responsive styles modular, preserve 3D SVG icon assets, and ensure all buttons maintain consistent flex alignment.
