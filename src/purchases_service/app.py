import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template, request, redirect, url_for
import requests
from common.vars import PURCHASE_API_URL

app = Flask(__name__, template_folder='templates')

# Mostrar formulario para registrar compra
@app.route('/purchases', methods=['GET'])
def show_purchase_form():
    return render_template('create_purchase.html')

# Procesar formulario de compra
@app.route('/purchases', methods=['POST'])
def submit_purchase():
    user_id = request.form.get('user_id', type=int)
    product_id = request.form.get('product_id', type=int)

    payload = {
        'user_id': user_id,
        'product_id': product_id
    }

    response = requests.post(f"{PURCHASE_API_URL}/purchases", json=payload)

    if response.status_code == 201:
        return redirect(url_for('view_purchases', user_id=user_id))
    else:
        error = response.json().get('error', 'Error desconocido')
        return f"<h2>Error: {error}</h2><a href='/purchases'>Volver</a>"

# Mostrar compras de un usuario
@app.route('/purchases/<int:user_id>', methods=['GET'])
def view_purchases(user_id):
    response = requests.get(f"{PURCHASE_API_URL}/purchases/{user_id}")
    purchases = response.json() if response.status_code == 200 else []
    return render_template('purchases.html', user_id=user_id, purchases=purchases)

if __name__ == '__main__':
    app.run(port=5006)