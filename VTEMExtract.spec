# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['VTEMExtract.py'],
             pathex=['C:\\Users\\David\\venv\\python39VTEM\\Lib\\site-packages', 'C:\\Users\\David\\Google Drive\\Programming\\Python\\VTEMExtract'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='VTEMExtract',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='heli.ico')
