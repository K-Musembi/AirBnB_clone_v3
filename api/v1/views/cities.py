#!/usr/bin/python3
"""view for state objects"""

from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from markupsafe import escape
from models.city import City
from models.state import State
from models import storage
import models


@app_views.route(
        "/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def all_cities(state_id):
    """retrieve all cities"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    if models.storage_t == "db":
        city_list = obj.cities
    else:
        city_list = obj.cities()
    new_list = []
    for city_obj in cities:
        new_list.append(city_obj.to_dict())
    return jsonify(new_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def single_city(city_id):
    """retrieve an object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """delete an object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    return jsonify({}), 200


@app_views.route(
        "states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """create a city"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    if "name" not in data:
        abort(404, message="Missing name")
    city_obj = City(data["name"])
    city_obj.state_id = state_id
    return jsonify(city_obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """update a city object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    updated = obj.to_dict()
    updated["name"] = data["name"]
    return jsonify(updated), 200
