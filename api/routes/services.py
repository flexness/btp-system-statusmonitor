# api/routes/services.py
from flask_restx import Namespace, Resource, fields, marshal_with
from sqlalchemy.orm import scoped_session
from ..models import Service, Tag
from ..factory import Session

from ..custom_fields import DepthLimitedNested

from .tags import tag_model

ns = Namespace('services', description='Service operations')
session = scoped_session(Session)

service_model = ns.model('Service', {
    'id': fields.Integer(readOnly=True, description='The service unique identifier'),
    'name': fields.String(required=True, description='The service name'),
    'status': fields.String(required=True, description='The service status'),
    'description': fields.String(description='The service description'),
    'endpoint': fields.String(description='The service endpoint'),
    'version': fields.String(description='The service version'),
    'contact': fields.String(description='The service contact'),
    'tags': fields.List(fields.Nested(tag_model))
    })

# Register the model
ns.models['Service'] = service_model

# Update the Service model to include the recursive reference
service_model['dependent_services'] = fields.List(DepthLimitedNested(service_model, max_depth=2))


@ns.route('/')
class ServiceList(Resource):
    @ns.doc('list_services')
    @ns.marshal_list_with(service_model)
    def get(self):
        return session.query(Service).all()

    @ns.doc('create_service')
    @ns.expect(service_model)
    @ns.marshal_with(service_model, code=201)
    def post(self):
        new_service = Service(
            name=ns.payload.get('name'),
            status=ns.payload.get('status'),
            description=ns.payload.get('description'),
            endpoint=ns.payload.get('endpoint'),
            version=ns.payload.get('version'),
            contact=ns.payload.get('contact')
        )
        session.add(new_service)
        session.commit()
        return new_service, 201

@ns.route('/<int:id>')
@ns.response(404, 'Service not found')
@ns.param('id', 'The service identifier')
class ServiceResource(Resource):
    @ns.doc('get_service')
    @ns.marshal_with(service_model)
    def get(self, id):
        service = session.query(Service).get(id)
        if service is None:
            ns.abort(404, "Service not found")
        return service

    @ns.doc('delete_service')
    @ns.response(204, 'Service deleted')
    def delete(self, id):
        service = session.query(Service).get(id)
        if service is None:
            ns.abort(404, "Service not found")
        session.delete(service)
        session.commit()
        return '', 204

    @ns.expect(service_model)
    @ns.marshal_with(service_model)
    def put(self, id):
        service = session.query(Service).get(id)
        if service is None:
            ns.abort(404, "Service not found")
        for key, value in ns.payload.items():
            setattr(service, key, value)
        session.commit()
        return service
