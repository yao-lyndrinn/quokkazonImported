from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import request, redirect, url_for
import datetime
from humanize import naturaltime

from .models.feedback import ProductFeedback, SellerFeedback

from flask import Blueprint
bp = Blueprint('feedback', __name__)

def kmostrecent(items,k):
    k_feedback = []
    for i in range(k): 
        k_feedback.append(items[i])
    return k_feedback

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

    
@bp.route('/productfeedback', methods=['GET','POST'])
def pfeedback_uid_sorted_date():
    items = ProductFeedback.get_by_uid_since( # sorted by posting time 
                    current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    if request.method == 'POST': 
        k = int(request.form['k'])
        items = kmostrecent(items,k)
    return render_template('productfeedback.html',
                      items=items,
                      humanize_time=humanize_time)

@bp.route('/productfeedback_byrating', methods=['GET','POST'])
def pfeedback_uid_sorted_rating():
    items = ProductFeedback.get_by_uid_sort_rating( # sorted by rating 
                    current_user.id)
    if request.method == 'POST': 
        k = int(request.form['k'])
        items = kmostrecent(items,k)
    return render_template('productfeedback.html',
                      items=items,
                      humanize_time=humanize_time)

@bp.route('/sellerfeedback', methods=['GET','POST'])
def sfeedback_uid_sorted_date():
    items = SellerFeedback.get_by_uid_since( # sorted by posting time 
                    current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    if request.method == 'POST': 
        k = int(request.form['k'])
        items = kmostrecent(items,k)
    return render_template('sellerfeedback.html',
                      items=items,
                      humanize_time=humanize_time)

@bp.route('/sellerfeedback_byrating', methods=['GET','POST'])
def sfeedback_uid_sorted_rating():
    items = SellerFeedback.get_by_uid_sort_rating( # sorted by rating 
                    current_user.id)
    if request.method == 'POST': 
        k = int(request.form['k'])
        items = kmostrecent(items,k)
    return render_template('sellerfeedback.html',
                      items=items,
                      humanize_time=humanize_time)