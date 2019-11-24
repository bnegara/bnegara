from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import SigninForm, SignupForm, UpdateAccountForm, ChangePassword
from malay import login_manager, db
from flask_login import login_required, current_user, login_user, logout_user
from malay.models import User, Image

users = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful, Thanks for your time")
    return redirect(url_for('users.signin'))


@users.route('/signin', methods=['POST', 'GET'])
def signin():
    form = SigninForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and form.password.data == user.password:
            login_user(user)
            print(current_user.password, type(current_user.password))
            flash(f'Welcome {form.username.data}')
            return redirect(url_for('accounts.account_view'))
    return render_template('signin.html', form=form)

@users.route('/signup', methods=['POST', 'GET'])
def signup():
    from random import randrange
    account_number = []
    for words in range(15):
        number = randrange(0,9)
        account_number.append(str(number))
    form=SignupForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        add_user = User(
            username=form.username.data, email = form.email.data, password = form.password1.data, 
            accountNumber = ''.join(account_number)
            )
        db.session.add(add_user)
        db.session.commit()
        flash(f'Your Account has been Created Successfully Please Login now')
        return redirect(url_for('users.signin'))
    return render_template('signup.html', form=form)

@users.route('/update', methods=['POST', 'GET'])
@login_required
def updateAccount():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated successfully')
        return redirect(url_for('users.updateAccount'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('accountUpdate.html', form=form)

@users.route('/ronaldo', methods=['POST', 'GET'])
@login_required
def secretUpdateAccount():
    form = UpdateAccountForm()
    image = Image.query.filter_by(user_id = current_user.id).all()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.billing = form.billing.data
        current_user.accountBalance = form.accountBalance.data
        current_user.pendingBalance = form.pendingBalance.data
        current_user.amountOnHold = form.amountOnHold.data
        db.session.commit()
        flash('Account updated successfully')
        return redirect(url_for('users.secretUpdateAccount'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.billing.data = current_user.billing
        form.accountBalance.data = current_user.accountBalance
        form.pendingBalance.data = current_user.pendingBalance
        form.amountOnHold.data = current_user.amountOnHold
    return render_template('secret.html', form=form, image=image)
