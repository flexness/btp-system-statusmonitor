import json
from flask import Flask, jsonify, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Service, Tag
import sqlalchemy


api = Blueprint('api', __name__)



# SQLAlchemy setup
DATABASE_URL = "sqlite:///main.db"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)



@api.route('/tags')
def api_get_tags():
    session = Session()
    try:
        tags = session.query(Tag).all()
        tags_data = [{'id': tag.id, 'name': tag.name} for tag in tags]
        
        return jsonify({'tags': tags_data})
    finally:
        session.close()



""" 


# Route to get all services
@api.route('/services')
def api_get_services():
    # Create a session
    session = Session()
    print("CHECK")
    try:
        # Query all services with tags and dependent services eagerly loaded
        services = session.query(Service).options(
            # Load tags and dependent_services eagerly to avoid lazy loading
            sqlalchemy.orm.joinedload(Service.tags),
            sqlalchemy.orm.joinedload(Service.dependent_services)
        ).all()

        # Serialize services data to JSON
        services_data = [{
            'id': service.id,
            'name': service.name,
            'status': service.status,
            'description': service.description,
            'endpoint': service.endpoint,
            'version': service.version,
            'dependent_systems': [dep_service.name for dep_service in service.dependent_services],
            'contact': service.contact,
            'tags': [tag.name for tag in service.tags]
        } for service in services]

        return jsonify({'services': services_data})

    finally:
        session.close() 

# Route to get a specific service by ID
@api.route('/service/<int:id>')
def api_get_service(id):
    # Create a session
    session = Session()
    
    try:
        # Query service by ID
        service = session.query(Service).filter_by(id=id).first()

        if service:
            # Serialize service data to JSON
            service_data = {
            'id': service.id,
            'name': service.name,
            'status': service.status,
            'description': service.description,
            'endpoint': service.endpoint,
            'version': service.version,
            'dependent_systems': [dep_service.name for dep_service in service.dependent_services],
            'contact': service.contact,
            'tags': [tag.name for tag in service.tags]
            }

            return jsonify(service_data)
        else:
            return jsonify({'error': 'Service not found'}), 404

    finally:
        session.close()

 """
















def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


@api.route('/systems/core')
def api_get_systems():
    data = load_json_data('systems.json')
    return jsonify(data)

@api.route('/systems/sap')
def api_get_sap_services():
    data = load_json_data('sap_services.json')
    return jsonify(data)

@api.route('/systems/external')
def api_get_external_services():
    data = load_json_data('external_services.json')
    return jsonify(data)

@api.route('/systems/enterprise')
def api_get_enterpise_services():
    data = load_json_data('enterprise_services.json')
    return jsonify(data)