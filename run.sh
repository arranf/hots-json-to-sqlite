#!/usr/bin/env bash
if [ ! -d "heroes-talents" ]; then
    git clone git@github.com:heroespatchnotes/heroes-talents.git
fi
# Update the submodule
git submodule foreach git pull origin master

# Ensure upload directory exists
rm -rf upload
mkdir upload

# Make a sqlite db
python3 convert_heroes.py

# Make update JSON
python3 create_json.py

# TODO pre-populate extra DB tables (?)