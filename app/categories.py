from flask import render_template
from flask import redirect, request, url_for, session
from flask_session import Session
from flask_login import current_user
from humanize import naturaltime
import datetime
from collections import defaultdict
import os, random

from .models.product import Product
from .models.feedback import ProductFeedback
from .models.inventory import Inventory
from .models.stock import Stock
from .models.category import Category
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('categories', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

ROWS = 24
@bp.route('/<category_id>', methods=['GET','POST'])
def category_products(category_id):
    page = request.args.get("page", 1, type=int)
    start = (page-1) * ROWS
    end = start + ROWS
    
    cat_items = Product.get_all_by_cat(category_id)
    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    summary = defaultdict(list)
    # items = Stock.get_all_in_stock()
    
    sort_by_price = request.args.get('sort', type=int)
    
    for item in inventory:
        product_prices[item.pid].append(item.price)
        summary[item.pid] = ProductFeedback.summary_ratings(item.pid)
    # if sort_by_price:
    #     items = Stock.get_stock_desc()
    
    paginated = cat_items[start:end]
    total_pages = len(cat_items)//24 + 1
    
    categories = Category.get_all()
    
    return render_template('products2.html', items=paginated,
                      inventory=inventory, 
                      summary=summary,
                      product_prices = product_prices,
                      page=page,
                      total_pages=total_pages,
                      categories=categories)
    
def sort_by_min_value(prices):
    return min(prices[1])
    
