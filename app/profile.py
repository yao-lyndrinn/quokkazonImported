
from flask import render_template
from flask_login import current_user, login_required

from flask import Blueprint
bp = Blueprint('profile', __name__)

@bp.route('/myprofile')
@login_required
def my_profile():
    # The user information will be loaded from the current_user proxy
    return render_template('myprofile.html',
                           title='My Profile',
                           current_user=current_user)

