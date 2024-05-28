#!/usr/bin/python3
"""view for amenity objects"""

from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models.amenity import Amenity
from models import storage
import models


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """retrieve all amenities"""
    all_objs = storage.all(Amenity)
    new_dct = []
    for obj in all_objs.values():
        new_dct.append(obj.to_dict())
    return jsonify(new_dct)


@app_views.route(
        "/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def single_amenity(amenity_id):
    """retrieve an object"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
        "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete an object"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """create an amenity"""
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    if "name" not in data:
        abort(404, message="Missing name")
    amenity_obj = Amenity(data["name"])
    return jsonify(amenity_obj.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """update an amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    if "name" not in data:
        abort(404, message="Missing name")
    updated = obj.to_dict()
    for key, value in data.items():
        if key in ("id", "created_at", "updated_at"):
            continue
        updated[key] = value
    return jsonify(updated), 200
