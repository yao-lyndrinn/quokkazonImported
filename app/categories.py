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
    category = Category.get_name(category_id)
    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    summary = defaultdict(list)
    items_stock = Stock.get_stock_by_cat(category_id)

    if request.method == 'GET':    
        if request.args.get('filter_by') == "available":
            if request.args.get('sort_by'):
                items = apply_sort(items_stock, request.args.get('sort_by'), category_id)
            else:
                items = apply_sort(items_stock, "a-z", category_id)
        else:
            if request.args.get('sort_by'):
                items = apply_sort(cat_items, request.args.get('sort_by'), category_id)
            else:
                items = apply_sort(cat_items, "a-z", category_id)
    
    for item in inventory:
        product_prices[item.pid].append(item.price)
        summary[item.pid] = ProductFeedback.summary_ratings(item.pid)

    paginated = items[start:end]
    total_pages = len(items)//24 + 1
    
    categories = Category.get_all()
    
    return render_template('products.html', items=paginated,
                      inventory=inventory, 
                      summary=summary,
                      product_prices = product_prices,
                      page=page,
                      total_pages=total_pages,
                      categories=categories,
                      category=category,
                      is_seller=Seller.is_seller(current_user))
    
def apply_sort(items, sort_by, category_id):
    stock_items = Stock.get_stock_by_cat(category_id)
    if sort_by == "high_price":
        sort_items = sorted(stock_items, key=lambda x: x.price, reverse=True)
    if sort_by == "low_price":
        sort_items = sorted(stock_items, key=lambda x: x.price)
    if sort_by == "a-z":
        sort_items = sorted(items, key=lambda x: x.name)
    if sort_by == "z-a":
        sort_items = sorted(items, key=lambda x: x.name, reverse=True)
    return sort_items

    
