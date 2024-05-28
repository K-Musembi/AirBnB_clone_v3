#!/usr/bin/python3
"""view for state objects"""

from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from markupsafe import escape
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """retrieve all objects"""

    dct = storage.all(State)
    new_lst = []
    for obj in dct.values():
        attrs = obj.to_dict()
        new_lst.append(attrs)
    return jsonify(new_lst)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def single_state(state_id):
    """retrieve an object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """delete an object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """create a state"""
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    if "name" not in data:
        abort(404, message="Missing name")
    new_state = State(data["name"])
    storage.new(new_state)
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """update an object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    updated = obj.to_dict()
    for key, value in data.items():
        if key in ("id", "created_at", "updated_at"):
            continue
        updated[key] = value
    return jsonify(updated), 200
