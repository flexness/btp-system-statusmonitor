# collection of route namespaces

# import all route namespaces
from .services import ns as service_ns
from .tags import ns as tags_ns

# register all route namespaces
# imported/used in /api/factory.py
def register_routes(api):
    api.add_namespace(service_ns, path='/services')
    api.add_namespace(tags_ns, path='/tags')