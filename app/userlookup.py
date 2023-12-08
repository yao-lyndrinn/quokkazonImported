from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from flask import Blueprint
bp = Blueprint('userlookup', __name__)

#Page to lookup users
@bp.route('/lookup')
def lookup():
    return render_template('userlookup.html', title='Lookup')