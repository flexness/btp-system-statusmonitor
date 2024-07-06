from flask import Flask, jsonify, request, Blueprint, url_for, flash, redirect, render_template, send_from_directory, current_app
from .services import db_connect, create_security_context
import pandas as pd
import json
import requests
from api.models import Service, Tag
from api.enums import ServiceType

from database import Session


# create blueprint for routes
routes = Blueprint('routes', __name__)

db_session = Session()
request_session = requests.Session()

@routes.route('/')
@routes.route('/index')
def index():
    return render_template('index.html',
    )


@routes.route('/admin')
def admin():
    # services = request_session.get('http://127.0.0.1:3000/api/services/').json()
    services = db_session.query(Service).all()
    # tags = request_session.get('http://127.0.0.1:3000/api/tags/').json()
    tags = db_session.query(Tag).all()
    service_types = ServiceType
    print(service_types)
    return render_template('admin.html',
        services=services,
        tags=tags,
        service_types=service_types
        )

@routes.route('/services')
def table():
    response = request_session.get('http://127.0.0.1:3000/api/services/')
    response.raise_for_status()
    sap_services = response.json()

    return render_template('table.html',
        sap_services=sap_services)


@routes.route('/check_service/<service_id>', methods=['GET'])
def check_service(service_id):
    db_session = Session()
    try:
        service = db_session.query(Service).get(service_id)
        if not service:
            print("Service not found")
            return jsonify({"error": "Service not found"}), 404
        
        try:
            response = requests.get(service.endpoint, timeout=5)
            print("status code: ", response.status_code)
            service.status = 'up' if response.status_code == 200 else 'down'
            db_session.commit()

        except requests.RequestException:
            service.status = 'down'
            print("not queryable, RequestException")
            print(response.status_code)
        
        return jsonify({
            "id": service.id,
            "status": service.status
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()



@routes.route("/addtag", methods=["POST"])
def add_tag():
    if request.method == 'POST':
        print("1")
        tag = request.form.get('tag_name')
        if tag is not None:
            try:
                response = requests.post('http://127.0.0.1:3000/api/tags/', json={'name': tag})            
                response.raise_for_status()
                print(tag)
                flash('Tag added successfully!', 'success')
            except requests.exceptions.RequestException as e:
                print(e)
                flash('Failed to add tag. Please try again.', 'error')
        else:
            flash('Please enter a tag name.', 'error')
    return redirect(url_for('routes.admin'))


@routes.route("/addservice", methods=["POST"])
def add_service():
    if request.method == 'POST':
        service_data = {
            'name': request.form.get('service_name'),
            'description': request.form.get('service_desc'),
            'endpoint': request.form.get('service_endpoint'),
            'version': request.form.get('service_name'),
            'contact': request.form.get('service_contact'),
            'dependent_services': request.form.getlist('services'),
            'tags': request.form.getlist('tags'),
            'type': request.form.get('service_type')
        }
        print(service_data)
        if service_data is not None:
            try:                
                response = requests.post('http://127.0.0.1:3000/api/services/', json=service_data)        
                response.raise_for_status()
                print("new service :", service_data)
                flash('service added successfully!', 'success')
            except requests.exceptions.RequestException as e:
                print(e)
                flash('Failed to add service. Please try again.', 'error')
        else:
            flash('Please enter a service name.', 'error')
    return redirect(url_for('routes.admin'))


@routes.route('/delete_service', methods=["POST"])
def delete_service():
    service_id = request.form.get('service_id')
    if not service_id:
        return jsonify({"error": "No service ID provided"}), 400

    try:
        service = db_session.query(Service).get(service_id)
        if not service:
            return jsonify({"error": "Service not found"}), 404
        
        db_session.delete(service)
        db_session.commit()
        flash('Service deleted successfully!', 'success')
        # return jsonify({"success": True}), 200
        return redirect(url_for('routes.admin'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@routes.route('/service/<int:id>')
def get_service(id):
    response = request_session.get(f'http://127.0.0.1:3000/api/services/{id}')
    response.raise_for_status()
    service = response.json()

    return render_template('service.html',
        service=service)


# Example route for search
@routes.route('/search', methods=['GET'])
def search_services():
    query_string = request.args.get('q', '').strip()

    if not query_string:
        return jsonify({'error': 'No search query provided'})

    try:
        # Perform a basic search using SQLAlchemy like operator
        search_results = db_session.query(Service).filter(
            Service.name.ilike(f'%{query_string}%')
        ).all()

        # Serialize search results to JSON
        results_data = [{
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'endpoint': service.endpoint,
            'tags': [tag.name for tag in service.tags]
            # Add more fields as needed
        } for service in search_results]

        return jsonify({'results': results_data})

    finally:
        db_session.close()


@routes.route('/hello')
def hello():
    return jsonify('Hello World!')

@routes.route("/dashboard")
def dashboard():

    return render_template('dashboard.html', 
        # sap_services=sap_services,
        # Include Dash CSS and JS in the template
        # dash_css=dash_app._external_stylesheets,
        # dash_js=dash_app._external_scripts
    )


@routes.route('/time')
def time():
    try:
        hana_conn = db_connect()
        cursor = hana_conn.cursor()
        cursor.execute("SELECT CURRENT_UTCTIMESTAMP FROM DUMMY")
        current_time = cursor.fetchone()
        cursor.close()
        hana_conn.close()
        return jsonify(current_time)
    
    except Exception as e:
        return jsonify('Error: ' + str(e))

@routes.route('/user')
def user():
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    security_context = create_security_context(jwt_token)
    return jsonify({
        'user_name': security_context.get_logon_name(),
        'email': security_context.get_email(),
        'family_name': security_context.get_family_name(),
        'given_name': security_context.get_given_name(),
        'scopes': security_context.get_granted_scopes()
    })
