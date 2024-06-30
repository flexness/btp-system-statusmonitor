from app.factory import create_app
from api.factory import create_api, init_db

from config import config

def run_app():
# create app instance
    app = create_app()
    api_blueprint = create_api()

    # Register the API blueprint with the main app
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = run_app()
    app.logger.info("Starting the Flask application")
    # app.config.from_object(config[config_name])
    app.run(host='localhost', port=app.config['PORT'], debug=True)