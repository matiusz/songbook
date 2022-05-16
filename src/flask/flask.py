from flask import Flask, render_template, send_from_directory, redirect

from src.flask.forms.forms import FilterForm
from flask import request

from src.obj.Config import config
from src.tools.chordShift import shiftChords
from src.obj.Songbook import Songbook
from src.obj.Song import Song

import os
import requests

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

    def reloadText(self, filt : str = None, detailed : bool = False):
        self.text = self.getText(filt, detailed)

    def getText(self, filt : str = None, detailed : bool = False):
        textLines = []
        for cat in sorted(self.catSongs.keys()):
            songs = []
            for song in self.catSongs[cat]:
                if filt:
                    if filt.lower() in song.title.lower():
                        songs.append(song.linkedTitle)
                    elif detailed:
                            if filt.lower() in song.filterString.lower():
                                songs.append(song.linkedTitle)
                else:
                    songs.append(song.linkedTitle)
            if songs:
                textLines.append(f"<h1>{cat}</h1>")
                textLines.extend(sorted(songs))
        return "<br>".join(textLines)

songList = SongList()

@app.route("/")
def start():
    return render_template("page.html")

@app.route("/toc")
def toc():
    filter = FilterForm()
    filter.validate_on_submit()
    filterString = request.args.get("filter")
    songList.reloadText(filterString, True)
    return render_template("songList.html", songListText = songList.text, filter = filter)

@app.route("/js/navBar.js")
def navBarJS():
    return send_from_directory(os.path.join(app.root_path,"js"),'navBar.js')

@app.route("/<category>/<title>")
def get_song(category, title):
    try:
        chordShift = int(request.args.get("chordShift", 0, int))
    except ValueError:
        chordShift = 0
    return render_template("song.html", song = Song.loadFromCatAndTitle(category, title), chordShift = chordShift, shiftChords = shiftChords)

@app.route('/favicon.ico')
def fav():
    return send_from_directory(app.root_path,'guitar.ico')

@app.route("/landing")
def landing():
    r = requests.get('https://circleci.com/api/v1.1/project/github/matiusz/songbook/latest/artifacts')
    for arti in r.json():
        if arti['path'] == 'songbook.pdf':
            return render_template("landing.html", pdfUrl = arti['url'])
