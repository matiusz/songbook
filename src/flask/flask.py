from flask import Flask, render_template, send_from_directory, redirect

from src.flask.forms.forms import FilterForm
from flask import request

from src.tools.chordShift import shiftChords
from src.obj.Songbook import Songbook
from src.obj.Song import Song
import os

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
def start(category = "Turystyczne", song = "Hawiarska Koliba"):
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
    return render_template("page.html", songList = songs, filter = filter, filterString = filterString, song = song, chordShift = chordShift, shiftChords = shiftChords)