from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

class ComisionForm(FlaskForm):
    comision = DecimalField("Comisión", validators=[DataRequired()])
    submit = SubmitField("Calcular")