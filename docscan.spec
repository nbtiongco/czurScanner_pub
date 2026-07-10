# -*- mode: python ; coding: utf-8 -*-

<<<<<<< HEAD

=======
block_cipher = None

# Analysis: Find all dependencies
>>>>>>> bd4fb053864653a911bed27bc922e7588e194398
a = Analysis(
    ['src/document_scanner/main.py'],
    pathex=['src'],
    binaries=[],
<<<<<<< HEAD
    datas=[('src/document_scanner/', 'document_scanner')],
    hiddenimports=[],
=======
    datas=[
        ('src/document_scanner/*.py', 'document_scanner'),
    ],
    hiddenimports=[
        'cv2',
        'numpy',
        'fire',
        'document_scanner',
        'document_scanner.scanner',
        'document_scanner.utils',
    ],
>>>>>>> bd4fb053864653a911bed27bc922e7588e194398
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
<<<<<<< HEAD
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

=======
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ: Python archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE: Executable
>>>>>>> bd4fb053864653a911bed27bc922e7588e194398
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
<<<<<<< HEAD
=======
    a.zipfiles,
>>>>>>> bd4fb053864653a911bed27bc922e7588e194398
    a.datas,
    [],
    name='docscan',
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
<<<<<<< HEAD
)
=======
)
>>>>>>> bd4fb053864653a911bed27bc922e7588e194398
