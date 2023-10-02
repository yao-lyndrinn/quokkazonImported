from flask import render_template
from flask_login import current_user
import datetime

from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('inventory', __name__)


@bp.route('/inventory')
def index():
    
    # find the products current user has bought:
    if current_user.is_authenticated:
        inventory = Inventory.get_all_by_sid(
            current_user.id)
    else:
        inventory = None
    # render the page by adding information to the index.html file
    return render_template('inventory.html',
                           avail_inventory=inventory)
    
