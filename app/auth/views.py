from app.forms import LoginForm, SignUpForm
from flask import (
    render_template, redirect, flash, session,
    url_for
    )
from . import auth # dentro del __init__.py
from app.firestore_service import get_user, user_put
from app.models import UserData, UserModel
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash("Ya estabas logueado")
        return redirect(url_for('index'))

    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    # Loggeo y redirección ya se
    # hacen en este view
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)
        # Si el user no existe en BD
        # regresa None
        if user_doc.to_dict(): #is not None:
            password_from_db = user_doc.to_dict()['password']


            if check_password_hash(user_doc.to_dict()['password'], password):
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido de nuevo')
                redirect(url_for('hello'))
            else:
                flash('La información del usuario no coincide')
        else:
            flash('El usuario no existe')

        return redirect(url_for('index'))
    return render_template('login.html', **context)


@auth.route('signup', methods=['GET','POST'])
def signup():
    signup_form = SignUpForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            #hasheamos el passwd
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data) #de firestore_service.py

            user = UserModel(user_data)
            # Loggeamos al usuario cuando se registra
            login_user(user)
            flash('Bienvenido')

            return redirect(url_for('hello'))
        else:
            flash('El usuario ya existe')

    return render_template('signup.html',**context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('regresa pronto')
    return redirect(url_for('auth.login'))