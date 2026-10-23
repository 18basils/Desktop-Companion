"""
Generate Free Community Avatar Pack for Desktop Companion
Creates 8 animated, transparent pixel art GIFs and packages them
into public/downloads/Companion-Avatar-Pack.zip along with an automated
1-click installer (Install-Avatars.bat).
"""

import os
import shutil
import zipfile
from PIL import Image, ImageDraw

PACK_DIR = os.path.join(os.path.dirname(__file__), "avatar_pack")
AVATARS_DIR = os.path.join(PACK_DIR, "avatars")
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "public", "downloads")
ZIP_OUT = os.path.join(DOWNLOADS_DIR, "Companion-Avatar-Pack.zip")

os.makedirs(AVATARS_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

W, H = 64, 64

def create_shiba_gif():
    frames = []
    for step in range(6):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        bob = 1 if step in (1, 4) else 0
        leg = 3 if step in (1, 2) else (-3 if step in (4, 5) else 0)

        # Body
        d.rectangle([20, 28 + bob, 44, 46 + bob], fill=(217, 119, 6, 255))
        d.rectangle([24, 32 + bob, 38, 44 + bob], fill=(254, 243, 199, 255))
        # Head
        d.rectangle([28, 16 + bob, 46, 32 + bob], fill=(245, 158, 11, 255))
        # Ears
        d.polygon([(30, 16 + bob), (34, 8 + bob), (38, 16 + bob)], fill=(180, 83, 9, 255))
        d.polygon([(40, 16 + bob), (44, 8 + bob), (48, 16 + bob)], fill=(180, 83, 9, 255))
        # Snout & Nose
        d.rectangle([40, 24 + bob, 48, 30 + bob], fill=(254, 243, 199, 255))
        d.rectangle([46, 25 + bob, 49, 28 + bob], fill=(15, 23, 42, 255))
        # Eye
        d.rectangle([34, 20 + bob, 37, 23 + bob], fill=(15, 23, 42, 255))
        d.rectangle([34, 20 + bob, 35, 21 + bob], fill=(255, 255, 255, 255))
        # Curly Tail
        tail_w = (step % 3) * 2
        d.polygon([(18, 30 + bob), (14, 22 + bob - tail_w), (19, 24 + bob)], fill=(217, 119, 6, 255))
        # Paws
        d.rectangle([23, 46 + leg, 28, 56 + leg], fill=(180, 83, 9, 255))
        d.rectangle([36, 46 - leg, 41, 56 - leg], fill=(180, 83, 9, 255))
        frames.append(img)
    frames[0].save(os.path.join(AVATARS_DIR, "shiba_inu.gif"), save_all=True, append_images=frames[1:], duration=120, loop=0, transparency=0, disposal=2)

def create_dragon_gif():
    frames = []
    for step in range(6):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        wing_y = -4 if step in (1, 2) else (2 if step in (4, 5) else 0)
        bob = 1 if step in (0, 3) else 0

        # Body & Belly
        d.rectangle([22, 28 + bob, 42, 46 + bob], fill=(16, 185, 129, 255))
        d.rectangle([28, 34 + bob, 38, 44 + bob], fill=(254, 240, 138, 255))
        # Head & Horns
        d.rectangle([28, 16 + bob, 48, 30 + bob], fill=(52, 211, 153, 255))
        d.polygon([(30, 16 + bob), (28, 8 + bob), (34, 16 + bob)], fill=(245, 158, 11, 255))
        d.polygon([(36, 16 + bob), (35, 10 + bob), (40, 16 + bob)], fill=(245, 158, 11, 255))
        # Snout & Eye
        d.rectangle([46, 22 + bob, 52, 28 + bob], fill=(52, 211, 153, 255))
        d.rectangle([38, 18 + bob, 42, 22 + bob], fill=(15, 23, 42, 255))
        d.rectangle([39, 19 + bob, 40, 20 + bob], fill=(255, 255, 255, 255))
        # Wings
        d.polygon([(24, 28 + bob), (12, 14 + wing_y), (30, 22 + wing_y)], fill=(245, 158, 11, 255))
        # Tail with flame
        d.rectangle([14, 38 + bob, 22, 42 + bob], fill=(16, 185, 129, 255))
        d.rectangle([10, 36 + bob, 14, 40 + bob], fill=(239, 68, 68, 255))
        # Feet
        d.rectangle([24, 46 + bob, 29, 54 + bob], fill=(5, 150, 105, 255))
        d.rectangle([35, 46 + bob, 40, 54 + bob], fill=(5, 150, 105, 255))
        frames.append(img)
    frames[0].save(os.path.join(AVATARS_DIR, "baby_dragon.gif"), save_all=True, append_images=frames[1:], duration=130, loop=0, transparency=0, disposal=2)

def create_panda_gif():
    frames = []
    for step in range(6):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        bob = -2 if step in (1, 2) else (1 if step in (4, 5) else 0)

        # White Body
        d.rectangle([20, 28 + bob, 44, 48 + bob], fill=(248, 250, 252, 255))
        # Black Arms / Shoulders
        d.rectangle([18, 30 + bob, 24, 42 + bob], fill=(15, 23, 42, 255))
        d.rectangle([40, 30 + bob, 46, 42 + bob], fill=(15, 23, 42, 255))
        # Head
        d.rectangle([22, 14 + bob, 42, 30 + bob], fill=(248, 250, 252, 255))
        # Black Ears
        d.rectangle([18, 10 + bob, 24, 16 + bob], fill=(15, 23, 42, 255))
        d.rectangle([40, 10 + bob, 46, 16 + bob], fill=(15, 23, 42, 255))
        # Eye Patches
        d.rectangle([25, 18 + bob, 30, 24 + bob], fill=(15, 23, 42, 255))
        d.rectangle([34, 18 + bob, 39, 24 + bob], fill=(15, 23, 42, 255))
        d.rectangle([27, 20 + bob, 29, 22 + bob], fill=(255, 255, 255, 255))
        d.rectangle([35, 20 + bob, 37, 22 + bob], fill=(255, 255, 255, 255))
        # Black Nose & Rosy Cheeks
        d.rectangle([31, 24 + bob, 33, 26 + bob], fill=(15, 23, 42, 255))
        d.rectangle([23, 25 + bob, 26, 27 + bob], fill=(251, 113, 133, 200))
        d.rectangle([38, 25 + bob, 41, 27 + bob], fill=(251, 113, 133, 200))
        # Feet
        d.rectangle([23, 48 + bob, 29, 56 + bob], fill=(15, 23, 42, 255))
        d.rectangle([35, 48 + bob, 41, 56 + bob], fill=(15, 23, 42, 255))
        frames.append(img)
    frames[0].save(os.path.join(AVATARS_DIR, "bouncing_panda.gif"), save_all=True, append_images=frames[1:], duration=140, loop=0, transparency=0, disposal=2)

def create_penguin_gif():
    frames = []
    for step in range(6):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        waddle = 2 if step in (1, 2) else (-2 if step in (4, 5) else 0)

        # Body
        d.rectangle([22 + waddle, 22, 42 + waddle, 48], fill=(15, 23, 42, 255))
        # White Belly
        d.rectangle([26 + waddle, 26, 38 + waddle, 46], fill=(248, 250, 252, 255))
        # Head
        d.rectangle([24 + waddle, 12, 40 + waddle, 24], fill=(15, 23, 42, 255))
        # Beak
        d.rectangle([30 + waddle, 18, 36 + waddle, 22], fill=(249, 115, 22, 255))
        # Eyes
        d.rectangle([27 + waddle, 15, 29 + waddle, 18], fill=(255, 255, 255, 255))
        d.rectangle([35 + waddle, 15, 37 + waddle, 18], fill=(255, 255, 255, 255))
        # Flippers
        flap_l = -3 if step in (1, 2) else 0
        flap_r = -3 if step in (4, 5) else 0
        d.rectangle([18 + waddle, 26 + flap_l, 22 + waddle, 40 + flap_l], fill=(30, 41, 59, 255))
        d.rectangle([42 + waddle, 26 + flap_r, 46 + waddle, 40 + flap_r], fill=(30, 41, 59, 255))
        # Feet
        d.rectangle([24, 48, 30, 53], fill=(249, 115, 22, 255))
        d.rectangle([34, 48, 40, 53], fill=(249, 115, 22, 255))
        frames.append(img)
    frames[0].save(os.path.join(AVATARS_DIR, "waddling_penguin.gif"), save_all=True, append_images=frames[1:], duration=120, loop=0, transparency=0, disposal=2)

def create_capybara_gif():
    frames = []
    for step in range(6):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        bob = 1 if step in (1, 4) else 0
        leg = 2 if step in (1, 2) else (-2 if step in (4, 5) else 0)

        # Body
        d.rectangle([18, 28 + bob, 44, 46 + bob], fill=(146, 64, 14, 255))
        # Snout / Head
        d.rectangle([36, 22 + bob, 52, 38 + bob], fill=(180, 83, 9, 255))
        # Ears
        d.rectangle([34, 20 + bob, 38, 24 + bob], fill=(120, 53, 15, 255))
        # Nose & Eye (chill half-closed)
        d.rectangle([48, 28 + bob, 52, 32 + bob], fill=(15, 23, 42, 255))
        d.line([(40, 26 + bob), (44, 26 + bob)], fill=(15, 23, 42, 255), width=2)
        # Orange on Head! (Classic Capybara meme)
        d.ellipse([40, 13 + bob, 48, 21 + bob], fill=(249, 115, 22, 255))
        d.rectangle([43, 11 + bob, 45, 13 + bob], fill=(34, 197, 94, 255)) # green leaf
        # Legs
        d.rectangle([21, 46 + leg, 26, 55 + leg], fill=(120, 53, 15, 255))
        d.rectangle([37, 46 - leg, 42, 55 - leg], fill=(120, 53, 15, 255))
        frames.append(img)
    frames[0].save(os.path.join(AVATARS_DIR, "chill_capybara.gif"), save_all=True, append_images=frames[1:], duration=150, loop=0, transparency=0, disposal=2)

def create_axolotl_gif():
    frames = []
    for step in range(6):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        gill_w = 2 if step in (1, 2) else (-1 if step in (4, 5) else 0)
        bob = -1 if step in (0, 3) else 1

        # Pink Body
        d.rectangle([22, 26 + bob, 42, 46 + bob], fill=(244, 114, 182, 255))
        # Big Smiling Head
        d.rectangle([20, 16 + bob, 44, 32 + bob], fill=(249, 168, 212, 255))
        # Feathery Frilly Gills (left & right)
        d.polygon([(20, 20 + bob), (10 - gill_w, 14 + bob), (18, 24 + bob)], fill=(236, 72, 153, 255))
        d.polygon([(20, 24 + bob), (8 - gill_w, 24 + bob), (18, 28 + bob)], fill=(236, 72, 153, 255))
        d.polygon([(44, 20 + bob), (54 + gill_w, 14 + bob), (46, 24 + bob)], fill=(236, 72, 153, 255))
        d.polygon([(44, 24 + bob), (56 + gill_w, 24 + bob), (46, 28 + bob)], fill=(236, 72, 153, 255))
        # Cute Eyes & Smile
        d.rectangle([26, 22 + bob, 29, 25 + bob], fill=(15, 23, 42, 255))
        d.rectangle([35, 22 + bob, 38, 25 + bob], fill=(15, 23, 42, 255))
        d.rectangle([29, 27 + bob, 35, 29 + bob], fill=(190, 24, 93, 255))
        # Water bubble floating up
        bubble_y = (step * 8) % 40
        d.ellipse([46, 42 - bubble_y, 52, 48 - bubble_y], outline=(56, 189, 248, 220), width=1)
        # Feet
        d.rectangle([24, 46 + bob, 29, 53 + bob], fill=(236, 72, 153, 255))
        d.rectangle([35, 46 + bob, 40, 53 + bob], fill=(236, 72, 153, 255))
        frames.append(img)
    frames[0].save(os.path.join(AVATARS_DIR, "pink_axolotl.gif"), save_all=True, append_images=frames[1:], duration=130, loop=0, transparency=0, disposal=2)

def create_star_gif():
    frames = []
    for step in range(6):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        glow = (step % 3) * 2

        # Golden 8-bit Star
        d.polygon([
            (32, 10 - glow), (37, 24), (52, 24),
            (40, 34), (45, 48 + glow), (32, 39),
            (19, 48 + glow), (24, 34), (12, 24), (27, 24)
        ], fill=(250, 204, 21, 255), outline=(217, 119, 6, 255))
        # Cute Eyes
        d.rectangle([28, 28, 30, 33], fill=(15, 23, 42, 255))
        d.rectangle([34, 28, 36, 33], fill=(15, 23, 42, 255))
        # Sparkles
        sp_x = (step * 11) % 50 + 7
        sp_y = (step * 17) % 40 + 10
        d.rectangle([sp_x, sp_y, sp_x + 2, sp_y + 2], fill=(255, 255, 255, 255))
        frames.append(img)
    frames[0].save(os.path.join(AVATARS_DIR, "golden_star.gif"), save_all=True, append_images=frames[1:], duration=110, loop=0, transparency=0, disposal=2)

def create_potion_gif():
    frames = []
    for step in range(6):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        liquid_glow = 10 if step in (1, 2) else (-10 if step in (4, 5) else 0)

        # Cork
        d.rectangle([28, 12, 36, 17], fill=(180, 83, 9, 255))
        # Glass Neck
        d.rectangle([29, 17, 35, 23], fill=(203, 213, 225, 180))
        # Glass Flask Bottle Body
        d.polygon([(29, 23), (16, 44), (48, 44), (35, 23)], fill=(203, 213, 225, 120))
        # Glowing Water / Hydration Potion
        d.polygon([(27, 28), (17, 43), (47, 43), (37, 28)], fill=(14, 165, 233, 220))
        # Bubbles rising
        b1_y = 40 - ((step * 4) % 14)
        b2_y = 38 - (((step + 2) * 5) % 12)
        d.ellipse([26, b1_y, 29, b1_y + 3], fill=(255, 255, 255, 240))
        d.ellipse([34, b2_y, 36, b2_y + 2], fill=(255, 255, 255, 240))
        # Glass shine highlight
        d.line([(22, 34), (20, 42)], fill=(255, 255, 255, 200), width=2)
        frames.append(img)
    frames[0].save(os.path.join(AVATARS_DIR, "magic_potion.gif"), save_all=True, append_images=frames[1:], duration=120, loop=0, transparency=0, disposal=2)

def create_installers_and_zip():
    # 1. Create Install-Avatars.bat
    bat_content = """@echo off
chcp 65001 >nul
title Desktop Companion - Community Avatar Pack Installer
color 0B
echo ======================================================================
echo    Desktop Companion - Free Community Avatar Pack (8 Mascots)
echo ======================================================================
echo.
echo Installing new animated avatars into your existing Desktop Companion...
echo NOTE: Your personal username, water goals, and schedules will remain 100%% INTACT!
echo.

set "TARGET_DIR=%LOCALAPPDATA%\\Programs\\Desktop Companion\\assets\\custom_avatars"
if not exist "%LOCALAPPDATA%\\Programs\\Desktop Companion" (
    if exist "..\\assets\\custom_avatars" (
        set "TARGET_DIR=..\\assets\\custom_avatars"
    ) else if exist "assets\\custom_avatars" (
        set "TARGET_DIR=assets\\custom_avatars"
    )
)

if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

echo Copying animated avatars to:
echo "%TARGET_DIR%"
echo.
xcopy /Y /Q "avatars\\*.gif" "%TARGET_DIR%\\" >nul

if %ERRORLEVEL% EQU 0 (
    echo ======================================================================
    echo   SUCCESS! 8 New Avatars Have Been Added to Your Companion!
    echo ======================================================================
    echo.
    echo Newly installed characters:
    echo   - Shiba Inu Puppy (shiba_inu.gif)
    echo   - Baby Dragon (baby_dragon.gif)
    echo   - Bouncing Panda (bouncing_panda.gif)
    echo   - Waddling Penguin (waddling_penguin.gif)
    echo   - Chill Capybara with Orange (chill_capybara.gif)
    echo   - Pink Smiling Axolotl (pink_axolotl.gif)
    echo   - Twinkling Golden Star (golden_star.gif)
    echo   - Magic Hydration Potion (magic_potion.gif)
    echo.
    echo HOW TO USE IN APP:
    echo   1. Right-click the blue 💧 Water Droplet in your taskbar tray.
    echo   2. Go to "Avatars & Skins" - your new pets will be listed under Custom!
    echo   3. Or turn on "Dynamic" and the companion will cycle through them!
    echo.
) else (
    echo [ERROR] Could not automatically locate Desktop Companion folder.
    echo Please copy the files in the "avatars" folder manually into:
    echo "%LOCALAPPDATA%\\Programs\\Desktop Companion\\assets\\custom_avatars"
)
echo.
pause
"""
    with open(os.path.join(PACK_DIR, "Install-Avatars.bat"), "w", encoding="utf-8") as f:
        f.write(bat_content)

    # 2. Create README.txt
    readme_content = """COMMUNITY AVATAR PACK (8 NEW MASCOTS)
=====================================
For Desktop Companion (Windows, Mac, Android, iOS)

INCLUDED PETS:
1. shiba_inu.gif       - Energetic golden Shiba Inu with wagging tail
2. baby_dragon.gif     - Tiny emerald dragon with flapping wings
3. bouncing_panda.gif  - Chubby panda that bounces with delight
4. waddling_penguin.gif- Antarctic tuxedo penguin
5. chill_capybara.gif  - Super chill capybara balancing an orange
6. pink_axolotl.gif    - Smiling aquatic axolotl with water bubbles
7. golden_star.gif     - Retro glowing 8-bit star
8. magic_potion.gif    - Animated bubbling cyan hydration potion

HOW TO INSTALL ON WINDOWS:
Method 1 (Automatic 1-Click):
  Simply double-click 'Install-Avatars.bat'. It will automatically copy all
  avatars to your existing installation without modifying your settings!

Method 2 (Manual Drag-and-Drop):
  1. Open Desktop Companion.
  2. Right-click the 💧 tray icon > Settings... > Avatars tab.
  3. Click 'Open Avatar Folder'.
  4. Drag and drop all .gif files from the 'avatars' folder into it.
  5. Done! Your new avatars appear immediately under 'Avatars & Skins'.

NOTE:
This expansion pack preserves your name, cups tracker, schedule, and quiet
hours. No reinstallation needed!
"""
    with open(os.path.join(PACK_DIR, "README.txt"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 3. Create Companion-Avatar-Pack.zip
    print(f"Creating zip bundle: {ZIP_OUT}...")
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add batch file & README
        zf.write(os.path.join(PACK_DIR, "Install-Avatars.bat"), "Install-Avatars.bat")
        zf.write(os.path.join(PACK_DIR, "README.txt"), "README.txt")
        # Add avatar gifs
        for file in os.listdir(AVATARS_DIR):
            if file.endswith(".gif"):
                full_p = os.path.join(AVATARS_DIR, file)
                zf.write(full_p, os.path.join("avatars", file))

    print(f"--> Done! Pack generated at {ZIP_OUT} ({os.path.getsize(ZIP_OUT):,} bytes)")

if __name__ == "__main__":
    print("Generating animated avatars...")
    create_shiba_gif()
    create_dragon_gif()
    create_panda_gif()
    create_penguin_gif()
    create_capybara_gif()
    create_axolotl_gif()
    create_star_gif()
    create_potion_gif()
    create_installers_and_zip()
