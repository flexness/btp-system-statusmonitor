from flask import Flask, jsonify, request
from cfenv import AppEnv
from config import Config

# add config switch later
def create_app():

    # create flask instance
    app = Flask(__name__)

    # set config from config.py
    app.config.from_object(Config)

    # import routes
    from . import routes

    # register blueprints
    app.register_blueprint(routes.routes)

    return app