from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager, login_manager, login_user, current_user


class Base(DeclarativeBase):
  pass
#intergrate SQLalchemy pachage and Login manager for login sessions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
