from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import redirect, url_for
import datetime
from humanize import naturaltime

from .models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)

@bp.route('/products/<int:product_id>')
def productDetail(product_id):
    product = Product.get(product_id)
    return render_template('productDetail.html',
                           product=product)
@bp.route('/products')
def products():
    items = Product.get_all()
    return render_template('products.html',
                      items=items)