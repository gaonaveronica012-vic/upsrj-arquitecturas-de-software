# Archivo: app.py (products_service)
# Descripción: API REST para gestión de productos
# ============================================================
import sys, os
from flask import Flask, jsonify, request
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.utils import load_item, save_item, get_host
from common.vars import PRODUCTS_FILE, PRODUCT_API_URL

app = Flask(__name__)

# ============================================================
# GET /products -> devolver todos los productos
# ============================================================
@app.route('/products', methods=['GET'])
def get_products():
    products = load_item(PRODUCTS_FILE) or []
    return jsonify({"Productos": products}), 200  # clave "Productos" para test

# ============================================================
# POST /products -> crear un producto nuevo
# ============================================================
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json(silent=True) or request.form
    name = data.get("name")
    price = data.get("price")

    if not name or not price:
        return jsonify({"error": "name y price requeridos"}), 400

    try:
        price = float(price)
    except ValueError:
        return jsonify({"error": "price debe ser un número"}), 400

    products = load_item(PRODUCTS_FILE) or []
    new_id = max([p['id'] for p in products], default=0) + 1
    new_product = {"id": new_id, "name": name, "price": price}
    products.append(new_product)
    save_item(PRODUCTS_FILE, products)

    return jsonify(new_product), 200

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    app.run(port=get_host(PRODUCT_API_URL))

