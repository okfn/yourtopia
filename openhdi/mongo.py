from pymongo import Connection as MongoConnection
from pymongo.dbref import DBRef
from pymongo.objectid import ObjectId
from pymongo.cursor import Cursor
from datetime import datetime, date
from json import JSONEncoder 

conn = MongoConnection() 

class MongoEncoder(JSONEncoder):
    
    def default(self, o):
        if isinstance(o, Cursor):
            return [x for x in o]
        if isinstance(o, DBRef):
            return o.as_doc().to_dict()
        elif isinstance(o, ObjectId):
            return unicode(o)
        elif isinstance(o, (datetime, date)):
            return o.isoformat()
        return JSONEncoder.default(self, o)

def jsonify(app, obj):
    from flask import request
    content = MongoEncoder().encode(obj) 
    if 'callback' in request.args:
        content = str(callback) + '(' + content+ ')'
    return app.response_class(content, mimetype='application/json')


def get_db():
    return conn['openhdi']


