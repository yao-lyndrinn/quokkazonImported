from flask import render_template
from flask_login import current_user
from flask import request, redirect, url_for
import datetime
from .models.feedback import SellerFeedback
from humanize import naturaltime

from .models.messages import Messages
from flask import Blueprint
bp = Blueprint('messages', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/my_message_history', methods=['POST','GET'])
def my_messages():
    interacted = Messages.has_message(current_user.id)
    print(interacted)
    return render_template('mymessages.html',
                        interacted=interacted,
                        humanize_time=humanize_time)

@bp.route('/my_message_history/<int:other_user>', methods=['POST','GET'])
def message_thread(other_user):
    messages = Messages.message_thread(current_user.id,other_user)
    other_user_name = SellerFeedback.get_name(other_user)
    return render_template('messages.html',
                        messages=messages,
                        other_user=other_user,
                        other_user_name=other_user_name,
                        humanize_time=humanize_time)

@bp.route('/new_message/<int:other_user>', methods=['POST','GET'])
def message_thread(other_user):
    messages = Messages.message_thread(current_user.id,other_user)
    other_user_name = SellerFeedback.get_name(other_user)
    return render_template('messages.html',
                        messages=messages,
                        other_user=other_user,
                        other_user_name=other_user_name,
                        humanize_time=humanize_time)