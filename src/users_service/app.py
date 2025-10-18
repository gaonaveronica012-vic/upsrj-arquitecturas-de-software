# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: app.py
# Descripción: Backend del microservicio
# ============================================================
# Archivo: users_service/app.py
# Descripción: Backend del microservicio de usuarios
# ============================================================
import sys, os
from flask import Flask, jsonify, request
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.utils import load_item, save_item, get_host
from common.vars import USERS_FILE, USER_API_URL

app = Flask(__name__)

# ============================================================
# GET /users -> devolver todos los usuarios
# ============================================================
@app.route('/users', methods=['GET'])
def get_users():
    users = load_item(USERS_FILE) or []
    return jsonify({"Usuarios": users}), 200  # clave "Usuarios" para compatibilidad test

# ============================================================
# GET /users/<id> -> devolver usuario por id
# ============================================================
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    users = load_item(USERS_FILE) or []
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

# ============================================================
# POST /users -> crear un usuario nuevo
# ============================================================
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(silent=True) or request.form
    name = data.get("name")

    if not name:
        return jsonify({"error": "Nombre requerido"}), 400  # Test espera mensaje de error

    users = load_item(USERS_FILE) or []

    # Generar nuevo ID incremental
    new_id = max([u['id'] for u in users], default=0) + 1
    new_user = {"id": new_id, "name": name}
    users.append(new_user)
    save_item(USERS_FILE, users)

    return jsonify(new_user), 200

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    app.run(port=get_host(USER_API_URL))



