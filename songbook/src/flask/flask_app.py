from flask import Flask, render_template, make_response

from ..obj.Config import config
from ..obj.Songbook import Songbook
from ..obj.Song import Song
from ..tools.getCategoriesConfig import getCategoriesConfig
import json
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

@app.route("/serve_js/app.js")
def serve_js():
    categories = json.dumps(list(sb.sb))
    name = config.dataFolder.split("/")[2]
    response = make_response(render_template("app.js", categories = categories, name = name))
    response.headers['Content-Type'] = 'text/javascript'
    return response


@app.route("/")
@app.route("/<category>/<song>.html")
async def start(category = None, song = None):
    songs = sb.sb
    cats = getCategoriesConfig(os.path.join(config.dataFolder, config.categoriesFile), songs, allowEmojis=True)
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
    return render_template("page.html", songList = songs, filter = filter, song = song, changelog = changelog, hasattr=hasattr, sorted=sorted, cats = cats)
