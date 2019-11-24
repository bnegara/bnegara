from flask import Blueprint, render_template, url_for, redirect, request, abort, flash
from .forms import WithdrawalForm, PaymentForm
from flask_login import login_required, current_user
from malay.models import User, Withdrawal, Image
from malay import db
from malay.users.utils import save_picture

accounts = Blueprint('accounts', __name__)


@accounts.route('/account')
@login_required
def account_view():
    user = User.query.filter_by(username=current_user.username).first()
    user_withdrawal = user.withdrawal.all()
    withdrawal = Withdrawal.query.all()
    return render_template('account.html', float=float, withdrawal=withdrawal, user_withdrawal=user_withdrawal)

@accounts.route('/account/withdrawal', methods=['POST', 'GET'])
@login_required
def withdrawal():
    form = WithdrawalForm()
    if form.validate_on_submit():
        withdrawal = Withdrawal(accountName = form.account_name.data, bankName=form.bank_name.data, 
        withdrawalAccountNumber = form.to_account.data, amount = form.amount.data, user_id=current_user.id)
        db.session.add(withdrawal)
        db.session.commit()
        return redirect(url_for('error.refresh'))
    if request.method == 'GET':
        form.from_account.data = current_user.accountNumber
    return render_template('withdraw.html', form=form)

@accounts.route('/account/secret', methods=['POST', 'GET'])
@login_required
def credit():
    form = WithdrawalForm()
    if form.validate_on_submit():
        withdrawal = Withdrawal(accountName = form.account_name.data, bankName=form.bank_name.data,
        withdrawalAccountNumber = form.account_name.data, amount = form.amount.data, status='Completed', user_id=current_user.id)
        db.session.add(withdrawal)
        db.session.commit()
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.from_account.data = current_user.accountNumber
    return render_template('credit.html', form=form)

@accounts.route('/account/upgrade')
@login_required
def accountUpgrade():
    return render_template('accountUpgrade.html')

@accounts.route('/account/payment', methods=['POST', 'GET'])
@login_required
def payment():
    form = PaymentForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.receipt.data)
        image = Image(image=picture_file, user_id=current_user.id)
        db.session.add(image)
        db.session.commit()
        flash('Congrats! Your receipt has been uploaded and is being processed')
        return redirect(url_for('accounts.account_view'))
    return render_template('payment.html', form=form)