from flask_frozen import Freezer
from src.flask.flask import app
from src.obj.Songbook import Songbook

freezer = Freezer(app)
#app.config['FREEZER_BASE_URL'] = "/Users/rjsp4n/Desktop/vscode/songbook/songbook/src/flask/build/"
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html; charset=utf-8'

@freezer.register_generator
def start():
    sb = Songbook()
    for cat in sb.sb:
        for sng in sb.sb[cat]:
            for i in range(0, 12):
                yield {'category': cat, 'song': sng.title, 'chordShift': i}

if __name__ == '__main__':
    freezer.freeze()