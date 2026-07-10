# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_scanner.py'],  # Use the root-level entry point
    pathex=[],
    binaries=[],
    datas=[
        ('src/document_scanner/*.py', 'document_scanner'),  # Include all Python files
    ],
    hiddenimports=[
        'cv2',
        'numpy', 
        'fire',
        'document_scanner',
        'document_scanner.scanner',
        'document_scanner.utils',
        'document_scanner.main',
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
    name='czur-scanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)