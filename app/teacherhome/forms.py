# -*- encoding: utf-8 -*-

#from msilib.schema import CheckBox
from flask_login import confirm_login
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, HiddenField, SubmitField, IntegerField,FileField, SubmitField, SelectField, FormField, FieldList, validators
from wtforms.validators import DataRequired, InputRequired
from flask_bootstrap5 import Bootstrap
from flask_wtf.file import FileField, FileRequired, FileAllowed





class CreateCourseForm(Form):
    title = StringField('title',
                         id='title_create',
                         validators=[DataRequired()])
    semester = StringField('semester',
                         id='course_semester',
                         validators=[DataRequired()])
    description = StringField('description',
                         id='course_desc',
                         validators=[DataRequired()])
    photo = StringField('photo',
                         id='photo',
                         validators=[DataRequired()])
    

class CreateAnnouncementForm(Form):
     announcement_title = StringField('Announcement Title',
                         id='announcement_title_create',
                         validators=[DataRequired()])
     announcement_date = StringField('Date',
                         id='announcement_date',
                         validators=[DataRequired()])
     announcement_description = StringField('Type your announcement here',
                         id='announcement_description',
                         validators=[DataRequired()])
     course_id = IntegerField('Course ID', validators=[DataRequired()])
     #course_id = HiddenField('Course ID', validators=[DataRequired()])
     #submit = SubmitField('Submit')
     


class CreateAssignmentForm(Form):
     assignment_title = StringField('Assignments title',
                         id='assignment_title_create',
                         validators=[DataRequired()])
     assignment_date = StringField('Deadline date',
                         id='deadline_date',
                         validators=[DataRequired()])
     assignment_description = StringField('Description here',
                         id='assignment_description',
                         validators=[DataRequired()])
     course_id = IntegerField('Course ID', validators=[DataRequired()])
     


class GradeForm(FlaskForm):
    student_grade = StringField('Grade for Student ')
    submit = SubmitField('Submit')
     
    
    
class FileUploadForm(FlaskForm):
    file = FileField('File', validators=[FileRequired(), FileAllowed(['pdf', 'docx', 'txt'], 'File types allowed: PDF, DOCX, TXT')])
    submit = SubmitField('Submit')


class DeleteAssignment(FlaskForm):
    assignment_id = HiddenField('Assignment  ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
 


class LectureForm(Form):
    title = StringField('Lecture Title', validators=[validators.DataRequired()])
    question_text = StringField('Question :', validators=[validators.DataRequired()])
    submit = SubmitField('Create Question')
    

class LiveForm(Form):
    title = StringField('Lecture Title', validators=[validators.DataRequired()])
    submit = SubmitField('Create Form and Lecture')
    

class ActivateForm(FlaskForm):
    lecture_id = HiddenField('Lecture ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

class DeactivateForm(FlaskForm):
    lecture_id = HiddenField('Lecture ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
