# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('haarcascade_frontalface_default.xml', '.'), ('cidlogo_cid.png', '.'), ('logo_resized.png', '.'), ('logo.png', '.'), ('automail.py', '.'), ('Capture_Image.py', '.'), ('check_camera.py', '.'), ('Recognize.py', '.'), ('Train_Image.py', '.'), ('utils.py', '.'), ('template.html', '.'), ('requirements.txt', '.'), ('school_management.db', '.'), ('setup_database.sql', '.'), ('Attendance', 'Attendance'), ('ImagesUnknown', 'ImagesUnknown'), ('StudentDetails', 'StudentDetails'), ('TrainingImage', 'TrainingImage'), ('train_recognizer.py', '.'), ('TrainingImageLabel', 'TrainingImageLabel'), ('train_model.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('v', None, 'OPTION')],
    name='main',
    debug=True,
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
