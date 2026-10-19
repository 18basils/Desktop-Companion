"""
Desktop Companion - Uninstaller
Version 2.0
"""

import sys
import os
import subprocess
import shutil
import winreg
import tempfile

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox, QProgressBar,
    QFrame, QMessageBox
)
from PyQt6.QtGui import QIcon, QFont


REG_UNINSTALL_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\DesktopCompanion"


def kill_running_process():
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", "Desktop Companion.exe"],
            capture_output=True,
            creationflags=0x08000000
        )
    except Exception:
        pass


def remove_shortcuts():
    home = os.path.expanduser("~")
    appdata = os.environ.get("APPDATA") or os.path.join(home, "AppData", "Roaming")

    desktop_lnk = os.path.join(home, "Desktop", "Desktop Companion.lnk")
    start_lnk = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Desktop Companion.lnk")
    startup_lnk = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "Desktop Companion.lnk")

    for lnk in [desktop_lnk, start_lnk, startup_lnk]:
        if os.path.exists(lnk):
            try:
                os.remove(lnk)
            except Exception:
                pass


def remove_registry_entry():
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, REG_UNINSTALL_KEY)
    except Exception:
        pass


def perform_uninstall(install_dir, keep_avatars_and_settings=False):
    kill_running_process()
    remove_shortcuts()
    remove_registry_entry()

    if keep_avatars_and_settings:
        # Preserve assets/custom_avatars and config.json in a backup or keep directory
        try:
            for item in os.listdir(install_dir):
                item_path = os.path.join(install_dir, item)
                if item == "config.json":
                    continue
                if item == "assets":
                    # Keep custom_avatars
                    for sub in os.listdir(item_path):
                        if sub != "custom_avatars":
                            sub_path = os.path.join(item_path, sub)
                            if os.path.isdir(sub_path):
                                shutil.rmtree(sub_path, ignore_errors=True)
                            else:
                                os.remove(sub_path)
                    continue
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                else:
                    os.remove(item_path)
        except Exception:
            pass
    else:
        # Full purge of install dir
        try:
            shutil.rmtree(install_dir, ignore_errors=True)
        except Exception:
            pass
        # Scheduled fallback in case of briefly locked file
        bat_cmd = f'ping 127.0.0.1 -n 3 > nul & rd /s /q "{install_dir}"'
        try:
            subprocess.Popen(
                ["cmd.exe", "/c", bat_cmd],
                creationflags=0x08000000
            )
        except Exception:
            pass


class UninstallWorker(QThread):
    progress = pyqtSignal(int, str)
    done = pyqtSignal(bool, str)

    def __init__(self, install_dir, keep_data):
        super().__init__()
        self.install_dir = install_dir
        self.keep_data = keep_data

    def run(self):
        try:
            self.progress.emit(20, "Stopping running Desktop Companion service...")
            kill_running_process()

            self.progress.emit(45, "Removing Windows shortcuts...")
            remove_shortcuts()

            self.progress.emit(70, "Unregistering from Windows Installed Apps...")
            remove_registry_entry()

            self.progress.emit(90, "Cleaning application files...")
            perform_uninstall(self.install_dir, self.keep_data)

            self.progress.emit(100, "Uninstallation completed successfully!")
            self.done.emit(True, "Success")
        except Exception as e:
            self.done.emit(False, str(e))


class UninstallerWindow(QWidget):
    def __init__(self, install_dir):
        super().__init__()
        self.install_dir = install_dir
        self.setWindowTitle("Uninstall Desktop Companion v2.0")
        self.setFixedSize(520, 360)

        ico_path = os.path.join(install_dir, "assets", "tray_icon.ico")
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))

        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                font-family: 'Segoe UI', system-ui, sans-serif;
                color: #0f172a;
            }
            QFrame.card {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 16px;
            }
            QPushButton.danger {
                background-color: #e11d48;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
                padding: 10px 22px;
            }
            QPushButton.danger:hover {
                background-color: #be123c;
            }
            QPushButton.secondary {
                background-color: #e2e8f0;
                color: #334155;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                padding: 10px 18px;
            }
            QPushButton.secondary:hover {
                background-color: #cbd5e1;
            }
            QProgressBar {
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background-color: #e2e8f0;
                text-align: center;
                height: 16px;
                font-size: 11px;
                font-weight: 600;
            }
            QProgressBar::chunk {
                background-color: #e11d48;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        # Header
        header = QHBoxLayout()
        icon_lbl = QLabel("🗑️")
        icon_lbl.setFont(QFont("Segoe UI Emoji", 24))
        title_lbl = QLabel("Uninstall Desktop Companion")
        title_lbl.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #e11d48;")
        header.addWidget(icon_lbl)
        header.addWidget(title_lbl)
        header.addStretch()
        layout.addLayout(header)

        # Card
        card = QFrame()
        card.setProperty("class", "card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)

        self.lbl_msg = QLabel("Are you sure you want to completely remove <b>Desktop Companion v1.2</b> from your computer?")
        self.lbl_msg.setWordWrap(True)
        self.lbl_msg.setTextFormat(Qt.TextFormat.RichText)
        card_layout.addWidget(self.lbl_msg)

        lbl_loc = QLabel(f"Location: <i>{self.install_dir}</i>")
        lbl_loc.setStyleSheet("color: #64748b; font-size: 11px;")
        lbl_loc.setWordWrap(True)
        card_layout.addWidget(lbl_loc)

        self.chk_keep = QCheckBox("Keep my custom avatars and personalized settings")
        self.chk_keep.setChecked(False)
        card_layout.addWidget(self.chk_keep)

        layout.addWidget(card)

        # Progress elements
        self.prog_lbl = QLabel("Ready to remove.")
        self.prog_lbl.setStyleSheet("color: #64748b; font-size: 12px;")
        self.prog_lbl.hide()
        layout.addWidget(self.prog_lbl)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Action Buttons
        self.btn_bar = QHBoxLayout()
        self.btn_bar.addStretch()

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setProperty("class", "secondary")
        self.btn_cancel.clicked.connect(self.close)
        self.btn_bar.addWidget(self.btn_cancel)

        self.btn_uninstall = QPushButton("Uninstall Desktop Companion")
        self.btn_uninstall.setProperty("class", "danger")
        self.btn_uninstall.clicked.connect(self.start_uninstall)
        self.btn_bar.addWidget(self.btn_uninstall)

        layout.addLayout(self.btn_bar)

    def start_uninstall(self):
        self.btn_uninstall.setEnabled(False)
        self.btn_cancel.setEnabled(False)
        self.chk_keep.setEnabled(False)
        self.prog_lbl.show()
        self.progress_bar.show()

        self.worker = UninstallWorker(self.install_dir, self.chk_keep.isChecked())
        self.worker.progress.connect(self.on_progress)
        self.worker.done.connect(self.on_done)
        self.worker.start()

    def on_progress(self, val, msg):
        self.progress_bar.setValue(val)
        self.prog_lbl.setText(msg)

    def on_done(self, success, msg):
        if success:
            QMessageBox.information(
                self,
                "Uninstalled",
                "Desktop Companion has been successfully removed from your computer."
            )
            self.close()
        else:
            QMessageBox.critical(self, "Error", f"Uninstallation encountered an issue: {msg}")
            self.btn_cancel.setEnabled(True)


def main():
    # If running frozen
    if getattr(sys, "frozen", False):
        install_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        install_dir = os.path.dirname(os.path.abspath(__file__))

    # Check if custom install-dir argument was passed
    if "--install-dir" in sys.argv:
        try:
            idx = sys.argv.index("--install-dir")
            if idx + 1 < len(sys.argv):
                install_dir = sys.argv[idx + 1]
        except Exception:
            pass

    # If running frozen and not already in temp worker mode, copy to temp and run there
    if getattr(sys, "frozen", False) and "--temp-worker" not in sys.argv:
        try:
            temp_dir = os.path.join(tempfile.gettempdir(), "DC_Uninstaller")
            os.makedirs(temp_dir, exist_ok=True)
            temp_exe = os.path.join(temp_dir, "Uninstall Desktop Companion.exe")
            shutil.copy2(sys.executable, temp_exe)
            cmd = [temp_exe, "--temp-worker", "--install-dir", install_dir] + sys.argv[1:]
            subprocess.Popen(cmd)
            sys.exit(0)
        except Exception:
            pass

    # Silent uninstall flag check
    if "--quiet" in sys.argv or "/S" in sys.argv:
        perform_uninstall(install_dir, keep_avatars_and_settings=False)
        sys.exit(0)

    app = QApplication(sys.argv)
    window = UninstallerWindow(install_dir)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
