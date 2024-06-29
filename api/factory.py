from flask import Flask


def create_api():
    app = Flask(__name__)

    # import routes
    from . import routes

    # register blueprints
    app.register_blueprint(routes.api)

    return app