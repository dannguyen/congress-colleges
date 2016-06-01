from time import sleep
from pathlib import Path
import requests
import yaml

BIOGUIDEURL = 'http://bioguide.congress.gov/scripts/biodisplay.pl?index='
# assume this is already downloaded
MEMBERS_DIR = Path('data', 'raw', 'unitedstates')
# create the bioguide directory for the raw html
DEST_DIR = Path('data', 'raw', 'bioguide', 'html')


members = []
# add current members
print("Reading list of current legislators")
members.extend(yaml.load(MEMBERS_DIR.joinpath('legislators-current.yaml').read_text()))
print("Reading list of historical legislators")
members.extend(yaml.load(MEMBERS_DIR.joinpath('legislators-historical.yaml').read_text()))
print("Total members:", len(members))


for i, m in enumerate(members):
    print(i, 'of', len(members))
    b_id = m['id']['bioguide']
    url = BIOGUIDEURL + b_id
    # e.g. data/raw/bioguide/B/B00012.html
    dest_path = DEST_DIR.joinpath(b_id[0], b_id + '.html')
    # create the directory, e.g. data/raw/bioguide/B/
    dest_path.parent.mkdir(exist_ok=True)
    if not dest_path.exists():
        try:
            print("Downloading", url, "to", dest_path)
            resp = requests.get(url)
            sleep(0.7)
        except (ConnectionError, ClosedPoolError) as e:
            print("Connection error",e,"...waiting")
            sleep(4)

        with dest_path.open('w') as f:
            f.write(resp.text)
