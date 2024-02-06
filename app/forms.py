from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, PasswordField, SubmitField,
    
)
from wtforms.validators import DataRequired, InputRequired, EqualTo

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

class SignUpForm(FlaskForm):
    username = StringField('Nombre de Usuario',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),
                             InputRequired(),
                             EqualTo(
                                'password_repeat',
                                 message='Passwords must match'
                                 )])

    password_repeat = PasswordField('Repite tu Password',validators=[DataRequired(),
                                    InputRequired()])
    submit = SubmitField('Enviar')

class TodoForm(FlaskForm):
    description = StringField('Descripción',validators=[DataRequired()])
    submit = SubmitField('Crear tarea')

class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')

class UpdateTodoForm(FlaskForm):
    submit = SubmitField('Actualizar')