from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired


class ShortenUrlForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL()])
    name = StringField('Name (optional)')
    submit = SubmitField('Shorten')
