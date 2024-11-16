from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Дозволити CORS для всього додатку

# Створення Blueprint
my_blueprint = Blueprint('my_blueprint', __name__)

@my_blueprint.route('/api/add_user', methods=['POST'])
def add_user_blueprint():
    return {"message": "User added via blueprint"}

# Додати CORS до Blueprint (зайве при CORS(app), але залишено для локальних змін)
CORS(my_blueprint)

# Реєстрація Blueprint
app.register_blueprint(my_blueprint)

# Інший Blueprint
domain = Blueprint('user', __name__)

users = []

@domain.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'email': data['email']
    }
    users.append(new_user)  # Виправлено помилку в методі
    return jsonify({"message": "User added", "user": new_user}), 201

@domain.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@domain.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    return jsonify({"message": "User deleted"}), 204

@domain.route('/geolocation', methods=['POST'])
def get_geolocation():
    data = request.get_json()

    if not data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({"error": "Invalid input"}), 400

    return jsonify({"message": "Geolocation received", "data": data}), 200

@domain.route('/')
def index():
    return "Flask API is running!"

# Реєстрація Blueprint
app.register_blueprint(domain)

if __name__ == '__main__':
    app.run(debug=True)
