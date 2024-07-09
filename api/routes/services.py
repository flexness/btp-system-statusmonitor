# api/routes/services.py
from flask_restx import Namespace, Resource, fields, marshal_with
from sqlalchemy.orm import scoped_session, joinedload

from ..models import Service, Tag, service_dependencies, service_tags
from database import Session
from flask import request
from .tags import tag_model
import logging


ns = Namespace('services', description='Service operations')
session = scoped_session(Session)

service_model = ns.model('Service', {
    'id': fields.Integer(readOnly=True, description='The service unique identifier'),
    'name': fields.String(required=True, description='The service name'),
    'status': fields.String(required=True, description='The service status'),
    'description': fields.String(required=True, description='The service description'),
    'endpoint': fields.String(required=True, description='The service endpoint'),
    'version': fields.String(required=True, description='The service version'),
    'contact': fields.String(required=True, description='The service contact'),
    'tags': fields.List(fields.Nested(tag_model), description='The service contact'),
    'type': fields.String(required=True, description='The service type')
    })

# Register the model
ns.models['Service'] = service_model

# add dependent_services AFTER init of model
# because dependent_services is a relationship to itself (a service depends on another service..)
service_model['dependent_services'] = fields.List(fields.Nested(service_model), description='The services depending on this service')


# ---
# SERIALIZE JSON RESPONSE FOR LISTING SERVICES
# ---
# adjust data response depending on the depth of relations 
# since services can be bi-diractional dependencies (receiver depends on sender, sender depends on receiver)
# which would create inifite loops regarding the 'dependent_services' field
# max_depth can be changed (0 display the first level of dependencies)
def serialize_service(service, depth=0, max_depth=0):
    # ignore dependencies if above max_depth 
    if depth > max_depth:
        return {
            'id': service.id,
            'name': service.name,
            'status': service.status,
            'description': service.description,
            'endpoint': service.endpoint,
            'version': service.version,
            'contact': service.contact,
            'tags': [{'id': tag.id, 'name': tag.name} for tag in service.tags],
            'type': service.type
        }

    # include dependencies by default
    return {
        'id': service.id,
        'name': service.name,
        'status': service.status,
        'description': service.description,
        'endpoint': service.endpoint,
        'version': service.version,
        'contact': service.contact,
        'tags': [{'id': tag.id, 'name': tag.name} for tag in service.tags],
        'type': service.type,
        'dependent_services': [serialize_service(dep, depth + 1, max_depth) for dep in service.dependent_services]
    }

@ns.route('/')
class ServiceList(Resource):
    @ns.doc('list_services')
    @ns.marshal_list_with(service_model)
    def get(self):
        try:
            logging.debug("Attempting to fetch services from the database")
            services = session.query(Service).options(joinedload(Service.dependent_services)).all()
            result = [serialize_service(service) for service in services]
            logging.debug(f"Fetched services: {result}")
            return result
        except Exception as e:
            logging.error(f"Error fetching services: {e}", exc_info=True)
            return {'error': 'An error occurred while fetching services'}, 500

    @ns.doc('create_service')
    @ns.expect(service_model)
    @ns.marshal_with(service_model, code=201)
    def post(self):
        # get data from app route request
        data = request.json 
        # print(request.json)

        # create service without relational data (needs id)
        new_service = Service(
            name=data.get('name') ,
            status=data.get('status'),
            description=data.get('description'),
            endpoint=data.get('endpoint'),
            version=data.get('version'),
            contact=data.get('contact'),
            type=data.get('type')
        )
        session.add(new_service)
        session.commit()

        # Retrieve the new service ID
        new_service_id = new_service.id

        # get relational data
        dependent_service_names = data.get('dependent_services', [])
        selected_tags = data.get('tags', [])
        print("api json rec: ", dependent_service_names, selected_tags)

        # retrieve IDs of dependent services from the database
        dependent_services = session.query(Service).filter(Service.id.in_(dependent_service_names)).all()

        # Add entries to the service_dependencies table
        for dependent_service in dependent_services:
            print(dependent_service.id)
            session.execute(service_dependencies.insert().values(
            service_id=new_service_id,
            dependent_service_id=dependent_service.id
        ))

        # retrieve IDs of dependent tags from the database
        tags = session.query(Tag).filter(Tag.id.in_(selected_tags)).all()

        # add entries to the service_tags table
        for tag in tags:
            print(tag.id)
            session.execute(service_tags.insert().values(
            service_id=new_service_id,
            tag_id=tag.id
        ))

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
