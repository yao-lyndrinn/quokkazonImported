
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from .models.purchase import Purchase
import datetime

bp = Blueprint('allpurchases', __name__)

@bp.route('/allpurchases', methods=['GET', 'POST'])
def allpurchases():
    if request.method == 'POST':
        uid = request.form.get('uid')
        # Fetch all purchases for the given uid since a very old date
        if uid != '' and uid.isnumeric():
            purchases = Purchase.get_all_by_uid_since(uid, datetime.datetime(1980, 1, 1, 0, 0, 0))
            return render_template('allpurchases.html', purchases=purchases)
        else:
            return jsonify({}), 404
    return render_template('allpurchases.html', purchases=[])

