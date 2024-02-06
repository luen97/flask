from flask_login import UserMixin
from .firestore_service import get_user


class UserData:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

class UserModel(UserMixin):
    # Queremos que cada vez que se cree este modelo, 
    # tenga username y password, no hacemos que herede
    # de UserData también porque queremos cambiar
    # el atrib de username a id  
    def __init__(self, user_data):
        """
        param user_data: UserData"""
        self.id = user_data.username
        self.password = user_data.password

    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc.id,
            password=user_doc.to_dict()['password']
        )
        
        return UserModel(user_data)
