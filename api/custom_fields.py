# api/v1/custom_fields.py
from flask_restx import fields

class DepthLimitedNested(fields.Nested):
    def __init__(self, nested, max_depth, *args, **kwargs):
        super(DepthLimitedNested, self).__init__(nested, *args, **kwargs)
        self.max_depth = max_depth

    def output(self, key, obj, **kwargs):
        depth = kwargs.get('depth', 0)
        if depth >= self.max_depth:
            return None
        kwargs['depth'] = depth + 1
        return super(DepthLimitedNested, self).output(key, obj, **kwargs)