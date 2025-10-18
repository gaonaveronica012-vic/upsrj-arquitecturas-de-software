# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: api.py
# Descripción: RESTful API de microservici
# ============================================================
# Archivo: api.py
# Descripción: RESTful API del microservicio de usuarios
# ============================================================
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from common.utils import load_item, save_item, get_host
from common.vars import USERS_FILE, USER_API_URL

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def api_get_users():
    users = load_item(USERS_FILE) or []
    return jsonify({"Usuarios": users}), 200

@app.route('/api/users', methods=['POST'])
def api_create_user():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Nombre requerido"}), 400

    users = load_item(USERS_FILE) or []
    new_id = max([u['id'] for u in users], default=0) + 1
    new_user = {"id": new_id, "name": data["name"]}
    users.append(new_user)
    save_item(USERS_FILE, users)

    return jsonify(new_user), 200

if __name__ == "__main__":
    app.run(port=get_host(USER_API_URL))
