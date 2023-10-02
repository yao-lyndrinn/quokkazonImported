from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import redirect, url_for
import datetime
from humanize import naturaltime

from .models.productfeedback import ProductFeedback

from flask import Blueprint
bp = Blueprint('productfeedback', __name__)

@bp.route('/productfeedback')
def sellerfeedback():
    # find all the ratings and reviews the current user has left for sellers 
    if current_user.is_authenticated:
        items = ProductFeedback.get_all_by_uid_since( # sorted by posting time 
                        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('productfeedback.html',
                      items=items,
                      humanize_time=humanize_time)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)
