"""
Desktop Companion - Standalone Installer & Setup Wizard
Version: 2.0.0 for Windows 10 & Windows 11 (x64)
"""

import sys
import os
import re
import json
import zipfile
import subprocess
import shutil
import winreg
from datetime import datetime

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QProgressBar, QCheckBox,
    QStackedWidget, QFrame, QScrollArea
)
from PyQt6.QtGui import QIcon, QFont, QPixmap, QDesktopServices
from PyQt6.QtCore import QUrl


def sanitize_user_name(name):
    """Security: sanitize username to prevent script/path injection and enforce reasonable length"""
    if not name:
        return "Friend"
    cleaned = re.sub(r"[^\w\s\-\.]", "", str(name).strip(), flags=re.UNICODE)
    cleaned = " ".join(cleaned.split())
    return cleaned[:30] if cleaned else "Friend"


def get_bundle_file(filename):
    """Retrieve path to bundled resource (supports PyInstaller onefile & local)"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


class InstallWorker(QThread):
    progress_signal = pyqtSignal(int, str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, user_name, install_dir, create_desktop, create_startmenu, create_startup):
        super().__init__()
        self.user_name = sanitize_user_name(user_name)
        self.install_dir = install_dir
        self.create_desktop = create_desktop
        self.create_startmenu = create_startmenu
        self.create_startup = create_startup

    def run(self):
        try:
            self.progress_signal.emit(5, "Checking for running instances & older versions...")
            # Automatically close older version if running to enable clean upgrade without file lock
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", "Desktop Companion.exe"],
                    capture_output=True,
                    creationflags=0x08000000
                )
            except Exception:
                pass

            self.progress_signal.emit(10, "Preparing Version 2.0 directory...")
            os.makedirs(self.install_dir, exist_ok=True)

            # Preserve settings & avatars if upgrading from v1
            existing_config_path = os.path.join(self.install_dir, "config.json")
            existing_cfg = {}
            if os.path.exists(existing_config_path):
                try:
                    with open(existing_config_path, "r", encoding="utf-8") as f:
                        existing_cfg = json.load(f)
                except Exception:
                    pass

            payload_zip = get_bundle_file("app_payload.zip")
            if not os.path.exists(payload_zip):
                payload_zip = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_payload.zip")

            if not os.path.exists(payload_zip):
                self.finished_signal.emit(False, "Could not find app_payload.zip installation archive.")
                return

            self.progress_signal.emit(25, "Extracting Version 2.0 application files...")
            base_canonical = os.path.abspath(self.install_dir)
            with zipfile.ZipFile(payload_zip, "r") as zf:
                total_files = len(zf.infolist())
                for i, file_info in enumerate(zf.infolist()):
                    # Zip-Slip security check: ensure destination path is strictly within install_dir
                    target_dest = os.path.abspath(os.path.join(self.install_dir, file_info.filename))
                    if not target_dest.startswith(base_canonical):
                        continue

                    # Don't overwrite existing custom avatars directory
                    if file_info.filename.startswith("assets/custom_avatars/") and os.path.exists(target_dest):
                        continue

                    zf.extract(file_info, self.install_dir)
                    if i % 10 == 0:
                        pct = 25 + int((i / total_files) * 45)
                        self.progress_signal.emit(pct, f"Extracting {file_info.filename[:25]}...")

            self.progress_signal.emit(75, f"Configuring preferences for {self.user_name}...")
            config_path = os.path.join(self.install_dir, "config.json")
            today_str = datetime.now().strftime("%Y-%m-%d")

            # Determine name: use entered name unless user kept default and had a prior custom name
            effective_name = self.user_name
            if effective_name in ("Friend", "") and existing_cfg.get("user_name"):
                effective_name = existing_cfg.get("user_name")

            config_data = {
                "version": "2.0.0",
                "user_name": sanitize_user_name(effective_name),
                "interval_minutes": existing_cfg.get("interval_minutes", 30),
                "snooze_minutes": existing_cfg.get("snooze_minutes", 15),
                "walk_speed": existing_cfg.get("walk_speed", 4),
                "screen_side": "left",
                "dynamic_avatar": existing_cfg.get("dynamic_avatar", True),
                "skin": existing_cfg.get("skin", "pixel_guy"),
                "daily_goal_cups": existing_cfg.get("daily_goal_cups", 8),
                "cups_today": existing_cfg.get("cups_today", 0),
                "last_date": existing_cfg.get("last_date", today_str),
                "break_types": existing_cfg.get("break_types", ["water", "eye_rest", "stretch"]),
                "witty_dialogue": existing_cfg.get("witty_dialogue", True),
                "schedule": existing_cfg.get("schedule", {
                    "enabled": True,
                    "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                    "start_time": "09:00",
                    "end_time": "18:30"
                }),
                "quiet_hours": existing_cfg.get("quiet_hours", {
                    "enabled": True,
                    "start_time": "22:00",
                    "end_time": "08:00"
                }),
                "sound_enabled": existing_cfg.get("sound_enabled", True)
            }
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4)

            # Ensure assets/custom_avatars exists
            custom_avatars_dir = os.path.join(self.install_dir, "assets", "custom_avatars")
            os.makedirs(custom_avatars_dir, exist_ok=True)

            self.progress_signal.emit(85, "Creating Windows shortcuts...")
            exe_path = os.path.join(self.install_dir, "Desktop Companion.exe")
            ico_path = os.path.join(self.install_dir, "assets", "tray_icon.ico")
            uninst_exe = os.path.join(self.install_dir, "Uninstall Desktop Companion.exe")

            # 1. Desktop shortcut
            if self.create_desktop:
                desktop_folder = os.path.join(os.path.expanduser("~"), "Desktop")
                if os.path.exists(desktop_folder):
                    lnk_path = os.path.join(desktop_folder, "Desktop Companion.lnk")
                    self.make_shortcut(exe_path, lnk_path, ico_path)

            # 2. Start menu shortcut
            if self.create_startmenu:
                appdata = os.environ.get("APPDATA") or os.path.expanduser(r"~\AppData\Roaming")
                programs_dir = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs")
                if os.path.exists(programs_dir):
                    lnk_path = os.path.join(programs_dir, "Desktop Companion.lnk")
                    self.make_shortcut(exe_path, lnk_path, ico_path)
                    if os.path.exists(uninst_exe):
                        uninst_lnk = os.path.join(programs_dir, "Uninstall Desktop Companion.lnk")
                        self.make_shortcut(uninst_exe, uninst_lnk, ico_path)

            # 3. Startup shortcut
            if self.create_startup:
                appdata = os.environ.get("APPDATA") or os.path.expanduser(r"~\AppData\Roaming")
                startup_dir = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
                if os.path.exists(startup_dir):
                    lnk_path = os.path.join(startup_dir, "Desktop Companion.lnk")
                    self.make_shortcut(exe_path, lnk_path, ico_path)

            # 4. Register in Windows Settings "Installed apps"
            self.progress_signal.emit(95, "Registering in Windows Installed Apps...")
            self.register_windows_uninstall(self.install_dir)

            self.progress_signal.emit(100, "Installation completed successfully!")
            self.finished_signal.emit(True, "Success")
        except Exception as e:
            self.finished_signal.emit(False, str(e))

    def register_windows_uninstall(self, install_dir):
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\DesktopCompanion"
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)

            uninstaller_exe = os.path.join(install_dir, "Uninstall Desktop Companion.exe")
            ico_path = os.path.join(install_dir, "assets", "tray_icon.ico")

            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "Desktop Companion")
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "2.0.0")
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "Desktop Companion")
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, install_dir)
            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, ico_path)
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'"{uninstaller_exe}"')
            winreg.SetValueEx(key, "QuietUninstallString", 0, winreg.REG_SZ, f'"{uninstaller_exe}" --quiet')
            winreg.SetValueEx(key, "EstimatedSize", 0, winreg.REG_DWORD, 75000)
            winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
        except Exception:
            pass

    def make_shortcut(self, target_exe, lnk_path, icon_path):
        try:
            # Escape single quotes for PowerShell string literal security
            esc_lnk = lnk_path.replace("'", "''")
            esc_exe = target_exe.replace("'", "''")
            esc_dir = os.path.dirname(target_exe).replace("'", "''")
            esc_ico = icon_path.replace("'", "''")

            ps_cmd = f"""
            $WshShell = New-Object -ComObject WScript.Shell;
            $Shortcut = $WshShell.CreateShortcut('{esc_lnk}');
            $Shortcut.TargetPath = '{esc_exe}';
            $Shortcut.WorkingDirectory = '{esc_dir}';
            $Shortcut.Description = 'Desktop Companion v2.0';
            """
            if os.path.exists(icon_path):
                ps_cmd += f"$Shortcut.IconLocation = '{esc_ico}, 0';"
            ps_cmd += "$Shortcut.Save();"
            subprocess.run(
                ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_cmd],
                creationflags=0x08000000,
                check=False
            )
        except Exception:
            pass


class InstallerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Companion v2.0 Setup")
        self.setFixedSize(680, 640)

        ico_file = get_bundle_file("assets/tray_icon.ico")
        if os.path.exists(ico_file):
            self.setWindowIcon(QIcon(ico_file))

        local_app = os.environ.get("LOCALAPPDATA") or os.path.expanduser(r"~\AppData\Local")
        self.install_dir = os.path.join(local_app, "Programs", "Desktop Companion")

        self.setStyleSheet("""
            QWidget {
                background-color: #0b1120;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                color: #f8fafc;
            }
            QLabel {
                color: #e2e8f0;
            }
            QLineEdit {
                background-color: #1e293b;
                border: 2px solid #334155;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 15px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #38bdf8;
                background-color: #0f172a;
            }
            QPushButton.primary {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
                color: #080c15;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 700;
                padding: 12px 26px;
            }
            QPushButton.primary:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38bdf8, stop:1 #7dd3fc);
            }
            QPushButton.secondary {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 500;
                padding: 10px 18px;
            }
            QPushButton.secondary:hover {
                background-color: #334155;
                color: #ffffff;
                border-color: #475569;
            }
            QCheckBox {
                font-size: 13px;
                color: #cbd5e1;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1.5px solid #475569;
                background-color: #1e293b;
            }
            QCheckBox::indicator:hover {
                border-color: #38bdf8;
            }
            QCheckBox::indicator:checked {
                background-color: #0284c7;
                border-color: #38bdf8;
            }
            QProgressBar {
                border: 1px solid #1e293b;
                border-radius: 8px;
                background-color: #111827;
                text-align: center;
                height: 18px;
                font-size: 12px;
                font-weight: 700;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
                border-radius: 7px;
            }
            QFrame.card {
                background-color: #111827;
                border: 1px solid #1f2937;
                border-radius: 12px;
                padding: 14px;
            }
        """)

        self.stacked = QStackedWidget(self)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stacked)

        # Build Page 1 (Input Name & Options)
        self.page_welcome = self.create_welcome_page()
        self.stacked.addWidget(self.page_welcome)

        # Build Page 2 (Instruction & Finish Page)
        self.page_instructions = self.create_instructions_page()
        self.stacked.addWidget(self.page_instructions)

    def create_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(36, 26, 36, 26)
        layout.setSpacing(14)

        # Header Hero
        header_layout = QHBoxLayout()
        header_icon = QLabel("💧")
        header_icon.setFont(QFont("Segoe UI Emoji", 32))
        
        header_text_layout = QVBoxLayout()
        title = QLabel("Desktop Companion v2.0 Setup")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff;")
        subtitle = QLabel("Personalized Hydration & Wellness Pet for Windows 10 & 11")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #94a3b8;")
        header_text_layout.addWidget(title)
        header_text_layout.addWidget(subtitle)

        header_layout.addWidget(header_icon)
        header_layout.addSpacing(10)
        header_layout.addLayout(header_text_layout)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("color: #1e293b; background-color: #1e293b; height: 1px;")
        layout.addWidget(div)

        # Card: What Should I Call You?!
        prompt_card = QFrame()
        prompt_card.setProperty("class", "card")
        prompt_layout = QVBoxLayout(prompt_card)
        prompt_layout.setSpacing(8)

        lbl_question = QLabel("What Should I Call You?!")
        lbl_question.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        lbl_question.setStyleSheet("color: #38bdf8;")

        lbl_desc = QLabel("Enter your name or nickname so your companion can greet you properly:")
        lbl_desc.setFont(QFont("Segoe UI", 12))
        lbl_desc.setStyleSheet("color: #94a3b8;")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Alex, Sarah, Batman, Boss...")
        self.name_input.setText("Friend")
        self.name_input.selectAll()

        prompt_layout.addWidget(lbl_question)
        prompt_layout.addWidget(lbl_desc)
        prompt_layout.addSpacing(4)
        prompt_layout.addWidget(self.name_input)

        layout.addWidget(prompt_card)

        # Options Card
        opts_card = QFrame()
        opts_card.setProperty("class", "card")
        opts_layout = QVBoxLayout(opts_card)
        opts_layout.setSpacing(8)

        lbl_opts = QLabel("Installation Options:")
        lbl_opts.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        opts_layout.addWidget(lbl_opts)

        self.chk_desktop = QCheckBox("Create Desktop shortcut")
        self.chk_desktop.setChecked(True)
        opts_layout.addWidget(self.chk_desktop)

        self.chk_startmenu = QCheckBox("Add to Start Menu & Windows Installed Apps")
        self.chk_startmenu.setChecked(True)
        opts_layout.addWidget(self.chk_startmenu)

        self.chk_startup = QCheckBox("Automatically start when Windows boots")
        self.chk_startup.setChecked(True)
        opts_layout.addWidget(self.chk_startup)

        lbl_path_info = QLabel(f"📂 Install Path: {self.install_dir}\n(Standard user app profile — no admin password required!)")
        lbl_path_info.setStyleSheet("color: #64748b; font-size: 11px;")
        opts_layout.addWidget(lbl_path_info)

        layout.addWidget(opts_card)

        # Progress elements
        self.prog_status = QLabel("Ready to install.")
        self.prog_status.setStyleSheet("color: #64748b; font-size: 12px;")
        self.prog_status.hide()
        layout.addWidget(self.prog_status)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Action Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_install = QPushButton("Begin Installation  ➔")
        self.btn_install.setProperty("class", "primary")
        self.btn_install.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_install.clicked.connect(self.start_installation)
        btn_layout.addWidget(self.btn_install)

        layout.addLayout(btn_layout)
        return page

    def create_instructions_page(self):
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(28, 18, 28, 18)
        page_layout.setSpacing(10)

        # Header
        # Header
        self.lbl_finish_title = QLabel("🎉 Installation Complete!")
        self.lbl_finish_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.lbl_finish_title.setStyleSheet("color: #34d399;")

        self.lbl_finish_sub = QLabel("Here is everything new in Desktop Companion v2.0:")
        self.lbl_finish_sub.setFont(QFont("Segoe UI", 12))
        self.lbl_finish_sub.setStyleSheet("color: #94a3b8;")

        page_layout.addWidget(self.lbl_finish_title)
        page_layout.addWidget(self.lbl_finish_sub)

        # Scrollable Instruction Cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        scroll_content = QWidget()
        cards_layout = QVBoxLayout(scroll_content)
        cards_layout.setSpacing(10)
        cards_layout.setContentsMargins(0, 0, 10, 0)

        # Card 1: System Tray & Running
        c1 = QFrame()
        c1.setProperty("class", "card")
        l1 = QVBoxLayout(c1)
        l1.setSpacing(5)
        t1 = QLabel("💧 1. Running in System Tray & Meeting Mode")
        t1.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        t1.setStyleSheet("color: #38bdf8;")
        d1 = QLabel(
            "• Runs silently in your Windows System Tray (next to your clock).<br>"
            "• <b>Windows 11 Tip:</b> Look inside the <b>^ (Show hidden icons)</b> menu! Drag the 💧 icon to your main taskbar to keep it pinned.<br>"
            "• <b>Left-Click 💧:</b> Summons your companion immediately onto your screen.<br>"
            "• <b>Right-Click 💧:</b> Opens the menu with <b>Settings...</b>, <b>Meeting Mode / Pause</b>, <b>Skins</b>, and <b>Exit</b>.<br>"
            "• <b>Meeting Mode:</b> Pause reminders for 30m, 1h, or 2h during calls or presentations!"
        )
        d1.setWordWrap(True)
        d1.setTextFormat(Qt.TextFormat.RichText)
        d1.setStyleSheet("color: #cbd5e1; font-size: 12px; line-height: 1.4;")
        l1.addWidget(t1)
        l1.addWidget(d1)
        cards_layout.addWidget(c1)

        # Card 2: Goals, Evolution & Breaks
        c2 = QFrame()
        c2.setProperty("class", "card")
        l2 = QVBoxLayout(c2)
        l2.setSpacing(5)
        t2 = QLabel("🥛 2. Daily Water Goal & Accessory Evolution")
        t2.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        t2.setStyleSheet("color: #38bdf8;")
        d2 = QLabel(
            "• <b>Daily Water Goal:</b> Tracks your cups today (default: 8 cups). Resets every morning!<br>"
            "• <b>Avatar Accessories:</b> Reaching 4 cups unlocks <b>pixel sunglasses 🕶️</b> on your avatar! Hitting your daily goal unlocks a <b>golden celebration crown 👑</b>!<br>"
            "• <b>Break Variety:</b> Gentle prompts rotate between Hydration 💧, 20-20-20 Eye Rest 👁️, and Posture Stretches 🧘."
        )
        d2.setWordWrap(True)
        d2.setTextFormat(Qt.TextFormat.RichText)
        d2.setStyleSheet("color: #cbd5e1; font-size: 12px; line-height: 1.4;")
        l2.addWidget(t2)
        l2.addWidget(d2)
        cards_layout.addWidget(c2)

        # Card 3: Interactive Petting & Custom Avatars
        c3 = QFrame()
        c3.setProperty("class", "card")
        l3 = QVBoxLayout(c3)
        l3.setSpacing(5)
        t3 = QLabel("🐾 3. Interactive Petting, Dragging & Custom Avatars")
        t3.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        t3.setStyleSheet("color: #38bdf8;")
        d3 = QLabel(
            "• <b>Pet Your Companion:</b> Click on the character on-screen to pat it and spawn floating hearts ❤️!<br>"
            "• <b>Drag & Reposition:</b> Click and drag the companion to move it anywhere along the bottom of your screen.<br>"
            "• <b>Settings Panel:</b> Right-click 💧 > <b>Settings...</b> opens the full GUI window to adjust goals, schedules, and import custom GIFs!"
        )
        d3.setWordWrap(True)
        d3.setTextFormat(Qt.TextFormat.RichText)
        d3.setStyleSheet("color: #cbd5e1; font-size: 12px; line-height: 1.4;")
        l3.addWidget(t3)
        l3.addWidget(d3)
        cards_layout.addWidget(c3)

        # Card 4: Uninstalling
        c4 = QFrame()
        c4.setProperty("class", "card")
        l4 = QVBoxLayout(c4)
        l4.setSpacing(5)
        t4 = QLabel("🗑️ 4. Official Windows Uninstaller")
        t4.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        t4.setStyleSheet("color: #fb7185;")
        d4 = QLabel(
            "• Desktop Companion is registered in <b>Windows Settings > Apps > Installed apps</b>.<br>"
            "• You can uninstall it anytime directly from Windows Settings or via <b>Uninstall Desktop Companion</b> in your Start Menu."
        )
        d4.setWordWrap(True)
        d4.setTextFormat(Qt.TextFormat.RichText)
        d4.setStyleSheet("color: #cbd5e1; font-size: 12px; line-height: 1.4;")
        l4.addWidget(t4)
        l4.addWidget(d4)
        cards_layout.addWidget(c4)

        scroll.setWidget(scroll_content)
        page_layout.addWidget(scroll)

        # Bottom Buttons
        btn_bar = QHBoxLayout()
        
        btn_open_folder = QPushButton("📁 Open App Folder")
        btn_open_folder.setProperty("class", "secondary")
        btn_open_folder.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_open_folder.clicked.connect(self.open_installed_folder)
        btn_bar.addWidget(btn_open_folder)

        btn_bar.addStretch()

        self.btn_launch = QPushButton("💧 Launch Desktop Companion v2.0 Now")
        self.btn_launch.setProperty("class", "primary")
        self.btn_launch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_launch.clicked.connect(self.launch_and_exit)
        btn_bar.addWidget(self.btn_launch)

        page_layout.addLayout(btn_bar)
        return page

    def start_installation(self):
        user_name = self.name_input.text().strip()
        if not user_name:
            user_name = "Friend"

        self.btn_install.setEnabled(False)
        self.name_input.setEnabled(False)
        self.prog_status.show()
        self.progress_bar.show()

        self.worker = InstallWorker(
            user_name=user_name,
            install_dir=self.install_dir,
            create_desktop=self.chk_desktop.isChecked(),
            create_startmenu=self.chk_startmenu.isChecked(),
            create_startup=self.chk_startup.isChecked()
        )
        self.worker.progress_signal.connect(self.on_install_progress)
        self.worker.finished_signal.connect(self.on_install_finished)
        self.worker.start()

    def on_install_progress(self, percent, message):
        self.progress_bar.setValue(percent)
        self.prog_status.setText(message)

    def on_install_finished(self, success, message):
        if success:
            user_name = self.name_input.text().strip() or "Friend"
            self.lbl_finish_title.setText(f"🎉 Installation Complete! Welcome, {user_name}!")
            self.stacked.setCurrentIndex(1)
        else:
            self.prog_status.setText(f"Error: {message}")
            self.prog_status.setStyleSheet("color: #e11d48; font-size: 13px; font-weight: bold;")
            self.btn_install.setEnabled(True)

    def open_installed_folder(self):
        try:
            os.startfile(self.install_dir)
        except Exception:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.install_dir))

    def launch_and_exit(self):
        exe_path = os.path.join(self.install_dir, "Desktop Companion.exe")
        if os.path.exists(exe_path):
            try:
                subprocess.Popen([exe_path], cwd=self.install_dir)
            except Exception:
                pass
        self.close()


def main():
    app = QApplication(sys.argv)
    window = InstallerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
