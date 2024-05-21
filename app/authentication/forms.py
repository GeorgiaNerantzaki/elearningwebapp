# -*- encoding: utf-8 -*-

from msilib.schema import CheckBox
from flask_login import confirm_login
from flask_wtf import Form
from wtforms import SelectMultipleField, StringField, PasswordField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import Email, DataRequired
from flask_bootstrap5 import Bootstrap




class LoginForm(Form):
    username = StringField('Email',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()
    
class CreateAccountForm(Form):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    roles = MultiCheckboxField('Roles', coerce=int)
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    confirm = PasswordField('confirm',
                             id='confirm',
                             validators=[DataRequired()])