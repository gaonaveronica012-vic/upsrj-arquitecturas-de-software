# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# ============================================================
# Archivo: app.py
# Descripción: Backend del microservicio de compras
# ============================================================
import sys, os
from datetime import datetime
from flask import Flask, jsonify, request
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.utils import load_item, save_item, get_host
from common.vars import PURCHASES_FILE, USERS_FILE, PURCHASE_API_URL, PRODUCTS_FILE

app = Flask(__name__)

# ============================================================
# GET /purchases -> Obtener todas las compras
# ============================================================
@app.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = load_item(PURCHASES_FILE)
    return jsonify({"Compras": purchases}), 200

# ============================================================
# POST /purchases -> Crear una compra
# ============================================================
@app.route('/purchases', methods=['POST'])
def create_purchase():
    data = request.get_json() or request.form
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not user_id:
        return jsonify({"error": "user_id missing"}), 400
    if not product_id:
        return jsonify({"error": "product_id missing"}), 400

    try:
        user_id = int(user_id)
        product_id = int(product_id)
    except ValueError:
        return jsonify({"error": "user_id y product_id deben ser enteros"}), 400

    users = load_item(USERS_FILE)
    products = load_item(PRODUCTS_FILE)

    if not any(u["id"] == user_id for u in users):
        return jsonify({"error": "user not found"}), 404
    if not any(p["id"] == product_id for p in products):
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
        if u["id"] == user_id:
            if "purchased_products" not in u:
                u["purchased_products"] = []
            if product_id not in u["purchased_products"]:
                u["purchased_products"].append(product_id)
            break
    save_item(USERS_FILE, users)

    return jsonify(new_purchase), 201

# ============================================================
# GET /purchases/<user_id> -> Obtener compras de un usuario
# ============================================================
@app.route('/purchases/<int:user_id>', methods=['GET'])
def get_purchases_by_user(user_id):
    users = load_item(USERS_FILE)
    if not any(u["id"] == user_id for u in users):
        return jsonify({"Compras": []}), 200

    purchases = load_item(PURCHASES_FILE)
    user_purchases = [p for p in purchases if p["user_id"] == user_id]
    return jsonify({"Compras": user_purchases}), 200

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    app.run(port=get_host(PURCHASE_API_URL))


