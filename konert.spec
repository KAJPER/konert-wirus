# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['konert.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'win32gui',
        'win32con',
        'win32api',
        'win32process',
        'wmi',
        'requests',
        'json',
        'logging',
        'pathlib',
        'ctypes',
        'subprocess',
        'winreg',
        'urllib3',
        'idna',
        'chardet',
        'base64'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WindowsSecurityService',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon='Windows.ico',
    version='file_version_info.txt'
) 