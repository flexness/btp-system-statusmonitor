import os
from dotenv import load_dotenv

load_dotenv()  # load .env vars


class Config:
    # default config envs
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    STATIC_FOLDER = 'static'

    # ALTERNATIVE DB: graphql and flask-sqlalchemy

    # HANA DB
    PORT = int(os.environ.get('PORT', 3000))
    HANA = {
        'host': os.environ.get('HANA_HOST'),
        'port': int(os.environ.get('HANA_PORT')),
        'user': os.environ.get('HANA_USER'),
        'password': os.environ.get('HANA_PASSWORD'),
        'certificate': os.environ.get('HANA_CERTIFICATE')
    }
    XSUAA = {
        'clientid': os.environ.get('XSUAA_CLIENTID'),
        'clientsecret': os.environ.get('XSUAA_CLIENTSECRET'),
        'url': os.environ.get('XSUAA_URL')
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}