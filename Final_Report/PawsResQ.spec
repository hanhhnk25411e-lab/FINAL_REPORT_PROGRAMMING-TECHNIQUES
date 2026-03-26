# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Final_Report/tests/test_WebPageMainWindown.py'],
    pathex=[],
    binaries=[],
    datas=[('Final_Report/images', 'Final_Report/images'), ('Final_Report/datasets', 'Final_Report/datasets'), ('Final_Report/PawsResQ', 'Final_Report/PawsResQ')],
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
    [],
    exclude_binaries=True,
    name='PawsResQ',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Final_Report/images/icon_app.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PawsResQ',
)
app = BUNDLE(
    coll,
    name='PawsResQ.app',
    icon='Final_Report/images/icon_app.icns',
    bundle_identifier=None,
)
