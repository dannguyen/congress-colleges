from flask import render_template, Flask
import foo

app = Flask(__name__)
legislators = foo.get_legislators()
top_schools = foo.get_schools()
liberal_arts_schools = [s for s in top_schools if s['category'] == 'liberal-arts']
national_universities = [s for s in top_schools if s['category'] == 'national-university']

@app.route('/')
def homepage():
    html = render_template('homepage.html',
                           legislators=legislators,
                           schools=top_schools,
                           liberal_arts_schools=liberal_arts_schools,
                           national_universities=national_universities)
    return html


@app.route('/schools/<slug>')
def schools(slug):
    school = next(t for t in top_schools if t['slug'] == slug)
    bids = [x['bioguide_id'] for x in school['legislators']]
    alumni = [m for m in legislators if m['bioguide_id'] in bids]
    xalumni = sorted(alumni, key=lambda m: (not m['in_office'], m['first_term_start'], m['last_name']))

    html = render_template('school.html', legislators=xalumni, school=school)
    return html

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
