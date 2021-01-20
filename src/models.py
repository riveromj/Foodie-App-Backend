from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    image = db.Column(db.String(250),nullable=False)
    ingredients = db.Column(db.String(250),nullable=False)
    elaboration = db.Column(db.String(250),nullable=False)
    num_comment = db.Column(db.Integer,nullable=False)
    date_recipe = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    #user_id = db.Column(db.Integer,ForeignKey('User.id'))
    #User = relationship("User")
    is_active = db.Column(db.Boolean(), unique = False, nullable = False)

    def __init__(self, title, image, ingredients, elaboration,num_comment):
        self.title = title
        self.image = image
        self.ingredients = ingredients
        self.elaboration = elaboration
        self.num_comment = num_comment
        self.is_active = True
    

    def __repr__(self):
        return '<Recipe %r>' % self.title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image":self.image,
            "ingredients":self.ingredients,
            "elaboration":self.elaboration,
            "num_comment":self.num_comment,
            "date_recipe":self.recipe,
        }
