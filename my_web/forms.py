from flask_wtf import FlaskForm

from wtforms.validators import DataRequired, NumberRange
from wtforms import SubmitField, TextAreaField, IntegerField
from random import randint

class ValuationForm(FlaskForm):
    valuation = TextAreaField(label="Valuation", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class FillRandomForm(FlaskForm):
    num_agents = IntegerField(label="Number of Agents", validators=[DataRequired(), NumberRange(min=2, max=8)])
    num_items = IntegerField(label="Number of Items", validators=[DataRequired(), NumberRange(min=4, max=15)])
    fr_submit = SubmitField(label="Random Example")