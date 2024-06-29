from flask import Flask, jsonify, request, Blueprint, render_template, send_from_directory, current_app
from .services import db_connect, create_security_context
import pandas as pd
import json
import requests

session = requests.Session()

# create blueprint for routes
routes = Blueprint('routes', __name__)


@routes.route('/')
@routes.route('/index')
def index():

    return render_template('index.html',

    )


@routes.route('/admin')
def admin():
    response = session.get('http://127.0.0.1:3000/api/services')
    response.raise_for_status()
    sap_services = response.json()

    return render_template('admin.html',
        sap_services=sap_services)

@routes.route('/table')
def table():
    response = session.get('http://127.0.0.1:3000/api/services')
    response.raise_for_status()
    sap_services = response.json()

    return render_template('table.html',
        sap_services=sap_services)




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
