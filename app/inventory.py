from flask import render_template
from flask_login import current_user
from flask import redirect, url_for
import datetime

from .models.inventory import Inventory
from .models.seller import Seller
from .models.product import Product

from flask import Blueprint
bp = Blueprint('inventory', __name__)


@bp.route('/inventory')
def inventory():
    # find the products current user has bought:
    if current_user.is_authenticated:
        inventory = Inventory.get_all_by_sid(
            current_user.id)
    else:
        inventory = None
    # render the page by adding information to the index.html file
    return render_template('inventory.html',
                           avail_inventory=inventory,
                           is_seller=Seller.is_seller(current_user),
                           product_class=Product)