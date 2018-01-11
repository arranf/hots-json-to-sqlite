import json
import sqlite3
import os
import datetime

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

DB_FILE_NAME = "heroes_companion.db"
HERO_TABLE_NAME = "heroes"
TALENTS_TABLE_NAME = "talents"
ABILITIES_TABLE_NAME = "abilities"
CONNECTION = sqlite3.connect(DB_FILE_NAME, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
CURSOR = CONNECTION.cursor()

with CONNECTION:
        CURSOR.row_factory = dict_factory
            
        CURSOR.execute("SELECT * FROM " + HERO_TABLE_NAME)
        hero_results = CURSOR.fetchall()
        CURSOR.execute("SELECT * FROM " + TALENTS_TABLE_NAME)
        talent_results = CURSOR.fetchall()
        CURSOR.execute("SELECT * FROM " + ABILITIES_TABLE_NAME)
        abilities_results = CURSOR.fetchall()

        results = {
            "id": datetime.datetime.utcnow().isoformat(),
            "heroes" : hero_results,
            "talents": talent_results,
            "abilities": abilities_results
        }

        with open('data.json', 'a') as f:
            json.dump(results, f, ensure_ascii=False)
CONNECTION.close()