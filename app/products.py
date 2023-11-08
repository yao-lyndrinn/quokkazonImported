from flask import render_template
from flask import redirect, request, url_for
from flask_login import current_user
from humanize import naturaltime
from collections import defaultdict

from .models.product import Product
from .models.inventory import Inventory
from .models.stock import Stock
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('products', __name__)

@bp.route('/products/<int:product_id>')
def productDetail(product_id):
    product = Product.get(product_id)
    return render_template('productDetail.html',
                           product=product)
        
@bp.route('/products', methods=['GET','POST'])
def products():
    items = Product.get_all()
    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    for item in inventory:
        product_prices[item.pid].append(item.price)
    if request.method == 'POST':
        products = Stock.get_all_in_stock()
        k_prod = []
        k = int(request.form['k'])
        for i in range(k):
            k_prod.append(products[i])
        return render_template('topProducts.html',
                    k_prod = k_prod, k = k)
    
    return render_template('products.html',
                      items=items, inventory=inventory, product_prices = product_prices, is_seller=Seller.is_seller(current_user))
    