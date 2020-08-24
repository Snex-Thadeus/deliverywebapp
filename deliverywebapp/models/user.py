from deliverywebapp import db, ma, app, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import secrets


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# it will add certain fileds to the user class that are essential to the user login


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(48), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User (' {self.id} ',' {self.username} ', '{self.email}', '{self.image_file}' )"

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
