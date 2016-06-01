from pathlib import Path
from lxml import html as htmlparser
import re
SRC_DIR = Path('data', 'raw', 'bioguide', 'html')
DEST_DIR = Path('data', 'raw', 'bioguide', 'text')

for fpath in SRC_DIR.glob('**/*.html'):
    print(fpath)
    hdoc = htmlparser.fromstring(fpath.read_text())
    t = hdoc.xpath('//p')[0].text_content()
    txt = re.sub(r'\s+', ' ', t) # replace/squish internal space characters/newlines
    txtlines = [x.strip() + '\n' for x in txt.split(';')]
    dest_path = DEST_DIR.joinpath(fpath.stem[0], fpath.stem + '.txt')
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with dest_path.open('w') as w:
        print("Writing", dest_path)
        w.writelines(txtlines)


