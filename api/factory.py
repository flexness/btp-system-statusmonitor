from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, version='1.0', title='Services API', description='Simple API to provide endpoints for managing services, tags, etc.')

def create_api():

    # import routes from /routes/__init__.py
    from .routes import register_routes
    register_routes(api)

    return api_blueprint
