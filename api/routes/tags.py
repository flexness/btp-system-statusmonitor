
# api/routes/tags.py
from flask_restx import Namespace, Resource, fields, marshal_with
from sqlalchemy.orm import scoped_session
from ..models import Tag, Tag
from ..factory import Session
from flask import request

ns = Namespace('tags', description='tags to group or mark tags')
session = scoped_session(Session)


tag_model = ns.model('Tag', {
    'id': fields.Integer(readOnly=True, description='The tag unique identifier'),
    'name': fields.String(required=True, description='The tag name')
})



@ns.route('/')
class TagList(Resource):
    @ns.doc('list_tags')
    @ns.marshal_list_with(tag_model)
    def get(self):
        return session.query(Tag).all()

    @ns.doc('create_tag')
    @ns.expect(tag_model)
    @ns.marshal_with(tag_model, code=201)
    def post(self):
        data = request.json  # Change to accept JSON
        name = data.get('name')  # Extract the name from JSON data
        print(name)
        new_tag = Tag(name=name)
        session.add(new_tag)
        session.commit()
        return new_tag, 201

@ns.route('/<int:id>')
@ns.response(404, 'Tag not found')
@ns.param('id', 'The tag identifier')
class TagResource(Resource):
    @ns.doc('get_tag')
    @ns.marshal_with(tag_model)
    def get(self, id):
        tag = session.query(Tag).get(id)
        if tag is None:
            ns.abort(404, "Tag not found")
        return tag

    @ns.doc('delete_tag')
    @ns.response(204, 'Tag deleted')
    def delete(self, id):
        tag = session.query(Tag).get(id)
        if tag is None:
            ns.abort(404, "Tag not found")
        session.delete(tag)
        session.commit()
        return '', 204

    @ns.expect(tag_model)
    @ns.marshal_with(tag_model)
    def put(self, id):
        tag = session.query(Tag).get(id)
        if tag is None:
            ns.abort(404, "Tag not found")
        for key, value in ns.payload.items():
            setattr(tag, key, value)
        session.commit()
        return tag
