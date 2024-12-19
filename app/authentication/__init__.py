# -*- encoding: utf-8 -*-

from flask import Blueprint
#define authentication blueprint
blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)
