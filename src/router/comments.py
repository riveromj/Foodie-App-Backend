import os
from datetime import datetime
from flask import Flask, request, jsonify
from models import db, User, Recipe

def comments_route(app, token_required):
    @app.route('/comments', method=['GET'])
    def get_all_comments():
        all_comments=db.session.query(Comments).all()
        comment_list=[]
        for comment in all_comments:
            comment_list.append(comment.serialize())
        return jsonify(comment_list), 200

    @app.route('/comments', method=['POST'])
    def create_comment():
        body=request.get_json()
        new_comment=Comments(body['text'], body['date_comment'], body['user_id'], body['recipe_id'])
        db.session.add(new_comment)
        db.session.commit()
        return jsonify('comentario creado'),200

    @app.route('/comments/<int:id>', method=['DELETE'])
    def delete_comment(id):
        body=request.get_json()
        comment=Comments.query.filter_by(id=id)
        comment.delete()
        db.session.commit()
        return jsonify('comentario borrado'),200
        