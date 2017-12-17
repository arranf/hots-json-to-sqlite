import os.path
import json
import sqlite3
import os
from pathlib import Path

DB_FILE_NAME = "heroes_companion.db"
IMAGE_PATH = "./heroes-talents/images/talents"
TALENTS_TABLE_NAME = "talents"
ABILITIES_TABLE_NAME = "abilities"
CONNECTION = sqlite3.connect(DB_FILE_NAME, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
CURSOR = CONNECTION.cursor()
CURSOR.execute('SELECT * FROM ' + TALENTS_TABLE_NAME) 
for row in CURSOR:
    my_file = Path(IMAGE_PATH + '/' + row[-1])
    if not my_file.is_file():
        print (row[3] + ' ' + row[7] + ' ' + row[-1])