#!/usr/bin/python3
"""view for review objects"""

from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route(
        "/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def all_reviews(place_id):
    """retrieve all reviews"""
    objs = storage.get(Place, place_id)
    if objs is None:
        abort(404)
    new_lst = []
    for obj in objs.reviews:
        new_lst.append(obj.to_dict())
    return jsonify(new_lst)


@app_views.route(
        "/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def single_review(review_id):
    """retrieve an object"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
        "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """delete an object"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    return jsonify({}), 200


@app_views.route(
        "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """create a review"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    if "user_id" not in data:
        abort(404, message="Missing user_id")
    user_obj = storage.get(User, data["user_id"])
    if user_obj is None:
        abort(404)
    if "text" not in data:
        abort(404, message="Missing text")
    review_obj = Review(place_id, data["user_id"], data["text"])
    return jsonify(review_obj.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """update a place object"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, message="Not a JSON")
    updated = obj.to_dict()
    for key, value in data.items():
        if key in ("id", "user_id", "place_id", "created_at", "updated_at"):
            continue
        updated[key] = value
    return jsonify(updated), 200
