from app.factory import create_app

# create app instance
app = create_app()

if __name__ == '__main__':
    app.logger.info("Starting the Flask application")
    app.run(host='localhost', port=app.config['PORT'], debug=True)