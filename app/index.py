from flask import render_template
from flask_login import current_user
from flask import redirect, request, url_for, session
from flask_session import Session
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.seller import Seller
from .models.feedback import ProductFeedback

from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.before_request
def activate_session():
    if request.path in ['/products/search_results']:
        session.modified = True

@bp.after_request
def deactivate_session(response):
    if request.path in ['', '/products']:
        session['search_term'] = ''
    return response

@bp.route('/')
def index():
    # get all available products for sale:
    top_pid = Purchase.get_top_ten()
    top_all = []
    
    for product in top_pid:
        top_all.append(Product.get(product))
    # products = Product.get_all()
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
                        avail_products=top_all,
                        purchase_history=purchases,
                        summary=summary_ratings,
                        is_seller=Seller.is_seller(current_user))
    
