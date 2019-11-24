from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, Length
from flask_login import current_user

class WithdrawalForm(FlaskForm):
    bankName = [
        ('Maybank', 'Maybank'),
        ('CIMB', 'CIMB')
    ]
    #transfer from account
    from_account = StringField('Transfer From')
    #transfer to account
    to_account = IntegerField('Transfer To', validators=[DataRequired()])
    #bank name
    bank_name = SelectField(u'Bank Name', choices=bankName, validators=[DataRequired()])
    #amount to transfer
    amount = IntegerField('Amount', validators=[DataRequired()])
    #account name
    account_name = StringField('Account Name', validators=[DataRequired(), Length(min=5)])

    

class PaymentForm(FlaskForm):
    receipt = FileField('Upload Receipt Image', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])