from flask import (
    Flask, request, make_response, redirect,
    escape, render_template, session, url_for,
    flash
)
from flask_bootstrap import Bootstrap

## Para formularios
# =======================================
from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, PasswordField, SubmitField
)
from wtforms.validators import DataRequired
# =======================================

import unittest

from app import create_app

app = create_app()

# Pasamos el nombre de la aplicación
# app = Flask(
#     __name__, # __name__ = main.py
#     template_folder='./templates',
#     static_folder='./static') 
# # Inicializamos
# bootstrap = Bootstrap(app)

# # Creamos la llave secreta para la session
# # sirve para encriptar info delicada
# app.config['SECRET_KEY'] = 'SUPER SECRETO'


#To do's
todos = ['Hacer almuerzo','mercar','lavar ropa']

# Modelos 

# Hereda de FlaskForm
class LoginForm(FlaskForm):

    # Campos de formulario
    username = StringField(
        'Nombre de ususario', 
        # Dato obligatorio
        # no olvidar inicializar ()
        validators=[DataRequired()], 
        )
    password = PasswordField(
        'Password', 
        validators=[DataRequired()]
        )

    # SUmbit button
    submit = SubmitField('Enviar')

# CLI
@app.cli.command()
def test():
    """Creo un comando para que ejecute todos
    los tests que diseño y almaceno en una carpeta
    de nombre tests"""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

# Errores

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_server_error(error):
  return render_template('500.html')

# Funcionalidades endpoints?

@app.route('/')
def index():
    # Tomamos la ip del usuario
    user_ip = request.remote_addr

    # Creamos un response que redirije
    # al usuario a la ruta /hello
    response = make_response(redirect('/hello'))

    # Guardamos la ip en la session
    session['user_ip'] = user_ip

    # Guardamos la ip en una cookie
    # Ya no la guardamos porque usamos la sesión
    # response.set_cookie('user_ip',user_ip)

    return response

@app.route('/hello', methods=['GET','POST'])
def hello():

    # Sacamos la ip de la cookie y no del response
    # user_ip = request.cookies.get('user_ip')

    # Pedimos la ip a la sesion, no al request
    # para que el usuario no pueda cambiarmela por ahí 
    user_ip = session.get('user_ip')
    # Para evitar una XSS (JS injection) 
    # https://www.youtube.com/watch?v=EoaDgUgS6QA
    # escapamos el user_ip
    user_ip = escape(user_ip)
    login_form = LoginForm()
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username
    }
    
    # Obtenemos los datos del formulario
    # y los agregamos a la session

    # Detecta cuando mando un POST
    # y valida la forma (formulario)
    # if (me hacen un POST y la forma es valida)
    if login_form.validate_on_submit():
        # Redirect al index
        # Saco el username de lo que enviaron
        # y lo metemos a la session
        username = login_form.username.data
        session['username'] = username

        flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))
    
    # Si hacen un GET, regreso este template
    return render_template('hello.html', **context)


if __name__ == '__main__':
    app.run(port = 5000, debug = True)
