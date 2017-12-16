#!/usr/bin/env bash
if [ ! -d "heroes-talents" ]; then
    git clone git@github.com:heroespatchnotes/heroes-talents.git
fi
python3 convert_heroes.py
