from flask import Flask, jsonify, request, Blueprint, url_for, flash, redirect, render_template, send_from_directory, current_app
from .services import db_connect, create_security_context
import pandas as pd
import json
import requests
from api.models import Service, Tag


# create blueprint for routes
routes = Blueprint('routes', __name__)

session = requests.Session()

@routes.route('/')
@routes.route('/index')
def index():

    return render_template('index.html',

    )


@routes.route('/admin')
def admin():
    services = session.get('http://127.0.0.1:3000/api/services').json()
    tags = session.get('http://127.0.0.1:3000/api/tags').json()

    # services = session.get('http://127.0.0.1:3000/api/services')
    # services.raise_for_status()

    # tags = session.get('http://127.0.0.1:3000/api/tags')
    # tags.raise_for_status()


    return render_template('admin.html',
        services=services,
        tags=tags
        )

@routes.route('/services')
def table():
    response = session.get('http://127.0.0.1:3000/api/services')
    response.raise_for_status()
    sap_services = response.json()

    return render_template('table.html',
        sap_services=sap_services)

@routes.route("/addtag", methods=["POST"])
def add_tag():
    if request.method == 'POST':
        print("1")
        tag = request.form.get('tag_name')
        if tag is not None:
            try:
                response = requests.post('http://127.0.0.1:3000/api/tags', json={'name': tag})            
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
            'description': request.form.get('service_description'),
            'endpoint': request.form.get('service_endpoint'),
            'version': request.form.get('service_name'),
            'contact': request.form.get('service_contact')
        }
        if service_data is not None:
            try:                
                response = requests.post('http://127.0.0.1:3000/api/services', json=service_data)        
                response.raise_for_status()
                print("new service :", service_data)
                flash('Tag added successfully!', 'success')
            except requests.exceptions.RequestException as e:
                print(e)
                flash('Failed to add tag. Please try again.', 'error')
        else:
            flash('Please enter a tag name.', 'error')
    return redirect(url_for('routes.admin'))



@routes.route('/service/<int:id>')
def get_service(id):
    response = session.get(f'http://127.0.0.1:3000/api/services/{id}')
    response.raise_for_status()
    service = response.json()

    return render_template('service.html',
        service=service)


# Example route for search
@routes.route('/search', methods=['GET'])
def search_services():
    query_string = request.args.get('q', '').strip()

    from api.routes import Session
    session = Session()

    if not query_string:
        return jsonify({'error': 'No search query provided'})

    try:
        # Perform a basic search using SQLAlchemy like operator
        search_results = session.query(Service).filter(
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
        session.close()


@routes.route('/hello')
def hello():
    return jsonify('Hello World!')

@routes.route("/dashboard")
def dashboard():
    response = session.get('http://127.0.0.1:3000/api/services')
    response.raise_for_status()
    sap_services = response.json()
    return render_template('dashboard.html', 
        sap_services=sap_services,
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
