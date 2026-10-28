#!/usr/bin/env python3
"""
================================================================================
OPEN GRAPH 1200x630 BANNER GENERATOR TEMPLATE
================================================================================
Generates a high-contrast, modern Open Graph banner (1200 x 630 px) with safe-zone
padding, customizable branding, gradient backgrounds, and optimized file size (<300 KB)
compatible with WhatsApp, Twitter/X, Facebook, LinkedIn, Slack, and Discord.

Requirements:
    pip install pillow

Usage:
    python generate_og_banner.template.py
================================================================================
"""

import os
from PIL import Image, ImageDraw, ImageFont

def generate_og_banner(
    output_path="og-image.png",
    title="Your Product Title",
    subtitle="Your catchphrase or primary value proposition goes here",
    tagline="Key feature 1 • Key feature 2 • Key feature 3",
    pill_text="v1.0 UNIVERSAL",
    primary_color=(56, 189, 248),    # Neon Cyan
    accent_color=(2, 132, 199),     # Deep Sky Blue
    bg_color_top=(15, 23, 42),       # Dark Slate Navy
    bg_color_bottom=(8, 12, 21),     # Cosmic Black
):
    width = 1200
    height = 630

    # 1. Create base RGB image
    img = Image.new("RGBA", (width, height), bg_color_top)
    draw = ImageDraw.Draw(img)

    # 2. Draw smooth vertical dark gradient
    for y in range(height):
        ratio = y / float(height)
        r = int(bg_color_top[0] * (1 - ratio) + bg_color_bottom[0] * ratio)
        g = int(bg_color_top[1] * (1 - ratio) + bg_color_bottom[1] * ratio)
        b = int(bg_color_top[2] * (1 - ratio) + bg_color_bottom[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # 3. Ambient glow ellipse in center
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for radius in range(350, 0, -25):
        alpha = int((1 - (radius / 350.0)) * 35)
        glow_draw.ellipse(
            [(width // 2 - radius, height // 2 - radius - 20),
             (width // 2 + radius, height // 2 + radius - 20)],
            fill=(accent_color[0], accent_color[1], accent_color[2], alpha)
        )
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # 4. Subtle Outer Border (Safe frame)
    draw.rounded_rectangle(
        [(16, 16), (width - 16, height - 16)],
        radius=20,
        outline=(primary_color[0], primary_color[1], primary_color[2], 80),
        width=2
    )

    # 5. Load fonts with fallback to default
    def get_font(size, bold=False):
        font_names = [
            "Segoe UI Bold.ttf" if bold else "Segoe UI.ttf",
            "Arial Bold.ttf" if bold else "Arial.ttf",
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
            "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf"
        ]
        for name in font_names:
            try:
                return ImageFont.truetype(name, size)
            except IOError:
                continue
        return ImageFont.load_default()

    font_title = get_font(52, bold=True)
    font_pill = get_font(13, bold=True)
    font_subtitle = get_font(22, bold=True)
    font_tagline = get_font(16, bold=False)

    # 6. Draw Version / Category Pill Badge
    pill_w = 150
    pill_h = 32
    pill_x = (width - pill_w) // 2
    pill_y = 100
    draw.rounded_rectangle(
        [(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)],
        radius=16,
        fill=(primary_color[0], primary_color[1], primary_color[2], 30),
        outline=(primary_color[0], primary_color[1], primary_color[2], 180),
        width=1
    )
    # Center pill text
    draw.text((width // 2, pill_y + 8), pill_text, fill=primary_color, font=font_pill, anchor="mm")

    # 7. Draw Main Title (Bold, Center)
    title_y = 220
    draw.text((width // 2, title_y), title, fill=(248, 250, 252), font=font_title, anchor="mm")

    # 8. Draw Subtitle (Center)
    sub_y = 300
    draw.text((width // 2, sub_y), subtitle, fill=(203, 213, 225), font=font_subtitle, anchor="mm")

    # 9. Draw Tagline / Features (Center)
    tag_y = 360
    draw.text((width // 2, tag_y), tagline, fill=(148, 163, 184), font=font_tagline, anchor="mm")

    # 10. Accent Line Underneath
    line_w = 300
    line_x = (width - line_w) // 2
    line_y = 420
    draw.line([(line_x, line_y), (line_x + line_w, line_y)], fill=(primary_color[0], primary_color[1], primary_color[2], 120), width=2)

    # 11. Convert to RGB and Save with Optimization (<300 KB)
    final_img = img.convert("RGB")
    final_img.save(output_path, "PNG", optimize=True)
    file_size_kb = os.path.getsize(output_path) / 1024.0

    print(f"[OK] Open Graph Banner generated: {output_path}")
    print(f"     Resolution: {width} x {height} px")
    print(f"     File Size:  {file_size_kb:.1f} KB (Target < 300 KB: {'PASS' if file_size_kb < 300 else 'WARN'})")

if __name__ == "__main__":
    generate_og_banner(output_path="og-image-sample.png")
