
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from flask import Blueprint
bp = Blueprint('profile', __name__)

from .models.seller import Seller
from .models.feedback import SellerFeedback

from humanize import naturaltime
import datetime

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/myprofile')
@login_required
def my_profile():
    a = Seller.get(current_user.id)
    sfeedback = None
    if a is None: 
        is_seller = False
    else:
        is_seller = True
        sfeedback = SellerFeedback.get_by_sid_sort_date_descending(current_user.id)
        summary = None
        if len(sfeedback) > 0: 
            summary = SellerFeedback.summary_ratings(current_user.id)

    # The user information will be loaded from the current_user proxy
    return render_template('myprofile.html',
                            is_seller = is_seller,
                           title='My Profile',
                           sfeedback = sfeedback,
                           summary = summary,
                           current_user=current_user,
                           humanize_time=humanize_time)

@bp.route('/register_seller')
@login_required
def reg_seller():
    Seller.add_seller(current_user.id)
    # The user information will be loaded from the current_user proxy
    return redirect(url_for('profile.my_profile'))

