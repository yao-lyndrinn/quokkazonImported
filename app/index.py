from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.seller import Seller
from .models.feedback import ProductFeedback

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all()
    pids = ProductFeedback.all_pids()
    summary_ratings = {} 
    for row in pids: 
        pid = row[0]
        summary_ratings[pid] = ProductFeedback.summary_ratings(pid)

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                        avail_products=products,
                        purchase_history=purchases,
                        summary=summary_ratings,
                        is_seller=Seller.is_seller(current_user))
    
