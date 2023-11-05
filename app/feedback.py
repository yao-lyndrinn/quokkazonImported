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
    count = 0
    for item in items: 
        count += 1 
        k_feedback.append(item)
        if count == k: break
    return k_feedback

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/uidfeedbacktop5', methods=['GET','POST'])
def all_feedback_uid_top5():
    pfeedback = ProductFeedback.get_all() 
    sfeedback = SellerFeedback.get_all()
    if request.method == 'POST': 
        uid = int(request.form['uid'])
        pfeedback = ProductFeedback.get_by_uid_since( # sorted by posting time 
                    uid, datetime.datetime(1980, 9, 14, 0, 0, 0))
        sfeedback = SellerFeedback.get_by_uid_since( # sorted by posting time 
                    uid, datetime.datetime(1980, 9, 14, 0, 0, 0))
        pfeedback = kmostrecent(pfeedback,5)
        sfeedback = kmostrecent(sfeedback,5)
        return render_template('allfeedback.html',
                        pfeedback=pfeedback,
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)
    return render_template('allfeedback.html',
                        pfeedback=pfeedback,
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)

@bp.route('/uidfeedback',methods = ['GET','POST'])
def all_feedback_uid():
    pfeedback = ProductFeedback.get_all() 
    sfeedback = SellerFeedback.get_all()
    if request.method == 'POST': 
        uid = int(request.form['uid'])
        pfeedback = ProductFeedback.get_by_uid_since( # sorted by posting time 
                    uid, datetime.datetime(1980, 9, 14, 0, 0, 0))
        sfeedback = SellerFeedback.get_by_uid_since( # sorted by posting time 
                    uid, datetime.datetime(1980, 9, 14, 0, 0, 0))
        return render_template('allfeedback.html',
                        pfeedback=pfeedback,
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)
    return render_template('allfeedback.html',
                        pfeedback=pfeedback,
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback')
def my_feedback():
    pfeedback = ProductFeedback.get_by_uid_since( # sorted by posting time 
                    current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    sfeedback = SellerFeedback.get_by_uid_since( # sorted by posting time 
                    current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    return render_template('myfeedback.html',
                        pfeedback=pfeedback,
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback_sorted_rating')
def my_feedback_sorted_rating():
    pfeedback = ProductFeedback.get_by_uid_sort_rating( # sorted by rating 
                    current_user.id)
    sfeedback = SellerFeedback.get_by_uid_sort_rating( # sorted by rating 
                    current_user.id)
    return render_template('myfeedback.html',
                        pfeedback=pfeedback,
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/edit/product/<int:product_id>', methods=['POST','GET'])
def product_feedback_edit(product_id):
    pfeedback = ProductFeedback.get_by_uid_pid( # sorted by rating 
                    current_user.id, product_id)
    return render_template('myfeedback_edit.html',
                        pfeedback=pfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/edit/product_rating', methods=['POST','GET'])
def product_rating_edit():
    if request.method == 'POST': 
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rating = int(request.form['rating'])
        pid = int(request.form['pid'])
        ProductFeedback.edit_rating(current_user.id, pid, rating, current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))

@bp.route('/myfeedback/edit/product_review', methods=['POST','GET'])
def product_review_edit():
    if request.method == 'POST': 
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        review = request.form['review']
        pid = int(request.form['pid'])
        ProductFeedback.edit_review(current_user.id, pid, review, current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))


@bp.route('/myfeedback/edit/seller/<int:seller_id>', methods=['POST','GET'])
def seller_feedback_edit(seller_id):
    sfeedback = SellerFeedback.get_by_uid_sid( # sorted by rating 
                    current_user.id, seller_id)
    return render_template('myfeedback_edit.html',
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/edit/seller_rating', methods=['POST','GET'])
def seller_rating_edit():
    if request.method == 'POST': 
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rating = int(request.form['rating'])
        sid = int(request.form['sid'])
        SellerFeedback.edit_rating(current_user.id, sid, rating, current_dateTime)
    return redirect(url_for('feedback.seller_feedback_edit',seller_id=sid))

@bp.route('/myfeedback/edit/seller_review', methods=['POST','GET'])
def seller_review_edit():
    if request.method == 'POST': 
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        review = request.form['review']
        sid = int(request.form['sid'])
        SellerFeedback.edit_review(current_user.id, sid, review, current_dateTime)
    return redirect(url_for('feedback.seller_feedback_edit',seller_id=sid))