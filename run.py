# -*- encoding: utf-8 -*-

import os
from flask import Flask, render_template
#from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit
from app.authentication.models import Users
from app.authentication.forms import LoginForm
from app.teacherhome.forms import CreateCourseForm
from app.config import config_dict
from app.database import db
from app import create_app
#from app import app

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
DEBUG = 'True'
# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)


@app.context_processor
def inject_app_data():
    app_data = {
        'html_title': 'eLearning Web Application',
        "name": "eLearning Flask Web App",
        "description": "A basic eLearning Flask app using bootstrap for layout",
        "author": "Georgia Nerantzaki",
        "project_name": "elearningwebapp",
        "keywords": "flask, webapp, basic"
    }
    return {'app_data': app_data}

#Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    app.run(use_reloader=False)
