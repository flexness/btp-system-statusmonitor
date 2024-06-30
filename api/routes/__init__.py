# api/routes/__init__.py
from .services import ns as service_ns
from .tags import ns as tags_ns


def register_routes(api):
    api.add_namespace(service_ns, path='/services')
    api.add_namespace(tags_ns, path='/tags')