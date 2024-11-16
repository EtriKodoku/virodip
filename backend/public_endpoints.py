from flask import Blueprint, request, jsonify
import json
from models import Users, Activity
from datetime import datetime

domain = Blueprint('not_user', __name__)


@domain.route('/geolocation', methods=['POST'])
def geolocation():
    try:
        # Отримання даних з реквесту
        data = json.loads(json.dumps(request.get_json()))

        email = data.get('email')
        action = data.get('action')
        time = data.get('time')

        # Перевірка даних
        if not email or action not in ['entered', 'exited'] or not time:
            return jsonify({"error": "Invalid input"}), 400

        # Перетворення часу в datetime
        time = datetime.fromisoformat(time)

        # Знаходження або створення користувача
        user, created = Users.get_or_create(email=email)

        # Оновлення статусу at_home
        if action == 'entered':
            user.at_home = True
        elif action == 'exited':
            user.at_home = False
        user.save()

        # Додавання запису в таблицю Activity
        Activity.create(user_id=user, action=action, time=time)

        return jsonify({"message": "Data saved successfully"}), 200
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