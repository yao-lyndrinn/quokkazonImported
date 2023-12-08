from flask import redirect, request, url_for, session, render_template, flash
from flask_session import Session
from flask_login import current_user
from humanize import naturaltime
import datetime
from collections import defaultdict
import os, random
import pandas as pd
import plotly
import plotly.express as px
import json

from .models.product import Product, ProductRating
from .models.feedback import ProductFeedback, SellerFeedback
from .models.purchase import Purchase
from .models.inventory import Inventory
from .models.stock import Stock
from .models.category import Category
from .models.seller import Seller

from flask import Blueprint

bp = Blueprint('products', __name__)

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

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

@bp.route('/products/<int:product_id>',methods = ['GET','POST'])
def product_detail(product_id):
    product = Product.get(product_id)
    inventory = Inventory.get_all_by_pid(product_id)
    inv_len = len(inventory)
    seller_names = {}
    seller_summary = {}
    for seller in inventory: 
        # get the name of the seller 
        seller_names[seller.sid] = SellerFeedback.get_name(seller.sid)
        # get summary feedback statistics for the seller 
        seller_summary[seller.sid] = SellerFeedback.summary_ratings(seller.sid)
    pfeedback = ProductFeedback.get_by_pid(product_id)
    pupvotes = {}
    for item in pfeedback:
        pupvotes[(item.uid,item.pid)] = ProductFeedback.upvote_count(item.uid,item.pid)[0][0]
    # get summary statistics for ratings 
    summary = ProductFeedback.summary_ratings(product_id)
   
    myupvotes = {}
    if current_user.is_authenticated: 
        has_purchased = ProductFeedback.has_purchased(current_user.id,product_id)
        if len(has_purchased) > 0: 
            my_product_feedback = ProductFeedback.get_by_uid_pid(current_user.id, product_id)
        else: 
            my_product_feedback = False
            has_purchased = False
        # which reviews the current user has upvoted 
        for reviewer,reviewed in pupvotes: 
            myupvotes[(reviewer,reviewed)] = ProductFeedback.my_upvote(current_user.id,reviewer,reviewed)[0][0]
        
        sid = Seller.get(current_user.id)
        if sid and Inventory.in_inventory(current_user.id, product_id):
            # Graph for orders over time
            orders_freq = [[f'{MONTHS[row[0]-1]} {row[1]}',row[2]] for row in Purchase.get_num_orders_per_month(current_user.id, product_id)]
            of_df = pd.DataFrame(orders_freq, columns=['Month','Count'])
            of_fig = px.line(of_df, x='Month',y='Count',title='Number of orders from me per month')
            order_freq_graph = json.dumps(of_fig, cls=plotly.utils.PlotlyJSONEncoder)
        else:
            order_freq_graph = None
    else: 
        my_product_feedback, has_purchased = False, False
    return render_template('productDetail.html',
                           product=product,
                           pfeedback=pfeedback,
                           pupvotes=pupvotes,
                           myupvotes=myupvotes,
                           summary=summary,
                           seller_names=seller_names,
                           seller_summary=seller_summary,
                           my_product_feedback = my_product_feedback,
                           has_purchased=has_purchased,
                           humanize_time=humanize_time,
                           inventory=inventory,
                           inv_len = inv_len,
                           order_freq_graph=order_freq_graph)

ROWS = 24
@bp.route('/products', methods=['GET','POST'])
def products():
    
    page = request.args.get("page", 1, type=int)
    start = (page-1) * ROWS
    end = start + ROWS
    
    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    summary = defaultdict(list)
    items_stock = Stock.get_all_in_stock()
    
    for item in inventory:
        product_prices[item.pid].append(item.price)
        summary[item.pid] = ProductFeedback.summary_ratings(item.pid)
                
    if request.method == 'GET':
        filter_by = request.args.get('filter_by') if request.args.get('filter_by') is not None else 'all'
        sort_by = request.args.get('sort_by') if request.args.get('sort_by') is not None else 'a-z'
        if sort_by == "top_reviews":
            items = ProductRating.all_ratings()
        elif sort_by == "low_price":
            items = Stock.get_stock_asc()
        elif sort_by == "high_price":
            items = Stock.get_stock_desc()
        else:
            if filter_by == "available":
                items = apply_sort(items_stock, sort_by)
            else:
                items = apply_sort(Product.get_all(), sort_by)
        

    paginated = items[start:end]
    total_pages = len(items)//24 + 1
    
    categories = Category.get_all()
    
    return render_template('products.html',
                      items=paginated,
                      inventory=inventory, 
                      summary=summary,
                      product_prices = product_prices,
                      page=page,
                      total_pages=total_pages,
                      categories=categories,
                      is_seller=Seller.is_seller(current_user),
                      category="All Products")


@bp.route('/products/search_results', methods=['GET','POST'])
def search_results():
    page = request.args.get("page", 1, type=int)
    start = (page-1) * ROWS
    end = start + ROWS
    
    search_term = request.args.get('search_term', '')

    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    summary = defaultdict(list)
    
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
    
    filter_by = request.args.get('filter_by') if request.args.get('filter_by') is not None else 'all'
    sort_by = request.args.get('sort_by') if request.args.get('sort_by') is not None else 'a-z'
    if sort_by == "top_reviews":
        items = search_products(search_term, ProductRating.all_ratings())
    elif sort_by == "low_price":
        items = search_products(search_term, Stock.get_stock_asc())
    elif sort_by == "high_price":
        items = search_products(search_term, Stock.get_stock_desc())
    else:
        if filter_by == "available":
            items = apply_sort(Stock.get_all_in_stock(), sort_by)
        else:
            items = apply_sort(search_products(search_term, Product.get_all()), sort_by)
    
    categories = Category.get_all()

    paginated = items[start:end]
    total_pages = len(items)//24 + 1
    return render_template('searchResults.html',
                            items = paginated,
                            inventory = inventory,
                            product_prices = product_prices,
                            search_term = search_term,
                            summary=summary,
                            len_products = len(items),
                            page=page,
                            total_pages=total_pages,
                            categories=categories,
                            is_seller=Seller.is_seller(current_user))
    
def search_products(search_term, products):
    search_results = [product for product in products if (search_term.lower() in product.name.lower()) or (search_term.lower() in product.description.lower())]
    return search_results


def apply_sort(items, sort_by):
    if sort_by == "a-z":
        sort_items = sorted(items, key=lambda x: x.name)
    if sort_by == "z-a":
        sort_items = sorted(items, key=lambda x: x.name, reverse=True)
    return sort_items

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']

    
@bp.route('/products/add_products', methods=['GET','POST'])
def add_products():
    categories=Category.get_all()
    if request.method == 'POST':
        name = request.form["name"]
        description = request.form["description"]
        altTxt = request.form["altTxt"]
        category = request.form["category"]
        pid = int(Product.newPID()[0][0]) + 1
        createdAt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updatedAt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # pid = Product.newPID()
        file = request.files['image']
        filename = file.filename
        filepath = os.path.join('/home/ubuntu/quokkazon/app/static/product_images', filename)
        file.save(filepath)
                
        Product.add_product(pid, name, description, "product_images/" + filename, altTxt, createdAt, updatedAt, category)
        
        if Inventory.add(pid, current_user.id, 0, 0, 0):
            return redirect(url_for('inventory.edit', product_id=pid, oq=0, on=0, op=0))
        flash(Product.get_name(pid) + ' already present in inventory!')
        
        return redirect(url_for('inventory.inventory'))
                
    return render_template('add_products.html', categories=categories)