from flask import render_template
from flask_login import current_user
from flask import request, redirect, url_for
import datetime
from .models.seller import Seller
from humanize import naturaltime

from .models.messages import Messages
from flask import Blueprint
bp = Blueprint('messages', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/my_message_history', methods=['POST','GET'])
def my_messages():
    messages = Messages.get_by_sender(current_user.id)
    return render_template('mymessages.html',
                        messages=messages,
                        humanize_time=humanize_time)
