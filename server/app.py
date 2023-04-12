#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/research')
def all_research():
    ret = []
    for research in Research.query.all():
        new = {
            'id':research.id,
            'topic': research.topic,
            'year': research.year,
            'page_count': research.page_count
        }
        ret.append(new)
    response = make_response(
        ret,
        200
    )
    return response

@app.route('/research/<int:id>', methods=['GET', 'DELETE'])
def res_by_id(id):
    ret = Research.query.filter(Research.id == id).first()
    if ret == None:
        body = {
            "error": "Research paper not found"
        }
        response = make_response(
            body,
            404
        )
        return response
    else:
        if request.method == 'GET':
            response = make_response(
                ret.to_dict(),
                200
            )
            return response
        elif request.method == 'DELETE':
            db.session.delete(ret)
            db.session.commit()
            body = {
                "message": 'Delete Successful!'
            }
            response = make_response(
                body, 
                200
            )
            return response
        
@app.route('/authors')
def authors():
    auth_list = []
    for auth in Author.query.all():
        auth_list.append(auth.to_dict())
    resp = make_response(
        auth_list,
        200
    )
    return resp

@app.route('/research_author', methods=['GET', 'POST'])
def research_authors():
    if request.method == 'GET':
        auth_list = []
        for res_auth in ResearchAuthors.query.all():
            auth_list.append(res_auth.to_dict())
        resp = make_response(
            auth_list,
            200
        )
        return resp
    if request.method == 'POST':
        new_ra = ResearchAuthors(
            author_id = request.form.get('author_id'),
            research_id = request.form.get('research_id')
        )
        db.session.add(new_ra)
        db.session.commit()
        resp = make_response(
            new_ra.to_dict(),
            201
        )
        return resp

if __name__ == '__main__':
    app.run(port=5555, debug=True)
