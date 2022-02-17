from flask import Flask, render_template, send_from_directory

from src.flask.forms.forms import FilterForm
from flask import request

from src.obj.Config import config
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

    def reloadText(self, filt : str = None, detailed : bool = False):
        self.text = self.getText(filt, detailed)

    def getText(self, filt : str = None, detailed : bool = False):
        textLines = []
        for cat in self.catSongs.keys():
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
                textLines.extend(songs)
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

@app.route("/<category>/<title>")
def get_song(category, title):
    return render_template("song.html", song = Song.loadFromCatAndTitle(category, title))

@app.route('/favicon.ico')
def fav():
    return send_from_directory(app.root_path,'guitar.ico')

