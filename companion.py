"""
Desktop Companion - Interactive Water Reminder Desktop Pet
Version: 2.0.0
"""

import sys
import os
import re
import ctypes
import json
import random
import winsound
import traceback
from datetime import datetime, time, timedelta

# 1. Set explicit AppUserModelID for Windows 10/11 taskbar / tray integration
try:
    myappid = "bs_czr_i11.desktopcompanion.hydration.20"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# 2. Immediately hide any console window if one was opened on Windows
try:
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0
except Exception:
    pass

# 3. Determine BASE_DIR (handles normal execution & PyInstaller frozen bundle)
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(BASE_DIR, "app.log")
try:
    log_fp = open(LOG_FILE, "a", encoding="utf-8", buffering=1)
    sys.stdout = log_fp
    sys.stderr = log_fp
except Exception:
    pass

venv_site = os.path.join(BASE_DIR, ".venv", "Lib", "site-packages")
if os.path.exists(venv_site) and venv_site not in sys.path:
    sys.path.insert(0, venv_site)

def log_crash(exctype, value, tb):
    try:
        with open(os.path.join(BASE_DIR, "crash.log"), "a", encoding="utf-8") as f:
            f.write(f"\n--- CRASH {datetime.now()} ---\n")
            traceback.print_exception(exctype, value, tb, file=f)
    except Exception:
        pass
    sys.__excepthook__(exctype, value, tb)
sys.excepthook = log_crash

from PyQt6.QtCore import Qt, QTimer, QRectF, QUrl, QPointF
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout,
    QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush,
    QPainterPath, QIcon, QPixmap, QMovie,
    QDesktopServices, QTransform, QPolygonF
)

from settings_dialog import SettingsDialog

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CUSTOM_AVATARS_DIR = os.path.join(ASSETS_DIR, "custom_avatars")
DRIP_WAV = os.path.join(ASSETS_DIR, "drip.wav")

AVAILABLE_SKINS = [
    "pixel_guy",
    "pixel_cat",
    "pixel_robot",
    "pixel_slime",
    "pixel_frog",
    "pixel_ghost",
    "pixel_puppy",
    "pixel_duck",
    "pixel_dino",
    "pixel_bear"
]

WITTY_WATER_QUOTES = [
    "Hydrate or Diedrate, {name}! 💧",
    "Brain is 75% water. Feed the machine, {name}! 🧠💦",
    "Stuck on a bug? Drink a glass of water and look again! 🐛➡️💧",
    "Your house plants are watered... what about you, {name}? 🌿",
    "1 glass of water = +10 Focus points! ⚡",
    "Keep calm and drink water, {name}! 🌊",
    "Time for high-quality H2O, {name}! 💧",
    "Water break! Your body will thank you. 💧",
    "Stay sharp and hydrated, {name}! 🥤",
    "Water loading: 99%... Have a sip! 💧"
]


def get_available_skins():
    skins = list(AVAILABLE_SKINS)
    if os.path.exists(CUSTOM_AVATARS_DIR):
        try:
            for f in os.listdir(CUSTOM_AVATARS_DIR):
                if f.lower().endswith((".gif", ".png")):
                    skins.append(f"custom:{f}")
        except Exception:
            pass
    return skins


def validate_config(cfg, default_config):
    """Security & integrity check: ensures all configuration values are safe, correctly typed, and within bounds"""
    validated = dict(default_config)
    try:
        # 1. user_name: string, max 30 chars, sanitized against injection
        name = str(cfg.get("user_name", default_config["user_name"])).strip()
        name = re.sub(r"[^\w\s\-\.]", "", name, flags=re.UNICODE)
        name = " ".join(name.split())
        validated["user_name"] = name[:30] if name else "Friend"

        # 2. interval_minutes: integer 1..360
        validated["interval_minutes"] = max(1, min(360, int(cfg.get("interval_minutes", 30))))

        # 3. snooze_minutes: integer 1..120
        validated["snooze_minutes"] = max(1, min(120, int(cfg.get("snooze_minutes", 15))))

        # 4. walk_speed: integer 1..15
        validated["walk_speed"] = max(1, min(15, int(cfg.get("walk_speed", 4))))

        # 5. daily_goal_cups: integer 1..30
        validated["daily_goal_cups"] = max(1, min(30, int(cfg.get("daily_goal_cups", 8))))

        # 6. cups_today: integer >= 0
        validated["cups_today"] = max(0, int(cfg.get("cups_today", 0)))

        # 7. booleans
        for b_key in ["dynamic_avatar", "sound_enabled", "witty_dialogue"]:
            validated[b_key] = bool(cfg.get(b_key, True))

        # 8. skin
        skin = str(cfg.get("skin", "pixel_guy"))
        if skin in AVAILABLE_SKINS or skin.startswith("custom:"):
            validated["skin"] = skin
        else:
            validated["skin"] = "pixel_guy"

        # 9. break_types
        b_types = cfg.get("break_types", ["water", "eye_rest", "stretch"])
        if isinstance(b_types, list):
            valid_breaks = [b for b in b_types if b in ("water", "eye_rest", "stretch")]
            validated["break_types"] = valid_breaks if valid_breaks else ["water"]

        # 10. schedule
        sched = cfg.get("schedule", {})
        if isinstance(sched, dict):
            validated["schedule"] = {
                "enabled": bool(sched.get("enabled", True)),
                "days": [d for d in sched.get("days", []) if d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]],
                "start_time": str(sched.get("start_time", "09:00")),
                "end_time": str(sched.get("end_time", "18:30"))
            }

        # 11. quiet_hours (silences companion completely e.g. 10:00 PM - 8:00 AM)
        qh = cfg.get("quiet_hours", {})
        if isinstance(qh, dict):
            validated["quiet_hours"] = {
                "enabled": bool(qh.get("enabled", True)),
                "start_time": str(qh.get("start_time", "22:00")),
                "end_time": str(qh.get("end_time", "08:00"))
            }
        else:
            validated["quiet_hours"] = {
                "enabled": True,
                "start_time": "22:00",
                "end_time": "08:00"
            }

        validated["last_date"] = str(cfg.get("last_date", default_config["last_date"]))
    except Exception:
        return default_config
    return validated


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


def load_config():
    today_str = datetime.now().strftime("%Y-%m-%d")
    default_config = {
        "version": "2.0.0",
        "user_name": "BS_CZR_i11",
        "interval_minutes": 30,
        "snooze_minutes": 15,
        "walk_speed": 4,
        "screen_side": "left",
        "dynamic_avatar": True,
        "skin": "pixel_guy",
        "daily_goal_cups": 8,
        "cups_today": 0,
        "last_date": today_str,
        "break_types": ["water", "eye_rest", "stretch"],
        "witty_dialogue": True,
        "schedule": {
            "enabled": True,
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "start_time": "09:00",
            "end_time": "18:30"
        },
        "quiet_hours": {
            "enabled": True,
            "start_time": "22:00",
            "end_time": "08:00"
        },
        "sound_enabled": True
    }
    cfg = dict(default_config)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    cfg = validate_config(loaded, default_config)
        except Exception:
            cfg = default_config
    else:
        cfg = default_config

    # Reset daily cups if day has changed
    if cfg.get("last_date") != today_str:
        cfg["cups_today"] = 0
        cfg["last_date"] = today_str
        save_config(cfg)
    return cfg


def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
    except Exception:
        pass


def is_in_quiet_hours(cfg):
    """Returns True if quiet hours are enabled and current system time falls within the window"""
    qh = cfg.get("quiet_hours", {})
    if not qh.get("enabled", True):
        return False

    now = datetime.now()
    start_str = qh.get("start_time", "22:00")
    end_str = qh.get("end_time", "08:00")
    try:
        sh, sm = map(int, start_str.split(":"))
        eh, em = map(int, end_str.split(":"))
        start_t = time(sh, sm)
        end_t = time(eh, em)
        if start_t <= end_t:
            return start_t <= now.time() <= end_t
        else:
            # Overnights spanning midnight e.g. 22:00 to 08:00
            return now.time() >= start_t or now.time() <= end_t
    except Exception:
        return False


def is_within_schedule(cfg):
    """
    Logically checks if the companion should run:
    1. If currently in Quiet Hours (e.g. 10:00 PM - 8:00 AM), companion is silenced completely.
    2. If working schedule is enabled, verifies active day and time window (supporting overnight spans).
    """
    # 1. Quiet hours override: never disturb during quiet hours
    if is_in_quiet_hours(cfg):
        return False

    # 2. Working hours schedule check
    sched = cfg.get("schedule", {})
    if not sched.get("enabled", True):
        return True

    now = datetime.now()
    days_map = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    current_day = days_map[now.weekday()]
    allowed_days = sched.get("days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    if current_day not in allowed_days:
        return False

    start_str = sched.get("start_time", "09:00")
    end_str = sched.get("end_time", "18:30")
    try:
        sh, sm = map(int, start_str.split(":"))
        eh, em = map(int, end_str.split(":"))
        start_t = time(sh, sm)
        end_t = time(eh, em)
        if start_t <= end_t:
            return start_t <= now.time() <= end_t
        else:
            # Overnight schedule span
            return now.time() >= start_t or now.time() <= end_t
    except Exception:
        return True


class AvatarWidget(QWidget):
    """
    Renders animated characters with procedural pixel skins, custom GIFs,
    unlockable accessories (sunglasses, crown), and interactive petting hearts.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(130, 105)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.frame = 0
        self.state = "WALKING"
        self.facing_left = False
        self.skin = "pixel_guy"
        self.particles = []
        self.hearts = []
        self.tear_offset = 0

        self.movies = {}
        self.current_movie = None
        self.load_custom_gifs()

    def set_skin(self, skin):
        self.skin = skin
        self.load_custom_gifs()
        self.update()

    def load_custom_gifs(self):
        self.movies = {}
        if self.current_movie:
            self.current_movie.stop()
            self.current_movie = None

        if self.skin.startswith("custom:"):
            filename = self.skin.split("custom:", 1)[1]
            path = os.path.join(CUSTOM_AVATARS_DIR, filename)
            if os.path.exists(path):
                movie = QMovie(path)
                movie.frameChanged.connect(lambda: self.update())
                self.movies["CUSTOM"] = movie
                return

        gif_map = {
            "WALKING": "walk.gif",
            "SAD_WALKING": "walk.gif",
            "IDLE": "idle.gif",
            "CELEBRATING": "celebrate.gif",
            "SAD": "sad.gif"
        }
        for st, filename in gif_map.items():
            path = os.path.join(ASSETS_DIR, filename)
            if os.path.exists(path):
                movie = QMovie(path)
                movie.frameChanged.connect(lambda: self.update())
                self.movies[st] = movie

    def set_state(self, state, facing_left=False):
        self.state = state
        self.facing_left = facing_left
        self.tear_offset = 0

        if state == "CELEBRATING":
            self.particles = [
                {"x": 65 + (i * 12 - 24), "y": 42, "vy": -2.8 - (i % 2), "alpha": 255}
                for i in range(5)
            ]
        elif state == "SAD":
            self.tear_offset = 0

        if "CUSTOM" in self.movies:
            target_movie = self.movies["CUSTOM"]
            if self.current_movie != target_movie:
                if self.current_movie:
                    self.current_movie.stop()
                self.current_movie = target_movie
                self.current_movie.start()
        elif self.state in self.movies:
            target_movie = self.movies[self.state]
            if self.current_movie != target_movie:
                if self.current_movie:
                    self.current_movie.stop()
                self.current_movie = target_movie
                self.current_movie.start()
        else:
            if self.current_movie:
                self.current_movie.stop()
                self.current_movie = None

        self.update()

    def spawn_hearts(self):
        self.hearts = [
            {"x": 65 + (i * 16 - 16), "y": 32, "vy": -1.8 - (i % 2) * 0.5, "alpha": 255}
            for i in range(3)
        ]
        self.update()

    def advance_frame(self):
        self.frame = (self.frame + 1) % 120

        if self.state == "CELEBRATING":
            for p in self.particles:
                p["y"] += p["vy"]
                p["alpha"] = max(0, p["alpha"] - 7)

        elif self.state == "SAD":
            self.tear_offset = (self.tear_offset + 0.6) % 14

        if self.hearts:
            for h in self.hearts:
                h["y"] += h["vy"]
                h["alpha"] = max(0, h["alpha"] - 7)
            self.hearts = [h for h in self.hearts if h["alpha"] > 0]

        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.globalPosition().toPoint()
            self._dragged = False

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and hasattr(self, "_drag_start"):
            delta = event.globalPosition().toPoint() - self._drag_start
            if delta.manhattanLength() > 4:
                self._dragged = True
                self.parent().on_avatar_dragged(delta.x())
                self._drag_start = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not getattr(self, "_dragged", False):
                self.parent().on_avatar_petted()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw GIF if active
        if self.current_movie and self.current_movie.isValid():
            pix = self.current_movie.currentPixmap()
            if not pix.isNull():
                target_w, target_h = 84, 84
                scaled = pix.scaled(target_w, target_h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                if not self.facing_left:
                    scaled = scaled.transformed(QTransform().scale(-1, 1))
                draw_x = (self.width() - scaled.width()) // 2
                draw_y = self.height() - scaled.height() - 5
                painter.drawPixmap(draw_x, draw_y, scaled)
                self.draw_hearts_and_particles(painter)
                painter.end()
                return

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        if not self.facing_left:
            painter.translate(self.width(), 0)
            painter.scale(-1, 1)

        center_x = 65
        base_y = 80
        bob_y = 0
        leg_offset = 0
        head_down_y = 0

        if self.state == "WALKING":
            cycle = (self.frame // 4) % 4
            bob_y = -2 if cycle in (1, 3) else 0
            leg_offset = 3 if cycle == 1 else (-3 if cycle == 3 else 0)
        elif self.state == "CELEBRATING":
            cycle = (self.frame // 3) % 4
            bob_y = -6 if cycle in (1, 2) else 0
        elif self.state == "SAD":
            head_down_y = 4
            bob_y = 1
        elif self.state == "SAD_WALKING":
            cycle = (self.frame // 5) % 4
            bob_y = 1 if cycle in (1, 3) else 0
            leg_offset = 2 if cycle == 1 else (-2 if cycle == 3 else 0)
            head_down_y = 4

        # Render specific skin
        if self.skin == "pixel_cat":
            self.draw_cat(painter, center_x, base_y, bob_y, leg_offset, head_down_y)
        elif self.skin == "pixel_robot":
            self.draw_robot(painter, center_x, base_y, bob_y, leg_offset, head_down_y)
        elif self.skin == "pixel_slime":
            self.draw_slime(painter, center_x, base_y, bob_y, leg_offset)
        elif self.skin == "pixel_frog":
            self.draw_frog(painter, center_x, base_y, bob_y, leg_offset, head_down_y)
        elif self.skin == "pixel_ghost":
            self.draw_ghost(painter, center_x, base_y, bob_y)
        elif self.skin == "pixel_puppy":
            self.draw_puppy(painter, center_x, base_y, bob_y, leg_offset, head_down_y)
        elif self.skin == "pixel_duck":
            self.draw_duck(painter, center_x, base_y, bob_y, leg_offset, head_down_y)
        elif self.skin == "pixel_dino":
            self.draw_dino(painter, center_x, base_y, bob_y, leg_offset, head_down_y)
        elif self.skin == "pixel_bear":
            self.draw_bear(painter, center_x, base_y, bob_y, leg_offset, head_down_y)
        else:
            self.draw_guy(painter, center_x, base_y, bob_y, leg_offset, head_down_y)

        # Draw Unlockable Accessories (Sunglasses 🕶️ / Crown 👑)
        self.draw_accessories(painter, center_x, base_y + bob_y + head_down_y)

        # Restore painter coordinates for particles & hearts
        painter.resetTransform()
        self.draw_hearts_and_particles(painter)
        painter.end()

    def draw_accessories(self, painter, center_x, head_y):
        try:
            cups = self.parent().config.get("cups_today", 0)
            goal = self.parent().config.get("daily_goal_cups", 8)

            # 1. Sunglasses when >= 4 cups and < goal
            if 4 <= cups < goal:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor(15, 23, 42))  # dark sunglasses
                sy = head_y - 28
                painter.drawRect(center_x - 12, sy, 10, 5)
                painter.drawRect(center_x + 2, sy, 10, 5)
                painter.drawRect(center_x - 2, sy + 1, 4, 2)
                painter.setBrush(QColor(255, 255, 255, 220))
                painter.drawRect(center_x - 11, sy + 1, 2, 2)
                painter.drawRect(center_x + 3, sy + 1, 2, 2)

            # 2. Golden Crown when daily goal is reached!
            elif cups >= goal and goal > 0:
                cy = head_y - 40
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor(234, 179, 8))  # gold
                painter.drawRect(center_x - 12, cy + 4, 24, 4)
                painter.drawRect(center_x - 12, cy, 4, 4)
                painter.drawRect(center_x - 2, cy - 2, 4, 6)
                painter.drawRect(center_x + 8, cy, 4, 4)
                # Jewels
                painter.setBrush(QColor(239, 68, 68))  # ruby
                painter.drawRect(center_x - 1, cy + 5, 2, 2)
                painter.setBrush(QColor(59, 130, 246))  # sapphire
                painter.drawRect(center_x - 8, cy + 5, 2, 2)
                painter.drawRect(center_x + 6, cy + 5, 2, 2)
        except Exception:
            pass

    def draw_hearts_and_particles(self, painter):
        # Draw Celebration Particles
        if self.state == "CELEBRATING":
            for p in self.particles:
                if p["alpha"] > 0:
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(QColor(56, 189, 248, int(p["alpha"])))
                    painter.drawRect(int(p["x"]), int(p["y"]), 5, 5)

        # Draw Floating Petting Hearts
        for h in self.hearts:
            if h["alpha"] > 0:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor(244, 63, 94, int(h["alpha"])))
                hx, hy = int(h["x"]), int(h["y"])
                painter.drawRect(hx - 4, hy, 4, 4)
                painter.drawRect(hx, hy, 4, 4)
                poly = QPolygonF([QPointF(hx - 4, hy + 3), QPointF(hx + 4, hy + 3), QPointF(hx, hy + 8)])
                painter.drawPolygon(poly)

    def draw_guy(self, painter, center_x, base_y, bob_y, leg_offset, head_down_y):
        # Legs
        painter.setBrush(QColor(51, 65, 85))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(center_x - 7, base_y - 10 + leg_offset, 5, 12)
        painter.drawRect(center_x + 2, base_y - 10 - leg_offset, 5, 12)
        painter.setBrush(QColor(226, 232, 240))
        painter.drawRect(center_x - 8, base_y + 2 + leg_offset, 6, 4)
        painter.drawRect(center_x + 1, base_y + 2 - leg_offset, 6, 4)

        # Body
        body_y = base_y - 24 + bob_y
        painter.setBrush(QColor(14, 165, 233))
        painter.drawRect(center_x - 9, body_y, 18, 16)

        # Arms
        arm_y = body_y + 2
        if self.state == "CELEBRATING":
            painter.setBrush(QColor(14, 165, 233))
            painter.drawRect(center_x - 14, arm_y - 6, 5, 12)
            painter.drawRect(center_x + 9, arm_y - 6, 5, 12)
        else:
            painter.setBrush(QColor(14, 165, 233))
            painter.drawRect(center_x - 13, arm_y - leg_offset, 4, 12)
            painter.drawRect(center_x + 9, arm_y + leg_offset, 4, 12)

        # Head & Cap
        head_y = body_y - 18 + head_down_y
        painter.setBrush(QColor(254, 215, 170))
        painter.drawRect(center_x - 8, head_y, 16, 16)
        painter.setBrush(QColor(2, 132, 199))
        painter.drawRect(center_x - 9, head_y - 4, 18, 6)
        painter.drawRect(center_x - 14, head_y - 1, 6, 3)

        # Eyes
        if self.state == "CELEBRATING":
            painter.setPen(QPen(QColor(15, 23, 42), 2))
            painter.drawLine(center_x - 5, head_y + 6, center_x - 2, head_y + 4)
            painter.drawLine(center_x + 2, head_y + 4, center_x + 5, head_y + 6)
        elif "SAD" in self.state:
            painter.setPen(QPen(QColor(15, 23, 42), 2))
            painter.drawLine(center_x - 5, head_y + 5, center_x - 2, head_y + 8)
            painter.drawLine(center_x + 2, head_y + 8, center_x + 5, head_y + 5)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(56, 189, 248))
            painter.drawEllipse(center_x - 6, int(head_y + 10 + self.tear_offset), 4, 5)
        else:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(15, 23, 42))
            painter.drawRect(center_x - 5, head_y + 5, 3, 4)
            painter.drawRect(center_x + 2, head_y + 5, 3, 4)

    def draw_cat(self, painter, center_x, base_y, bob_y, leg_offset, head_down_y):
        cat_y = base_y - 20 + bob_y
        painter.setBrush(QColor(249, 115, 22))  # Orange cat
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(center_x - 12, cat_y, 24, 16)

        # Ears
        head_y = cat_y - 12 + head_down_y
        painter.drawPolygon(QPolygonF([QPointF(center_x - 10, head_y + 4), QPointF(center_x - 6, head_y - 6), QPointF(center_x - 2, head_y + 4)]))
        painter.drawPolygon(QPolygonF([QPointF(center_x + 2, head_y + 4), QPointF(center_x + 6, head_y - 6), QPointF(center_x + 10, head_y + 4)]))

        # Head
        painter.drawRect(center_x - 11, head_y, 22, 14)

        # Eyes & Nose
        painter.setBrush(QColor(15, 23, 42))
        painter.drawRect(center_x - 6, head_y + 5, 3, 3)
        painter.drawRect(center_x + 3, head_y + 5, 3, 3)
        painter.setBrush(QColor(244, 63, 94))
        painter.drawRect(center_x - 1, head_y + 8, 2, 2)

        # Paws & Tail
        painter.setBrush(QColor(234, 88, 12))
        painter.drawRect(center_x - 10, base_y - 4 + leg_offset, 6, 6)
        painter.drawRect(center_x + 4, base_y - 4 - leg_offset, 6, 6)
        painter.drawRect(center_x - 16, cat_y - 4, 4, 10)

    def draw_robot(self, painter, center_x, base_y, bob_y, leg_offset, head_down_y):
        bot_y = base_y - 22 + bob_y
        painter.setPen(Qt.PenStyle.NoPen)
        # Antenna
        painter.setBrush(QColor(239, 68, 68))
        painter.drawRect(center_x - 2, bot_y - 24 + head_down_y, 4, 6)
        painter.drawEllipse(center_x - 3, bot_y - 28 + head_down_y, 6, 6)

        # Head
        painter.setBrush(QColor(148, 163, 184))
        painter.drawRect(center_x - 12, bot_y - 18 + head_down_y, 24, 16)
        # Visor
        painter.setBrush(QColor(56, 189, 248))
        painter.drawRect(center_x - 9, bot_y - 14 + head_down_y, 18, 6)

        # Body
        painter.setBrush(QColor(100, 116, 139))
        painter.drawRect(center_x - 10, bot_y, 20, 16)
        # Heart light
        painter.setBrush(QColor(34, 197, 94))
        painter.drawRect(center_x - 3, bot_y + 4, 6, 6)

        # Treads / Legs
        painter.setBrush(QColor(51, 65, 85))
        painter.drawRect(center_x - 9, base_y - 6 + leg_offset, 6, 8)
        painter.drawRect(center_x + 3, base_y - 6 - leg_offset, 6, 8)

    def draw_slime(self, painter, center_x, base_y, bob_y, leg_offset):
        slime_y = base_y - 18 + bob_y
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(56, 189, 248))
        path = QPainterPath()
        path.addRoundedRect(QRectF(center_x - 14, slime_y, 28, 20), 12, 12)
        painter.drawPath(path)

        # Eyes & Smile
        painter.setBrush(QColor(15, 23, 42))
        painter.drawEllipse(center_x - 7, int(slime_y + 6), 4, 5)
        painter.drawEllipse(center_x + 3, int(slime_y + 6), 4, 5)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(center_x - 6, int(slime_y + 7), 2, 2)
        painter.drawEllipse(center_x + 4, int(slime_y + 7), 2, 2)

    def draw_frog(self, painter, center_x, base_y, bob_y, leg_offset, head_down_y):
        frog_y = base_y - 18 + bob_y
        painter.setPen(Qt.PenStyle.NoPen)
        # Big Frog Eyes
        painter.setBrush(QColor(34, 197, 94))
        painter.drawEllipse(center_x - 11, int(frog_y - 8 + head_down_y), 8, 8)
        painter.drawEllipse(center_x + 3, int(frog_y - 8 + head_down_y), 8, 8)
        painter.setBrush(QColor(15, 23, 42))
        painter.drawEllipse(center_x - 9, int(frog_y - 6 + head_down_y), 4, 4)
        painter.drawEllipse(center_x + 5, int(frog_y - 6 + head_down_y), 4, 4)

        # Head & Body
        painter.setBrush(QColor(74, 222, 128))
        painter.drawRect(center_x - 14, int(frog_y + head_down_y), 28, 16)
        painter.setBrush(QColor(254, 240, 138))  # Belly
        painter.drawRect(center_x - 7, int(frog_y + 6), 14, 10)

        # Webbed feet
        painter.setBrush(QColor(34, 197, 94))
        painter.drawRect(center_x - 12, base_y - 3 + leg_offset, 8, 4)
        painter.drawRect(center_x + 4, base_y - 3 - leg_offset, 8, 4)

    def draw_ghost(self, painter, center_x, base_y, bob_y):
        ghost_y = base_y - 26 + bob_y
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(241, 245, 249, 230))
        path = QPainterPath()
        path.addRoundedRect(QRectF(center_x - 12, ghost_y, 24, 24), 10, 10)
        painter.drawPath(path)

        # Eyes
        painter.setBrush(QColor(15, 23, 42))
        painter.drawEllipse(center_x - 7, int(ghost_y + 6), 4, 5)
        painter.drawEllipse(center_x + 3, int(ghost_y + 6), 4, 5)
        painter.setBrush(QColor(244, 114, 182, 180))  # Blush
        painter.drawEllipse(center_x - 10, int(ghost_y + 11), 3, 2)
        painter.drawEllipse(center_x + 7, int(ghost_y + 11), 3, 2)

    def draw_puppy(self, painter, center_x, base_y, bob_y, leg_offset, head_down_y):
        dog_y = base_y - 20 + bob_y
        painter.setPen(Qt.PenStyle.NoPen)
        # Golden Fur Body
        painter.setBrush(QColor(217, 119, 6))
        painter.drawRect(center_x - 12, dog_y, 24, 16)
        # Cream Chest
        painter.setBrush(QColor(254, 243, 199))
        painter.drawRect(center_x - 6, dog_y + 4, 12, 10)

        # Head
        head_y = dog_y - 14 + head_down_y
        painter.setBrush(QColor(245, 158, 11))
        painter.drawRect(center_x - 11, head_y, 22, 16)

        # Floppy Ears (bobs with animation)
        painter.setBrush(QColor(180, 83, 9))
        painter.drawRect(center_x - 15, head_y + 1, 5, 12)
        painter.drawRect(center_x + 10, head_y + 1, 5, 12)

        # Muzzle & Nose
        painter.setBrush(QColor(254, 243, 199))
        painter.drawRect(center_x - 5, head_y + 8, 10, 7)
        painter.setBrush(QColor(15, 23, 42))
        painter.drawRect(center_x - 2, head_y + 7, 4, 3)

        # Eyes & Happy Tongue
        if self.state == "CELEBRATING" or self.state == "IDLE":
            painter.setBrush(QColor(244, 63, 94))  # Little pink tongue
            painter.drawRect(center_x - 2, head_y + 13, 4, 4)
        painter.setBrush(QColor(15, 23, 42))
        painter.drawRect(center_x - 6, head_y + 4, 3, 3)
        painter.drawRect(center_x + 3, head_y + 4, 3, 3)

        # Stepping Paws & Wagging Tail
        painter.setBrush(QColor(180, 83, 9))
        painter.drawRect(center_x - 10, base_y - 4 + leg_offset, 6, 6)
        painter.drawRect(center_x + 4, base_y - 4 - leg_offset, 6, 6)
        # Tail wagging with leg_offset
        tail_wag = int(leg_offset * 1.5)
        painter.drawRect(center_x - 16, dog_y + 2 + tail_wag, 4, 8)

    def draw_duck(self, painter, center_x, base_y, bob_y, leg_offset, head_down_y):
        duck_y = base_y - 20 + bob_y
        painter.setPen(Qt.PenStyle.NoPen)
        # Yellow Plump Body
        painter.setBrush(QColor(250, 204, 21))
        painter.drawRect(center_x - 11, duck_y, 22, 16)

        # Head
        head_y = duck_y - 12 + head_down_y
        painter.setBrush(QColor(254, 224, 71))
        painter.drawRect(center_x - 8, head_y, 16, 14)

        # Orange Bill / Beak
        painter.setBrush(QColor(249, 115, 22))
        painter.drawRect(center_x + 6, head_y + 5, 8, 5)

        # Eye with glimmer
        painter.setBrush(QColor(15, 23, 42))
        painter.drawRect(center_x + 1, head_y + 4, 3, 3)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(center_x + 1, head_y + 4, 1, 1)

        # Little Wing
        painter.setBrush(QColor(234, 179, 8))
        painter.drawRect(center_x - 9, duck_y + 3, 8, 8)

        # Orange Webbed Feet waddling
        painter.setBrush(QColor(234, 88, 12))
        painter.drawRect(center_x - 7, base_y - 4 + leg_offset, 6, 5)
        painter.drawRect(center_x + 2, base_y - 4 - leg_offset, 6, 5)

    def draw_dino(self, painter, center_x, base_y, bob_y, leg_offset, head_down_y):
        dino_y = base_y - 22 + bob_y
        painter.setPen(Qt.PenStyle.NoPen)
        # Emerald Dino Body
        painter.setBrush(QColor(16, 185, 129))
        painter.drawRect(center_x - 10, dino_y, 20, 18)

        # Soft Mint Belly
        painter.setBrush(QColor(167, 243, 208))
        painter.drawRect(center_x - 4, dino_y + 4, 10, 12)

        # Head & Big Snout
        head_y = dino_y - 14 + head_down_y
        painter.setBrush(QColor(52, 211, 153))
        painter.drawRect(center_x - 8, head_y, 18, 15)
        painter.drawRect(center_x + 4, head_y + 5, 6, 8)  # Snout

        # Eye
        painter.setBrush(QColor(15, 23, 42))
        painter.drawRect(center_x + 2, head_y + 4, 3, 3)

        # Back Spikes (Orange Dino Ridges)
        painter.setBrush(QColor(245, 158, 11))
        painter.drawPolygon(QPolygonF([QPointF(center_x - 8, head_y + 1), QPointF(center_x - 12, head_y - 3), QPointF(center_x - 8, head_y - 1)]))
        painter.drawPolygon(QPolygonF([QPointF(center_x - 10, dino_y + 4), QPointF(center_x - 14, dino_y + 1), QPointF(center_x - 10, dino_y + 2)]))
        painter.drawPolygon(QPolygonF([QPointF(center_x - 10, dino_y + 12), QPointF(center_x - 14, dino_y + 9), QPointF(center_x - 10, dino_y + 10)]))

        # Tiny Dino Arms
        painter.setBrush(QColor(16, 185, 129))
        painter.drawRect(center_x + 4, dino_y + 6, 5, 3)

        # Tail & Feet
        painter.drawRect(center_x - 16, dino_y + 8, 6, 6)
        painter.setBrush(QColor(5, 150, 105))
        painter.drawRect(center_x - 8, base_y - 4 + leg_offset, 6, 6)
        painter.drawRect(center_x + 2, base_y - 4 - leg_offset, 6, 6)

    def draw_bear(self, painter, center_x, base_y, bob_y, leg_offset, head_down_y):
        bear_y = base_y - 22 + bob_y
        painter.setPen(Qt.PenStyle.NoPen)
        # Warm Bear Body
        painter.setBrush(QColor(146, 64, 14))
        painter.drawRect(center_x - 12, bear_y, 24, 18)

        # Honey Belly Patch
        painter.setBrush(QColor(253, 230, 138))
        painter.drawRect(center_x - 6, bear_y + 4, 12, 12)

        # Head
        head_y = bear_y - 14 + head_down_y
        painter.setBrush(QColor(180, 83, 9))
        painter.drawRect(center_x - 10, head_y, 20, 15)

        # Round Bear Ears with Tan Insets
        painter.setBrush(QColor(146, 64, 14))
        painter.drawEllipse(center_x - 12, int(head_y - 4), 6, 6)
        painter.drawEllipse(center_x + 6, int(head_y - 4), 6, 6)
        painter.setBrush(QColor(253, 230, 138))
        painter.drawEllipse(center_x - 11, int(head_y - 3), 4, 4)
        painter.drawEllipse(center_x + 7, int(head_y - 3), 4, 4)

        # Muzzle & Heart Nose
        painter.drawRect(center_x - 5, head_y + 7, 10, 6)
        painter.setBrush(QColor(15, 23, 42))
        painter.drawRect(center_x - 2, head_y + 7, 4, 3)

        # Eyes
        painter.drawRect(center_x - 6, head_y + 4, 3, 3)
        painter.drawRect(center_x + 3, head_y + 4, 3, 3)

        # Sturdy Bear Paws
        painter.setBrush(QColor(120, 53, 15))
        painter.drawRect(center_x - 9, base_y - 4 + leg_offset, 6, 6)
        painter.drawRect(center_x + 3, base_y - 4 - leg_offset, 6, 6)


class SpeechBubble(QWidget):
    """
    Floating speech bubble card with progress badge and action buttons.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(310)
        self.setFixedHeight(132)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 22)
        layout.setSpacing(6)

        # Cup progress badge
        self.badge_lbl = QLabel(self)
        self.badge_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.badge_lbl.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        self.badge_lbl.setStyleSheet("color: #38bdf8; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 6px; padding: 2px 10px;")
        layout.addWidget(self.badge_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.label.setStyleSheet("color: #f8fafc; background: transparent;")
        layout.addWidget(self.label)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.setSpacing(10)

        self.btn_yes = QPushButton("YES", self)
        self.btn_yes.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_yes.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.btn_yes.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
                color: #080c15;
                border: none;
                border-radius: 7px;
                padding: 7px 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38bdf8, stop:1 #7dd3fc);
            }
        """)
        self.btn_layout.addWidget(self.btn_yes)

        self.btn_later = QPushButton("Remind me later", self)
        self.btn_later.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_later.setFont(QFont("Segoe UI", 9))
        self.btn_later.setStyleSheet("""
            QPushButton {
                background: rgba(30, 41, 59, 0.85);
                color: #cbd5e1;
                border: 1px solid rgba(148, 163, 184, 0.25);
                border-radius: 7px;
                padding: 7px 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: rgba(51, 65, 85, 0.95);
                color: #ffffff;
                border-color: #38bdf8;
            }
        """)
        self.btn_layout.addWidget(self.btn_later)

        layout.addLayout(self.btn_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        rect = QRectF(2, 2, self.width() - 4, self.height() - 16)
        path = QPainterPath()
        path.addRoundedRect(rect, 14, 14)

        tail_x = 55
        path.moveTo(tail_x - 8, self.height() - 16)
        path.lineTo(tail_x, self.height() - 3)
        path.lineTo(tail_x + 8, self.height() - 16)
        path.closeSubpath()

        # Dark luxury acrylic background with cyan neon glow border
        painter.setBrush(QBrush(QColor(15, 23, 42, 245)))
        painter.setPen(QPen(QColor(56, 189, 248, 160), 1.5))
        painter.drawPath(path)
        painter.end()


class DesktopCompanion(QWidget):
    """
    Main transparent overlay coordinating the lifecycle, motion, dynamic avatars, and tray.
    """
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.paused_until = None
        self.current_break_type = "water"

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(320, 240)

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(10, 5, 10, 0)
        self.vbox.setSpacing(0)

        self.bubble = SpeechBubble(self)
        self.vbox.addWidget(self.bubble, alignment=Qt.AlignmentFlag.AlignLeft)

        self.avatar = AvatarWidget(self)
        self.avatar.set_skin(self.config.get("skin", "pixel_guy"))
        self.vbox.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignLeft)

        self.bubble.btn_yes.clicked.connect(self.on_yes_clicked)
        self.bubble.btn_later.clicked.connect(self.on_later_clicked)

        self.state = "OFFSCREEN"
        self.current_x = 0
        self.target_x = 0
        self.window_y = 0

        # Animation Ticker (started ON DEMAND when onscreen to achieve 0.0% CPU when idle)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.on_animation_tick)

        # Drift-free Scheduled Reminder & System Clock Synchronizer (runs every 10s)
        self.next_reminder_time = datetime.now() + timedelta(minutes=self.config.get("interval_minutes", 30))
        self.clock_sync_timer = QTimer(self)
        self.clock_sync_timer.timeout.connect(self.on_clock_sync_tick)
        self.clock_sync_timer.start(10000)

        # Interval Reminder Timer
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.on_scheduled_reminder_tick)
        interval_ms = max(1, self.config.get("interval_minutes", 30)) * 60 * 1000
        self.reminder_timer.start(interval_ms)

        self.transition_timer = QTimer(self)
        self.transition_timer.setSingleShot(True)
        self.transition_timer.timeout.connect(self.on_transition_timeout)

        # Setup Windows System Tray
        self.setup_system_tray()

        # Initial launch greeting after 1 second
        QTimer.singleShot(1000, lambda: self.start_walk_in(force=True))

    def check_midnight_reset(self):
        """
        Synchronizes with system calendar date and resets daily cups at midnight (00:00:00).
        Ensures reliable reset across multi-day background runs, system sleep, or hibernation.
        """
        today_str = datetime.now().strftime("%Y-%m-%d")
        last_date = self.config.get("last_date", "")
        if last_date != today_str:
            old_cups = self.config.get("cups_today", 0)
            print(f"[{datetime.now()}] Midnight date change detected: {last_date} -> {today_str}. Resetting daily cups from {old_cups} to 0.")
            self.config["cups_today"] = 0
            self.config["last_date"] = today_str
            save_config(self.config)
            self.update_tray_tooltip()
            if hasattr(self, "_settings_dlg") and self._settings_dlg and self._settings_dlg.isVisible():
                self._settings_dlg.lbl_progress.setText(f"Today's Intake: <b>0</b> / {self.config.get('daily_goal_cups', 8)} cups")
            return True
        return False

    def schedule_next_reminder(self, minutes=None):
        if minutes is None:
            minutes = self.config.get("interval_minutes", 30)
        self.next_reminder_time = datetime.now() + timedelta(minutes=minutes)
        print(f"[{datetime.now()}] Next reminder scheduled for {self.next_reminder_time.strftime('%H:%M:%S')} ({minutes}m from now)")

    def on_clock_sync_tick(self):
        """
        High-precision system clock synchronization tick (runs every 10 seconds).
        Guarantees midnight cup reset, pause expiration, and drift-free schedule execution.
        """
        # 1. Midnight reset verification
        self.check_midnight_reset()

        now = datetime.now()

        # 2. Check if user's manual pause/meeting mode has expired
        if self.paused_until and now >= self.paused_until:
            print(f"[{datetime.now()}] Meeting Mode / Pause ended. Resuming companion.")
            self.paused_until = None
            self.schedule_next_reminder()
            self.update_tray_tooltip()
            self.rebuild_tray_menu()

        # 3. If companion is idle offscreen, check if scheduled break is due
        if self.state == "OFFSCREEN":
            if self.paused_until and now < self.paused_until:
                return
            if not is_within_schedule(self.config):
                return
            if hasattr(self, "next_reminder_time") and self.next_reminder_time:
                if now >= self.next_reminder_time:
                    print(f"[{datetime.now()}] Scheduled break due ({self.next_reminder_time.strftime('%H:%M:%S')}). Initiating walk-in.")
                    self.start_walk_in(force=False)

    def setup_system_tray(self):
        self.tray = QSystemTrayIcon(self)

        ico_path = os.path.join(ASSETS_DIR, "tray_icon.ico")
        if os.path.exists(ico_path):
            tray_icon = QIcon(ico_path)
        else:
            pix = QPixmap(32, 32)
            pix.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pix)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setBrush(QColor(14, 165, 233))
            painter.setPen(Qt.PenStyle.NoPen)
            path = QPainterPath()
            path.moveTo(16, 4)
            path.cubicTo(16, 4, 6, 18, 6, 23)
            path.arcTo(6, 14, 20, 18, 180, 180)
            path.cubicTo(26, 18, 16, 4, 16, 4)
            painter.drawPath(path)
            painter.end()
            tray_icon = QIcon(pix)

        self.tray.setIcon(tray_icon)
        self.setWindowIcon(tray_icon)
        QApplication.instance().setWindowIcon(tray_icon)
        self.update_tray_tooltip()

        self.tray.activated.connect(self.on_tray_activated)

        # Context Menu
        self.tray_menu = QMenu()
        self.tray_menu.setStyleSheet("""
            QMenu {
                background-color: #0f172a;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 10px;
                padding: 6px;
                font-family: 'Segoe UI', system-ui, sans-serif;
                font-size: 13px;
                color: #f8fafc;
            }
            QMenu::item {
                padding: 7px 24px 7px 14px;
                border-radius: 6px;
            }
            QMenu::item:selected {
                background-color: #1e293b;
                color: #38bdf8;
            }
            QMenu::separator {
                height: 1px;
                background-color: #334155;
                margin: 4px 6px;
            }
        """)

        self.rebuild_tray_menu()
        self.tray.show()

        # Display brief notification on startup
        QTimer.singleShot(500, lambda: self.tray.showMessage(
            "Desktop Companion v2.0 Active 💧",
            "Running in background. Right-click 💧 for Settings, Avatars & Meeting Mode.",
            QSystemTrayIcon.MessageIcon.Information,
            3000
        ))

    def rebuild_tray_menu(self):
        self.tray_menu.clear()

        # 1. Summon Companion
        act_summon = self.tray_menu.addAction("💧 Summon Companion")
        act_summon.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        act_summon.triggered.connect(lambda: self.start_walk_in(force=True))

        self.tray_menu.addSeparator()

        # 2. Avatars Submenu
        menu_avatars = self.tray_menu.addMenu("🎨 Avatars & Skins")
        self.populate_skins_menu(menu_avatars)

        # 3. Meeting Mode / Pause Submenu
        menu_pause = self.tray_menu.addMenu("⏸️ Meeting Mode / Pause")
        self.populate_pause_menu(menu_pause)

        # 4. Schedule & Quiet Hours Submenu
        menu_sched = self.tray_menu.addMenu("📅 Schedule & Quiet Hours")
        self.populate_schedule_menu(menu_sched)

        self.tray_menu.addSeparator()

        # 5. Settings
        act_settings = self.tray_menu.addAction("⚙️ Settings...")
        act_settings.triggered.connect(self.open_settings)

        # 6. Open Project / App Folder
        act_folder = self.tray_menu.addAction("📁 Open App Folder")
        act_folder.triggered.connect(self.open_app_folder)

        self.tray_menu.addSeparator()

        # 7. Exit
        act_exit = self.tray_menu.addAction("❌ Exit")
        act_exit.triggered.connect(QApplication.instance().quit)

        self.tray.setContextMenu(self.tray_menu)

    def populate_schedule_menu(self, menu):
        sched = self.config.get("schedule", {})
        qh = self.config.get("quiet_hours", {})

        # Working Hours summary item
        s_time = sched.get("start_time", "09:00")
        e_time = sched.get("end_time", "18:30")
        s_days = len(sched.get("days", []))
        sched_on = sched.get("enabled", True)
        if sched_on:
            act_work = menu.addAction(f"💼 Work Hours: {s_time} - {e_time} ({s_days} days)")
        else:
            act_work = menu.addAction("💼 Work Hours: Disabled (24/7)")
        act_work.setEnabled(False)

        menu.addSeparator()

        # Quiet Hours toggle & status
        qh_on = qh.get("enabled", True)
        qh_start = format_time_12h(qh.get("start_time", "22:00"))
        qh_end = format_time_12h(qh.get("end_time", "08:00"))
        in_qh = is_in_quiet_hours(self.config)

        status_suffix = " (Active Now)" if in_qh else ""
        act_qh_toggle = menu.addAction(f"🌙 Quiet Hours: {qh_start} — {qh_end}{status_suffix}")
        act_qh_toggle.setCheckable(True)
        act_qh_toggle.setChecked(qh_on)
        act_qh_toggle.triggered.connect(self.toggle_quiet_hours)

        menu.addSeparator()
        act_open_sched = menu.addAction("⚙️ Configure Schedule in Settings...")
        act_open_sched.triggered.connect(lambda: self.open_settings(initial_tab=2))

    def toggle_quiet_hours(self, checked):
        if "quiet_hours" not in self.config:
            self.config["quiet_hours"] = {}
        self.config["quiet_hours"]["enabled"] = checked
        save_config(self.config)
        self.update_tray_tooltip()
        self.rebuild_tray_menu()
        state_str = "Enabled 🌙" if checked else "Disabled ☀️"
        self.tray.showMessage(
            "Quiet Hours Updated",
            f"Quiet hours are now {state_str}.",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def populate_skins_menu(self, menu):
        is_dynamic = self.config.get("dynamic_avatar", True)
        curr_skin = self.config.get("skin", "pixel_guy")

        act_dyn = menu.addAction("✨ Dynamic (Auto-Cycle every interval)")
        act_dyn.setCheckable(True)
        act_dyn.setChecked(is_dynamic)
        act_dyn.triggered.connect(lambda: self.select_skin("dynamic"))

        menu.addSeparator()

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
            act = menu.addAction(name)
            act.setCheckable(True)
            act.setChecked(not is_dynamic and curr_skin == key)
            act.triggered.connect(lambda checked, k=key: self.select_skin(k))

        custom_skins = [s for s in get_available_skins() if s.startswith("custom:")]
        if custom_skins:
            menu.addSeparator()
            for cs in custom_skins:
                fname = cs.split("custom:", 1)[1]
                act = menu.addAction(f"Custom: {fname}")
                act.setCheckable(True)
                act.setChecked(not is_dynamic and curr_skin == cs)
                act.triggered.connect(lambda checked, k=cs: self.select_skin(k))

    def select_skin(self, skin_key):
        if skin_key == "dynamic":
            self.config["dynamic_avatar"] = True
        else:
            self.config["dynamic_avatar"] = False
            self.config["skin"] = skin_key
            self.avatar.set_skin(skin_key)
        save_config(self.config)
        self.rebuild_tray_menu()

    def populate_pause_menu(self, menu):
        now = datetime.now()
        if self.paused_until and now < self.paused_until:
            t_str = self.paused_until.strftime("%H:%M")
            act_res = menu.addAction(f"▶️ Resume Reminders (Paused until {t_str})")
            act_res.triggered.connect(self.resume_reminders)
        else:
            act_30 = menu.addAction("Pause for 30 minutes")
            act_30.triggered.connect(lambda: self.pause_reminders(30))
            act_60 = menu.addAction("Pause for 1 hour")
            act_60.triggered.connect(lambda: self.pause_reminders(60))
            act_120 = menu.addAction("Pause for 2 hours")
            act_120.triggered.connect(lambda: self.pause_reminders(120))
            act_day = menu.addAction("Pause for rest of today")
            act_day.triggered.connect(lambda: self.pause_reminders(720))

    def pause_reminders(self, minutes):
        self.paused_until = datetime.now() + timedelta(minutes=minutes)
        self.update_tray_tooltip()
        self.rebuild_tray_menu()
        t_str = self.paused_until.strftime("%H:%M")
        self.tray.showMessage("Reminders Paused ⏸️", f"Paused until {t_str}. Click Resume to unpause.", QSystemTrayIcon.MessageIcon.Information, 2500)

    def resume_reminders(self):
        self.paused_until = None
        self.schedule_next_reminder()
        self.update_tray_tooltip()
        self.rebuild_tray_menu()
        self.tray.showMessage("Reminders Resumed ▶️", "Companion active on normal schedule.", QSystemTrayIcon.MessageIcon.Information, 2000)

    def update_tray_tooltip(self):
        self.check_midnight_reset()
        name = self.config.get("user_name", "BS_CZR_i11")
        cups = self.config.get("cups_today", 0)
        goal = self.config.get("daily_goal_cups", 8)
        now = datetime.now()

        status_lines = [f"Desktop Companion ({name})"]

        if self.paused_until and now < self.paused_until:
            t_str = self.paused_until.strftime("%H:%M")
            status_lines.append(f"⏸️ Paused until {t_str}")
        elif is_in_quiet_hours(self.config):
            qh = self.config.get("quiet_hours", {})
            e_12h = format_time_12h(qh.get("end_time", "08:00"))
            status_lines.append(f"🌙 Quiet Hours Active (until {e_12h})")
        elif not is_within_schedule(self.config):
            status_lines.append("💤 Outside Active Schedule")
        else:
            if hasattr(self, "next_reminder_time") and self.next_reminder_time and now < self.next_reminder_time:
                nxt_str = self.next_reminder_time.strftime("%H:%M")
                status_lines.append(f"⏰ Next break at {nxt_str}")

        status_lines.append(f"💧 {cups}/{goal} Cups Today")
        self.tray.setToolTip("\n".join(status_lines))

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.start_walk_in(force=True)

    def open_settings(self, initial_tab=0):
        self.check_midnight_reset()
        self._settings_dlg = SettingsDialog(self.config, BASE_DIR, initial_tab=initial_tab)
        self._settings_dlg.settings_saved.connect(self.on_settings_saved)
        self._settings_dlg.show()
        self._settings_dlg.raise_()
        self._settings_dlg.activateWindow()

    def on_settings_saved(self, new_cfg):
        self.config = new_cfg
        save_config(self.config)
        self.schedule_next_reminder(self.config.get("interval_minutes", 30))
        interval_ms = max(1, self.config.get("interval_minutes", 30)) * 60 * 1000
        self.reminder_timer.stop()
        self.reminder_timer.start(interval_ms)
        if not self.config.get("dynamic_avatar", True):
            self.avatar.set_skin(self.config.get("skin", "pixel_guy"))
        self.update_tray_tooltip()
        self.rebuild_tray_menu()

    def open_app_folder(self):
        try:
            os.startfile(BASE_DIR)
        except Exception:
            QDesktopServices.openUrl(QUrl.fromLocalFile(BASE_DIR))

    def on_scheduled_reminder_tick(self):
        now = datetime.now()
        if self.paused_until and now < self.paused_until:
            return
        if is_within_schedule(self.config):
            self.start_walk_in(force=False)

    def get_next_skin(self):
        all_skins = get_available_skins()
        current = self.config.get("skin", "pixel_guy")
        try:
            idx = all_skins.index(current)
            next_idx = (idx + 1) % len(all_skins)
        except ValueError:
            next_idx = 0
        return all_skins[next_idx]

    def on_avatar_dragged(self, dx):
        self.current_x += dx
        screen = QApplication.primaryScreen().availableGeometry()
        self.current_x = max(screen.left() - 50, min(screen.right() - self.width() + 50, self.current_x))
        self.move(int(self.current_x), int(self.window_y))

    def on_avatar_petted(self):
        if self.state in ("PROMPTING", "WALKING_IN", "IDLE"):
            name = self.config.get("user_name", "BS_CZR_i11")
            self.avatar.spawn_hearts()
            pet_replies = [
                f"Hehe, thanks {name}! ❤️",
                f"Aww, *pat pat*! 🥰",
                f"*Happy companion noises* ✨",
                f"Love you too, {name}! 💕"
            ]
            self.bubble.label.setText(random.choice(pet_replies))
            self.bubble.show()
            self.avatar.set_state("CELEBRATING", facing_left=False)
            QTimer.singleShot(1800, lambda: self.avatar.set_state("IDLE", facing_left=False) if self.state == "PROMPTING" else None)

    def closeEvent(self, event):
        print(f"[{datetime.now()}] DesktopCompanion.closeEvent triggered -> Hiding window.")
        event.ignore()
        self.hide()

    def start_walk_in(self, force=False):
        print(f"[{datetime.now()}] start_walk_in called (force={force}, current_state={self.state})")
        # Ensure system calendar date is synced and daily cups are reset if midnight passed
        self.check_midnight_reset()

        if self.state in ("WALKING_IN", "PROMPTING", "REACTING_YES", "REACTING_SAD"):
            print(f"[{datetime.now()}] start_walk_in skipped - already active.")
            return

        now = datetime.now()
        if not force and self.paused_until and now < self.paused_until:
            print(f"[{datetime.now()}] start_walk_in skipped - paused.")
            return

        if not force and not is_within_schedule(self.config):
            print(f"[{datetime.now()}] start_walk_in skipped - outside schedule.")
            return

        # DYNAMIC AVATAR: Cycle to next skin
        if self.config.get("dynamic_avatar", True):
            next_skin = self.get_next_skin()
            self.config["skin"] = next_skin
            save_config(self.config)
            self.avatar.set_skin(next_skin)

        # Audio chime (non-blocking)
        if self.config.get("sound_enabled", True) and os.path.exists(DRIP_WAV):
            try:
                winsound.PlaySound(DRIP_WAV, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                pass

        # Pick break type
        break_types = self.config.get("break_types", ["water"])
        if not break_types:
            break_types = ["water"]
        self.current_break_type = random.choice(break_types)

        screen = QApplication.primaryScreen().availableGeometry()
        self.window_y = screen.bottom() - self.height() + 5
        self.target_x = screen.left() + 25
        self.current_x = screen.left() - self.width() - 10

        self.state = "WALKING_IN"
        self.move(int(self.current_x), int(self.window_y))
        self.show()

        # START ANIMATION TIMER ONLY WHEN ONSCREEN! (0.0% CPU when offscreen)
        self.anim_timer.start(16)

        self.bubble.hide()
        user_name = self.config.get("user_name", "BS_CZR_i11")
        cups = self.config.get("cups_today", 0)
        goal = self.config.get("daily_goal_cups", 8)

        if self.current_break_type == "water":
            if self.config.get("witty_dialogue", True):
                quote = random.choice(WITTY_WATER_QUOTES).format(name=user_name)
                self.bubble.label.setText(f"{quote}\nDid you drink water? 💧")
            else:
                self.bubble.label.setText(f"Hey, {user_name}!\nDid you drink water? 💧")
            self.bubble.badge_lbl.setText(f"🥛 {cups} / {goal} Cups Today")
            self.bubble.badge_lbl.show()
            self.bubble.btn_yes.setText("YES")
            self.bubble.btn_later.setText("Remind me later")
        elif self.current_break_type == "eye_rest":
            self.bubble.label.setText(f"Hey, {user_name}! 20-20-20 Eye Break!\nLook 20 feet away for 20 seconds. 👁️")
            self.bubble.badge_lbl.hide()
            self.bubble.btn_yes.setText("Rested! 👀")
            self.bubble.btn_later.setText("Remind me later")
        elif self.current_break_type == "stretch":
            self.bubble.label.setText(f"Hey, {user_name}! Posture check!\nRoll shoulders & do a quick stretch! 🧘")
            self.bubble.badge_lbl.hide()
            self.bubble.btn_yes.setText("Stretched! ✨")
            self.bubble.btn_later.setText("Remind me later")

        self.bubble.btn_yes.show()
        self.bubble.btn_later.show()
        self.avatar.set_state("WALKING", facing_left=False)

    def start_prompt(self):
        print(f"[{datetime.now()}] start_prompt: displaying question bubble")
        self.state = "PROMPTING"
        self.avatar.set_state("IDLE", facing_left=False)
        self.bubble.show()

    def on_yes_clicked(self):
        if self.state != "PROMPTING":
            return

        self.check_midnight_reset()

        self.state = "REACTING_YES"
        self.bubble.btn_yes.hide()
        self.bubble.btn_later.hide()

        name = self.config.get("user_name", "BS_CZR_i11")
        if self.current_break_type == "water":
            cups = self.config.get("cups_today", 0) + 1
            goal = self.config.get("daily_goal_cups", 8)
            self.config["cups_today"] = cups
            save_config(self.config)
            self.update_tray_tooltip()
            self.bubble.badge_lbl.setText(f"🥛 {cups} / {goal} Cups Today")

            if cups < goal:
                self.bubble.label.setText(f"Nice! 💦 Glass {cups}/{goal} recorded!\nKeep it up, {name}!")
            elif cups == goal:
                self.bubble.label.setText(f"🎉 DAILY GOAL REACHED ({cups}/{goal})!\nYou are fully hydrated, {name}! 🏆")
            else:
                self.bubble.label.setText(f"Hydration superstar! 🌊\n{cups}/{goal} glasses today!")
        elif self.current_break_type == "eye_rest":
            self.bubble.label.setText(f"Awesome! 👁️✨\nYour eyes are refreshed, {name}!")
        elif self.current_break_type == "stretch":
            self.bubble.label.setText(f"Nice stretch! 🧘✨\nBack to being productive, {name}!")

        self.schedule_next_reminder(self.config.get("interval_minutes", 30))
        self.avatar.set_state("CELEBRATING", facing_left=False)
        self.transition_timer.start(2500)

    def on_later_clicked(self):
        if self.state != "PROMPTING":
            return

        self.state = "REACTING_SAD"
        self.bubble.btn_yes.hide()
        self.bubble.btn_later.hide()
        self.bubble.badge_lbl.hide()
        self.bubble.label.setText("Aww... please take care soon! 🥺")
        self.avatar.set_state("SAD", facing_left=False)

        snooze_min = self.config.get("snooze_minutes", 15)
        self.schedule_next_reminder(snooze_min)
        self.reminder_timer.stop()
        self.reminder_timer.start(snooze_min * 60 * 1000)

        self.transition_timer.start(2200)

    def on_transition_timeout(self):
        self.bubble.hide()
        if self.state == "REACTING_YES":
            self.state = "WALKING_OUT_HAPPY"
            self.avatar.set_state("WALKING", facing_left=False)
        else:
            self.state = "WALKING_OUT_SAD"
            self.avatar.set_state("SAD_WALKING", facing_left=True)

    def on_animation_tick(self):
        self.avatar.advance_frame()
        speed = self.config.get("walk_speed", 4)

        if self.state == "WALKING_IN":
            if self.current_x < self.target_x:
                self.current_x += speed
                self.move(int(self.current_x), int(self.window_y))
            else:
                self.current_x = self.target_x
                self.move(int(self.current_x), int(self.window_y))
                self.start_prompt()

        elif self.state == "WALKING_OUT_HAPPY":
            screen = QApplication.primaryScreen().availableGeometry()
            if self.current_x < screen.right() + 20:
                self.current_x += speed
                self.move(int(self.current_x), int(self.window_y))
            else:
                self.state = "OFFSCREEN"
                self.hide()
                # STOP ANIMATION TIMER WHEN OFFSCREEN! 0.0% CPU usage while waiting!
                self.anim_timer.stop()
                interval_ms = max(1, self.config.get("interval_minutes", 30)) * 60 * 1000
                self.reminder_timer.stop()
                self.reminder_timer.start(interval_ms)
                self.schedule_next_reminder(self.config.get("interval_minutes", 30))

        elif self.state == "WALKING_OUT_SAD":
            screen = QApplication.primaryScreen().availableGeometry()
            sad_speed = max(2, int(speed * 0.75))
            if self.current_x > screen.left() - self.width() - 20:
                self.current_x -= sad_speed
                self.move(int(self.current_x), int(self.window_y))
            else:
                self.state = "OFFSCREEN"
                self.hide()
                # STOP ANIMATION TIMER WHEN OFFSCREEN! 0.0% CPU usage while waiting!
                self.anim_timer.stop()


IPC_SERVER_NAME = "companion_ipc"


def main():
    print(f"[{datetime.now()}] Main started. Checking single instance...")
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 1. Single-Instance Check
    socket = QLocalSocket()
    socket.connectToServer(IPC_SERVER_NAME)
    if socket.waitForConnected(300):
        print(f"[{datetime.now()}] Existing instance found. Sent SUMMON and exiting.")
        socket.write(b"SUMMON\n")
        socket.waitForBytesWritten(300)
        socket.disconnectFromServer()
        socket.close()
        return 0

    print(f"[{datetime.now()}] Primary instance starting...")
    # 2. Start Primary Instance
    companion = DesktopCompanion()

    # 3. Setup IPC server so clicks summon companion
    ipc_server = QLocalServer()
    ipc_server.removeServer(IPC_SERVER_NAME)
    ipc_server.listen(IPC_SERVER_NAME)

    _last_summon_time = 0.0

    def on_ipc_connection():
        nonlocal _last_summon_time
        client = ipc_server.nextPendingConnection()
        if not client:
            return

        import time as _t
        now_ts = _t.time()
        # Security & Rate limiting: prevent socket spamming (1 summon per 1.5s)
        if now_ts - _last_summon_time < 1.5:
            client.disconnectFromServer()
            client.close()
            return

        # Security: limit read payload to 64 bytes to prevent buffer exhaustion
        if client.waitForReadyRead(200):
            payload = bytes(client.read(64)).strip()
            if payload == b"SUMMON":
                _last_summon_time = now_ts
                print(f"[{datetime.now()}] Verified SUMMON signal received -> Summoning companion.")
                companion.start_walk_in(force=True)

        client.disconnectFromServer()
        client.close()

    ipc_server.newConnection.connect(on_ipc_connection)
    companion._ipc_server = ipc_server

    app.aboutToQuit.connect(lambda: print(f"[{datetime.now()}] aboutToQuit signal received!"))

    exit_code = app.exec()
    print(f"[{datetime.now()}] app.exec() returned with exit code: {exit_code}")
    return exit_code


if __name__ == "__main__":
    main()
