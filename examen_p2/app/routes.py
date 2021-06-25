from flask_login.utils import login_required, logout_user
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegisterForm, NoteForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Note
from app import db

# Nuevo Index o actualizado.
@app.route("/")
@app.route("/index", methods=["GET"])
@login_required
def index():
    # Solo pueda acceder el usuario.
    notes = Note.query.filter_by(users_id = current_user.id).all()
    return render_template("notes_index.html", notes=notes)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        #POST
        #Iniciar sesión con base de datos
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("No se encontro el usuario o la contraseña esta incorrecta")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash("Iniciaste Sesión correctamente, Hola {}".format(form.username.data))
        return redirect("/index")
    return render_template("login.html", title="Login",form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(form)
        if user is None:
            user = User()
            user.username = form.username.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Usuario creado exitosamente")

        else:
            flash("El usuario ya existe")
            return redirect(url_for("register"))
        
        
        return redirect("/index")
    return render_template("register.html", title="Register",form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# Procedimientos de Notas/Index
@app.route("/index/create", methods=["GET", "POST"])
@login_required
def notes_create():
    form = NoteForm()
    if form.validate_on_submit():
        print(form.title.data)
        nota = Note(title = form.title.data, body = form.body.data, users_id = current_user.id)
        db.session.add(nota)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        # Pendiente el formulario
        return render_template("notes_create.html", form=form)

@app.route("/index/destroy/<int:id>", methods=["GET"])
@login_required
def notes_destroy(id):
    # Revisar la BD por si existe ese curso.
    nota = Note.query.filter_by(id=id).first()
    # Eliminarlo de la base de datos.
    db.session.delete(nota)
    db.session.commit()
    # Redireccionar a notes_create
    return redirect(url_for("index"))

# Para mostrar notas individuales y no el total (Index)
@app.route("/index/<int:id_nota>", methods=["GET", "POST"])
def notes_show(id_nota):
    note = Note.query.filter_by(id=id_nota).first()
    return render_template("notes_show.html", note=note)

# @app.route("/index/<int:id_nota>/share")
# def notes_share(id_nota):
#     note = Note.query.filter_by(id=id_nota).first()
#     random_uuid = app_uuid.uuid4()
#     url = app.url_for('notes_show', id_nota=id_nota)
#     return render_template("notes_show.html", note=note)

# @app.route("/index/<int:id_nota>/share/<uuid(strict=False):id>")
# def notes_share_id(id):
#     note = Note.query.filter_by(uuid=id).first()
#     return render_template("notes_show.html", note=note)