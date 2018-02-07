#!/usr/bin/python3
import re
import json
import sqlite3
import subprocess
import datetime
import os
import http.client

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_sha(repo):
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo).decode('ascii').strip()
    return sha

def get_patch_number():
    conn = http.client.HTTPSConnection("api.github.com")
    headers = {'User-Agent': 'hero_data_to_json'}
    if 'GITHUB_OAUTH_KEY' in os.environ:
        headers['Authorization'] = 'token ' + os.environ['GITHUB_OAUTH_KEY']
    conn.request("GET", "/repos/heroespatchnotes/heroes-talents/commits", headers=headers)
    res = conn.getresponse()
    data = res.read()
    response_data = json.loads(data.decode("utf-8"))
    patch_number = ''
    for commit in response_data:
        if 'commit' not in commit or 'message' not in commit['commit']:
            break
        commit_message = commit['commit']['message']
        match = re.search(r'\d+\.\d+', commit_message)
        if match is not None:
            patch_number = match.group()
            break
    print('Patch ' + patch_number)
    return patch_number

def get_patch_date(patch_number):
    conn = http.client.HTTPSConnection("data.heroescompanion.com")
    conn.request("GET", "/v1/patches", headers={'User-Agent': 'hero_data_to_json'})
    res = conn.getresponse()
    data = res.read()
    response_data = json.loads(data.decode("utf-8"))
    patch_date = ''
    for patch in response_data:
        if 'liveDate' in patch:
            patch_date = patch['liveDate']
            break
    print('Patch Date: ' + patch_date)
    return patch_date

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

    patch_number = get_patch_number()

    results = {
        "id": datetime.datetime.utcnow().isoformat(),
        "patch": patch_number,
        "patch_date": get_patch_date(patch_number),
        "sha": get_sha('./heroes-talents'),
        "heroes" : hero_results,
        "talents": talent_results,
        "abilities": abilities_results
    }

    with open('./upload/data.json', 'w') as f:
        json.dump(results, f, ensure_ascii=False)
CONNECTION.close()
