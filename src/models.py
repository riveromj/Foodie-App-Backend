from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(80), unique = False, nullable = False)
    image = db.Column(db.Text), nullable = True)
    is_active = db.Column(db.Boolean(), unique = False, nullable = False)

    def __init__(self, email, password, image):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.image = image
        self.is_active = True

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.username,
            "email": self.email,
            "image": self.image

            # do not serialize the password, its a security breach
        }
