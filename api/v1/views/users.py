#!/usr/bin/python3
"""users module"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User"""
    if request.is_json:
        data = request.get_json()
        if "email" in data:
            if "password" in data:
                new_user = User(**data)
                storage.new(new_user)
                new_user.save()
                return jsonify(new_user.to_dict()), 201
            else:
                abort(400, "Missing password")
        else:
            abort(400, "Missing email")
    else:
        abort(400, "Not a JSON")


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict())
    else:
        abort(400, "Not a JSON")
