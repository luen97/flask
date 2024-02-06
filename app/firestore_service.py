import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# from app import login_manager #creado en el init

# Nos autenticamos en el firestore
credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential, {
  'projectId': 'platzi-flaskpower',
})

# Creamos una instancia de un servicio de firestore
# a un cliente de firestore
db = firestore.client()

# @login_manager.user_loader
def get_users():
    return db.collection('users').get()

# @login_manager.user_loader
def get_user(user_id):
  return db.collection('users').document(user_id).get()

def get_todos(user_id):
  return db.collection('users')\
        .document(user_id)\
        . collection('todos').get()

def user_put(user_data):
  user_ref = db.collection('users').document(user_data.username)
  user_ref.set({'password': user_data.password})

def put_todo(user_id, description):
  todos_collection_ref = db.collection('users').document(user_id).collection('todos')
  # Se agrega con un random ID en firestore
  todos_collection_ref.add({'description':description, 'done':False})

def delete_user(user_id):
  user_ref = db.collection('users').document(user_id)
  user_ref.delete()

def _get_todo_ref(user_id, todo_id):
  return db.document(f'users/{user_id}/todos/{todo_id}')

def delete_todo(user_id, todo_id):
  todo_ref = _get_todo_ref(user_id, todo_id)
  todo_ref.delete()

def update_todo(user_id, todo_id, done):
  # El update switchea el bool
  todo_done = not bool(done)
  todo_ref = _get_todo_ref(user_id, todo_id)
  todo_ref.update({'done': not done})
