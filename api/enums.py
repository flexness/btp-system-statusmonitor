from enum import Enum


class ServiceType(Enum):
    APPLICATION_SERVER = 'application_server'
    DATABASE_SERVER = 'database_server'
    WEB_SERVER = 'web_server'
    MIDDLEWARE = 'middleware'
    INTERFACE = 'interface'
    API = 'api'
    JOB_SCHEDULER = 'job_scheduler'
    SECURITY_SERVICE = 'security_service'
    MONITORING_SERVICE = 'monitoring_service'
    DEVOPS_SERVICE = 'devops_service'
    ERP_MODULE = 'erp_module'
    CLOUD_SERVICE = 'cloud_service'
    FILE_SERVER = 'file_server'
    MAIL_SERVER = 'mail_server'
    IDENTITY_PROVIDER = 'identity_provider'
    LOAD_BALANCER = 'load_balancer'
    CACHE_SERVICE = 'cache_service'
    PLATFORM = 'platform'


class ServiceScope(Enum):
    TYPE1 = 'internal'
    TYPE2 = 'external'


class Persons(Enum):
    Person1 = 'SZ 1234567'
    Person2 = 'SZ 1234577'