
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
    hooksconfig={},
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
