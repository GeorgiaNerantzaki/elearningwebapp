# -*- encoding: utf-8 -*-


from flask import Blueprint
#define student's blueprint
blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix=''
)
