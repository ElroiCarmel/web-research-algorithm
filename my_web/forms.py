from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import ValidationError


class RequiredOnSubmit:
    """
    Behaves like DataRequired, but only when the *submit* button was clicked.
    """

    def __init__(self, message="This field is required."):
        self.message = message

    def __call__(self, form, field):
        # Only enforce if the *real* submit button was clicked
        if form.submit.data and not field.data.strip():
            raise ValidationError(self.message)


class ValuationForm(FlaskForm):
    valuation = TextAreaField(label="Valuation", validators=[RequiredOnSubmit()])
    submit = SubmitField(label="Submit")
    fill_random = SubmitField(label="Random Valuation")
