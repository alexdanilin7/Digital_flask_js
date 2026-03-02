import sqlite3

from flask import Flask, jsonify, request, render_template
from database import Database

app = Flask(__name__)
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    """Все пользователи"""
    users = db.get_all_users()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """Пользователь по ID"""
    user = db.get_user_by_id(user_id)

    if user is None:
        return jsonify({"error": "Пользователь не найден"}), 404

    return jsonify(user.to_dict())

@app.route('/users', methods=['POST'])
def create_user():
    """Создание пользователя"""
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Необходимо указать имя и email"}), 400

    try:
        new_user = db.create_user(data['name'], data['email'])
        return jsonify({
            "message": "Пользователь успешно добавлен",
            "id": new_user.id
        }), 201
    except sqlite3.IntegrityError:
        # Обработка уникальности email
        return jsonify({"error": "Пользователь с таким email уже существует"}), 400

if __name__ == '__main__':
    app.run(debug=True)