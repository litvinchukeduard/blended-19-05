from mongoengine import connect, Document, StringField
import bcrypt

mongo_connection = connect('users', host='localhost', username='root', password='example')

class User(Document):
    email = StringField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def __str__(self):
        return f'User: {self.username}'
