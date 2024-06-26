from flask import Flask, jsonify, request, Blueprint, render_template, send_from_directory, current_app
from .services import db_connect, create_security_context

import json
# create blueprint for routes
routes = Blueprint('routes', __name__)

# Load SAP system landscape data from JSON file
with open('systems.json') as json_file:
    sap_landscape = json.load(json_file)

with open('sap_services.json') as json_file:
    sap_services = json.load(json_file)

with open('external_services.json') as json_file:
    external_services = json.load(json_file)

with open('enterprise_services.json') as json_file:
    enterprise_services = json.load(json_file)
@routes.route('/')
@routes.route('/index')
def index():

    return render_template('index.html',
        sap_landscape=sap_landscape,
        sap_services=sap_services,
        external_services=external_services,
        enterprise_services=enterprise_services
    )


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


@routes.route('/api/systems/core')
def api_get_systems():
    data = load_json_data('systems.json')
    return jsonify(data)

@routes.route('/api/systems/sap')
def api_get_sap_services():
    data = load_json_data('sap_services.json')
    return jsonify(data)

@routes.route('/api/systems/external')
def api_get_external_services():
    data = load_json_data('external_services.json')
    return jsonify(data)

@routes.route('/api/systems/enterprise')
def api_get_enterpise_services():
    data = load_json_data('enterprise_services.json')
    return jsonify(data)


@routes.route('/hello')
def hello():
    return jsonify('Hello World!')

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
