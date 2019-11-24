from flask import Blueprint, render_template, url_for
from flask_login import current_user
from malay.models import User, Withdrawal
error = Blueprint('error', __name__)

@error.route('/error1')
def confirmWithdrawal():
    return render_template('confirmWithdrawal.html')

@error.route('/refresh001')
def refresh():
    return render_template('firstRefresh.html')

@error.route('/refresh001.error1')
def firstBilling():
    user = User.query.all()
    return render_template('firstBilling.html', user = user)

