# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=['.'],
    binaries=[],
     datas=[
        ('LICENSE', 'LICENSE'),
        ('README.md', 'README.md'),
        ('.streamlit/config.toml', '.streamlit'),
        ('app.py', '.'),
        ('badges/quality.svg', 'badges/quality.svg'),
        ('models/*.py', 'models'),
        ('pages/*.py', 'pages'),
        ('static/*', 'static'),
        ('utils/*py', 'utils'),
    ],
     hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebEngineWidgets',
        'streamlit',
        'dateutil',
        'validators',
        'streamlit_tags',
        'streamlit_star_rating ',
        'toml',
        'pandas',
        'tempfile',
        'typing',
        'zipfile',
        'csv',
        'subprocess',
        'atexit',
        'sys'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    copy_metadata=[
        ('streamlit', None),
        ('dateutil', None),
        ('validators', None),
        ('streamlit_tags', None),
        ('streamlit_star_rating', None),
        ('toml', None),
        ('pandas', None),
    ],
    collect_data=[
        ('streamlit', None),
        ('dateutil', None),
        ('validators', None),
        ('streamlit_tags', None),
        ('streamlit_star_rating', None),
        ('toml', None),
        ('pandas', None),
    ]
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ElabLite',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ElabListe'
)
