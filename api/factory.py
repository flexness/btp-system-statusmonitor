from flask import Flask, Blueprint
from flask_restx import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from database import Session

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, version='1.0', title='Services API', description='Simple API to provide endpoints for managing services, tags, etc.')

def create_api():
    # app = Flask(__name__)
    # api.init_app(app)

    # import routes
    from .routes import register_routes
    register_routes(api)

    return api_blueprint
