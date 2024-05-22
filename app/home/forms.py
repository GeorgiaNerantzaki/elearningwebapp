# -*- encoding: utf-8 -*-

#from msilib.schema import CheckBox
from flask_login import confirm_login
from flask_wtf import FlaskForm, Form
from wtforms import HiddenField, StringField, PasswordField, SubmitField,FileField,SelectField, validators, RadioField
from wtforms.validators import DataRequired, InputRequired
from flask_bootstrap5 import Bootstrap
from flask_wtf.file import FileField, FileRequired, FileAllowed



class Enroll(FlaskForm):
    course_id = HiddenField('Course ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

class Unenroll(FlaskForm):
    enrollment_id = HiddenField('Enrollment  ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

class SolutionUploadForm(FlaskForm):
    solution = FileField('File', validators=[FileRequired(), FileAllowed(['pdf', 'docx', 'txt'], 'File types allowed: PDF, DOCX, TXT')])
    submit = SubmitField('Submit')
    

class FeedbackForm(FlaskForm):
    comment_field = StringField('Any feedback, questions about the lecture,requests etc(your response will be anonymous!).(Note:Anything you submit here must be relevant to the content of lecture not to the course in general!) ')
    submit = SubmitField('Submit')
    

# class LikertForm(FlaskForm):
#     def __init__(self, lecture_questions, *args, **kwargs):
#         super(LikertForm, self).__init__(*args, **kwargs)

#         for idx, question in enumerate(lecture_questions, start=1):
#             field_name = f'question_{idx}'
#             setattr(self, field_name, RadioField(question, choices=[
#                 ('5', 'Strongly Agree'),
#                 ('4', 'Agree'),
#                 ('3', 'Neutral'),
#                 ('2', 'Disagree'),
#                 ('1', 'Strongly Disagree')
#             ]))
