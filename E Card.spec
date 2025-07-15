# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ecarddemo.py'],
    pathex=[],
    binaries=[],
    datas=[('emperor.jpg', '.'), ('slave.jpg', '.'), ('citizen.jpg', '.'), ('back.jpg', '.'), ('flip.wav', '.'), ('win.wav', '.'), ('lose.wav', '.'), ('draw.wav', '.'), ('click.wav', '.'), ('theme.wav', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='E Card',
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
    icon=['icon.ico'],
)
