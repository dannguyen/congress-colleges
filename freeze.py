"""
Run `freeze.py` to generate a build/ directory of static files

Tutorial: http://first-news-app.readthedocs.io/en/latest/#act-5-hello-internet
Docs: http://pythonhosted.org/Frozen-Flask/
"""

from flask_frozen import Freezer
from app import app
import foo
freezer = Freezer(app)
# yeah, I'm being lazy
app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True


# have to iterate through every school to generate a school path
@freezer.register_generator
def schools():
    for s in foo.get_schools():
        yield {'slug': s['slug']}


if __name__ == '__main__':
    freezer.freeze()
