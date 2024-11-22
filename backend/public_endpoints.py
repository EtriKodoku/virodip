from flask import Blueprint, request, jsonify
from models import Users, Activity
from datetime import datetime
import pytz

domain = Blueprint("not_user", __name__)


@domain.route("/geolocation", methods=["POST"])
def geolocation():
    with open("request.txt", "a") as file:
        file.write(request.get_data().decode('utf-8'))
        file.close()
    try:
        # Отримання даних з реквесту
        data = request.get_json()
        email = data["email"]
        action = data["action"]
        time_data = data["time"]

        # Перевірка даних
        if not email or action not in ["entered", "exited"] or not time:
            return jsonify({"error": "Invalid input"}), 400

        # Перетворення часу в datetime
        date_format = "%B %d, %Y at %I:%M%p"
        ua_timezone = pytz.timezone("Europe/Kyiv")
        time = datetime.strptime(time_data, date_format)
        time = ua_timezone.localize(time)

        # Знаходження або створення користувача
        user, created = Users.get_or_create(email=email)

        # Оновлення статусу at_home
        if action == "entered":
            user.at_home = True
        elif action == "exited":
            user.at_home = False
        user.save()

        # Додавання запису в таблицю Activity
        Activity.create(user_id=user, action=action, time=time)

        return jsonify({"message": "Data saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500