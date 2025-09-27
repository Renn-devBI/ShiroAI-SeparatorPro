import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_dependencies():
    """Install dependencies needed for PyInstaller"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "auto-py-to-exe"])

def build_with_pyinstaller():
    """Build executable using PyInstaller"""
    # Create spec file content
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

datas = []
datas.extend(collect_all('spleeter'))
datas.extend(collect_all('customtkinter'))
datas.extend(collect_all('pygame'))
datas.extend(collect_all('mutagen'))
datas.extend(collect_all('PIL'))

a = Analysis(
    ['vocaloffline.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'spleeter',
        'customtkinter',
        'pygame',
        'mutagen',
        'PIL',
        'tkinter',
        'numpy',
        'tensorflow',
        'librosa',
        'requests'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ShiroAI_Separator_Pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='yukichibi.ico',
)
"""

    # Write spec file
    with open('shiroai.spec', 'w') as f:
        f.write(spec_content)
    
    # Run PyInstaller
    subprocess.check_call([sys.executable, "-m", "PyInstaller", "shiroai.spec", "--clean"])

def build_with_auto_py_to_exe():
    """Build using auto-py-to-exe (GUI)"""
    subprocess.check_call([sys.executable, "-m", "auto_py_to_exe"])

def main():
    """Main function"""
    print("🚀 ShiroAI Separator Pro - Executable Builder")
    print("1. Build with PyInstaller (command line)")
    print("2. Build with Auto PY to EXE (GUI)")
    
    choice = input("Select option (1 or 2): ").strip()
    
    if choice == "1":
        print("Installing dependencies...")
        install_dependencies()
        print("Building executable with PyInstaller...")
        build_with_pyinstaller()
        print("✅ Build completed! Check the 'dist' folder.")
    elif choice == "2":
        print("Launching Auto PY to EXE GUI...")
        build_with_auto_py_to_exe()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()