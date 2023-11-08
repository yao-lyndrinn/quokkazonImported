from flask import render_template
from flask import redirect, request, url_for, session
from flask_session import Session
from humanize import naturaltime
from collections import defaultdict
import os, random

from .models.product import Product
from .models.inventory import Inventory
from .models.stock import Stock

from flask import Blueprint
bp = Blueprint('products', __name__)

@bp.before_request
def activate_session():
    if request.path in ['/products/search_results']:
        session.modified = True

@bp.after_request
def deactivate_session(response):
    if request.path in ['', '/products']:
        session['search_term'] = ''
    return response

@bp.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.get(product_id)
    
    image_folder = '/home/ubuntu/quokkazon/app/static/product_images'
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    random_image = random.choice(image_files)
    
    inventory = Inventory.get_all_by_pid(product_id)
    inv_len = len(inventory)
    
    return render_template('productDetail.html',
                           product=product, 
                           image="product_images/"+random_image,
                           inventory=inventory,
                           inv_len = inv_len)
        
ROWS = 10
@bp.route('/products', methods=['GET','POST'])
def products():
    page = request.args.get('page', 1, type=int)
    items = Product.get_all()
    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    start_idx = (page - 1) * ROWS
    end_idx = start_idx + ROWS
    
    for item in inventory:
        product_prices[item.pid].append(item.price)
        
    paginated_items = items[start_idx:end_idx]
    total_pages = len(items)//10 + 1
    return render_template('products.html',
                      items=items, 
                      inventory=inventory, 
                      product_prices = product_prices, 
                      page=page,
                      total_pages = total_pages)
    
@bp.route('/products/search_results', methods=['GET','POST'])
def search_results():
    page = request.args.get('page', 1, type=int)
    search_term = request.args.get('search_term', '')
    # items = Product.get_all()
    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    start_idx = (page - 1) * ROWS
    end_idx = start_idx + ROWS
    
    for item in inventory:
        product_prices[item.pid].append(item.price)
    if request.method == 'POST':
        search_term = request.form['search_term']
        session['search_term'] = search_term
        if not search_term:
            return redirect(url_for('products.products'))
    if request.method == 'GET':
        search_term = session.get('search_term')
    products = search_products(search_term)

        
    paginated_items = products[start_idx:end_idx]
    total_pages = len(products)//10 + 1
    return render_template('searchResults.html',
                            items = products,
                            inventory = inventory,
                            product_prices = product_prices,
                            page=page,
                            total_pages = total_pages,
                            search_term = search_term,
                            len_products = len(products))
    
def search_products(search_term):
    products = Product.get_all()
    search_results = [product for product in products if search_term.lower() in product.name.lower()]
    return search_results
    