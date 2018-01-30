#!/usr/bin/python3
import re
import json
import sqlite3
import subprocess
import datetime

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_sha(repo):
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo).decode('ascii').strip()
    return sha

def get_patch_number():
    import http.client
    conn = http.client.HTTPSConnection("api.github.com")
    conn.request("GET", "/repos/heroespatchnotes/heroes-talents/commits", headers={'User-Agent': 'hero_data_to_json'})
    res = conn.getresponse()
    data = res.read()
    response_data = json.loads(data.decode("utf-8"))
    print(response_data)
    patch_number = ''
    for commit in response_data:
        if 'commit' not in commit or 'message' not in commit['commit']:
            break
        commit_message = commit['commit']['message']
        print(commit_message)
        match = re.search(r'\d+\.\d+', commit_message)
        if match is not None:
            patch_number = match.group()
            print(patch_number)
            break
        return patch_number

DB_FILE_NAME = "upload/heroes_companion.db"
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
        "patch": get_patch_number(),
        "sha": get_sha('./heroes-talents'),
        "heroes" : hero_results,
        "talents": talent_results,
        "abilities": abilities_results
    }

    with open('./upload/data.json', 'w') as f:
        json.dump(results, f, ensure_ascii=False)
CONNECTION.close()
