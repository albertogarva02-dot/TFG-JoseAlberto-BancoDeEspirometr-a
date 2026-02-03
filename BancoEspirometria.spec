# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('interfaz', 'interfaz'),
        ('imagenes', 'imagenes'),
        ('documentos', 'documentos'),
        ('imagenes_in_simetria', 'imagenes_in_simetria'),
        ('imagenes_out_simetria', 'imagenes_out_simetria'),
        ('codigos', 'codigos'), 
],
    hiddenimports=[
        # BASE DE DATOS
        'mysql.connector',
        'mysql.connector.locales.eng.client_error',
        'mysql.connector.plugins',

        # INTERFAZ (Qt)
        'PySide6.QtXml',        
        'PySide6.QtCharts',      
        'PySide6.QtPdf',         
        'PySide6.QtPdfWidgets',
        'PySide6.QtNetwork',     

        # CALCULOS
        'scipy.special._ufuncs', 
        'scipy.linalg',
        'scipy.signal',
        'sklearn',               
        'sklearn.utils._cython_blas',
        'sklearn.neighbors.typedefs',
        'sklearn.neighbors.quad_tree',
        'sklearn.tree',
        'sklearn.tree._utils',
        'sklearn.decomposition',

        # HARDWARE Y COMUNICACIONES
        'pymodbus',
        'pymodbus.client',
        'pywinusb',
        'pywinusb.hid',
        
        # OTROS
        'openpyxl',
        'pandas',
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
    [],
    exclude_binaries=True,
    name='BancoEspirometria',
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
    icon='imagenes/icono_app.ico', 
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BancoEspirometria',
)
