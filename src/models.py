from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(80), unique= True, nullable= False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(80), unique = False, nullable= False)
    urlImg = db.Column(db.Text, nullable = True)
    is_active = db.Column(db.Boolean(), unique = False, nullable = False)

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.is_active = True

    def __repr__(self): return '<User %r>' % self.id   

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
    date_comment = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer)
    recipe_id = db.Column(db.Integer)

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
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_category = db.Column(db.String(250),unique= True,nullable=False)

    def __init__(self, name_category):
        self.name_category =name_category

    def serialize(self):
        return{
            "id":self.id,
            "name_categoy": self.name_category
        }
class Recipe_Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_category = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=True)
    #id_recipe = db.Column(db.Integer, db.ForeignKey('recipe.id'),nullable=True)
    category = relationship("Category")
   #recipe = relationship("Recipe")

    def __init__(self, id_category):
        self.id_category = id_category
       # self.id_recipe = id_recipe

    def serialize(self):
        return{
            "id":self.id,
            "id_category":self.id_category,
            #"id_recipe":self.id_recipe
        }
       

      