from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import relationship
db = SQLAlchemy()

#COMMENTS END POINTS >>>>>>>>>>>>>>>>>>

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(80), unique= True, nullable= False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(80), unique = False, nullable= False)
    urlImg = db.Column(db.Text, nullable = True, default = 'https://3000-eebc3df8-f426-41f7-8f32-d9211915975b.ws-eu03.gitpod.io/default_user_profile.png')
    is_active = db.Column(db.Boolean(), unique = False, nullable = False, default= True)
    comments = db.relationship('Comments', cascade="all,delete", backref='user', lazy=True)

    #def __repr__(self): return '<User %r>' % self.id 
    def __str__(self):        
        return '{} <{}>' .format(self.email, self.user_name)   

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "urlImg": self.urlImg
        }

    def password_bcrypt(self):
        return self.password 
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text  = db.Column(db.String(250),nullable=False)
    date_comment = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean(), unique = False, nullable = False, default = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    
    
    
    def __repr__(self):
        return '<Comments %r>' % self.text

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "date_comment": self.date_comment,
            "is_active": self.is_active,
            "user_id": self.user_id,
            "recipe_id": self.recipe_id
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    image = db.Column(db.String(250),nullable=False)
    is_active = db.Column(db.Boolean(), unique = False, nullable = False, default = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = relationship("Recipe")
    user = relationship("User")

    def __repr__(self):
        return '<Favorites %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image":self.image,            
            "is_active": self.is_active,
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
            "name_category": self.name_category
        }
class Recipe_Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_category = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=True)
    id_recipe = db.Column(db.Integer, db.ForeignKey('recipe.id'),nullable=True)
    category = relationship("Category")
    recipe = relationship("Recipe", cascade = "all,delete", backref = 'recipe_Category')

    def serialize(self):
        return{
            "id":self.id,
            "id_category":self.id_category,
            "id_recipe":self.id_recipe
        }
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    image = db.Column(db.String(250),nullable=False)
    ingredients = db.Column(db.String(250),nullable=False)
    elaboration = db.Column(db.String(250),nullable=False)
    is_active = db.Column(db.Boolean(), unique = False, nullable = False, default = True)
    date_recipe = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    comments = db.relationship('Comments', cascade = "all,delete", backref = 'recipe', lazy = True)
    user = relationship("User")
   
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image":self.image,
            "ingredients":self.ingredients,
            "elaboration":self.elaboration,
            "date_recipe":self.date_recipe,
            "user_id":self.user_id,
            "user_name":self.user.user_name,
            "comments": list(map(lambda comment: comment.serialize(), self.comments)),
            "is_active": self.is_active
        }


      



      