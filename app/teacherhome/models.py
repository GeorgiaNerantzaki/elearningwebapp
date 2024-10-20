# app/models.py
from app.database import db
#from app.authentication.models import Users
from datetime import datetime
import time

#define course table
class Course(db.Model):

    __tablename__ = 'Courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    proffessor = db.Column(db.String(100), nullable=False)
    enrollments = db.relationship('Enrollment', back_populates='course')
    announcement = db.relationship('Announcement',back_populates ='course_announcement')
    document = db.relationship('Document',back_populates ='course_doc')
    assignment = db.relationship('Assignment',back_populates ='course_assignment')
    assignment_solution = db.relationship('AssignmentSolution',back_populates ='solution_for_course')
    lecture = db.relationship('Lecture',back_populates ='lecture_course')
    response_for_course = db.relationship('Responses',back_populates ='response_course')
    response_for_lecture = db.relationship('Lectureresponses',back_populates ='response_lecture')
    course_feedback  = db.relationship('FeedbackComment',back_populates ='feedback_course')
    
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            
            setattr(self, property, value)

    def __repr__(self):
        return str(self.title)
    

def create_test_courses(app):
    if Course.query.count() == 0:
       test_courses = [
         Course(title = 'Physics', photo = '/media/images/course-image.jpg', semester = '2024B' , description = 'Introduction',proffessor  = 'teacher' ) 
       ]
       for course in test_courses:
          db.session.add(course)
          app.logger.info('%s course created successfully',course.title)
       db.session.commit()     
#define enrollment table   
class Enrollment(db.Model):
    __tablename__ = 'Enrollments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'), nullable=False)
    grade  = db.Column(db.String(2), nullable=True)

    user = db.relationship('Users', back_populates='courses')
    course = db.relationship('Course', back_populates='enrollments')
    
#define announcement table
class Announcement(db.Model):
    __tablename__ = 'Announcements'
    id = db.Column(db.Integer, primary_key=True)
    announcement_title = db.Column(db.String(100), nullable=False)
    announcement_description = db.Column(db.Text, nullable=True)
    announcement_date = db.Column(db.String(20), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'), nullable=False)
    

    course_announcement = db.relationship('Course',back_populates ='announcement')
    
    def __repr__(self):
        return str(self.announcement_title)

#define document table
class Document(db.Model):
    __tablename__ = 'Documents' 
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(30),nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'), nullable=False)
    
    course_doc = db.relationship('Course',back_populates ='document')
    
    def __repr__(self):
        return str(self.filename)
    


    
#define assignment table    
class Assignment(db.Model):
    __tablename__ = 'Assignment'
    id = db.Column(db.Integer, primary_key=True)
    assignment_title = db.Column(db.String(30),nullable=False)
    assignment_desc = db.Column(db.Text, nullable=True)
    deadline_date =  db.Column(db.String(30),nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'), nullable=False)
    course_assignment = db.relationship('Course',back_populates ='assignment')
    student_solution   = db.relationship('AssignmentSolution',back_populates ='solution_for_assignment', cascade= 'all', passive_deletes = True)
    def __repr__(self):
        return str(self.assignment_title)
    
#define assignment solution table
class AssignmentSolution(db.Model):
    __tablename__ = 'Assignment_Solutions' 
    id = db.Column(db.Integer, primary_key=True)
    filename_solution = db.Column(db.String(30),nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('Assignment.id', ondelete='CASCADE'), nullable=False)
    student =  db.Column(db.String(30),nullable=False)
    
    solution_for_course = db.relationship('Course',back_populates ='assignment_solution')
    solution_for_assignment= db.relationship('Assignment',back_populates ='student_solution')
    
    def __repr__(self):
        return str(self.filename)
    
#define lecture table
class Lecture(db.Model):
    __tablename__ = 'Lectures'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'))
    title = db.Column(db.String(40),nullable=True)
    question_text = db.Column(db.String(255))
    lecture_activated = db.Column(db.Boolean(),default = False)
    lecture_course = db.relationship('Course',back_populates ='lecture')
    lecture_response = db.relationship('Responses',back_populates ='response_for_lecture')
    lecture_feedback = db.relationship('FeedbackComment',back_populates ='feedback_lecture')
def __repr__(self):
        return str(self.title)    


 

#define responses for the assessment table
class Responses(db.Model):
    __tablename__ = 'Responses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    lecture_id = db.Column(db.Integer, db.ForeignKey('Lectures.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'))
    response_value = db.Column(db.String(40),nullable=True)
    response_course = db.relationship('Course',back_populates ='response_for_course')
    user = db.relationship('Users',back_populates ='user_response')
    response_for_lecture = db.relationship('Lecture',back_populates ='lecture_response')
    
    # def __init__(self, user_id, lecture_id, course_id, response_value):
    #     self.user_id = user_id
    #     self.lecture_id = lecture_id
    #     self.course_id = course_id
    #     self.response_value = response_value


    def __repr__(self):
        return str(self.response_value) 
    

#define responses for the likert live form  table
class Lectureresponses(db.Model):
    __tablename__ = 'Responses during the lecture'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'))
    lecture_id = db.Column(db.Integer, db.ForeignKey('Lectures.id'))
    response_value = db.Column(db.Integer)
    response_lecture = db.relationship('Course',back_populates ='response_for_lecture')
    user = db.relationship('Users',back_populates ='user_responses_inlecture')
    
    # def __init__(self, user_id, lecture_id, course_id, response_value):
    #     self.user_id = user_id
    #     self.lecture_id = lecture_id
    #     self.course_id = course_id
    #     self.response_value = response_value


    def __repr__(self):
        return str(self.response_value) 


#define feedback(or questions) table
class FeedbackComment(db.Model):
    __tablename__ = 'Feedback Comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'))
    lecture_id = db.Column(db.Integer, db.ForeignKey('Lectures.id'))
    comment = db.Column(db.String(100),nullable=True)
    feedback_course = db.relationship('Course',back_populates ='course_feedback')
    feedback_user = db.relationship('Users',back_populates ='user_feedback')
    feedback_lecture = db.relationship('Lecture',back_populates ='lecture_feedback')
    def __repr__(self):
        return str(self.comment)

    

    
    