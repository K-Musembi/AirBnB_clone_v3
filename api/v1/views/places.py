#!/usr/bin/python3
"""view for place objects"""

from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route(
        "/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def all_places(city_id):
    """retrieve all places"""
    objs = storage.get(City, city_id)
    if objs is None:
        abort(404)
    new_lst = []
    for obj in objs.places:
        new_lst.append(obj.to_dict())
    return jsonify(new_lst)


@app_views.route(
        "/places/<place_id>", methods=["GET"], strict_slashes=False)
def single_place(place_id):
    """retrieve an object"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
        "/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """delete an object"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    return jsonify({}), 200


@app_views.route(
        "/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """create a place"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    if "user_id" not in data:
        abort(404, message="Missing user_id")
    user_obj = storage.get(User, data["user_id"])
    if user_obj is None:
        abort(404)
    if "name" not in data:
        abort(404, message="Missing name")
    place_obj = Place(city_id, data["user_id"], data["name"])
    return jsonify(place_obj.to_dict()), 201


@app_views.route(
        "/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """update a place object"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    updated = obj.to_dict()
    for key, value in data.items():
        if key in ("id", "user_id", "city_id", "created_at", "updated_at"):
            continue
        updated[key] = value
    return jsonify(updated), 200
