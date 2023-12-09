from flask import render_template
from flask_login import current_user
from flask import request, redirect, url_for
import datetime
from .models.seller import Seller
from .models.category import Category 
from humanize import naturaltime
import os 
is_seller = False
from .models.feedback import ProductFeedback, SellerFeedback

from flask import Blueprint
bp = Blueprint('feedback', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/feedback_history/<int:uid>', methods=['POST','GET'])
def my_feedback(uid):
    # render the feedback history page for a given user 
    name = SellerFeedback.get_name(uid) # name of the user 
    pfeedback = ProductFeedback.get_by_uid(uid) # get the user's feedback for products 
    pupvotes = {}
    my_pupvotes = {}
    for item in pfeedback: 
        # get the user's upvotes for product reviews 
        pupvotes[(item.uid,item.pid)] = ProductFeedback.upvote_count(item.uid,item.pid)[0][0]
    
    # get the user's feedback for sellers 
    sfeedback = SellerFeedback.get_by_uid(uid)
    supvotes = {}
    my_supvotes = {}
    for item in sfeedback:
        supvotes[(item.uid,item.sid)] = SellerFeedback.upvote_count(item.uid,item.sid)[0][0]
        
    # if the current user is logged in, then they can upvote reviews 
    if current_user.is_authenticated: 
        if Seller.find(current_user.id): 
            is_seller = True 
        # get the current user's upvotes for product reviews 
        for reviewer, reviewed in pupvotes:
            my_pupvotes[(reviewer,reviewed)] = ProductFeedback.my_upvote(current_user.id,reviewer,reviewed)[0][0]
        # get the current user's upvotes for seller reviews 
        for reviewer, reviewed in supvotes:
            my_supvotes[(reviewer,reviewed)] = SellerFeedback.my_upvote(current_user.id,reviewer,reviewed)[0][0]
    sorted_categories = sorted(Category.get_all(), key=lambda x: x.name)
    return render_template('myfeedback.html',
                        uid = uid,
                        name = name,
                        pfeedback=pfeedback,
                        pupvotes = pupvotes,
                        my_pupvotes = my_pupvotes,
                        my_supvotes = my_supvotes,
                        sfeedback=sfeedback,
                        supvotes=supvotes,
                        is_seller=is_seller,
                        categories=sorted_categories,
                        humanize_time=humanize_time)
    
@bp.route('/myfeedback/add/<int:product_id>/<name>', methods=['POST','GET'])
def product_submission_form(product_id,name):
    if current_user.is_authenticated: 
        # go to the feedback submission form for this product 
        if Seller.find(current_user.id): 
            is_seller = True 
        sorted_categories = sorted(Category.get_all(), key=lambda x: x.name)
        return render_template('myfeedback_add.html',
                                product_id=product_id,
                                is_seller=is_seller,
                                name=name,
                                type="product",
                                categories=sorted_categories,
                                humanize_time=humanize_time)

    return redirect(url_for('users.login'))

@bp.route('/myfeedback/add/product', methods=['POST','GET'])
def product_add_feedback(): 
    if request.method == 'POST': 
        # submit feedback 
        if Seller.find(current_user.id): 
            is_seller = True 
        pid = int(request.form['pid'])
        rating = int(request.form['rating'])
        review = request.form['review']
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # get image file and format properly 
        file = request.files['image']
        filename = file.filename
        filepath = os.path.join('/home/ubuntu/quokkazon/app/static/product_images', filename)
        file.save(filepath)
        
        ProductFeedback.add_feedback(current_user.id,pid,rating,review,current_dateTime, "product_images/" + filename)
        pfeedback = ProductFeedback.get_by_uid_pid(current_user.id, pid)
        sorted_categories = sorted(Category.get_all(), key=lambda x: x.name)
        return render_template('myfeedback_edit.html',
                            pfeedback=pfeedback,
                            is_seller=is_seller,
                            categories=sorted_categories,
                            humanize_time=humanize_time)
    
    # if the user did not click a button to get to this page, redirect them to the home page 
    return redirect(url_for('index.index'))  
   
@bp.route('/myfeedback/edit/product/<int:product_id>', methods=['POST','GET'])
def product_feedback_edit(product_id):
    if current_user.is_authenticated: 
        # go to the feedback editing page for this product 
        if Seller.find(current_user.id): 
            is_seller = True
        pfeedback = ProductFeedback.get_by_uid_pid(current_user.id, product_id)
        sorted_categories = sorted(Category.get_all(), key=lambda x: x.name)
        return render_template('myfeedback_edit.html',
                            pfeedback=pfeedback,
                            is_seller=is_seller,
                            categories=sorted_categories,
                            humanize_time=humanize_time)
    
    return redirect(url_for('index.index'))      
 
@bp.route('/myfeedback/edit/product_rating', methods=['POST','GET'])
def product_rating_edit():
    if request.method == "POST":
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rating = int(request.form['rating'])
        pid = int(request.form['pid'])
        ProductFeedback.edit_rating(current_user.id, pid, rating, current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))      

@bp.route('/myfeedback/edit/product_review', methods=['POST','GET'])
def product_review_edit():
    if request.method == "POST":
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        review = request.form['review']
        pid = int(request.form['pid'])
        ProductFeedback.edit_review(current_user.id, pid, review, current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))

@bp.route('/myfeedback/edit/product_image', methods=['POST','GET'])
def product_image_edit():
    if request.method == 'POST': 
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # get image file and format properly 
        file = request.files['image']
        filename = file.filename
        filepath = os.path.join('/home/ubuntu/quokkazon/app/static/product_images', filename)
        file.save(filepath)

        pid = int(request.form['pid'])
        ProductFeedback.edit_image(current_user.id, pid, "product_images/" + filename, current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))


@bp.route('/myfeedback/delete/<int:product_id>', methods=['POST','GET'])
def product_remove_feedback(product_id):
    # when a user removes their product feedback, also remove any associated upvotes 
    if current_user.is_authenticated: 
        ProductFeedback.remove_upvotes(current_user.id,product_id)
        ProductFeedback.remove_feedback(current_user.id,product_id)
    return redirect(url_for('feedback.my_feedback',uid=current_user.id))
    
@bp.route('/myfeedback/delete/product_review', methods=['POST','GET'])
def product_remove_review():
    if request.method == 'POST': 
        pid = int(request.form['pid'])
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ProductFeedback.remove_upvotes(current_user.id,pid)
        ProductFeedback.edit_review(current_user.id, pid,'',current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))

    
@bp.route('/myfeedback/delete/image', methods=['POST','GET'])
def product_remove_image():
    if request.method == 'POST': 
        pid = int(request.form['pid'])
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ProductFeedback.edit_image(current_user.id, pid,'',current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))

@bp.route('/productfeedback/remove_upvote', methods=['POST','GET'])
def remove_upvote_product_review():
    if request.method == "POST":
        reviewer =  int(request.form['reviewer'])
        product = int(request.form['reviewed'])
        page = request.form['page']
        ProductFeedback.remove_my_upvote(current_user.id,reviewer,product)
        if page == "myfeedback":
            return redirect(url_for('feedback.my_feedback',uid=current_user.id))
        elif page == "publicfeedback":
            uid = int(request.form['uid'])
            return redirect(url_for('feedback.my_feedback',uid=uid))
        return redirect(url_for('products.product_detail',product_id=product))

    return redirect(url_for('index.index'))

@bp.route('/productfeedback/upvote', methods=['POST','GET'])
def upvote_product_review():
    if request.method == "POST":
        reviewer =  int(request.form['reviewer'])
        product = int(request.form['reviewed'])
        page = request.form['page']
        ProductFeedback.add_my_upvote(current_user.id,reviewer,product)
        if page == "myfeedback":
            return redirect(url_for('feedback.my_feedback',uid=current_user.id))
        elif page == "publicfeedback":
            uid = int(request.form['uid'])
            return redirect(url_for('feedback.my_feedback',uid=uid))
        return redirect(url_for('products.product_detail',product_id=product))

    return redirect(url_for('index.index'))


@bp.route('/myfeedback/edit/seller/<int:seller_id>', methods=['POST','GET'])
def seller_feedback_edit(seller_id):
    if current_user.is_authenticated:
        if Seller.find(current_user.id): 
                is_seller = True 
        sfeedback = SellerFeedback.get_by_uid_sid( # sorted by rating 
                        current_user.id, seller_id)
        sorted_categories = sorted(Category.get_all(), key=lambda x: x.name)
        return render_template('myfeedback_edit.html',
                            sfeedback=sfeedback,
                            is_seller=is_seller,
                            categories=sorted_categories,
                            humanize_time=humanize_time)
    return redirect(url_for('index.index'))

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
    return redirect(url_for('feedback.public_profile',user_id=sid))
    
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
        if Seller.find(current_user.id):
            is_seller = True
        sid = int(request.form['sid'])
        rating = int(request.form['rating'])
        review = request.form['review']
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        SellerFeedback.add_feedback(current_user.id,sid,rating,review,current_dateTime)
        sfeedback = SellerFeedback.get_by_uid_sid(current_user.id, sid)
        sorted_categories = sorted(Category.get_all(), key=lambda x: x.name)
        return render_template('myfeedback_edit.html',
                            sfeedback=sfeedback,
                            is_seller=is_seller,
                            categories=sorted_categories,
                            humanize_time=humanize_time)
    return redirect(url_for('index.index'))


@bp.route('/myfeedback/add/<int:seller_id>', methods=['POST','GET'])
def seller_submission_form(seller_id):
    if current_user.is_authenticated: 
        if Seller.find(current_user.id):
            is_seller = True
        name = SellerFeedback.get_name(seller_id)
        sorted_categories = sorted(Category.get_all(), key=lambda x: x.name)
        return render_template('myfeedback_add.html',
                                seller_id=seller_id,
                                is_seller = is_seller,
                                name=name,
                                type="seller",
                                categories=sorted_categories,
                                humanize_time=humanize_time)
    return redirect(url_for('index.index'))


@bp.route('/sellerfeedback/remove_upvote', methods=['POST','GET'])
def remove_upvote_seller_review():
    if request.method == "POST":
        reviewer =  int(request.form['reviewer'])
        seller = int(request.form['seller'])
        SellerFeedback.remove_my_upvote(current_user.id,reviewer,seller)
        page = request.form['page']
        if page == "myfeedback":
            return redirect(url_for('feedback.my_feedback',uid=current_user.id))
        elif page == "publicfeedback":
            uid = int(request.form['uid'])
            return redirect(url_for('feedback.my_feedback',uid=uid))
        elif page=="myprofile":
            return redirect(url_for('profile.my_profile'))
        return redirect(url_for('feedback.public_profile',user_id=seller))
    return redirect(url_for('index.index'))

@bp.route('/sellerfeedback/upvote', methods=['POST','GET'])
def upvote_seller_review():
    if request.method == "POST":
        reviewer =  int(request.form['reviewer'])
        seller = int(request.form['seller'])
        SellerFeedback.add_my_upvote(current_user.id,reviewer,seller)
        page = request.form['page']
        if page == "myfeedback":
            return redirect(url_for('feedback.my_feedback',uid=current_user.id))
        elif page == "publicfeedback":
            uid = int(request.form['uid'])
            return redirect(url_for('feedback.my_feedback',uid=uid))
        elif page=="myprofile":
            return redirect(url_for('profile.my_profile'))
        return redirect(url_for('feedback.public_profile',user_id=seller))
    return redirect(url_for('index.index'))
        
@bp.route('/public_profile/<int:user_id>', methods=['POST','GET'])
def public_profile(user_id):
    summary = None
    sfeedback = SellerFeedback.get_by_sid(user_id)
    sorted_by_upvotes = SellerFeedback.sorted_by_upvotes(user_id)
    supvotes = {}
    for item in sfeedback:
        supvotes[(item.uid,item.sid)] = SellerFeedback.upvote_count(item.uid,item.sid)[0][0]
    top3 = []
    count = 0
    for item in sorted_by_upvotes: 
        top3.append(item)
        count += 1 
        if count == 3: break
    myupvotes = {}
    if current_user.is_authenticated: 
        if Seller.find(current_user.id):
            is_seller = True
        # whether the current logged-in user has purchased from this seller before 
        has_purchased  = SellerFeedback.has_purchased(current_user.id,user_id)
        if has_purchased is not None: 
            my_seller_feedback = SellerFeedback.get_by_uid_sid(current_user.id, user_id)
        else: 
            # the user has not purchased from this seller before 
            has_purchased = False
            my_seller_feedback = False
        # which reviews the current user has upvoted 
        for reviewer,seller in supvotes: 
            myupvotes[(reviewer,seller)] = SellerFeedback.my_upvote(current_user.id,reviewer,seller)[0][0]
    else: 
        has_purchased, my_seller_feedback = False, False

    user_is_seller = Seller.get(user_id)
    if user_is_seller is not None: 
        if Seller.has_products(user_id):
            summary = SellerFeedback.summary_ratings(user_id)    
        user_is_seller = True
    else: 
        user_is_seller = False 
  
    info = Seller.find(user_id)
    feedback_for_other_sellers = SellerFeedback.user_summary_ratings(user_id)
    feedback_for_products = ProductFeedback.user_summary_ratings(user_id)
    sorted_categories = sorted(Category.get_all(), key=lambda x: x.name)
    return render_template('publicProfile.html',
                            sfeedback=sfeedback,
                            supvotes=supvotes,
                            myupvotes=myupvotes,
                            summary=summary,
                            user_is_seller=user_is_seller,
                            categories=sorted_categories,
                            is_seller=is_seller,
                            user_id=user_id,
                            top3=top3,
                            first_name = info[2],
                            last_name = info[3],
                            email = info[1],
                            humanize_time=humanize_time,
                            has_purchased = has_purchased,
                            my_seller_feedback=my_seller_feedback,
                            feedback_for_other_sellers=feedback_for_other_sellers,
                            feedback_for_products=feedback_for_products)