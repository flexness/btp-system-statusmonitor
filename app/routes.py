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

# special route
# for listing all auto mapped routes
# e.g. routes created by flask_restx for internal API calls
# so you can use:
# endpoint_url = url_for('api.tags_tag_list')

@routes.route('/internal-routes')
def list_internal_routes():
    import urllib
    data = []
    for rule in current_app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        url = urllib.parse.unquote(f'{rule}')
        line = f"{rule.endpoint}: {url} ({methods})"
        data.append(line)
    # return "<br>".join(sorted(output))
    return render_template('default.html', data=data)



@routes.route('/')
@routes.route('/index')
def index():
    
    service_types = ServiceType
    service_types=service_types
    return render_template('index.html',
        service_types=service_types
    )

@routes.route('/admin')
def admin():
    services = db_session.query(Service).all()
    tags = db_session.query(Tag).all()
    service_types = ServiceType
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
    try:
        if service_id:
            db_session = Session()
            service = db_session.query(Service).get(service_id)
        else:
            service = request.form.get('service_endpoint')
        if not service:
            print("Service or endpoint not found")
            return jsonify({"error": "Service not found"}), 404
        try:
            response = requests.get(service.endpoint, timeout=5)
            print("response: ", response)
            for item in response:
                print(item)
            match response.status_code:
                case 200:
                    service.status = 'up'
                case 404:
                    service.status = 'down'
                    print("404")
                case "n/q":
                    service.status = 'n/q'
                case _:
                    service.status = 'down'

        except requests.RequestException as e:
            service.status = 'n/q'
            # return jsonify({"error": str(e)}), 500
        
        print("service status: ", service.status)
        db_session.commit()

        return jsonify({
            "id": service.id,
            "status": service.status
        })
    
    except Exception as e:
        db_session.rollback()  # Rollback in case of any other exception
        return jsonify({"error": str(e)}), 500
    
    finally:
        db_session.close()


@routes.route("/check_endpoint", methods=["POST"])
def check_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        service_endpoint = data.get("service_endpoint")
        if service_endpoint is not None:
            try:
                response = requests.get(service_endpoint, timeout=5)
                print("response: ", response)
                match response.status_code:
                    case 200:
                        return jsonify({"status": "up"})
                    case 404:
                        return jsonify({"status": "down"})
                    case "n/q":
                        return jsonify({"status": "n/q"})
                    case _:
                        return jsonify({"status": "down"})
            except requests.RequestException as e:
                return jsonify({"status": "n/q"})
        else:
            return jsonify({"error": "Service not found"})


@routes.route("/addtag", methods=["POST"])
def add_tag():
    if request.method == 'POST':
        print("1")
        tag = request.form.get('tag_name')
        url = url_for('api.tags_tag_list')
        print(url)
        if tag is not None:
            with current_app.test_client() as client:
                endpoint_url = url_for('api.tags_tag_list')
                response = client.post(endpoint_url, json={'name': tag})
                print(response)
                # return jsonify(response), response.status_code
                return redirect(url_for('routes.admin'))
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
                
                tags_instances = [db_session.query(Tag).get(tag_id) for tag_id in service_data['tags']]
                dependent_services_instances = [db_session.query(Service).get(service_id) for service_id in service_data['dependent_services']]

                new_service = Service(
                    name=service_data['name'],
                    description=service_data['description'],
                    endpoint=service_data['endpoint'],
                    version=service_data['version'],
                    type=service_data['type'],
                    tags=tags_instances,  
                    dependent_services=dependent_services_instances
                )
                db_session.add(new_service)
                db_session.commit()
                new_service_id = new_service.id
                # response = requests.post('http://127.0.0.1:3000/api/services/', json=service_data)        
                # response.raise_for_status()
                print("new service :", new_service_id)
                flash('service added successfully!', 'success')
                # check service ping (+ write to db)
                check_service(new_service_id)
            except Exception as e:
                db_session.rollback()
            # except requests.exceptions.RequestException as e:
                print(e)
                flash('Failed to add service. Please try again.', 'error')
            finally:
                db_session.close()
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


@routes.route('/edit_service', methods=["POST"])
def edit_service():
    if request.method == 'POST':

        service_id = request.form.get('service_id')
        if not service_id:
            return jsonify({"error": "No service ID provided"}), 400

        try:
            service = db_session.query(Service).get(service_id)
            if not service:
                return jsonify({"error": "Service not found"}), 404
            
            # get the form data
            name = request.form.get('service_name')
            description = request.form.get('service_desc')
            endpoint = request.form.get('service_endpoint')
            version = request.form.get('service_name')
            contact = request.form.get('service_contact')
            dependent_services = request.form.getlist('services')
            tags = request.form.getlist('tags')
            type = request.form.get('service_type')
            print("dependent services: ", dependent_services)

            if str(service_id) in dependent_services:
                dependent_services.remove(str(service_id))

            tags_instances = [db_session.query(Tag).get(tag_id) for tag_id in tags]
            dependent_services_instances = [db_session.query(Service).get(service_id) for service_id in dependent_services]

            # update the service
            service.name = name
            service.description = description
            service.endpoint = endpoint
            service.version = version
            service.contact = contact
            service.dependent_services = dependent_services_instances
            service.tags = tags_instances
            service.type = type

            print("service after update: ", service)

            db_session.commit()
            flash('Service edited successfully!', 'success')
            # return jsonify({"success": True}), 200
            
            return redirect(url_for('routes.admin'))
        
        except Exception as e:
            db_session.rollback()
            return jsonify({"error": str(e)}), 500
        
        finally:
            db_session.close()

    return redirect(url_for('routes.admin'))


@routes.route('/service/<int:id>')
def get_service(id):
    with current_app.test_client() as client:
        endpoint_url = url_for('api.services_service_resource', id=id)
        response = client.get(endpoint_url)
        service_data = response.get_json()
        print(response.data)

        return render_template('service.html',
            service=service_data)


# mining route for search
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






@routes.route('/hello')
def hello():
    return jsonify('Hello World!')
