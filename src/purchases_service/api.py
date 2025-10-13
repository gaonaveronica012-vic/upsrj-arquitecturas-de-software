import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from datetime import datetime
import requests
from common.utils import load_item, save_item, get_host
from common.vars import PURCHASES_FILE, PURCHASE_API_URL, USER_API_URL, PRODUCT_API_URL, USERS_FILE

app = Flask(__name__)

# Validar existencia de usuario
def user_exists(user_id):
    try:
        response = requests.get(f"http://localhost:{get_host(USER_API_URL)}/api/users/{user_id}")
        return response.status_code == 200
    except:
        return False

# Validar existencia de producto
def product_exists(product_id):
    try:
        response = requests.get(f"http://localhost:{get_host(PRODUCT_API_URL)}/api/products/{product_id}")
        return response.status_code == 200
    except:
        return False

# Registrar nueva compra
@app.route('/purchases', methods=['POST'])
def create_purchase():
    data = request.get_json()

    # Validar que lleguen ambos campos
    if not data or 'user_id' not in data or 'product_id' not in data:
        return jsonify({'error': 'user_id and product_id are required'}), 400

    user_id = data.get('user_id')
    product_id = data.get('product_id')

    if not user_exists(user_id):
        return jsonify({'error': 'User does not exist'}), 400
    if not product_exists(product_id):
        return jsonify({'error': 'Product does not exist'}), 400

    purchases = load_item(PURCHASES_FILE)
    new_id = max([p['id'] for p in purchases], default=0) + 1
    timestamp = datetime.now().isoformat()

    new_purchase = {
        'id': new_id,
        'user_id': user_id,
        'product_id': product_id,
        'timestamp': timestamp
    }

    purchases.append(new_purchase)
    save_item(PURCHASES_FILE, purchases)

    # Actualizar purchased_products en users.json
    users = load_item(USERS_FILE)
    for user in users:
        if user['id'] == user_id:
            if product_id not in user['purchased_products']:
                user['purchased_products'].append(product_id)
            break
    save_item(USERS_FILE, users)

    return jsonify(new_purchase), 201  # 201 creado correctamente

# Listar compras por usuario
@app.route('/purchases/<int:user_id>', methods=['GET'])
def get_purchases_by_user(user_id):
    purchases = load_item(PURCHASES_FILE)
    user_purchases = [p for p in purchases if p['user_id'] == user_id]
    # Devuelve 200 incluso si la lista está vacía
    return jsonify(user_purchases), 200

if __name__ == '__main__':
    app.run(port=get_host(PURCHASE_API_URL))
