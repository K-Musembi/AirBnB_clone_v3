#!/usr/bin/python3
"""view for user objects"""

from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """retrieve all users"""
    all_objs = storage.all(User)
    new_lst = []
    for obj in all_objs.values():
        new_lst.append(obj.to_dict())
    return jsonify(new_lst)


@app_views.route(
        "/users/<user_id>", methods=["GET"], strict_slashes=False)
def single_user(user_id):
    """retrieve an object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
        "/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """delete an object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """create a user"""
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    if "email" not in data:
        abort(404, message="Missing email")
    if "password" not in data:
        abort(404, message="Missing password")
    email = data["email"]
    password = data["password"]
    user_obj = User(email, password)
    return jsonify(user_obj.to_dict()), 201


@app_views.route(
        "/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """update a user object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    updated = obj.to_dict()
    for key, value in data.items():
        if key in ("id", "email", "created_at", "updated_at"):
            continue
        updated[key] = value
    return jsonify(updated), 200
