#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from flask import make_response, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route("/status", methods=["GET"])
def status():
    """return status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def object_count():
    """count of objects of a class"""
    data = {}
    for key, value in classes.items():
        number = storage.count(value)
        data.update({key: number})
    return jsonify(data)
