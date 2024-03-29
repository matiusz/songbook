from flask_frozen import Freezer
from ..src.flask.flask_app import app
from ..src.obj.Songbook import Songbook

freezer = Freezer(app)
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html; charset=utf-8'

@freezer.register_generator
def start():
    sb = Songbook()
    for cat in sb.sb:
        for sng in sb.sb[cat]:
            yield {'category': cat, 'song': sng.title}


def main():
    freezer.freeze()


if __name__ == '__main__':
    main()