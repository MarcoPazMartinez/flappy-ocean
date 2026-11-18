# -*- mode: python ; coding: utf-8 -*-
# Receta de PyInstaller para generar FlappyDiver.exe (un solo archivo, sin consola).
# Se usa con:  pyinstaller FlappyDiver.spec

a = Analysis(
    ["src/main.py"],
    pathex=["src"],
    binaries=[],
    datas=[
        ("assets/images", "assets/images"),
        ("assets/sounds", "assets/sounds"),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="FlappyDiver",
    debug=False,
    strip=False,
    upx=False,              # UPX hace que los antivirus desconfien mas
    console=False,          # sin ventana negra de consola
    icon="assets/icono.ico",
)
