#!/usr/bin/env python3
"""
Desktop Companion - Complete Windows Build Automation Script
Rebuilds the entire Windows distribution chain on a clean machine:
  1. Desktop Companion executable & dependencies (via Desktop Companion.spec)
  2. app_payload.zip (bundled payload for installer)
  3. Uninstall Desktop Companion wizard (via Uninstall Desktop Companion.spec)
  4. Desktop Companion Setup wizard (via Desktop Companion Setup.spec)
  5. public/downloads/Desktop-Companion-Windows.zip (for Firebase Hosting distribution)
"""

import os
import sys
import shutil
import zipfile
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_pyinstaller_cmd():
    venv_pyinstaller = os.path.join(ROOT_DIR, ".venv", "Scripts", "pyinstaller.exe")
    if os.path.exists(venv_pyinstaller):
        return [venv_pyinstaller]
    venv_py = os.path.join(ROOT_DIR, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_py):
        return [venv_py, "-m", "PyInstaller"]
    return [sys.executable, "-m", "PyInstaller"]

def run_cmd(args):
    print(f"\n--> Running: {' '.join(args)}")
    res = subprocess.run(args, cwd=ROOT_DIR)
    if res.returncode != 0:
        print(f"FAILED with return code: {res.returncode}")
        sys.exit(res.returncode)

def main():
    print("=" * 60)
    print("  Building Desktop Companion Windows Distribution Chain")
    print("=" * 60)

    pyinstaller_base = get_pyinstaller_cmd()

    # 1. Build Desktop Companion application folder
    print("\n[Step 1/5] Building main Desktop Companion binaries...")
    run_cmd(pyinstaller_base + ["--clean", "--noconfirm", "Desktop Companion.spec"])

    # 2. Package into app_payload.zip
    print("\n[Step 2/5] Creating app_payload.zip from dist/Desktop Companion...")
    dist_app = os.path.join(ROOT_DIR, "dist", "Desktop Companion")
    payload_zip = os.path.join(ROOT_DIR, "app_payload.zip")
    if os.path.exists(payload_zip):
        os.remove(payload_zip)

    with zipfile.ZipFile(payload_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(dist_app):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, dist_app)
                zf.write(full_path, rel_path)
    print(f"Created: {payload_zip} ({os.path.getsize(payload_zip):,} bytes)")

    # 3. Build Uninstaller wizard
    print("\n[Step 3/5] Building Uninstaller wizard...")
    run_cmd(pyinstaller_base + ["--clean", "--noconfirm", "Uninstall Desktop Companion.spec"])

    # 4. Build Standalone Installer wizard
    print("\n[Step 4/5] Building Desktop Companion Setup.exe...")
    run_cmd(pyinstaller_base + ["--clean", "--noconfirm", "Desktop Companion Setup.spec"])

    # 5. Package for Firebase Hosting
    print("\n[Step 5/5] Packaging into public/downloads/Desktop-Companion-Windows.zip...")
    downloads_dir = os.path.join(ROOT_DIR, "public", "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    setup_exe = os.path.join(ROOT_DIR, "dist", "Desktop Companion Setup.exe")
    final_zip = os.path.join(downloads_dir, "Desktop-Companion-Windows.zip")

    if os.path.exists(setup_exe):
        with zipfile.ZipFile(final_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(setup_exe, "Desktop Companion Setup.exe")
        print(f"Created: {final_zip} ({os.path.getsize(final_zip):,} bytes)")
    else:
        print(f"Warning: {setup_exe} not found!")

    print("\n" + "=" * 60)
    print("  Build complete! All Windows deliverables updated.")
    print("=" * 60)

if __name__ == "__main__":
    main()
