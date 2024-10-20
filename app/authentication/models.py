# -*- encoding: utf-8 -*-

#from flask_login import UserMixin
from app.database import db, login_manager
from app.authentication.util import hash_pass
from flask_security import UserMixin, RoleMixin

from app.teacherhome.models import Course
#define a table that consisits of roles id and users id 
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('Users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('Roles.id')))    
#define Users table
class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref='roled')
    courses = db.relationship('Enrollment', back_populates='user')
    user_response = db.relationship('Responses',back_populates ='user')
    user_responses_inlecture = db.relationship('Lectureresponses',back_populates ='user')
    user_feedback  = db.relationship('FeedbackComment',back_populates ='feedback_user')
    
    def __init__(self, **kwargs):
        roles = kwargs.pop('roles', [])
        super(Users, self).__init__(**kwargs)
        for role in roles:
            self.roles.append(role)
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
               
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)
    
# create table in database for storing roles
class Role(db.Model, RoleMixin):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    
#create test users meaning that users are predefined for ease purposes in development when we restart the application with a new database
def create_test_users(app):
             if Role.query.count() == 0:
                 test_roles = [
                      Role(name='student'),
                      Role(name='teacher'),
                      Role(name='admin')
                 ] 
                 for role in test_roles:
                       db.session.add(role)
                       app.logger.info('%s role created successfully',role.name)
                 db.session.commit()         
                 
             if Users.query.count() == 0:
                 admin_role = Role.query.filter_by(name='admin').first()
                 student_role = Role.query.filter_by(name='student').first()
                 teacher_role = Role.query.filter_by(name='teacher').first()
                 # Add test users when the database is empty
                 test_users = [
                     Users(username='admin', email='admin@elearningweb.app',password='1234',active = True, roles=[admin_role]),
                     Users(username='teacher', email='teacher@elearningweb.app',password='1234',active = True, roles=[teacher_role]),
                     Users(username='student', email='student@elearningweb.app',password='1234',active = True, roles=[student_role])
                     
                     # Add more test users as needed
                 ]
                 for user in test_users:
                     db.session.add(user)
                     app.logger.info('%s created successfully', user.username)

                 db.session.commit()
                 
            
 #loads the user based on ID            
@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()

#loads user based on username in a post request
@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

