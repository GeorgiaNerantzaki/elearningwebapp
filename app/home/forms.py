# -*- encoding: utf-8 -*-

#from msilib.schema import CheckBox
from flask_login import confirm_login
from flask_wtf import FlaskForm, Form
from wtforms import HiddenField, StringField, PasswordField, SubmitField,FileField,SelectField, validators, RadioField
from wtforms.validators import DataRequired, InputRequired
from flask_bootstrap5 import Bootstrap
from flask_wtf.file import FileField, FileRequired, FileAllowed

#student forms here
#enrollment to course form
class Enroll(FlaskForm):
    course_id = HiddenField('Course ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
#unenroll button
class Unenroll(FlaskForm):
    enrollment_id = HiddenField('Enrollment  ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
#form for uploading files with solutions for assignment
class SolutionUploadForm(FlaskForm):
    solution = FileField('File', validators=[FileRequired(), FileAllowed(['pdf', 'docx', 'txt'], 'File types allowed: PDF, DOCX, TXT')])
    submit = SubmitField('Submit')
    
#real time feedback form for questions in the oprional form 
class FeedbackForm(FlaskForm):
    comment_field = StringField('Any feedback, questions about the lecture,requests etc(your response will be anonymous!).(Note:Anything you submit here must be relevant to the content of lecture not to the course in general!) ')
    submit = SubmitField('Submit')
    
