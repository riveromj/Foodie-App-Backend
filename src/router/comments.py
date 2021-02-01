import os
from flask import Flask, request, jsonify, url_for
from models import db, User, Recipe, Comments

def comments_route(app, token_required):
    @app.route('/comments', methods=['GET'])
    def get_all_comments():
        all_comments=db.session.query(Comments).all()
        comment_list=[]
        for comment in all_comments:
            comment_list.append(comment.serialize())
        return jsonify(comment_list), 200

    @app.route('/comments', methods=['POST'])
    def create_comment():
        body=request.get_json()
        print(body)
        new_comment=Comments(text = body['text'], user_id = body['user_id'], recipe_id = body['recipe_id'])
        print(new_comment)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.serialize()),201

    @app.route('/comments/<int:id>', methods=['DELETE'])
    def delete_comment(id):
        body=request.get_json()
        comment=Comments.query.filter_by(id=id)
        comment.delete()
        db.session.commit()
        return jsonify('comentario borrado'),200
        