# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['vocaloffline.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('yukichibi.ico', '.'),
        # Jika ada file konfigurasi atau aset lainnya, tambahkan di sini
    ],
    hiddenimports=[
        'pygame',
        'mutagen',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'customtkinter',
        'spleeter',
        'spleeter.separator',
        'spleeter.audio.adapter',
        'spleeter.utils.configuration',
        'tkinter',
        'queue',
        'json',
        'threading',
        'tempfile',
        'shutil',
        'time',
        'gc',
        'pathlib',
        'os',
        'sys',
        're',
        'io',
        'subprocess'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ShiroAIvoc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Changed to False untuk menyembunyikan console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='yukichibi.ico',  # Menambahkan icon
)