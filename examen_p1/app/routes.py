from app import app
from flask import render_template
from app.forms import ComisionForm
from decimal import Decimal

def ComisionT(cantidad):
    cantidad1 = Decimal(cantidad)
    total = Decimal(cantidad)
    comisionfija = Decimal(5)
    if cantidad1 >= Decimal(50000) and cantidad1 <= Decimal(249999.99):
        total -= cantidad1*Decimal(0.0365) + comisionfija
    elif cantidad1 >= Decimal(250000) and cantidad1 <= Decimal(499999.99):
        total -= cantidad1*Decimal(0.0345) + comisionfija
    elif cantidad1 >= Decimal(500000) and cantidad1 <= Decimal(999999.99):
        total -= cantidad1*Decimal(0.0315) + comisionfija
    elif cantidad1 > 1000000:
        total -= cantidad1*Decimal(0.0295) + comisionfija
    else:
        total -= 5
    return total

@app.route('/', methods=["GET","POST"])
# @app.route('/index')
def index():
    form = ComisionForm()
    if form.validate_on_submit():
        comision = form.comision.data
        total = ComisionT(comision)
        return  render_template("resultado.html", comision=comision, total=total)
    return render_template("index.html", form = form)