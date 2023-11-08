from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import request, redirect, url_for
import datetime
from humanize import naturaltime

from .models.feedback import ProductFeedback, SellerFeedback

from flask import Blueprint
bp = Blueprint('feedback', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/product/feedback',methods = ['GET','POST'])
def product_feedback():
    pfeedback = ProductFeedback.get_all() 
    pid = None
    name = None
    if request.method == 'POST': 
        pid = request.form['pid']
        name = request.form['name']
        pfeedback = ProductFeedback.get_by_pid(pid)# sorted by posting time
        summary = ProductFeedback.summary_ratings(pid)
    return render_template('productfeedback.html',
                        pfeedback=pfeedback,
                        pid=pid, 
                        name=name,
                        summary=summary,
                        humanize_time=humanize_time)

@bp.route('/product/feedback/sorted',methods = ['GET','POST'])
def product_feedback_sorted_rating():
    pid = None
    name = None
    pfeedback = ProductFeedback.get_all() 
    if request.method == 'POST': 
        pid = request.form['pid']
        name = request.form['name']
        pfeedback = ProductFeedback.get_by_pid_sort_rating(pid)# sorted by posting time
        summary = ProductFeedback.summary_ratings(pid)
    return render_template('productfeedback.html',
                        pfeedback=pfeedback,
                        pid=pid,
                        name=name,
                        summary=summary,
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

@bp.route('/myfeedback/delete/<int:product_id>', methods=['POST','GET'])
def product_remove_feedback(product_id):
    if request.method == 'POST': 
        ProductFeedback.remove_feedback(current_user.id,product_id)
    return redirect(url_for('feedback.my_feedback_sorted_rating'))

@bp.route('/myfeedback/delete/product_review', methods=['POST','GET'])
def product_remove_review():
    if request.method == 'POST': 
        pid = int(request.form['pid'])
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ProductFeedback.edit_review(current_user.id, pid,'',current_dateTime)
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

@bp.route('/myfeedback/delete/<int:seller_id>', methods=['POST','GET'])
def seller_remove_feedback(seller_id):
    if request.method == 'POST': 
        SellerFeedback.remove_feedback(current_user.id,seller_id)
    return redirect(url_for('feedback.my_feedback_sorted_rating'))

@bp.route('/myfeedback/delete/seller_review', methods=['POST','GET'])
def seller_remove_review():
    if request.method == 'POST': 
        seller_id = int(request.form['sid'])
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        SellerFeedback.edit_review(current_user.id, seller_id,'',current_dateTime)
    return redirect(url_for('feedback.seller_feedback_edit',seller_id=seller_id))
