from flask import Blueprint, request, jsonify
import json
from models import Users, Activity
from datetime import datetime

domain = Blueprint("user", __name__)


@domain.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    print(request.environ.get("token_data"))
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid input"}), 400

    user, created = Users.get_or_create(email=data["email"])
    return jsonify({"message": "User added", "user": user}), 201


@domain.route("/user_activity/<int:user_id>", methods=["GET"])
def user_activity(user_id):
    try:
        user = Users.get_or_none(Users.id == user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        activities = Activity.select().where(Activity.user_id == user)
        activity_list = [
            {"id": activity.id, "action": activity.action, "time": activity.time}
            for activity in activities
        ]
        activity_list.reverse()
        return (
            jsonify(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "at_home": user.at_home,
                    },
                    "activities": activity_list,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@domain.route("/list_users", methods=["GET"])
def list_users():
    try:
        users = Users.select()
        user_list = [
            {"id": user.id, "email": user.email, "at_home": user.at_home}
            for user in users
        ]

        return jsonify({"users": user_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@domain.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    Users.delete().where(Users.id == user_id).execute()
    Activity.delete().where(Activity.user_id == user_id).execute()
    return jsonify({"message": "User deleted"}), 200


if __name__ == "__main__":
    print("YOU ARE IDIOT!!@")
