# -*- coding:utf-8 -*-
import json
import sqlite3
import os
import hashlib

DB_FILE_NAME = "./upload/heroes_companion.db"
HERO_JSON_PATH = "./heroes-talents/hero"
HERO_TABLE_NAME = "heroes"
TALENTS_TABLE_NAME = "talents"
ABILITIES_TABLE_NAME = "abilities"
CONNECTION = sqlite3.connect(DB_FILE_NAME, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
CURSOR = CONNECTION.cursor()

def init_db():
    CURSOR.execute("""CREATE TABLE IF NOT EXISTS `abilities` (
	`Id`	INTEGER NOT NULL,
	`HeroId`	INTEGER NOT NULL,
	`AbilityId`	TEXT NOT NULL UNIQUE,
	`CharacterForm`	INTEGER,
	`Name`	TEXT NOT NULL,
	`Description`	TEXT,
	`Hotkey`	TEXT,
	`Cooldown`	TEXT,
	`ManaCost`	TEXT,
	`Trait`	INTEGER DEFAULT 0,
    `Sha3256` TEXT,
	PRIMARY KEY(Id)
);""")
    CONNECTION.commit()
    CURSOR.execute(""" CREATE TABLE IF NOT EXISTS `heroes` (
	`Id`	INTEGER NOT NULL,
	`HeroId`	INTEGER,
	`Name`	TEXT NOT NULL UNIQUE,
	`ShortName`	TEXT NOT NULL UNIQUE,
	`AttributeId`	TEXT,
	`IconFileName`	TEXT,
	`Role`	TEXT NOT NULL,
	`Type`	TEXT NOT NULL,
	`ReleaseDate`	TEXT,
    `Sha3256` TEXT,
	PRIMARY KEY(Id)
);""")
    CONNECTION.commit()
    CURSOR.execute("""CREATE TABLE IF NOT EXISTS `talents` (
	`Id`	INTEGER,
	`HeroId`	INTEGER,
	`AbilityId`	TEXT,
	`TalentTreeId`	TEXT,
	`ToolTipId`	TEXT,
	`Level`	INTEGER,
	`SortOrder`	INTEGER,
	`Name`	TEXT,
	`Description`	TEXT,
	`IconFileName`	TEXT,
    `Sha3256` TEXT,
    UNIQUE(HeroId, ToolTipId, TalentTreeId)
	PRIMARY KEY(Id)
);""")
    CONNECTION.commit()

def insert_hero_info():
    to_hash = hero_info.get('id') + hero_info.get('name') + hero_info.get('shortName') + hero_info.get('attributeId') + hero_info.get('icon') + hero_info.get('role') + hero_info.get('type')
    sha3_256 = hashlib.sha3_256(to_hash.encode('utf-8')).hexdigest()

    CURSOR.execute(
        "INSERT OR IGNORE INTO {} (HeroId, Name, ShortName, AttributeId, IconFileName, Role, Type, ReleaseDate, Sha3256) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)".format(HERO_TABLE_NAME),
        (hero_info.get('id'),
         hero_info.get('name'),
         hero_info.get('shortName'),
         hero_info.get('attributeId'),
         hero_info.get('icon'),
         hero_info.get('role'),
         hero_info.get('type'),
         hero_info.get('releaseDate'),
         sha3_256
        ))
    CONNECTION.commit()


def insert_talent_info():
    for level, level_talents in hero_info['talents'].items():
        for talent in level_talents:
            toHash = hero_info.get('id') + talent.get('abilityId') + talent.get('talentTreeId') + talent.get('tooltipId') + level + talent.get('name') + talent.get('description') + talent.get('name')
            sha3_256 = hashlib.sha3_256(toHash.encode('utf-8')).hexdigest()
            CURSOR.execute(
                "INSERT OR IGNORE INTO {} (HeroId, AbilityId, TalentTreeId, ToolTipId, Level, SortOrder, Name, Description, IconFileName, Sha3256) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(TALENTS_TABLE_NAME),
                (hero_info.get('id'),
                 talent.get('abilityId'),
                    talent.get('talentTreeId'),
                    talent.get('tooltipId'),
                    level,
                    talent.get('sort'),
                    talent.get('name'),
                    talent.get('description'),
                    talent.get('icon'),
                    sha3_256
                ))
            CONNECTION.commit()


def insert_ability_info():
    for form_name, form in hero_info['abilities'].items():
        for ability in form:
            toHash = hero_info.get('id') + ability.get('abilityId') + form_name + ability.get('name') + ability.get('description') + str(ability.get('hotkey')) + str(ability.get('cooldown')) + str(ability.get('manaCost'))
            sha3_256 = hashlib.sha3_256(toHash.encode('utf-8')).hexdigest()

            CURSOR.execute(
                "INSERT OR IGNORE INTO {} (HeroId, AbilityId, CharacterForm, Name, Description, Hotkey, Cooldown, ManaCost, Trait, Sha3256) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(ABILITIES_TABLE_NAME),
                (hero_info.get('id'),
                 ability.get('abilityId'),
                 form_name,
                 ability.get('name'),
                 ability.get('description'),
                 ability.get('hotkey'),
                 ability.get('cooldown'),
                 ability.get('manaCost'),
                 ('trait' in ability and bool(
                     ability['trait'] is True)),
                 sha3_256
                ))
            CONNECTION.commit()

with CONNECTION:
    init_db()
    for filename in os.listdir(HERO_JSON_PATH):
        path_to_file = os.path.join(HERO_JSON_PATH, filename)
        with open(path_to_file) as f:
            hero_info = json.load(f)
            insert_hero_info()
            insert_talent_info()
            insert_ability_info()
CONNECTION.close()
