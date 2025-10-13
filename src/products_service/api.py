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
from common.vars import PRODUCTS_FILE, PRODUCT_API_URL

app = Flask(__name__)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = load_item(PRODUCTS_FILE)
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    products = load_item(PRODUCTS_FILE)
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(port=get_host(PRODUCT_API_URL))