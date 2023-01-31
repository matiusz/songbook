from flask import Flask, render_template, send_from_directory, redirect

from src.flask.forms.forms import FilterForm
from flask import request

from src.tools.chordShift import shiftChords
from src.obj.Songbook import Songbook
from src.obj.Song import Song
import os
import markdown2
import re

try:
    port = int(os.getenv('PORT'))
except TypeError:
    port = 5000
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class SongList:
    def __init__(self):
        self.catSongs = Songbook().sb
        self.text = self.getText()

sb = Songbook()

@app.route("/")
@app.route("/<category>/<song>")
def start(category = None, song = None):
    filter = FilterForm()
    filter.validate_on_submit()
    filterString = request.args.get("filter")
    try:
        chordShift = int(request.args.get("chordShift", 0, int))
    except ValueError:
        chordShift = 0
    if filterString:
        songs = sb.filteredSongs(filterString)
    else:
        songs = sb.sb
    try:
        song = Song.loadFromCatAndTitle(category, song)
    except Exception as e:
        song = None
    changelog = None
    if song == None and category == None:
        try:
            with open('CHANGELOG.md', "r", encoding="utf-8") as f:
                text = f.read()
                pattern2 = r' \(\[\w{7}\]\(https.+\)\)'
                text = re.sub(pattern2, '', text)
                text = re.sub('CHANGELOG', 'Historia zmian', text)
            changelog = markdown2.markdown(text)
        except Exception as ex:
            changelog = "<p></p>"
    return render_template("page.html", songList = songs, filter = filter, filterString = filterString, song = song, chordShift = chordShift, shiftChords = shiftChords, changelog = changelog)