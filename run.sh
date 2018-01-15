#!/usr/bin/env bash
if [ ! -d "heroes-talents" ]; then
    git clone git@github.com:heroespatchnotes/heroes-talents.git
fi
rm -rf upload
mkdir upload
python3 convert_heroes.py
python3 create_json.py