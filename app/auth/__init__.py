from flask import Blueprint

# Creamos un espacio aparte para los
# loggueos, 
auth = Blueprint('auth', __name__,url_prefix='/auth')

# Importamos después del auth
from . import views