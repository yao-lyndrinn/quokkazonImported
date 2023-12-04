
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from flask import Blueprint
bp = Blueprint('profile', __name__)

from .models.seller import Seller
from .models.feedback import SellerFeedback

from humanize import naturaltime
import datetime

from .models.user import User


def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/myprofile')
@login_required
def my_profile():
    a = Seller.get(current_user.id)
    sfeedback = None
    supvotes = {}
    if a is None: 
        is_seller = False
    else:
        is_seller = True
        sfeedback = SellerFeedback.get_by_sid(current_user.id)
        for item in sfeedback:
            supvotes[(item.uid,item.sid)] = SellerFeedback.upvote_count(item.uid,item.sid)[0][0]
        summary = None
        if len(sfeedback) > 0: 
            summary = SellerFeedback.summary_ratings(current_user.id)

    # The user information will be loaded from the current_user proxy
    return render_template('myprofile.html',
                            is_seller = is_seller,
                           title='My Profile',
                           sfeedback = sfeedback,
                           supvotes=supvotes,
                           summary = summary,
                           current_user=current_user,
                           humanize_time=humanize_time)

@bp.route('/register_seller')
@login_required
def reg_seller():
    Seller.add_seller(current_user.id)
    # The user information will be loaded from the current_user proxy
    return redirect(url_for('profile.my_profile'))



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