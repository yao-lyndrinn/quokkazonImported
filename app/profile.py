
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from flask import Blueprint
bp = Blueprint('profile', __name__)

from .models.seller import Seller
from .models.feedback import SellerFeedback, ProductFeedback
from .models.purchase import Purchase
from .models.product import Product

from humanize import naturaltime
import datetime
import pandas as pd
import plotly
import plotly.express as px
import json
from .models.user import User

# List of month abbreviations for analytics graph
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

# User personal page
@bp.route('/myprofile')
@login_required
def my_profile():
    a = Seller.get(current_user.id)
    sfeedback = None
    order_count_graph, order_freq_graph, ratings_graph = None, None, None
    supvotes = {}
    myupvotes = {}
    summary = None
    order_count_graph, order_freq_graph = None, None
    if a is None: 
        is_seller = False
    else:
        is_seller = True

        # Create a graph for top selling products by count for a particular seller
        order_counts = Purchase.get_order_counts_by_sid(current_user.id)
        oc_df = pd.DataFrame(order_counts[:min(len(order_counts), 10)], columns=['ID','Product','Count sold'])
        oc_fig = px.bar(oc_df, x='Product', y='Count sold', title='Top Selling Products', text_auto=True, color_discrete_sequence=['#8E7618'])
        order_count_graph = json.dumps(oc_fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Create a graph for the total number orders over time for a particular seller across all products
        orders_freq = [[f'{MONTHS[row[0]-1]} {row[1]}',row[2]] for row in Purchase.get_num_orders_per_month(current_user.id)]
        of_df = pd.DataFrame(orders_freq, columns=['Month','Count'])
        of_fig = px.line(of_df, x='Month',y='Count',title='Total Number of Orders Per Month')
        order_freq_graph = json.dumps(of_fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Create a graph for the average seller rating over time by month
        num_ratings, sum, avg_ratings = 0, 0, []
        ratings_freq = SellerFeedback.get_seller_ratings(current_user.id)
        if ratings_freq:
            m = ratings_freq[0][0]
            y = ratings_freq[0][1]
            current_year = datetime.datetime.now().year
            current_month = datetime.datetime.now().month
            i = 0
            while m <= 12 and y < current_year or m <= current_month and y == current_year:
                while len(ratings_freq) > 0 and ratings_freq[0][0] == m and ratings_freq[0][1] == y:
                    sum += ratings_freq[0][2]
                    num_ratings += 1
                    ratings_freq.pop(0)
                avg_ratings.append([f'{MONTHS[int(m)-1]} {y}', float(sum/num_ratings)])
                m += 1
                if m > 12:
                    m = 1
                    y += 1
            rt_df = pd.DataFrame(avg_ratings, columns=['Month','Count'])
            rt_fig = px.line(rt_df, x='Month',y='Count',title='Average Rating Over Time')
            ratings_graph = json.dumps(rt_fig, cls=plotly.utils.PlotlyJSONEncoder)

    sfeedback = SellerFeedback.get_by_sid(current_user.id)
    supvotes = {}
    myupvotes = {}
    sorted_by_upvotes = SellerFeedback.sorted_by_upvotes(current_user.id)
    for item in sfeedback:
        supvotes[(item.uid,item.sid)] = SellerFeedback.upvote_count(item.uid,item.sid)[0][0]
    summary = SellerFeedback.summary_ratings(current_user.id)
    for reviewer,seller in supvotes: 
        myupvotes[(reviewer,seller)] = SellerFeedback.my_upvote(current_user.id,reviewer,seller)[0][0]
    count = 0
    top3 = []
    for item in sorted_by_upvotes: 
        top3.append(item)
        count += 1 
        if count == 3: break

    feedback_for_other_sellers = SellerFeedback.user_summary_ratings(current_user.id)
    feedback_for_products = ProductFeedback.user_summary_ratings(current_user.id)
    # The user information will be loaded from the current_user proxy
    return render_template('myprofile.html',
                            is_seller = is_seller,
                           title='My Profile',
                           order_count_graph=order_count_graph,
                           order_freq_graph=order_freq_graph,
                           ratings_graph=ratings_graph,
                           sfeedback = sfeedback,
                           supvotes=supvotes,
                           my_supvotes=myupvotes,
                           top3=top3,
                           summary = summary,
                           current_user=current_user,
                           feedback_for_other_sellers=feedback_for_other_sellers,
                           feedback_for_products=feedback_for_products,
                           humanize_time=humanize_time)

# Registers a user as a seller
@bp.route('/register_seller')
@login_required
def reg_seller():
    Seller.add_seller(current_user.id)
    # The user information will be loaded from the current_user proxy
    return redirect(url_for('profile.my_profile'))


# Allows for personal info to be changed
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Retrieve form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')

        User.update_user_info(current_user.id, email, firstname, lastname, address, phone_number)
        #flash('Profile updated successfully!')
        return redirect(url_for('profile.my_profile'))

    return render_template('edit_profile.html')


# Allows for balance to be topped-up
@bp.route('/top_up', methods=['GET', 'POST'])
@login_required
def top_up():
    if request.method == 'POST':
        # Retrieve form data
        added_money = request.form.get("added_money")

        User.top_up(current_user.id, current_user.balance, added_money)
       # flash('Balance topped up successfully!')
        return redirect(url_for('profile.my_profile'))

    return render_template('top_up.html')