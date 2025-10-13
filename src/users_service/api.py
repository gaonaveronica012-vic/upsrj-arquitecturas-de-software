# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: api.py
# Descripción: RESTful API de microservicio
# ============================================================
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify
from common.utils import load_item, get_host
from common.vars import USERS_FILE, USER_API_URL

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = load_item(USERS_FILE)
    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    users = load_item(USERS_FILE)
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(port=get_host(USER_API_URL))
