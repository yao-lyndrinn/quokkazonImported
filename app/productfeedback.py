from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import redirect, url_for
import datetime
from humanize import naturaltime

from .models.productfeedback import ProductFeedback

from flask import Blueprint
bp = Blueprint('productfeedback', __name__)

@bp.route('/productfeedback/allbydate')
def pfeedback_uid_sorted_date():
    # find all the ratings and reviews the current user has left for products 
    if current_user.is_authenticated:
        items = ProductFeedback.get_all_by_uid_since( # sorted by posting time 
                        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('productfeedback.html',
                      items=items,
                      humanize_time=humanize_time)

@bp.route('/productfeedback/top5bydate')
def pfeedback_uid_sorted_date_top5():
    if current_user.is_authenticated:
        items = ProductFeedback.get_n_most_recent_by_uid( # five most recent reviews
                        current_user.id, 5)
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('productfeedback.html',
                      items=items,
                      humanize_time=humanize_time)

@bp.route('/productfeedback/byrating')
def pfeedback_uid_sorted_rating():
    # find all the ratings and reviews the current user has left for products 
    if current_user.is_authenticated:
        items = ProductFeedback.get_all_by_uid_sort_rating( # sorted by rating 
                        current_user.id)
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('productfeedback.html',
                      items=items,
                      humanize_time=humanize_time)

# @bp.route('/productfeedback/filterbyrating')
# def pfeedback_uid_filter_rating(rating):
#     # find all the ratings and reviews the current user has left for products 
#     if current_user.is_authenticated:
#         items = ProductFeedback.get_by_uid_filter_by_rating( # sorted by rating 
#                         current_user.id,rating)
#     else:
#         return jsonify({}), 404
#     # render the page by adding information to the index.html file
#     return render_template('productfeedback.html',
#                       items=items,
#                       humanize_time=humanize_time)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)
