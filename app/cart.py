from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import redirect, url_for
import datetime
from humanize import naturaltime

from .models.cart import CartItem

from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
    # find the items the current user has added to their wishlist
    if current_user.is_authenticated:
        items = CartItem.get_all_by_uid(
                        current_user.id)
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                      items=items)


@bp.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(seller_id, product_id, quantity, saved_for_later):
    CartItem.add_item(current_user.id, seller_id, product_id, quantity, saved_for_later)
    return redirect(url_for('cart.cart'))

