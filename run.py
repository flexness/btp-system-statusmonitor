from app.factory import create_app
from api.factory import create_api
from database import init_db
from config import DevelopmentConfig

def run_app():  
    # create app instance
    app = create_app()
    
    print(app.config)

    # init db if not existing on app startup
    init_db()    

    # cget/reate api blueprint
    api_blueprint = create_api()

    # register api blueprint to app
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = run_app()
    app.logger.info("Starting the Flask application")
    # app.config.from_object(config[config_name])
    app.run(host='localhost', port=app.config['PORT'], debug=True)