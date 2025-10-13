# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: api.py
# Descripción: RESTful API de microservicio
# ============================================================
# src/gateway/api.py
from flask import Flask, jsonify
import requests

app = Flask(__name__)

USERS_API = 'http://localhost:5003/api'
PRODUCTS_API = 'http://localhost:5005/api'
PURCHASES_API = 'http://localhost:5007/api'

@app.route('/api/users/<int:user_id>/purchases', methods=['GET'])
def user_with_purchases(user_id):
    # 1) Obtener usuario
    try:
        r_user = requests.get(f'{USERS_API}/users/{user_id}', timeout=2)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'users_service unreachable', 'details': str(e)}), 502
    if r_user.status_code != 200:
        return jsonify({'error': 'user not found', 'status': r_user.status_code}), r_user.status_code
    user = r_user.json()

    # 2) Obtener compras del usuario
    try:
        r_p = requests.get(f'{PURCHASES_API}/purchases/{user_id}', timeout=2)
        purchases = r_p.json() if r_p.status_code == 200 else []
    except:
        purchases = []

    # 3) Para cada compra obtener info del producto
    purchased_products = []
    for p in purchases:
        pid = p.get('product_id')
        try:
            rprod = requests.get(f'{PRODUCTS_API}/products/{pid}', timeout=2)
            if rprod.status_code == 200:
                purchased_products.append(rprod.json())
            else:
                purchased_products.append({'id': pid, 'name': '<unavailable>'})
        except:
            purchased_products.append({'id': pid, 'name': '<unavailable>'})

    response = {
        'user': {'id': user.get('id'), 'name': user.get('name')},
        'purchased_products': purchased_products
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)
# src/gateway/api.py
from flask import Flask, jsonify
import requests

app = Flask(__name__)

USERS_API = 'http://localhost:5003/api'
PRODUCTS_API = 'http://localhost:5005/api'
PURCHASES_API = 'http://localhost:5007/api'

@app.route('/api/users/<int:user_id>/purchases', methods=['GET'])
def user_with_purchases(user_id):
    # 1) Obtener usuario
    try:
        r_user = requests.get(f'{USERS_API}/users/{user_id}', timeout=2)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'users_service unreachable', 'details': str(e)}), 502
    if r_user.status_code != 200:
        return jsonify({'error': 'user not found', 'status': r_user.status_code}), r_user.status_code
    user = r_user.json()

    # 2) Obtener compras del usuario
    try:
        r_p = requests.get(f'{PURCHASES_API}/purchases/{user_id}', timeout=2)
        purchases = r_p.json() if r_p.status_code == 200 else []
    except:
        purchases = []

    # 3) Para cada compra obtener info del producto
    purchased_products = []
    for p in purchases:
        pid = p.get('product_id')
        try:
            rprod = requests.get(f'{PRODUCTS_API}/products/{pid}', timeout=2)
            if rprod.status_code == 200:
                purchased_products.append(rprod.json())
            else:
                purchased_products.append({'id': pid, 'name': '<unavailable>'})
        except:
            purchased_products.append({'id': pid, 'name': '<unavailable>'})

    response = {
        'user': {'id': user.get('id'), 'name': user.get('name')},
        'purchased_products': purchased_products
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)
