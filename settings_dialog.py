"""
Desktop Companion - Visual Settings GUI
Version 2.0 - Fluent Dark Studio Edition
"""

import os
import re
import shutil
import winsound
from datetime import datetime, time
from PyQt6.QtCore import Qt, pyqtSignal, QTime, QUrl
from PyQt6.QtWidgets import (
    QDialog, QWidget, QLabel, QLineEdit, QComboBox,
    QSpinBox, QCheckBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QTabWidget, QFrame, QFileDialog,
    QTimeEdit, QMessageBox, QProgressBar
)
from PyQt6.QtGui import (
    QIcon, QFont, QDesktopServices, QImageReader,
    QMovie, QPainter, QColor, QPixmap
)


def format_time_12h(hhmm_str):
    """Converts 24h 'HH:MM' string to friendly 12h string e.g. '10:00 PM' or '8:00 AM'"""
    try:
        sh, sm = map(int, hhmm_str.split(":"))
        t = time(sh, sm)
        am_pm = "AM" if t.hour < 12 else "PM"
        hour_12 = t.hour % 12
        if hour_12 == 0:
            hour_12 = 12
        return f"{hour_12}:{t.minute:02d} {am_pm}"
    except Exception:
        return hhmm_str


class ToggleSwitch(QCheckBox):
    """Modern iOS/Windows 11 style toggle switch matching the user's design"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 26)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText("")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        is_on = self.isChecked()
        # Vibrant neon cyan when active, sleek slate when inactive
        bg_color = QColor(2, 132, 199) if is_on else QColor(51, 65, 85)
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 1, 48, 24, 12, 12)

        # Crisp white knob
        painter.setBrush(Qt.GlobalColor.white)
        knob_x = 26 if is_on else 3
        painter.drawEllipse(knob_x, 3, 20, 20)
        painter.end()


class SettingsDialog(QDialog):
    settings_saved = pyqtSignal(dict)

    def __init__(self, config, base_dir, parent=None, initial_tab=0):
        super().__init__(parent)
        self.config = dict(config)
        # Ensure system date is synced
        today_str = datetime.now().strftime("%Y-%m-%d")
        if self.config.get("last_date") != today_str:
            self.config["cups_today"] = 0
            self.config["last_date"] = today_str

        self.base_dir = base_dir
        self.assets_dir = os.path.join(base_dir, "assets")
        self.custom_avatars_dir = os.path.join(self.assets_dir, "custom_avatars")
        os.makedirs(self.custom_avatars_dir, exist_ok=True)

        self.setWindowTitle("Desktop Companion Studio v2.0")
        self.setFixedSize(580, 620)

        ico_path = os.path.join(self.assets_dir, "tray_icon.ico")
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))

        self.setStyleSheet("""
            QDialog {
                background-color: #0b1120;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                color: #f8fafc;
            }
            QLabel {
                color: #e2e8f0;
                font-size: 13px;
            }
            QLineEdit, QComboBox, QSpinBox, QTimeEdit {
                background-color: #1e293b;
                border: 1.5px solid #334155;
                border-radius: 8px;
                padding: 7px 12px;
                font-size: 13px;
                color: #f8fafc;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTimeEdit:focus {
                border-color: #38bdf8;
                background-color: #0f172a;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e293b;
                color: #f8fafc;
                selection-background-color: #0284c7;
                border: 1px solid #334155;
                border-radius: 6px;
                outline: none;
            }
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.08);
                background-color: #0f172a;
                border-radius: 12px;
                top: -1px;
            }
            QTabBar::tab {
                background: #1e293b;
                color: #94a3b8;
                padding: 9px 18px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 600;
                font-size: 12px;
                margin-right: 4px;
                border: 1px solid transparent;
            }
            QTabBar::tab:hover {
                background: #273549;
                color: #f1f5f9;
            }
            QTabBar::tab:selected {
                background: #0f172a;
                color: #38bdf8;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-bottom: 2px solid #38bdf8;
            }
            QCheckBox {
                font-size: 13px;
                color: #e2e8f0;
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
            QPushButton.primary {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
                color: #080c15;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 700;
                padding: 9px 22px;
            }
            QPushButton.primary:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38bdf8, stop:1 #7dd3fc);
            }
            QPushButton.secondary {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 500;
                padding: 8px 16px;
            }
            QPushButton.secondary:hover {
                background-color: #334155;
                color: #ffffff;
                border-color: #475569;
            }
            QFrame.card {
                background-color: #111827;
                border: 1px solid #1f2937;
                border-radius: 12px;
                padding: 14px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        icon_badge = QLabel("💧")
        icon_badge.setFont(QFont("Segoe UI Emoji", 20))
        icon_badge.setStyleSheet("""
            background: rgba(2, 132, 199, 0.2);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 12px;
            padding: 4px 8px;
        """)

        v_title = QVBoxLayout()
        v_title.setSpacing(1)
        title_lbl = QLabel("Desktop Companion Studio")
        title_lbl.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #ffffff;")

        sub_lbl = QLabel("Personalize your desk buddy, hydration targets & schedules")
        sub_lbl.setFont(QFont("Segoe UI", 10))
        sub_lbl.setStyleSheet("color: #94a3b8;")
        v_title.addWidget(title_lbl)
        v_title.addWidget(sub_lbl)

        header.addWidget(icon_badge)
        header.addLayout(v_title)
        header.addStretch()

        ver_pill = QLabel("v2.0 PRO")
        ver_pill.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        ver_pill.setStyleSheet("""
            color: #38bdf8;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 6px;
            padding: 4px 10px;
        """)
        header.addWidget(ver_pill)
        layout.addLayout(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tab_general = self.create_general_tab()
        self.tab_wellness = self.create_wellness_tab()
        self.tab_schedule = self.create_schedule_tab()
        self.tab_avatars = self.create_avatars_tab()

        self.tabs.addTab(self.tab_general, "👤 General")
        self.tabs.addTab(self.tab_wellness, "💧 Wellness & Goals")
        self.tabs.addTab(self.tab_schedule, "⏰ Schedule")
        self.tabs.addTab(self.tab_avatars, "🎨 Avatars & Skins")
        if 0 <= initial_tab < self.tabs.count():
            self.tabs.setCurrentIndex(initial_tab)
        layout.addWidget(self.tabs)

        # Bottom Buttons
        btn_bar = QHBoxLayout()
        btn_bar.addStretch()

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setProperty("class", "secondary")
        self.btn_cancel.clicked.connect(self.reject)
        btn_bar.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("Save Settings")
        self.btn_save.setProperty("class", "primary")
        self.btn_save.clicked.connect(self.save)
        btn_bar.addWidget(self.btn_save)

        layout.addLayout(btn_bar)

    def create_general_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(18, 18, 18, 18)
        l.setSpacing(14)

        # Card 1: User Profile & Cadence
        card_profile = QFrame()
        card_profile.setProperty("class", "card")
        l_prof = QVBoxLayout(card_profile)
        l_prof.setSpacing(12)

        lbl_prof_sec = QLabel("User Profile & Reminders")
        lbl_prof_sec.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl_prof_sec.setStyleSheet("color: #38bdf8;")
        l_prof.addWidget(lbl_prof_sec)

        # Name
        h_name = QHBoxLayout()
        lbl_name = QLabel("Companion Callout:")
        lbl_name.setFixedWidth(140)
        self.txt_name = QLineEdit(self.config.get("user_name", "BS_CZR_i11"))
        self.txt_name.setPlaceholderText("Enter your name...")
        h_name.addWidget(lbl_name)
        h_name.addWidget(self.txt_name)
        l_prof.addLayout(h_name)

        # Interval
        h_int = QHBoxLayout()
        lbl_int = QLabel("Reminder Interval:")
        lbl_int.setFixedWidth(140)
        self.combo_interval = QComboBox()
        for m in [15, 20, 30, 45, 60, 90]:
            self.combo_interval.addItem(f"Every {m} minutes", m)
        curr_int = self.config.get("interval_minutes", 30)
        idx = self.combo_interval.findData(curr_int)
        if idx >= 0:
            self.combo_interval.setCurrentIndex(idx)
        h_int.addWidget(lbl_int)
        h_int.addWidget(self.combo_interval)
        l_prof.addLayout(h_int)

        # Snooze
        h_snz = QHBoxLayout()
        lbl_snz = QLabel("Snooze Duration:")
        lbl_snz.setFixedWidth(140)
        self.combo_snooze = QComboBox()
        for m in [5, 10, 15, 20, 30]:
            self.combo_snooze.addItem(f"{m} minutes", m)
        curr_snz = self.config.get("snooze_minutes", 15)
        idx = self.combo_snooze.findData(curr_snz)
        if idx >= 0:
            self.combo_snooze.setCurrentIndex(idx)
        h_snz.addWidget(lbl_snz)
        h_snz.addWidget(self.combo_snooze)
        l_prof.addLayout(h_snz)

        l.addWidget(card_profile)

        # Card 2: Audio & Dialogues
        card_audio = QFrame()
        card_audio.setProperty("class", "card")
        l_aud = QVBoxLayout(card_audio)
        l_aud.setSpacing(12)

        lbl_aud_sec = QLabel("Sound & Dialogues")
        lbl_aud_sec.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl_aud_sec.setStyleSheet("color: #38bdf8;")
        l_aud.addWidget(lbl_aud_sec)

        h_snd = QHBoxLayout()
        self.chk_sound = QCheckBox("Gentle water droplet chime sound effect")
        self.chk_sound.setChecked(self.config.get("sound_enabled", True))
        btn_test_snd = QPushButton("🔊 Test Chime")
        btn_test_snd.setProperty("class", "secondary")
        btn_test_snd.clicked.connect(self.test_sound)
        h_snd.addWidget(self.chk_sound)
        h_snd.addStretch()
        h_snd.addWidget(btn_test_snd)
        l_aud.addLayout(h_snd)

        self.chk_dialogue = QCheckBox("Show witty, motivational speech bubble lines")
        self.chk_dialogue.setChecked(self.config.get("witty_dialogue", True))
        l_aud.addWidget(self.chk_dialogue)

        l.addWidget(card_audio)
        l.addStretch()
        return w

    def create_wellness_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(18, 18, 18, 18)
        l.setSpacing(14)

        # 1. Card: Daily Hydration Target & Live Progress Bar
        card_goal = QFrame()
        card_goal.setProperty("class", "card")
        l_goal = QVBoxLayout(card_goal)
        l_goal.setSpacing(10)

        h_goal = QHBoxLayout()
        lbl_goal = QLabel("Daily Water Goal:")
        lbl_goal.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl_goal.setFixedWidth(130)
        self.spin_goal = QSpinBox()
        self.spin_goal.setRange(1, 20)
        self.spin_goal.setValue(self.config.get("daily_goal_cups", 8))
        self.spin_goal.setSuffix(" cups (glasses)")
        self.spin_goal.valueChanged.connect(self.update_wellness_progress)
        h_goal.addWidget(lbl_goal)
        h_goal.addWidget(self.spin_goal)
        l_goal.addLayout(h_goal)

        # Progress bar
        self.prog_bar = QProgressBar()
        self.prog_bar.setRange(0, 100)
        self.prog_bar.setTextVisible(True)
        self.prog_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                height: 18px;
                text-align: center;
                color: #ffffff;
                font-size: 11px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
                border-radius: 7px;
            }
        """)
        l_goal.addWidget(self.prog_bar)

        h_prog = QHBoxLayout()
        self.lbl_progress = QLabel()
        self.lbl_progress.setFont(QFont("Segoe UI", 11))
        btn_reset = QPushButton("Reset Today's Count")
        btn_reset.setProperty("class", "secondary")
        btn_reset.clicked.connect(self.reset_cups)
        h_prog.addWidget(self.lbl_progress)
        h_prog.addStretch()
        h_prog.addWidget(btn_reset)
        l_goal.addLayout(h_prog)

        l.addWidget(card_goal)

        # 2. Card: Break Variety Options
        card_breaks = QFrame()
        card_breaks.setProperty("class", "card")
        l_breaks = QVBoxLayout(card_breaks)
        l_breaks.setSpacing(10)

        lbl_types = QLabel("Enabled Wellness & Break Reminders:")
        lbl_types.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl_types.setStyleSheet("color: #38bdf8;")
        l_breaks.addWidget(lbl_types)

        break_types = self.config.get("break_types", ["water", "eye_rest", "stretch"])
        self.chk_water = QCheckBox("💧 Hydration (Drink Water reminders)")
        self.chk_water.setChecked("water" in break_types)
        l_breaks.addWidget(self.chk_water)

        self.chk_eyes = QCheckBox("👀 20-20-20 Eye Rest (Relieve screen fatigue)")
        self.chk_eyes.setChecked("eye_rest" in break_types)
        l_breaks.addWidget(self.chk_eyes)

        self.chk_stretch = QCheckBox("🧘 Posture & Quick Stretch (Shoulder & neck roll)")
        self.chk_stretch.setChecked("stretch" in break_types)
        l_breaks.addWidget(self.chk_stretch)

        l.addWidget(card_breaks)
        l.addStretch()

        self.update_wellness_progress()
        return w

    def update_wellness_progress(self):
        cups = self.config.get("cups_today", 0)
        goal = max(1, self.spin_goal.value())
        pct = min(100, int((cups / goal) * 100))
        self.prog_bar.setValue(pct)
        if cups >= goal:
            self.lbl_progress.setText(f"Today: <b>{cups}</b> / {goal} cups 🌟 <span style='color:#38bdf8; font-weight:bold;'>Goal Achieved!</span>")
        else:
            self.lbl_progress.setText(f"Today: <b>{cups}</b> / {goal} cups ({pct}%)")

    def create_schedule_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(18, 18, 18, 18)
        l.setSpacing(14)

        # 1. Card: Working Hours Schedule
        card_work = QFrame()
        card_work.setProperty("class", "card")
        l_work = QVBoxLayout(card_work)
        l_work.setSpacing(10)

        sched = self.config.get("schedule", {})
        self.chk_sched_enabled = QCheckBox("Enable working hours schedule")
        self.chk_sched_enabled.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.chk_sched_enabled.setStyleSheet("color: #38bdf8;")
        self.chk_sched_enabled.setChecked(sched.get("enabled", True))
        l_work.addWidget(self.chk_sched_enabled)

        # Days
        lbl_days = QLabel("Active Days:")
        lbl_days.setStyleSheet("color: #94a3b8; font-weight: 600;")
        l_work.addWidget(lbl_days)

        active_days = sched.get("days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.day_checkboxes = {}
        h_days1 = QHBoxLayout()
        h_days2 = QHBoxLayout()

        days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, d in enumerate(days_list):
            cb = QCheckBox(d[:3])
            cb.setChecked(d in active_days)
            self.day_checkboxes[d] = cb
            if i < 4:
                h_days1.addWidget(cb)
            else:
                h_days2.addWidget(cb)
        h_days1.addStretch()
        h_days2.addStretch()
        l_work.addLayout(h_days1)
        l_work.addLayout(h_days2)

        # Time range
        lbl_time = QLabel("Working Hours:")
        lbl_time.setStyleSheet("color: #94a3b8; font-weight: 600;")
        l_work.addWidget(lbl_time)

        h_time = QHBoxLayout()
        start_str = sched.get("start_time", "09:00")
        end_str = sched.get("end_time", "18:30")

        self.time_start = QTimeEdit()
        self.time_start.setDisplayFormat("HH:mm")
        sh, sm = map(int, start_str.split(":"))
        self.time_start.setTime(QTime(sh, sm))

        self.time_end = QTimeEdit()
        self.time_end.setDisplayFormat("HH:mm")
        eh, em = map(int, end_str.split(":"))
        self.time_end.setTime(QTime(eh, em))

        h_time.addWidget(QLabel("From:"))
        h_time.addWidget(self.time_start)
        h_time.addSpacing(10)
        h_time.addWidget(QLabel("To:"))
        h_time.addWidget(self.time_end)
        h_time.addStretch()
        l_work.addLayout(h_time)

        l.addWidget(card_work)

        # 2. Card: Quiet Hours
        card_quiet = QFrame()
        card_quiet.setProperty("class", "card")
        l_quiet = QVBoxLayout(card_quiet)
        l_quiet.setSpacing(10)

        h_qh_header = QHBoxLayout()
        v_qh_text = QVBoxLayout()
        v_qh_text.setSpacing(2)

        lbl_qh_title = QLabel("Quiet hours")
        lbl_qh_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lbl_qh_title.setStyleSheet("color: #ffffff;")

        self.lbl_quiet_subtitle = QLabel("10:00 PM — 8:00 AM")
        self.lbl_quiet_subtitle.setStyleSheet("color: #94a3b8; font-size: 12px;")

        v_qh_text.addWidget(lbl_qh_title)
        v_qh_text.addWidget(self.lbl_quiet_subtitle)

        h_qh_header.addLayout(v_qh_text)
        h_qh_header.addStretch()

        qh_data = self.config.get("quiet_hours", {})
        self.toggle_quiet = ToggleSwitch()
        self.toggle_quiet.setChecked(qh_data.get("enabled", True))
        h_qh_header.addWidget(self.toggle_quiet)

        l_quiet.addLayout(h_qh_header)

        # Divider line
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("color: #1e293b; background-color: #1e293b; height: 1px;")
        l_quiet.addWidget(div)

        # Quiet Hours Time Pickers
        h_qh_times = QHBoxLayout()
        qh_s = qh_data.get("start_time", "22:00")
        qh_e = qh_data.get("end_time", "08:00")

        self.time_quiet_start = QTimeEdit()
        self.time_quiet_start.setDisplayFormat("HH:mm")
        qsh, qsm = map(int, qh_s.split(":"))
        self.time_quiet_start.setTime(QTime(qsh, qsm))

        self.time_quiet_end = QTimeEdit()
        self.time_quiet_end.setDisplayFormat("HH:mm")
        qeh, qem = map(int, qh_e.split(":"))
        self.time_quiet_end.setTime(QTime(qeh, qem))

        h_qh_times.addWidget(QLabel("From:"))
        h_qh_times.addWidget(self.time_quiet_start)
        h_qh_times.addSpacing(10)
        h_qh_times.addWidget(QLabel("To:"))
        h_qh_times.addWidget(self.time_quiet_end)
        h_qh_times.addStretch()
        l_quiet.addLayout(h_qh_times)

        lbl_qh_hint = QLabel("🌙 Silences all companion popups, reminders & sounds during these hours.")
        lbl_qh_hint.setStyleSheet("color: #64748b; font-size: 11px;")
        l_quiet.addWidget(lbl_qh_hint)

        self.toggle_quiet.toggled.connect(self.update_quiet_ui_state)
        self.time_quiet_start.timeChanged.connect(self.update_quiet_subtitle)
        self.time_quiet_end.timeChanged.connect(self.update_quiet_subtitle)
        self.update_quiet_ui_state(self.toggle_quiet.isChecked())

        l.addWidget(card_quiet)
        l.addStretch()
        return w

    def update_quiet_ui_state(self, checked):
        self.time_quiet_start.setEnabled(checked)
        self.time_quiet_end.setEnabled(checked)
        self.update_quiet_subtitle()

    def update_quiet_subtitle(self):
        if self.toggle_quiet.isChecked():
            s_str = self.time_quiet_start.time().toString("HH:mm")
            e_str = self.time_quiet_end.time().toString("HH:mm")
            s_12h = format_time_12h(s_str)
            e_12h = format_time_12h(e_str)
            self.lbl_quiet_subtitle.setText(f"{s_12h} — {e_12h}")
            self.lbl_quiet_subtitle.setStyleSheet("color: #38bdf8; font-size: 12px; font-weight: 600;")
        else:
            self.lbl_quiet_subtitle.setText("Disabled (Off)")
            self.lbl_quiet_subtitle.setStyleSheet("color: #64748b; font-size: 12px; font-style: italic;")

    def create_avatars_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(18, 18, 18, 18)
        l.setSpacing(14)

        # 1. Preview Card
        card_prev = QFrame()
        card_prev.setProperty("class", "card")
        card_prev.setStyleSheet("""
            QFrame.card {
                background-color: #0b1120;
                border: 1.5px solid #1e293b;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        l_prev = QVBoxLayout(card_prev)
        l_prev.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_avatar_preview = QLabel()
        self.lbl_avatar_preview.setFixedSize(140, 110)
        self.lbl_avatar_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_avatar_preview.setStyleSheet("""
            background: #0f172a;
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 16px;
        """)
        l_prev.addWidget(self.lbl_avatar_preview, alignment=Qt.AlignmentFlag.AlignCenter)

        self.lbl_preview_title = QLabel("Select or Customize Your Desktop Buddy")
        self.lbl_preview_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.lbl_preview_title.setStyleSheet("color: #38bdf8; margin-top: 4px;")
        l_prev.addWidget(self.lbl_preview_title, alignment=Qt.AlignmentFlag.AlignCenter)
        l.addWidget(card_prev)

        # 2. Selector Card
        card_sel = QFrame()
        card_sel.setProperty("class", "card")
        l_sel = QVBoxLayout(card_sel)
        l_sel.setSpacing(10)

        lbl_skin = QLabel("Active Companion Skin:")
        lbl_skin.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl_skin.setStyleSheet("color: #f8fafc;")
        l_sel.addWidget(lbl_skin)

        self.combo_skin = QComboBox()
        self.refresh_avatar_list()
        self.combo_skin.currentIndexChanged.connect(self.update_avatar_preview)
        l_sel.addWidget(self.combo_skin)

        h_btns = QHBoxLayout()
        btn_import = QPushButton("📥 Import Custom Avatar (.gif)...")
        btn_import.setProperty("class", "secondary")
        btn_import.clicked.connect(self.import_avatar)
        h_btns.addWidget(btn_import)

        btn_folder = QPushButton("📁 Open Avatars Folder")
        btn_folder.setProperty("class", "secondary")
        btn_folder.clicked.connect(self.open_avatars_folder)
        h_btns.addWidget(btn_folder)
        l_sel.addLayout(h_btns)

        l.addWidget(card_sel)

        info_box = QLabel(
            "<b>💡 Custom Avatars:</b> Drop any animated <b>.gif</b> or <b>.png</b> file into "
            "the <i>custom_avatars</i> folder. Desktop Companion automatically loads and walks with it on your screen!"
        )
        info_box.setWordWrap(True)
        info_box.setTextFormat(Qt.TextFormat.RichText)
        info_box.setStyleSheet("background-color: #111827; border: 1px solid #1f2937; padding: 10px; border-radius: 8px; color: #94a3b8; font-size: 11px;")
        l.addWidget(info_box)

        l.addStretch()
        self.update_avatar_preview()
        return w

    def update_avatar_preview(self):
        skin_data = self.combo_skin.currentData()
        if not skin_data or skin_data == "dynamic":
            self.lbl_preview_title.setText("✨ Dynamic Auto-Cycling (Random every reminder)")
            walk_path = os.path.join(self.assets_dir, "walk.gif")
            if os.path.exists(walk_path):
                mv = QMovie(walk_path)
                self.lbl_avatar_preview.setMovie(mv)
                mv.start()
            else:
                self.lbl_avatar_preview.setText("✨\nDynamic")
            return

        self.lbl_preview_title.setText(f"Active Skin: {self.combo_skin.currentText()}")
        if skin_data.startswith("custom:"):
            fname = skin_data.split("custom:", 1)[1]
            cpath = os.path.join(self.custom_avatars_dir, fname)
            if os.path.exists(cpath):
                if cpath.lower().endswith(".gif"):
                    mv = QMovie(cpath)
                    self.lbl_avatar_preview.setMovie(mv)
                    mv.start()
                else:
                    pm = QPixmap(cpath)
                    self.lbl_avatar_preview.setPixmap(pm.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                return

        walk_path = os.path.join(self.assets_dir, "walk.gif")
        if os.path.exists(walk_path):
            mv = QMovie(walk_path)
            self.lbl_avatar_preview.setMovie(mv)
            mv.start()
        else:
            self.lbl_avatar_preview.setText(self.combo_skin.currentText())

    def refresh_avatar_list(self):
        self.combo_skin.clear()
        self.combo_skin.addItem("✨ Dynamic (Auto-Cycle every interval)", "dynamic")

        preset_skins = [
            ("pixel_guy", "Pixel Guy 🧢"),
            ("pixel_cat", "Cute Kitty 🐱"),
            ("pixel_robot", "Robo Buddy 🤖"),
            ("pixel_slime", "Water Slime 💧"),
            ("pixel_frog", "Forest Frog 🐸"),
            ("pixel_ghost", "Spooky Ghost 👻"),
            ("pixel_puppy", "Playful Puppy 🐶"),
            ("pixel_duck", "Rubber Duck 🦆"),
            ("pixel_dino", "Mini Dino 🦖"),
            ("pixel_bear", "Honey Bear 🐻")
        ]
        for key, name in preset_skins:
            self.combo_skin.addItem(name, key)

        if os.path.exists(self.custom_avatars_dir):
            for f in os.listdir(self.custom_avatars_dir):
                if f.lower().endswith((".gif", ".png")):
                    self.combo_skin.addItem(f"Custom: {f}", f"custom:{f}")

        # Select current
        if self.config.get("dynamic_avatar", True):
            self.combo_skin.setCurrentIndex(0)
        else:
            curr = self.config.get("skin", "pixel_guy")
            idx = self.combo_skin.findData(curr)
            if idx >= 0:
                self.combo_skin.setCurrentIndex(idx)

    def import_avatar(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Avatar GIF or Image", "", "Animated GIFs & Images (*.gif *.png)"
        )
        if not file_path:
            return

        # Security Check 1: Extension whitelist
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in [".gif", ".png"]:
            QMessageBox.warning(self, "Unsupported Format", "Security Notice: Only verified .gif and .png images are permitted.")
            return

        # Security Check 2: File size limit (15 MB) to prevent memory exhaustion / DoS
        try:
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if size_mb > 15:
                QMessageBox.warning(self, "File Too Large", f"The selected avatar is {size_mb:.1f} MB.\nPlease select an image under 15 MB.")
                return
        except Exception:
            return

        # Security Check 3: Image integrity validation (ensure not a renamed malicious binary)
        reader = QImageReader(file_path)
        if not reader.canRead():
            QMessageBox.critical(self, "Invalid Image", "Security Verification Failed: The selected file could not be parsed as a valid image.")
            return

        # Security Check 4: Sanitize destination filename against path traversal
        raw_name = os.path.basename(file_path)
        clean_name = re.sub(r"[^\w\-\.]", "_", raw_name)
        if not clean_name.lower().endswith((".gif", ".png")):
            clean_name += ext

        dest_path = os.path.join(self.custom_avatars_dir, clean_name)
        try:
            shutil.copy2(file_path, dest_path)
            self.refresh_avatar_list()
            idx = self.combo_skin.findData(f"custom:{clean_name}")
            if idx >= 0:
                self.combo_skin.setCurrentIndex(idx)
            QMessageBox.information(self, "Avatar Imported", f"'{clean_name}' was securely verified and imported!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not import file: {e}")

    def open_avatars_folder(self):
        try:
            os.startfile(self.custom_avatars_dir)
        except Exception:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.custom_avatars_dir))

    def test_sound(self):
        drip_wav = os.path.join(self.assets_dir, "drip.wav")
        if os.path.exists(drip_wav):
            winsound.PlaySound(drip_wav, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def reset_cups(self):
        self.config["cups_today"] = 0
        self.config["last_date"] = datetime.now().strftime("%Y-%m-%d")
        self.update_wellness_progress()

    def save(self):
        # Gather & Sanitize changes
        raw_name = str(self.txt_name.text()).strip()
        cleaned_name = re.sub(r"[^\w\s\-\.]", "", raw_name, flags=re.UNICODE)
        cleaned_name = " ".join(cleaned_name.split())
        self.config["user_name"] = cleaned_name[:30] if cleaned_name else "Friend"
        self.config["interval_minutes"] = max(1, min(360, int(self.combo_interval.currentData() or 30)))
        self.config["snooze_minutes"] = max(1, min(120, int(self.combo_snooze.currentData() or 15)))
        self.config["sound_enabled"] = bool(self.chk_sound.isChecked())
        self.config["witty_dialogue"] = bool(self.chk_dialogue.isChecked())
        self.config["daily_goal_cups"] = max(1, min(30, int(self.spin_goal.value())))

        # Breaks
        breaks = []
        if self.chk_water.isChecked():
            breaks.append("water")
        if self.chk_eyes.isChecked():
            breaks.append("eye_rest")
        if self.chk_stretch.isChecked():
            breaks.append("stretch")
        if not breaks:
            breaks = ["water"]  # at least water
        self.config["break_types"] = breaks

        # Schedule
        active_days = [d for d, cb in self.day_checkboxes.items() if cb.isChecked()]
        self.config["schedule"] = {
            "enabled": self.chk_sched_enabled.isChecked(),
            "days": active_days,
            "start_time": self.time_start.time().toString("HH:mm"),
            "end_time": self.time_end.time().toString("HH:mm")
        }

        # Quiet Hours
        self.config["quiet_hours"] = {
            "enabled": bool(self.toggle_quiet.isChecked()),
            "start_time": self.time_quiet_start.time().toString("HH:mm"),
            "end_time": self.time_quiet_end.time().toString("HH:mm")
        }

        # Skin
        selected_skin = self.combo_skin.currentData()
        if selected_skin == "dynamic":
            self.config["dynamic_avatar"] = True
        else:
            self.config["dynamic_avatar"] = False
            self.config["skin"] = selected_skin

        self.settings_saved.emit(self.config)
        self.accept()
