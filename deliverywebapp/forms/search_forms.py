from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SearchViewProductsForm(FlaskForm):
    q = StringField('q', validators=[DataRequired()])