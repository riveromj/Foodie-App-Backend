from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import datetime

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    image = db.Column(db.String(250),nullable=False)
    ingredients = db.Column(db.String(250),nullable=False)
    elaboration = db.Column(db.String(250),nullable=False)
    num_comment = db.Column(db.Integer)
    date_recipe = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    user = relationship("User")

    def __init__(self, title, image, ingredients, elaboration,num_comment,user_id):
        self.title = title
        self.image = image
        self.ingredients = ingredients
        self.elaboration = elaboration
        self.num_comment = num_comment
        self.user_id = user_id

    def __str__(self):  # sustituye a def __repr__ es la forma mas actualizada de python        
       return '{} <{}>' .format(self.user_name, self.email)
        
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image":self.image,
            "ingredients":self.ingredients,
            "elaboration":self.elaboration,
            "num_comment":self.num_comment,
            "date_recipe":self.date_recipe,
            "user_id":self.user_id,
            "user_name":self.user.user_name
        }
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(80), unique= True, nullable= False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(80), unique = False, nullable= False)
    urlImg = db.Column(db.Text, nullable = True)
    is_active = db.Column(db.Boolean(), unique = False, nullable = False)
    #recipce=  relationship("Recipe") para borrar las recetas del usuario

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.is_active = True

   #def __repr__(self): return '<User %r>' % self.user_name 
    def __str__(self):  # sustituye a repr         
       return '{} <{}>' .format(self.user_name, self.email)  

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "urlImg": self.urlImg

            # do not serialize the password, its a security breach
        }

    def password_bcrypt(self):
        return self.password
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text  = db.Column(db.String(250),nullable=False)
    date_comment = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, primary_key=True)

    #def __repr__(self):
        #return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "date_comment": self.date,
            "user_id": self.user_id,
            "recipe_id": self.recipe_id
        }
      