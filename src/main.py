"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Comments
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

        #COMMENTS

@app.route('/comments', method=['GET'])
def get_all_comments():
    all_comments=db.session.query(Comments).all()
    print(all_comments)
    comment_list=[]
    for comment in all_comments:
        comment_list.append(comment.serialize())
        print(comment_list)
    return jsonify(comment_list), 200

@app.route('/comments', method=['POST'])
def create_comment():
    body=request.get_json()
    new_comment=Comments(body['text'], body['date_comment'], body['user_id'], body['recipe_id'])
    db.session.add(new_comment)
    db.session.commit()
    print(new_comment.serialize())
    return jsonify('comentario creado'),200

@app.route('/comments/<int:id>', method=['DELETE'])
def delete_comment(id):
    body=request.get_json()
    comment=Comments.query.filter_by(id=id)
    comment.delete()
    db.session.commit()
    return jsonify('comentario borrado'),200
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
