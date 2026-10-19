"""
Generate Open Graph 1200x630 banner and mobile icons for Companion Hub
"""
import os
import sys
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QImage, QPainter, QColor, QFont, QPen, QBrush,
    QLinearGradient, QRadialGradient, QPainterPath
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_ASSETS = os.path.join(BASE_DIR, "public", "assets")
os.makedirs(PUBLIC_ASSETS, exist_ok=True)

def create_og_image():
    width = 1200
    height = 630
    img = QImage(width, height, QImage.Format.Format_ARGB32)
    img.fill(QColor(8, 12, 21))

    painter = QPainter(img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

    # 1. Dark cosmic radial gradient background
    rad_grad = QRadialGradient(width / 2, height / 2 - 40, 600)
    rad_grad.setColorAt(0.0, QColor(15, 23, 42, 255))
    rad_grad.setColorAt(0.5, QColor(11, 17, 32, 255))
    rad_grad.setColorAt(1.0, QColor(8, 12, 21, 255))
    painter.setBrush(QBrush(rad_grad))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRect(0, 0, width, height)

    # Ambient cyan glow in background
    glow_grad = QRadialGradient(width / 2, height / 2 - 30, 320)
    glow_grad.setColorAt(0.0, QColor(2, 132, 199, 45))
    glow_grad.setColorAt(0.7, QColor(34, 211, 238, 15))
    glow_grad.setColorAt(1.0, QColor(8, 12, 21, 0))
    painter.setBrush(QBrush(glow_grad))
    painter.drawEllipse(int(width / 2 - 400), int(height / 2 - 350), 800, 700)

    # Subtle cyan border around image
    painter.setPen(QPen(QColor(56, 189, 248, 70), 3))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawRoundedRect(12, 12, width - 24, height - 24, 20, 20)

    # 2. Glowing Drop Badge
    badge_rect = QRectF(width / 2 - 42, 60, 84, 84)
    badge_grad = QLinearGradient(badge_rect.topLeft(), badge_rect.bottomRight())
    badge_grad.setColorAt(0.0, QColor(2, 132, 199, 240))
    badge_grad.setColorAt(1.0, QColor(34, 211, 238, 240))
    painter.setBrush(QBrush(badge_grad))
    painter.setPen(QPen(QColor(56, 189, 248, 200), 2))
    painter.drawRoundedRect(badge_rect, 24, 24)

    # Water drop icon
    f_drop = QFont("Segoe UI Emoji", 36)
    painter.setFont(f_drop)
    painter.setPen(QColor(255, 255, 255))
    painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, "💧")

    # 3. Main Title
    f_title = QFont("Segoe UI", 48, QFont.Weight.Bold)
    f_title.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1)
    painter.setFont(f_title)
    painter.setPen(QColor(248, 250, 252))
    painter.drawText(QRectF(0, 165, width, 65), Qt.AlignmentFlag.AlignCenter, "Companion Hub")

    # Version Pill
    v_pill_rect = QRectF(width / 2 - 70, 242, 140, 30)
    painter.setBrush(QColor(34, 211, 238, 30))
    painter.setPen(QPen(QColor(56, 189, 248, 120), 1.5))
    painter.drawRoundedRect(v_pill_rect, 15, 15)
    f_pill = QFont("Segoe UI", 12, QFont.Weight.Bold)
    painter.setFont(f_pill)
    painter.setPen(QColor(56, 189, 248))
    painter.drawText(v_pill_rect, Qt.AlignmentFlag.AlignCenter, "v2.0 UNIVERSAL")

    # 4. Tagline & Description
    f_desc = QFont("Segoe UI", 20, QFont.Weight.DemiBold)
    painter.setFont(f_desc)
    painter.setPen(QColor(203, 213, 225))
    painter.drawText(QRectF(80, 290, width - 160, 40), Qt.AlignmentFlag.AlignCenter, "Interactive Desktop Pet & Hydration Coach")

    f_sub = QFont("Segoe UI", 15)
    painter.setFont(f_sub)
    painter.setPen(QColor(148, 163, 184))
    painter.drawText(QRectF(80, 335, width - 160, 30), Qt.AlignmentFlag.AlignCenter, "Walks quietly on your screen • Daily water goal tracker • Meeting mode • Custom avatars")

    # 5. Pixel Mascot Characters Preview
    f_chars = QFont("Segoe UI Emoji", 26)
    painter.setFont(f_chars)
    painter.setPen(QColor(255, 255, 255))
    painter.drawText(QRectF(80, 385, width - 160, 50), Qt.AlignmentFlag.AlignCenter, "🧢   🐱   🤖   💧   🐸   👻")

    # 6. Supported Platform Badges
    platforms = [
        ("💻 Windows 10 / 11", 160),
        ("📱 Android Phone", 420),
        ("🍏 Apple macOS", 680),
        ("📱 Apple iOS", 910)
    ]
    f_badge = QFont("Segoe UI", 13, QFont.Weight.DemiBold)
    painter.setFont(f_badge)
    for name, x in platforms:
        p_rect = QRectF(x, 460, 190, 42)
        painter.setBrush(QColor(17, 24, 39, 220))
        painter.setPen(QPen(QColor(56, 189, 248, 80), 1.5))
        painter.drawRoundedRect(p_rect, 10, 10)
        painter.setPen(QColor(226, 232, 240))
        painter.drawText(p_rect, Qt.AlignmentFlag.AlignCenter, name)

    # 7. Domain Footer
    f_url = QFont("Segoe UI", 14, QFont.Weight.Bold)
    painter.setFont(f_url)
    painter.setPen(QColor(56, 189, 248))
    painter.drawText(QRectF(0, 545, width, 30), Qt.AlignmentFlag.AlignCenter, "https://mycompanionhub.web.app")

    painter.end()
    out_path = os.path.join(PUBLIC_ASSETS, "og-image.png")
    img.save(out_path, "PNG")
    print(f"Saved OG Image to {out_path} ({os.path.getsize(out_path)} bytes)")

def create_apple_touch_icon():
    size = 180
    img = QImage(size, size, QImage.Format.Format_ARGB32)
    img.fill(QColor(8, 12, 21))

    painter = QPainter(img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    
    grad = QLinearGradient(0, 0, size, size)
    grad.setColorAt(0.0, QColor(2, 132, 199))
    grad.setColorAt(1.0, QColor(34, 211, 238))
    painter.setBrush(QBrush(grad))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, size, size, 40, 40)

    f_drop = QFont("Segoe UI Emoji", 84)
    painter.setFont(f_drop)
    painter.setPen(QColor(255, 255, 255))
    painter.drawText(QRectF(0, 0, size, size), Qt.AlignmentFlag.AlignCenter, "💧")
    painter.end()

    out_path = os.path.join(PUBLIC_ASSETS, "apple-touch-icon.png")
    img.save(out_path, "PNG")
    print(f"Saved Apple Touch Icon to {out_path}")

if __name__ == "__main__":
    from PyQt6.QtGui import QGuiApplication
    app = QGuiApplication(sys.argv)
    create_og_image()
    create_apple_touch_icon()
