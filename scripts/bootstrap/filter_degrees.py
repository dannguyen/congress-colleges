"""
Not finished; attempt to determine which congressmembers got which degrees
"""

from pathlib import Path
import re
import yaml
CURRENT_MEMBERS_PATH = Path('data', 'raw', 'unitedstates', 'legislators-current.yaml')
TEXT_DIR = Path('data', 'raw', 'bioguide', 'text')
UNDERGRAD_PATTERNS = [re.compile(r'(?<!\.)\bB\.?[AS]\b'), # B.S or B.A
                    re.compile(r'(?<!\.)\bA\.?B\b'), # A.B. smith college,
                    re.compile(r'(?<!\.)\bB\.?B\.?A\b'), # B.B.A,
                    re.compile(r'(?<!\.)\bB\.?U\.?S\b'), # B.U.S.,
                    re.compile(r'')
                    re.compile(r'bachelor of (?:art|science)', re.IGNORECASE),
                    re.compile(r'(?:graduated|degree).+?(?:college|university)', re.IGNORECASE)
                   ]

print("Reading list of current legislators")
members = yaml.load(CURRENT_MEMBERS_PATH.read_text())
print("Total members:", len(members))

# read in the data, add it to each member dict object
college_members = []
nocollege_members = []
for m in members:
    b_id = m['id']['bioguide']
    tpath = TEXT_DIR.joinpath(b_id[0], b_id + '.txt')
    print("Reading", tpath)
    txt = tpath.read_text()
    m['biotext'] = txt.splitlines()
    # while we're here, check for college attendance
    if any(p for p in UNDERGRAD_PATTERNS if p.search(txt)):
        college_members.append(m)
    else:
        nocollege_members.append(m)

