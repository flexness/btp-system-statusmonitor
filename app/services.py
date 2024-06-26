from hdbcli import dbapi
from sap import xssec
from cfenv import AppEnv

cfenv = AppEnv()    

def db_connect():
    hana = cfenv.get_service(name='my-hana')
    conn = dbapi.connect(
        address=hana.credentials['host'],
        port=int(hana.credentials['port']),
        user=hana.credentials['user'],
        password=hana.credentials['password'],
        encrypt='true',
        sslTrustStore=hana.credentials['certificate']
    )
    return conn

def create_security_context(jwt_token):
    uaa_service = cfenv.get_service(name='my-xsuaa')
    security_context = xssec.create_security_context(jwt_token, uaa_service.credentials)
    return security_context
