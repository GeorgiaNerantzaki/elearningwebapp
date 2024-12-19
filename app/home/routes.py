# -*- encoding: utf-8 -*-

from app.home import blueprint
from flask import send_from_directory, render_template, flash, redirect, url_for, has_request_context, request, session, Response, current_app
from flask_login import login_required, current_user
from flask_security import roles_accepted
from jinja2 import TemplateNotFound
from app.home.forms import Enroll, Unenroll, SolutionUploadForm,FeedbackForm
from app.teacherhome.models import Course, Enrollment, Announcement, Document, Assignment,AssignmentSolution, Lecture,Responses,Lectureresponses,FeedbackComment
from app.database import db
import os
from werkzeug.exceptions import NotFound
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from pytz import utc
import time
import threading
from uuid import uuid4



#urls that students have access only

#student index page url
@blueprint.route('/index')
@roles_accepted('admin', 'student')
def index():
    form = Unenroll()
    if current_user.is_authenticated:
     enrolled_courses = Course.query.join(Enrollment).filter(Enrollment.user_id == current_user.id).all()
     
    else:
        enrolled_courses = []
    return render_template('home/index.html', segment='index',form=form,enrolled_courses=enrolled_courses)

#for loading templates
@blueprint.route('/<template>')
def route_template(template):

   
    image_extensions = ['png', 'jpg', 'jpeg', 'gif', 'ico']

    
    if any(template.endswith('.' + ext) for ext in image_extensions):
        
        image_path = os.path.join(current_app.root_path, 'media', 'images', template)
        if os.path.isfile(image_path):
            return send_from_directory(os.path.join(current_app.root_path, 'media', 'images'), template)
        else:
            
            return Response('', status=404)

    if not template.endswith('.html'):
        template += '.html'

    try:
        
        segment = get_segment(request)

        
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        
        current_app.logger.error(f"Unhandled exception: {e}")
        return render_template('home/page-500.html'), 500

#all courses page for students to enroll 
@blueprint.route('/allcourses')
@roles_accepted('admin', 'student')
def all_courses():
      all_courses = Course.query.all()
      form = Enroll()
      return render_template('home/allcourses.html', alL_courses=all_courses, form=form)

#course details (description etc)
@blueprint.route('/coursedetails/<int:course_id>')
@roles_accepted('admin', 'student')
def coursedetails(course_id):
 coursedetails = Course.query.get(course_id)  
 assignment = Assignment.query.get(course_id)
 course = Course.query.get(course_id)
 #lecture = Lecture.query.get(course_id)
 lecture = Lecture.query.get(course_id)
 return render_template('home/coursedetails.html',coursedetails = coursedetails, assignment =assignment,course = course,lecture =lecture)

#announcement page
@blueprint.route('/announcements/<int:course_id>')
@roles_accepted('admin', 'student')
def announcements(course_id):
 course = Course.query.get(course_id)
 announcements = Announcement.query.filter_by(course_id=course_id).all()
 assignment = Assignment.query.get(course_id)
 lecture = Lecture.query.get(course_id)
 return render_template('home/announcements.html', course=course,announcements = announcements,assignment =assignment,lecture = lecture)






#assignment page
@blueprint.route('/view_assignment/<int:course_id>', methods=['GET','POST'])
@roles_accepted('admin','student')
def view_assignment(course_id):
    
    #assignment = Assignment.query.get(assignment_id)
    assignments = Assignment.query.filter_by(course_id=course_id).all()
    form = SolutionUploadForm()
    course = Course.query.get(course_id)
    lecture = Lecture.query.get(course_id)
    if assignments is None:
        
        return "Assignments not found", 404

    
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()

    if enrollment is None:
        
        return "You are not enrolled in this course", 403
    

    return render_template('home/assignments.html',assignments=assignments, course = course, form = form,lecture = lecture)

#url for saving the files for assignment from the students(its a button)
@blueprint.route('/upload_solution/<int:course_id>/<int:assignment_id>', methods=['GET','POST'])
@roles_accepted('admin','student')
def upload_solution(course_id,assignment_id):
 form = SolutionUploadForm()
 assignment = Assignment.query.get(assignment_id)
 if request.method == 'POST' and form.validate_on_submit():
        uploaded_file = form.solution.data

        
        directory = os.path.join('media', 'uploads', str(course_id))
        absolute_path = os.path.abspath(directory)

        if not os.path.exists(absolute_path):
            os.makedirs(absolute_path)


        
        unique_filename = uuid4().hex + '_' + uploaded_file.filename
        file_path = os.path.join(absolute_path, secure_filename(unique_filename))
        uploaded_file.save(file_path)

       
        solution = AssignmentSolution(filename_solution=secure_filename(unique_filename), course_id=course_id, assignment_id = assignment_id, student = current_user.username)
        db.session.add(solution)
        db.session.commit()

        return redirect(url_for('home_blueprint.view_assignment', course_id=course_id))
    
    
#enroll button
@blueprint.route('/enroll_course/<int:course_id>', methods=['POST'])
@roles_accepted('admin', 'student')
def enroll_course(course_id):
    if request.method == 'POST':
     if Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first():
        flash('You are already enrolled in this course', 'info')
        return redirect(url_for('home_blueprint.all_courses', course_id=course_id))
    enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    flash('You enrolled successfully','success')
    return redirect(url_for('home_blueprint.all_courses',course_id = course_id))

#unenroll button
@blueprint.route('/unenroll_course/<int:course_id>', methods=['POST'])
@roles_accepted('admin', 'student')
def unenroll_course(course_id):
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        flash('You unenrolled successfully', 'success')
    else:
        flash('You are not enrolled in this course', 'error')
    return redirect(url_for('home_blueprint.index'))

  

#course material page
@blueprint.route('/view_documents/<int:course_id>')
@roles_accepted('admin', 'student')
def view_documents(course_id):
 
 viewdocuments = Document.query.filter_by(course_id = course_id).all()  
 course  = Course.query.get(course_id)
 lecture = Lecture.query.get(course_id)
 return render_template('home/documents.html',viewdocuments = viewdocuments, course = course,lecture = lecture)

#grades page
@blueprint.route('/view_grade/<int:course_id>')
@roles_accepted('admin', 'student')
def view_grade(course_id):
    user_id = current_user.id  
    course  = Course.query.get(course_id)
    
    assignment = Assignment.query.get(course_id)
    lecture = Lecture.query.get(course_id)
    grade = Enrollment.query.filter_by(user_id= current_user.id, course_id = course_id).first()
    return render_template('home/grades.html', grade = grade, course = course,assignment =assignment,lecture = lecture )
  


#list of lectures in links
@blueprint.route('/view_lectures/<int:course_id>')
@roles_accepted('admin', 'student')
def view_lectures(course_id):
      
    course = Course.query.get(course_id)
    assignment = Assignment.query.get(course_id)
    lecture = Lecture.query.get(course_id)
    lectures = Lecture.query.filter_by(course_id = course_id).all()
    return render_template('home/questionaire.html',  lectures = lectures, course =course,assignment =assignment,lecture = lecture )

#saves students response in the quiz
@blueprint.route('/submit_response/<int:course_id>/<int:lecture_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'student')
def submit_response(course_id,lecture_id):
     lecture  = Lecture.query.get(lecture_id)
     course = Course.query.get(course_id)
     assignment  = Assignment.query.get(course_id)
     
     if request.method =='POST':
        response_value = request.form.get(f'response_{lecture.id}')
        existing_response = Responses.query.filter_by(user_id=current_user.id,
                                                       lecture_id=lecture_id,
                                                       course_id=course_id).first()
        if existing_response:
            flash('You have already submitted your response!', 'info')
        else:
            new_response = Responses(user_id=current_user.id,
                                     lecture_id=lecture_id,
                                     course_id=course_id,
                                     response_value=response_value)
            db.session.add(new_response)
            db.session.commit()
            flash('Response had been  submitted successfully!', 'success')
     else:
       
          response_value = None
     return render_template('home/likertform.html', lecture=lecture, course=course,response_value =response_value,assignment =assignment )




#saves real time response during the lecture and the questions
@blueprint.route('/live_response/<int:course_id>/<int:lecture_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'student')
def live_response(course_id, lecture_id):
     course = Course.query.get(course_id)
     lecture = Lecture.query.get(lecture_id)
     form = FeedbackForm()
     response_value = None
     

     if request.method == 'POST':
          response_value = request.form.get(f'response_{lecture.id}')
          existing_response = Lectureresponses.query.filter_by(user_id=current_user.id, course_id=course_id,lecture_id = lecture_id).first()
          if existing_response:
            db.session.delete(existing_response)
            db.session.commit()
          new_response = Lectureresponses(
              user_id=current_user.id,
              course_id=course_id,
              response_value=response_value,
              lecture_id = lecture_id)
          db.session.add(new_response)
          db.session.commit()
     if form.validate_on_submit():
         feedback_comment = form.comment_field.data
         new_comment = FeedbackComment(
              user_id=current_user.id,
              course_id=course_id,
              comment=feedback_comment,
              lecture_id = lecture_id
             )
         db.session.add(new_comment)
         db.session.commit()

     return render_template('home/liveform.html', course=course,lecture = lecture,response_value =response_value, form = form)

#shows all the lectures in links similar to view_lectures
@blueprint.route('/liveformlectures/<int:course_id>')
@roles_accepted('admin', 'student')
def liveformlectures(course_id):
  
    course = Course.query.get(course_id)
    assignment = Assignment.query.get(course_id)
    lectures = Lecture.query.filter_by(course_id = course_id).all()
    lecture = Lecture.query.get(course_id)
    return render_template('home/liveformlectures.html',  lectures = lectures, course =course,assignment =assignment, lecture = lecture )




    


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
