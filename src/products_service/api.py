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
from flask import Flask, request, jsonify
from common.utils import load_item, save_item, get_host
from common.vars import PRODUCTS_FILE, PRODUCT_API_URL

app = Flask(__name__)

@app.route('/api/products', methods=['GET'])
def api_get_products():
    products = load_item(PRODUCTS_FILE) or []
    return jsonify({"Productos": products}), 200

@app.route('/api/products', methods=['POST'])
def api_create_product():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("price"):
        return jsonify({"error": "name y price requeridos"}), 400

    try:
        price = float(data.get("price"))
    except ValueError:
        return jsonify({"error": "price debe ser un número"}), 400

    products = load_item(PRODUCTS_FILE) or []
    new_id = max([p['id'] for p in products], default=0) + 1
    new_product = {"id": new_id, "name": data["name"], "price": price}
    products.append(new_product)
    save_item(PRODUCTS_FILE, products)

    return jsonify(new_product), 200

if __name__ == "__main__":
    app.run(port=get_host(PRODUCT_API_URL))
