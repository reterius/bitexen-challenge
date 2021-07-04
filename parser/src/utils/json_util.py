import datetime

from bson import ObjectId
from flask import json
from marshmallow.compat import unicode


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()

        elif isinstance(obj, ObjectId):
            return unicode(obj)

        return json.JSONEncoder.default(self, obj)
