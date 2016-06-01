from os.path import join
import csv
import json
DATA_DIR = join('.', 'data')
LEGISLATORS_PATH = join(DATA_DIR, 'wrangled', 'top-college-legislators.json')
SCHOOLS_PATH = join(DATA_DIR, 'wrangled', 'top-colleges.json')

def get_legislators():
    with open(LEGISLATORS_PATH) as rf:
        data = json.load(rf)
    return data

def get_schools():
    with open(SCHOOLS_PATH) as rf:
        data = json.load(rf)

    return sorted(data, key=lambda s: (s['rank'], s['category'], s['name']))

