# -*- encoding: utf-8 -*-

import os

from flask import Flask, render_template, redirect, request, url_for , current_app, session
#from flask_login import LoginManager, current_user
from flask_login import LoginManager, login_manager, login_user, current_user
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
import logging

from app.authentication.forms import LoginForm
from app.authentication.models import Users, Role, create_test_users
from app.teacherhome.models import Course, Enrollment, Announcement, Assignment, Document, AssignmentSolution, Responses, Lecture,create_test_courses, FeedbackComment 
from app.teacherhome.forms import CreateCourseForm, CreateAnnouncementForm, CreateAssignmentForm, GradeForm
from app.database import db, login_manager
from app.home.forms import FeedbackForm

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    user_datastore = SQLAlchemySessionUserDatastore(db.session, Users, Role)
    security = Security(app, user_datastore)
            
def register_blueprints(app):
    for module_name in ('authentication', 'home', 'teacherhome'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):
    def initialize_database():
        try:
            with app.app_context():
                db.create_all()
                create_test_users(app)
                create_test_courses(app)
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

           
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()
    initialize_database()
    

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove() 


def create_app(config):
    logging.basicConfig(filename='record.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
   
    app = Flask(__name__)
    app.logger.setLevel(logging.DEBUG)        
    app.config.from_object(config)
    register_blueprints(app)
    app.logger.info('Registered blueprints')
    register_extensions(app)
    app.logger.info('Registering extensions')
    configure_database(app)
    app.logger.info('Configure database')
    app.secret_key = 'your_secret_key'
    #app.config['UPLOAD_FOLDER'] = 'static/files'
    # def has_no_empty_params(rule):
    #     defaults = rule.defaults or {}  # Use an empty dictionary if defaults is None
    #     return all(defaults.get(arg) is not None for arg in rule.arguments)

    # @app.route("/site-map")
    # def site_map():
    #     links = []
    #     for rule in app.url_map.iter_rules():
    #         # Filter out rules we can't navigate to in a browser
    #         # and rules that require parameters
    #         if "GET" in rule.methods and has_no_empty_params(rule):
    #             url = url_for(rule.endpoint, **(rule.defaults or {}))
    #             links.append((url, rule.endpoint))
    #             app.logger.info('URL "' + url + '" on rule.endpoint "' + rule.endpoint + '"')        
    #     if not current_user.is_authenticated:
    #        return render_template('login.html',
    #                   form=LoginForm)
    #     return redirect(url_for('home_blueprint.index'))
            
    return app
