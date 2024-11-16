from flask import Blueprint, request, jsonify
import json
from models import Users, Activity
from datetime import datetime


domain = Blueprint('user', __name__)





@domain.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    print(request.environ.get('token_data'))
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Invalid input"}), 400


    user, created = Users.get_or_create(email=data['email'])
    return jsonify({"message": "User added", "user": user}), 201


@domain.route('/user_activity/<int:user_id>', methods=['GET'])
def user_activity(user_id):
    try:
        user = Users.get_or_none(Users.id == user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        activities = Activity.select().where(Activity.user_id == user)
        activity_list = [{
            "id": activity.id,
            "action": activity.action,
            "time": activity.time.isoformat()
        } for activity in activities]

        return jsonify({
            "user": {"id": user.id, "email": user.email, "at_home": user.at_home},
            "activities": activity_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@domain.route('/list_users', methods=['GET'])
def list_users():
    try:
        users = Users.select()
        user_list = [{
            "id": user.id,
            "email": user.email,
            "at_home": user.at_home
        } for user in users]

        return jsonify({"users": user_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@domain.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    Users.delete().where(Users.id == user_id).execute()
    Activity.delete().where(Activity.user_id == user_id).execute()
    return jsonify({"message": "User deleted"}), 200

# @domain.route('/geolocation', methods=['POST'])
# def geolocation():
#     try:
#         # Отримання даних з реквесту
#         data = json.loads(json.dumps(request.get_json()))

#         email = data.get('email')
#         action = data.get('action')
#         time = data.get('time')

#         # Перевірка даних
#         if not email or action not in ['entered', 'exited'] or not time:
#             return jsonify({"error": "Invalid input"}), 400

#         # Перетворення часу в datetime
#         time = datetime.fromisoformat(time)

#         # Знаходження або створення користувача
#         user, created = Users.get_or_create(email=email)

#         # Оновлення статусу at_home
#         if action == 'entered':
#             user.at_home = True
#         elif action == 'exited':
#             user.at_home = False
#         user.save()

#         # Додавання запису в таблицю Activity
#         Activity.create(user_id=user, action=action, time=time)

#         return jsonify({"message": "Data saved successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@domain.route('/')
def index():
    return "Flask API is running!"
