# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: api.py
# Descripción: RESTful API del microservicio de compras
# ============================================================
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from common.utils import load_item, save_item, get_host
from common.vars import PURCHASES_FILE, PURCHASE_API_URL, USERS_FILE, PRODUCTS_FILE
from datetime import datetime

app = Flask(__name__)

# GET todas las compras
@app.route('/api/purchases', methods=['GET'])
def api_get_purchases():
    purchases = load_item(PURCHASES_FILE)
    return jsonify({"Compras": purchases}), 200

# POST nueva compra
@app.route('/api/purchases', methods=['POST'])
def api_create_purchase():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo JSON requerido"}), 400

    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not user_id or not product_id:
        return jsonify({"error": "user_id y product_id son requeridos"}), 400

    try:
        user_id = int(user_id)
        product_id = int(product_id)
    except ValueError:
        return jsonify({"error": "Campos deben ser enteros"}), 400

    users = load_item(USERS_FILE)
    products = load_item(PRODUCTS_FILE)

    if not any(u['id'] == user_id for u in users):
        return jsonify({"error": "user not found"}), 404
    if not any(p['id'] == product_id for p in products):
        return jsonify({"error": "product not found"}), 404

    purchases = load_item(PURCHASES_FILE)
    new_id = max([p['id'] for p in purchases], default=0) + 1

    new_purchase = {
        "id": new_id,
        "user_id": user_id,
        "product_id": product_id,
        "timestamp": datetime.now().isoformat()
    }
    purchases.append(new_purchase)
    save_item(PURCHASES_FILE, purchases)

    # Actualizar productos comprados del usuario
    for u in users:
        if u['id'] == user_id:
            if 'purchased_products' not in u:
                u['purchased_products'] = []
            u['purchased_products'].append(product_id)
            break
    save_item(USERS_FILE, users)

    return jsonify(new_purchase), 201

# Main
if __name__ == "__main__":
    app.run(port=get_host(PURCHASE_API_URL))




