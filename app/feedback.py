from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import request, redirect, url_for
import datetime
from .models.seller import Seller
from humanize import naturaltime

from .models.feedback import ProductFeedback, SellerFeedback

from flask import Blueprint
bp = Blueprint('feedback', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/feedback_history/<int:uid>', methods=['POST','GET'])
def my_feedback(uid):
    name = SellerFeedback.get_name(uid)
    pfeedback = ProductFeedback.get_by_uid(uid)
    pupvotes = {}
    for item in pfeedback: 
        pupvotes[(item.uid,item.pid)] = ProductFeedback.upvote_count(item.uid,item.pid)[0][0]
    sfeedback = SellerFeedback.get_by_uid(uid)
    supvotes = {}
    for item in sfeedback:
        supvotes[(item.uid,item.sid)] = SellerFeedback.upvote_count(item.uid,item.sid)[0][0]
    return render_template('myfeedback.html',
                        uid = uid,
                        name = name,
                        pfeedback=pfeedback,
                        pupvotes = pupvotes,
                        sfeedback=sfeedback,
                        supvotes=supvotes,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/add/<int:product_id>/<name>', methods=['POST','GET'])
def product_submission_form(product_id,name):
    return render_template('myfeedback_add.html',
                            product_id=product_id,
                            name=name,
                            type="product",
                            humanize_time=humanize_time)

@bp.route('/myfeedback/add/product', methods=['POST','GET'])
def product_add_feedback():
    if request.method == 'POST': 
        pid = int(request.form['pid'])
        rating = int(request.form['rating'])
        review = request.form['review']
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ProductFeedback.add_feedback(current_user.id,pid,rating,review,current_dateTime)
        pfeedback = ProductFeedback.get_by_uid_pid(current_user.id, pid)
    return render_template('myfeedback_edit.html',
                        pfeedback=pfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/edit/product/<int:product_id>', methods=['POST','GET'])
def product_feedback_edit(product_id):
    pfeedback = ProductFeedback.get_by_uid_pid(current_user.id, product_id)
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
        ProductFeedback.remove_upvotes(current_user.id,product_id)
        ProductFeedback.remove_feedback(current_user.id,product_id)
    return redirect(url_for('feedback.my_feedback'))

@bp.route('/myfeedback/delete/product_review', methods=['POST','GET'])
def product_remove_review():
    if request.method == 'POST': 
        pid = int(request.form['pid'])
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ProductFeedback.remove_upvotes(current_user.id,pid)
        ProductFeedback.edit_review(current_user.id, pid,'',current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))

@bp.route('/productfeedback/remove_upvote', methods=['POST','GET'])
def remove_upvote_product_review():
    reviewer =  int(request.form['reviewer'])
    product = int(request.form['reviewed'])
    ProductFeedback.remove_my_upvote(current_user.id,reviewer,product)
    return redirect(url_for('products.product_detail',product_id=product))

@bp.route('/productfeedback/upvote', methods=['POST','GET'])
def upvote_product_review():
    if request.method == 'POST':
        reviewer =  int(request.form['reviewer'])
        product = int(request.form['reviewed'])
        ProductFeedback.add_my_upvote(current_user.id,reviewer,product)
    return redirect(url_for('products.product_detail',product_id=product))
    

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

@bp.route('/myfeedback/delete', methods=['POST','GET'])
def seller_remove_feedback():
    if request.method == 'POST':
        sid = int(request.form['sid'])
        SellerFeedback.remove_upvotes(current_user.id, sid)
        SellerFeedback.remove_feedback(current_user.id,sid)
    return redirect(url_for('feedback.seller_personal',seller_id=sid))

@bp.route('/myfeedback/delete/seller_review', methods=['POST','GET'])
def seller_remove_review():
    if request.method == 'POST': 
        seller_id = int(request.form['sid'])
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        SellerFeedback.remove_upvotes(current_user.id, seller_id)
        SellerFeedback.edit_review(current_user.id, seller_id,'',current_dateTime)
    return redirect(url_for('feedback.seller_feedback_edit',seller_id=seller_id))

@bp.route('/myfeedback/add/seller', methods=['POST','GET'])
def seller_add_feedback():
    if request.method == 'POST': 
        sid = int(request.form['sid'])
        rating = int(request.form['rating'])
        review = request.form['review']
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        SellerFeedback.add_feedback(current_user.id,sid,rating,review,current_dateTime)
        sfeedback = SellerFeedback.get_by_uid_sid(current_user.id, sid)
    return render_template('myfeedback_edit.html',
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/add/<int:seller_id>', methods=['POST','GET'])
def seller_submission_form(seller_id):
    name = SellerFeedback.get_name(seller_id)
    return render_template('myfeedback_add.html',
                            seller_id=seller_id,
                            name=name,
                            type="seller",
                            humanize_time=humanize_time)

@bp.route('/sellerfeedback/remove_upvote', methods=['POST','GET'])
def remove_upvote_seller_review():
    reviewer =  int(request.form['reviewer'])
    seller = int(request.form['seller'])
    SellerFeedback.remove_my_upvote(current_user.id,reviewer,seller)
    return redirect(url_for('feedback.seller_personal',seller_id=seller))

@bp.route('/sellerfeedback/upvote', methods=['POST','GET'])
def upvote_seller_review():
    if request.method == 'POST':
        reviewer =  int(request.form['reviewer'])
        seller = int(request.form['seller'])
        SellerFeedback.add_my_upvote(current_user.id,reviewer,seller)
    return redirect(url_for('feedback.seller_personal',seller_id=seller))
        
@bp.route('/public_profile/<int:seller_id>', methods=['POST','GET'])
def seller_personal(seller_id):
    summary = None
    sfeedback = SellerFeedback.get_by_sid(seller_id)
    supvotes = {}
    for item in sfeedback:
        supvotes[(item.uid,item.sid)] = SellerFeedback.upvote_count(item.uid,item.sid)[0][0]
    myupvotes = {}
    if current_user.is_authenticated: 
        # whether the current logged-in user has purchased from this seller before 
        has_purchased  = SellerFeedback.has_purchased(current_user.id,seller_id)
        if has_purchased is not None: 
            my_seller_feedback = SellerFeedback.get_by_uid_sid(current_user.id, seller_id)
        else: 
            # the user has not purchased from this seller before 
            has_purchased = False
            my_seller_feedback = False
        # which reviews the current user has upvoted 
        for reviewer,seller in supvotes: 
            myupvotes[(reviewer,seller)] = SellerFeedback.my_upvote(current_user.id,reviewer,seller)[0][0]
    else: 
        has_purchased, my_seller_feedback = False, False

    a = Seller.has_products(seller_id) 
    if(a):
        summary = SellerFeedback.summary_ratings(seller_id)    
  
    info = Seller.find(seller_id)
    feedback_for_other_sellers = SellerFeedback.user_summary_ratings(seller_id)
    feedback_for_products = ProductFeedback.user_summary_ratings(seller_id)
    return render_template('publicProfile.html',
                            sfeedback=sfeedback,
                            supvotes=supvotes,
                            myupvotes=myupvotes,
                            summary=summary,
                            seller_id=seller_id,
                            first_name = info[2],
                            last_name = info[3],
                            email = info[1],
                            humanize_time=humanize_time,
                            has_products = a,
                            has_purchased = has_purchased,
                            my_seller_feedback=my_seller_feedback,
                            feedback_for_other_sellers=feedback_for_other_sellers,
                            feedback_for_products=feedback_for_products)