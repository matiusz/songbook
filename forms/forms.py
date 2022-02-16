from wtforms import StringField
from flask_wtf import FlaskForm

class FilterForm(FlaskForm):
    filter = StringField('Search: ')