from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import redirect, url_for
import datetime
from humanize import naturaltime

from .models.sellerfeedback import SellerFeedback

from flask import Blueprint
bp = Blueprint('sellerfeedback', __name__)

@bp.route('/sellerfeedback_allbydate')
def sfeedback_uid_sorted_date():
    # find all the ratings and reviews the current user has left for sellers 
    if current_user.is_authenticated:
        items = SellerFeedback.get_all_by_uid_since( # sorted by posting time 
                        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('sellerfeedback.html',
                      items=items,
                      humanize_time=humanize_time)

@bp.route('/sellerfeedback_top5bydate')
def sfeedback_uid_sorted_date_top5():
    if current_user.is_authenticated:
        items = SellerFeedback.get_n_most_recent_by_uid( # five most recent reviews
                        current_user.id, 5)
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('sellerfeedback.html',
                      items=items,
                      humanize_time=humanize_time)

@bp.route('/sellerfeedback_byrating')
def sfeedback_uid_sorted_rating():
    # find all the ratings and reviews the current user has left for sellers 
    if current_user.is_authenticated:
        items = SellerFeedback.get_all_by_uid_sort_rating( # sorted by rating 
                        current_user.id)
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('sellerfeedback.html',
                      items=items,
                      humanize_time=humanize_time)
def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)