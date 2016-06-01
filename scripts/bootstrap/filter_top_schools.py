from collections import OrderedDict, defaultdict
from pathlib import Path
import csv
import json
import re
import yaml
CURRENT_CONGRESS_ENDYEAR = 2017
DEST_PATH = Path('data', 'wrangled', 'top-college-legislators.json')
DEST_PATH.parent.mkdir(parents=True, exist_ok=True)
TEXT_DIR = Path('data', 'raw', 'bioguide', 'text')

HISTORICAL_MEMBERS_PATH = Path('data', 'raw', 'unitedstates', 'legislators-historical.yaml')
CURRENT_MEMBERS_PATH = Path('data', 'raw', 'unitedstates', 'legislators-current.yaml')
TOP_SCHOOLS_PATH = Path('data', 'usnews', 'top_schools.csv')

top_schools = list(csv.DictReader(TOP_SCHOOLS_PATH.read_text().splitlines())):

counted_members = []
print("Reading current members")
counted_members.extend(yaml.load(CURRENT_MEMBERS_PATH.read_text()))

# collect the historical members
print("Reading historical members")
for m in yaml.load(HISTORICAL_MEMBERS_PATH.read_text()):
    # add them only if they were first elected 1950 or afterwards
    if m['terms'][0]['start'] > '1950':
        counted_members.append(m)

print("Total members elected 1950 or after:", len(counted_members))

schooled_members = []
# let's wrangle it a bit
for m in counted_members:
    w = OrderedDict()
    w['bioguide_id'] = m['id']['bioguide']
    last_term = m['terms'][-1]
    if last_term['type'] == 'sen':
        w['type'] = 'Senator'
    elif last_term['type'] == 'rep':
        w['type'] = 'Representative'
    else:
        continue # skip delegates
    ###
    w['party'] = last_term['party']
    w['state'] = last_term['state']
    w['district'] = last_term.get('district')
    ## add flag for in_office
    w['in_office'] = last_term['end'] > str(CURRENT_CONGRESS_ENDYEAR)
    # add boilerplate info
    w['last_name'] = m['name']['last']
    w['first_name'] = m['name']['first']
    w['gender'] = m['bio']['gender']
    w['birthday'] = m['bio'].get('birthday')

    # now, add the bio text
    tpath = TEXT_DIR.joinpath(w['bioguide_id'][0], w['bioguide_id'] + '.txt')
    txt = tpath.read_text()
    w['bioguide_text'] = txt.splitlines()

    # now, match them to schools
    w['top-schools'] = defaultdict(list)

    for line in w['bioguide_text']:
        for school in top_schools:
            if school['name'] in line or (school['alias_pattern'] and
                 re.compile(school['alias_pattern']).search(line)):
                    w['top-schools'][school['name']].append(line)

    schooled_members.append(w)

print("Of", len(counted_members), 'legislators elected since 1950,')
print(len([s for s in schooled_members if s['top-schools']]), 'legislators have an affiliation with one of the top U.S. News colleges')



DEST_PATH.write_text(json.dumps(schooled_members, indent=2))


