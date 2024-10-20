# -*- encoding: utf-8 -*-

import logging
from flask import  flash, render_template, redirect, url_for , current_app, has_request_context, request, session, jsonify
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from app.database import db

from app.teacherhome import blueprint
from app.teacherhome.forms import CreateCourseForm, CreateAnnouncementForm, CreateAssignmentForm,GradeForm, FileUploadForm, LectureForm,DeleteAssignment,LiveForm,ActivateForm,DeactivateForm
from app.teacherhome.models import Course, Announcement, Assignment, Document, Enrollment,Lecture,Responses, AssignmentSolution, Lectureresponses,FeedbackComment
from app.authentication.models import Users
from flask import render_template, request
from flask_login import login_required
from flask_security import roles_accepted
from werkzeug.utils import secure_filename
from jinja2 import TemplateNotFound
from itertools import zip_longest
import os
from collections import Counter
import time
from datetime import datetime, timedelta
from uuid import uuid4

#teacher's homepage url
@blueprint.route('/teacher')
@roles_accepted('admin','teacher')
def index():
    user_id  = current_user.id  
    
   
    teacher_courses = Course.query.filter_by(proffessor=current_user.username).all()
    return render_template('teacherhome/teacherindex.html', segment ='teacherindex', teacher_courses = teacher_courses)
#url to upload any template related to teacher's activities
@blueprint.route('teacher/<template>')
#@login_required 
@roles_accepted('admin', 'teacher')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

       
        segment = get_segment(request)

        
        return render_template("teacherhome/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('teacherhome/page-404.html'), 404

    except:
        return render_template('teacherhome/page-500.html'), 500
    



#url for viewing course's details
@blueprint.route('teacher/courseteacher/<int:course_id>')
@roles_accepted('admin','teacher')
def courseteacher(course_id):
 courseteacher = Course.query.get(course_id) 
 
 return render_template('teacherhome/courseteacher.html',courseteacher =  courseteacher)


#url to create course
@blueprint.route('teacher/createcourse', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def createcourse():
    form = CreateCourseForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        semester = form.semester.data
        description = form.description.data
        photo = form.photo.data
        proffessor = current_user.username
       
        course = Course.query.filter_by(title=title).first()
        if course:
            return render_template('teacherhome/createcourse.html',
                                   msg='Course already created',
                                   success=False,
                                   form=form)


        
        course = Course(**request.form)
        course.proffessor = current_user.username
        db.session.add(course)
        db.session.commit()

        return render_template('teacherhome/createcourse.html',
                               msg='Course created',
                               success=True,
                               form=form)

    else:
        return render_template('teacherhome/createcourse.html', form=form)
    
#url to upload course announcements    
@blueprint.route('/teacher/announcementsteacher/<int:course_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def announcementsteacher(course_id):
    form = CreateAnnouncementForm(request.form)
    course = Course.query.get(course_id)
    if request.method == 'POST' and form.validate():
        announcement_title = form.announcement_title.data
        announcement_description = form.announcement_description.data
        announcement_date = form.announcement_date.data
        
      
        course_id = form.course_id.data  
        
  

       
        announcement_course = Announcement(
            announcement_title=announcement_title,
            announcement_description=announcement_description,
            announcement_date=announcement_date,
            course_id=course_id
        )
        
        db.session.add(announcement_course)
        db.session.commit()

        return render_template('teacherhome/announcementsteacher.html',
                               msg='Announcement created',
                               success=True,
                               form=form,course = course)
    
        

    else:
        return render_template('teacherhome/announcementsteacher.html', form=form, course = course)
    




#url to upload course material
@blueprint.route('teacher/documentsteacher/<int:course_id>', methods = ['GET','POST'])
@roles_accepted('admin', 'teacher')
def upload_document(course_id):
    form  = FileUploadForm()
    course =Course.query.get(course_id)
    if request.method == 'POST' and form.validate_on_submit():
        uploaded_file  = form.file.data

   


        directory = os.path.join('media', 'documents', str(course_id))
        absolute_path = os.path.abspath(directory)

        if not os.path.exists(absolute_path):
            os.makedirs(absolute_path)


        
        unique_filename = uuid4().hex + '_' + uploaded_file.filename
        file_path =os.path.join(absolute_path, secure_filename(unique_filename))
        uploaded_file.save(file_path)

        document = Document(filename=secure_filename(unique_filename), course_id=course_id)
        db.session.add(document)
        db.session.commit()

        return redirect(url_for('teacherhome_blueprint.upload_document', course_id=course_id))

    documents = Document.query.filter_by(course_id=course_id).all()
    return render_template("teacherhome/documentsteacher.html", form=form, documents=documents,course =course)
    


   


#url for the delete document button
@blueprint.route('teacher/delete_document/<int:course_id>/<int:document_id>', methods=['POST'])
@roles_accepted('admin', 'teacher')
def delete_document(course_id,document_id):
    document = Document.query.filter_by(course_id=course_id).first()
    if document:
        db.session.delete(document)
        db.session.commit()
        flash('The document is deleted', 'success')
    else:
        flash('Could not delete the document', 'error')
    return redirect(url_for('teacherhome_blueprint.upload_document', course_id = course_id))
    


#url for the delete assignment button
@blueprint.route('/delete_assignment/<int:course_id>/<int:assignment_id>', methods=['POST'])
@roles_accepted('admin', 'teacher')
def delete_assignment(course_id,assignment_id):
    assignment = Assignment.query.filter_by(course_id = course_id).first()
    solutions = AssignmentSolution.query.filter_by(course_id = course_id, assignment_id = assignment_id).all()
    if assignment:
        db.session.delete(assignment)
        for solution in solutions:
         db.session.delete(solution)
        db.session.commit()
        
       
        flash('The assignment is deleted', 'success')
    else:
        flash('The assignment does not exist', 'error')
    return redirect(url_for('teacherhome_blueprint.addassignment',course_id =course_id))
       
    



#url for ulploading assignments
@blueprint.route('teacher/assignmentsteacher/<int:course_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def addassignment(course_id):
    form = CreateAssignmentForm(request.form)
    deleteassignmentform = DeleteAssignment()
    course= Course.query.get(course_id)
    assignments = Assignment.query.filter_by(course_id = course_id).all()
    #student_solutions = None
    # if assignments:
     #student_solutions =AssignmentSolution.query.join(Assignment).filter(AssignmentSolution.assignment_id == Assignment.id).all()
    if request.method == 'POST' and form.validate():
        assignment_title = form.assignment_title.data
        assignment_description = form.assignment_description.data
        deadline_date = form.assignment_date.data
        
       
        course_id = form.course_id.data  
        
        

       
        assignment = Assignment(
            assignment_title=assignment_title,
            assignment_desc=assignment_description,
            deadline_date=deadline_date,
            course_id=course_id
        )
        
        db.session.add(assignment)
        db.session.commit()

    return render_template('teacherhome/assignmentsteacher.html',
                               msg='Assignment created',
                               success=True,
                               course = course,
                               assignments = assignments,
                               deleteassignmentform =deleteassignmentform,
                               form=form)

    # else:
    #     return render_template('teacherhome/assignmentsteacher.html', form=form ,deleteassignmentform=deleteassignmentform ,course=course,assignments =assignments)
    


#url for viewing students solution for the assignment
@blueprint.route('teacher/assignmentsolution/<int:course_id>/<int:assignment_id>')
@roles_accepted('admin', 'teacher')
def assignmentsolution(course_id,assignment_id):
    course = Course.query.get(course_id)
    assignment = Assignment.query.get(assignment_id)
    assignmentsolutions = AssignmentSolution.query.filter_by(course_id = course_id,assignment_id = assignment_id ).all()
    return render_template('teacherhome/assignmentsolution.html',assignmentsolutions =assignmentsolutions,course =course,assignment =assignment)

#url for viewing course's lectures
@blueprint.route('teacher/lectures/<int:course_id>')
@roles_accepted('admin', 'teacher')
def lectures(course_id):
    course = Course.query.get(course_id)
    lectures = Lecture.query.filter_by(course_id = course_id).all()
    return render_template('teacherhome/lecturesteacher.html',  lectures = lectures, course =course )

#url for viewing students reposnses to the questionaire (assessment)
@blueprint.route('/questionaire_responses/<int:course_id>/<int:lecture_id>')
@roles_accepted('admin', 'teacher')
def questionaire_responses(course_id, lecture_id):
    course = Course.query.get(course_id)
    lecture = Lecture.query.filter_by(course_id=course_id, id=lecture_id).first()
    responses = Responses.query.filter_by(course_id=course_id, lecture_id=lecture_id).all()
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    percentage_of_students = None
    response_values = [response.response_value for response in responses if response.response_value is not None]
    response_count = len(response_values)
    enrolled_students = len(enrollments)
    if enrolled_students == 0:
     flash('No enrolled students yet!','info')
    else:
     percentage_of_students  = (100 * response_count)/enrolled_students
    #mean_response = sum(response_values) / response_count if response_count > 0 else 0
    mode_response = max(set(response_values), key=response_values.count) if response_count > 0 else 0
    option_counts = Counter(response_values)
    return render_template('teacherhome/questionaireresponses.html',course = course, lecture=lecture, responses=responses, 
                           response_count=response_count, mode_response=mode_response,option_counts =option_counts,percentage_of_students  = percentage_of_students )







    
##url for viewing students reposnses to the likerts scale live form
@blueprint.route('teacher/liveform_responses/<int:course_id>/<int:lecture_id>')
@roles_accepted('admin', 'teacher')
def liveform_responses(course_id,lecture_id):
    course = Course.query.get(course_id)
    # lecture = Lecture.query.get(course_id)
    feedback_from_students = FeedbackComment.query.filter_by(course_id = course_id,lecture_id = lecture_id).all()
    lecture = Lecture.query.filter_by(course_id=course_id, id=lecture_id).first()
    activateform = ActivateForm()
    deactivateform = DeactivateForm()
    liveresponses =  Lectureresponses.query.filter_by(course_id=course_id, lecture_id = lecture_id).all()
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    percentage_of_students = None
    response_values = [response.response_value for response in liveresponses if response.response_value is not None]
    response_count = len(response_values)
    enrolled_students = len(enrollments)
    if enrolled_students == 0:
     flash('No enrolled students yet!','info')
    else:
     percentage_of_students  = (100 * response_count)/enrolled_students
    mean_response = sum(response_values) / response_count if response_count > 0 else 0
    mode_response = max(set(response_values), key=response_values.count) if response_count > 0 else 0
    low_responses_count = sum(1 for response in response_values if response <= 3)
    low_responses_percentage = (100 * low_responses_count)/response_count if response_count > 0 else 0 
    option_counts = Counter(response_values)
    return render_template('teacherhome/liveformresponses.html',course = course, liveresponses=liveresponses, 
                           response_count=response_count, mode_response=mode_response,mean_response =mean_response,option_counts =option_counts, lecture = lecture,activateform =activateform,deactivateform =deactivateform, enrolled_students =enrolled_students,percentage_of_students = percentage_of_students,low_responses_count = low_responses_count,low_responses_percentage =low_responses_percentage,feedback_from_students =feedback_from_students)

#url for uploading grades to each student
@blueprint.route('teacher/pass_grades/<int:course_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def pass_grades(course_id):
    form = GradeForm()
    
    course = Course.query.get(course_id)
    enrolled_students = Enrollment.query.filter_by(course_id=course_id).all()

    if form.validate_on_submit():
        
        for enrollment in enrolled_students:
            student_id = enrollment.user_id
            new_grade = form.student_grade.data
            enrollment.grade = new_grade
            db.session.commit()

        flash('Grades have been successfully updated!', 'success')
    
    return render_template('teacherhome/gradesteacher.html', form=form,course=course, enrolled_students=enrolled_students)

#url for creating lecture
@blueprint.route('teacher/create_lecture/<int:course_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def create_lecture(course_id):
         form = LectureForm(request.form)
         course = Course.query.get(course_id)
         #new_lecture = None
         if request.method == 'POST' and form.validate():
         
           lecture_title = form.title.data
           lecture  = Lecture.query.filter_by(title = lecture_title).first()
           question_text = form.question_text.data
           lecture_question = Lecture(course_id = course_id , title = lecture_title, question_text = question_text)
           db.session.add(lecture_question)
           db.session.commit()

          
           return redirect(url_for('teacherhome_blueprint.create_lecture', course_id = course_id)) 
         #if request.method == 'GET':
         
         return render_template('teacherhome/questionaireteacher.html', form=form,course =course)

@blueprint.route('teacher/create_liveform/<int:course_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def create_liveform(course_id):
         form = LiveForm(request.form)
         course = Course.query.get(course_id)
         #new_lecture = None
         if request.method == 'POST' and form.validate():
           
           lecture_title = form.title.data
           
           new_lecture = Lecture(course_id = course_id , title = lecture_title)
           db.session.add(new_lecture)
           db.session.commit()

          
           return redirect(url_for('teacherhome_blueprint.create_liveform', course_id = course_id)) 
         #if request.method == 'GET':
         
         return render_template('teacherhome/createliveform.html', form=form,course =course)

#url for the activate likert live form button
@blueprint.route('teacher/activate_liveform/<int:course_id>/<int:lecture_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def activate_liveform(course_id,lecture_id):
     # course = Course.query.get(course_id)
     lecture = Lecture.query.get(lecture_id)
     
     lecture.lecture_activated = True
     db.session.commit()
     flash('Form activated successfully !', 'success')
     return redirect(url_for('teacherhome_blueprint.liveform_responses',course_id = course_id,lecture_id = lecture_id))





        
    
    

#url for the deactivate likert live form button    
@blueprint.route('teacher/deactivate_liveform/<int:course_id>/<int:lecture_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def deactivate_liveform(course_id,lecture_id):
    course = Course.query.get(course_id)
    lecture = Lecture.query.get(lecture_id)
    lecture.lecture_activated = False
    db.session.commit()
    flash('Form deactivated successfully !', 'success')
    return redirect(url_for('teacherhome_blueprint.liveform_responses', course_id=course_id, lecture_id=lecture_id))
#url for viewing course's lectures
@blueprint.route('teacher/liveformlectures/<int:course_id>')
@roles_accepted('admin', 'teacher')
def liveformlectures(course_id):
    course = Course.query.get(course_id)
    lectures = Lecture.query.filter_by(course_id = course_id).all()
    return render_template('teacherhome/liveformlectures.html',  lectures = lectures, course =course )



    

def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'teacherindex'

        return segment

    except:
        return None
    