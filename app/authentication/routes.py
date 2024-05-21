# -*- encoding: utf-8 -*-
import logging
from flask import  flash, render_template, redirect, request, url_for , current_app, session

from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_security import roles_accepted
from app.database import db
from app import login_manager

from app.authentication import blueprint
from app.authentication.forms import LoginForm, CreateAccountForm
from app.authentication.models import Users, Role
from app.authentication.util import verify_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))



@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    #logging.Logger.info('Hit Login')  
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        
        username = request.form['username']
        password = request.form['password']

        
        user = Users.query.filter_by(email=username).first()

        
        if user and verify_pass(password, user.password):
            login_user(user)
            logging.info('%s login successfully', user.username)
            return redirect(url_for('authentication_blueprint.route_default'))
        
        flash('Invalid password provided', 'error')
        return render_template('accounts/login.html', form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)
    else:
       
        if user_has_role('admin'):
            return redirect(url_for('home_blueprint.index'))
        elif user_has_role('teacher'):
            return redirect(url_for('teacherhome_blueprint.index'))
        elif user_has_role('student'):
            return redirect(url_for('home_blueprint.index'))
        else:
            return redirect(url_for('home_blueprint.index'))

    return redirect(url_for('home_blueprint.index'))


def user_has_role(role_name):
    if not current_user.is_authenticated:
        return False  

  
    return any(role.name == role_name for role in current_user.roles)

@blueprint.route('/register', methods=['GET', 'POST'])
# @roles_accepted('admin')
def register():
    create_account_form = CreateAccountForm(request.form)
    create_account_form.roles.choices = [(role.id, role.name) for role in Role.query.all()]
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        roles_selected = create_account_form.roles.data
        #confirm_password= request.form['confirm']
        
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        
        #user = Users(**request.form) 
        user = Users(username=username, email=email, password=password) 
        user.roles = Role.query.filter(Role.id.in_(roles_selected)).all()
        user.active = True 
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
