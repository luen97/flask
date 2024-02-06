from flask import (
    request, make_response, redirect,
    escape, render_template, session, url_for,
    flash
)
from flask_bootstrap import Bootstrap

import unittest

# Traemos los módulos de la app
from app import create_app
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
from app.firestore_service import get_users, get_todos, put_todo, delete_todo, update_todo

from flask_login import login_required, current_user

app = create_app()

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
@login_required
def hello():
    user_ip = session.get('user_ip')
    # Para evitar una XSS (JS injection) 
    # https://www.youtube.com/watch?v=EoaDgUgS6QA
    # escapamos el user_ip
    user_ip = escape(user_ip)
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)
        flash('Tu tarea se creo con exito')
        return redirect(url_for('hello'))

    return render_template('hello.html', **context)

@app.route('/todo/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))

@app.route('/todo/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id,done):
    # Casteamos el done (bool) como int
    user_id = current_user.id
    print('Done', done)
    update_todo(user_id=user_id,todo_id=todo_id,done=done)
    redirect(url_for('hello'))

if __name__ == '__main__':
    app.run(port = 5000, debug = True)
