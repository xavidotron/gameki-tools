import os.path

TOP_DIR = os.path.relpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if TOP_DIR == '.':
    TOP_DIR = ''
else:
    TOP_DIR += '/'
GAMEKI_DIR = os.path.relpath(os.path.dirname(os.path.dirname(__file__)))
if GAMEKI_DIR == '.':
    GAMEKI_DIR = ''
else:
    GAMEKI_DIR += '/'
