from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class FilterForm(FlaskForm):
    filter = StringField('Search: ')