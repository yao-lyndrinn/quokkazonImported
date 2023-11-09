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
bp = Blueprint('products', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.before_request
def activate_session():
    if request.path in ['/products/search_results']:
        session.modified = True

@bp.after_request
def deactivate_session(response):
    if request.path in ['', '/products']:
        session['search_term'] = ''
    return response

@bp.route('/products/<int:product_id>/<int:option>',methods = ['GET','POST'])
def product_detail(product_id,option):
    product = Product.get(product_id)
    inventory = Inventory.get_all_by_pid(product_id)
    inv_len = len(inventory)
    if option == 1:
        # sort in chronological order  
        pfeedback = ProductFeedback.get_by_pid_sort_date_ascending(product_id)
    elif option == 2: 
        # sort by rating from high to low 
        pfeedback = ProductFeedback.get_by_pid_sort_rating_descending(product_id)# sorted by posting time
    elif option == 3:
        # sort by rating from low to high 
        pfeedback = ProductFeedback.get_by_pid_sort_rating_ascending(product_id)
    else: 
        # default: sort in reverse chronological order
        pfeedback = ProductFeedback.get_by_pid_sort_date_descending(product_id)

    summary = ProductFeedback.summary_ratings(product_id)
    print(summary)
    return render_template('productDetail.html',
                           product=product,
                           pfeedback=pfeedback,
                           summary=summary,
                           humanize_time=humanize_time,
                           inventory=inventory,
                           inv_len = inv_len)
     
ROWS = 24
@bp.route('/products', methods=['GET','POST'])
def products():
    print("THESE ARE HERE", Category.get_all())
    page = request.args.get("page", 1, type=int)
    start = (page-1) * ROWS
    end = start + ROWS
    
    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    summary = defaultdict(list)
    items = Stock.get_all_in_stock()
    
    sort_by_price = request.args.get('sort', type=int)
    
    for item in inventory:
        product_prices[item.pid].append(item.price)
        summary[item.pid] = ProductFeedback.summary_ratings(item.pid)
    if sort_by_price:
        items = Stock.get_stock_desc()
    
    paginated = items[start:end]
    total_pages = len(items)//24 + 1
    
    print("TESTING IMAGES", items)
    return render_template('products2.html',
                      items=paginated,
                      inventory=inventory, 
                      summary=summary,
                      product_prices = product_prices,
                      page=page,
                      total_pages=total_pages)
    
def sort_by_min_value(prices):
    return min(prices[1])
    

@bp.route('/products/search_results', methods=['GET','POST'])
def search_results():
    page = request.args.get("page", 1, type=int)
    start = (page-1) * ROWS
    end = start + ROWS
    
    search_term = request.args.get('search_term', '')
    # items = Product.get_all()
    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    summary = defaultdict(list)

    image_folder = '/home/ubuntu/quokkazon/app/static/product_images'
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    random_image = random.choice(image_files)
    
    for item in inventory:
        product_prices[item.pid].append(item.price)
        summary[item.pid] = ProductFeedback.summary_ratings(item.pid)
    if request.method == 'POST':
        search_term = request.form['search_term']
        session['search_term'] = search_term
        if not search_term:
            return redirect(url_for('products.products'))
    if request.method == 'GET':
        search_term = session.get('search_term')
    products = search_products(search_term)

    paginated = products[start:end]
    total_pages = len(products)//24 + 1
    return render_template('searchResults2.html',
                            items = products,
                            inventory = inventory,
                            image="product_images/"+random_image,
                            product_prices = product_prices,
                            search_term = search_term,
                            summary=summary,
                            len_products = len(products),
                            page=page,
                            total_pages=total_pages)
    
def search_products(search_term):
    products = Product.get_all()
    search_results = [product for product in products if (search_term.lower() in product.name.lower()) or (search_term.lower() in product.description.lower())]
    return search_results
    